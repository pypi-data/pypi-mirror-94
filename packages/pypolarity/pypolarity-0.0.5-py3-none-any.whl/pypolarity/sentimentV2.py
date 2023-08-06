# %%
from typing import List
from pythainlp import word_tokenize
from pythainlp.corpus.common import thai_words
from pythainlp.util.trie import dict_trie
from pythainlp.tokenize import sent_tokenize
import pymongo
import os

file_list = os.listdir('lexicon-thai/sentiment')

DB_URL = "mongodb://root:root@titipakorn.xyz:27000"
DB_NAME = "keywords4classification"
COL_NAME = "level1"

BUSINESS_TYPES = ["MBB", "FBB", "video", "insurance", "game", "finance", "iot"]

# %%

# load lexicon
file_list = os.listdir('lexicon-thai/sentiment')

positive_tmp = []
negative_tmp = []

for f in file_list:
    with open('./lexicon-thai/sentiment/' + f ) as c:
        words = c.readlines() # list of str
        if f[0:3] == 'pos':
            positive_tmp += words
        elif f[0:3] == 'neg':
            negative_tmp += words

# remove the last '\n' from all words
positive_words = []
for p in positive_tmp:
    if p[-1] == '\n':
        positive_words.append(p[0:-1])
    else:
        positive_words.append(p)

negative_words = []
for p in negative_tmp:
    if p[-1] == '\n':
        negative_words.append(p[0:-1])
    else:
        negative_words.append(p)

del positive_tmp
del negative_tmp

# %%

# read the keywords from DB 
myclient = pymongo.MongoClient(DB_URL)
mydb = myclient[DB_NAME]
mycol = mydb[COL_NAME]

def get_keywords(business_type: str):
    myquery = { "business_type": business_type }
    mydoc = mycol.find_one(myquery) # https://stackoverflow.com/questions/28968660

    return mydoc['keywords']

def get_keywords_all_business():
    """
    returns Dict[str->list]
        str is the name of business type: MBB, FBB, etc. Defined in BUSINESS_TYPES above
        list is the keywords for that type
    """
    keywords_all = dict()
    for b in BUSINESS_TYPES:
        keywords = get_keywords(b)
        keywords_all[b] = keywords

    return keywords_all

# %%
# add all the keywords to custom pythai dictionary
keywords_all = get_keywords_all_business()
custom_words_list = set(thai_words())
for key in keywords_all.keys():
    w_list = keywords_all[key]
    for w in w_list:
        custom_words_list.add(w)

trie = dict_trie(custom_words_list)

def getSentenceThatContainsThisKeyword(sentence_spans, keyword_pos):
    """
    input:
        sentence_spans: as returned from getSentenceSpans()

    return:
        sentence: string
        or None if keyword_pos is not inside any span
    """

    for span, sentence in sentence_spans:
        if keyword_pos >= span[0] and keyword_pos <= span[1]:
            return sentence

    return None


def getSentenceSpans(test_sentences: List):
    """
    input:
        test_sentences: list of string, each string is a sentence, tokenized by pythai crf

    return:
        sentence_spans: 
            list of ([start,end], sentence). Where,
            [start, end] is span (inclusive, word-level position) for each sentence,
            start and end are relative to the whole string

            sentence is string
    """

    sentence_spans = []
    
    previous_end = 0
    for s in test_sentences:
        words = word_tokenize(s, engine='newmm', custom_dict=trie) # find the length (word level) for sentence s 
        sentence_spans.append( ([previous_end, previous_end + len(words) - 1], s) )
        previous_end += len(words)

    return sentence_spans


# %%
def get_contexts(test_string: str):
    """
    input:
        test_string: the news
    return:
        zip of 5 lists:
            keywords_found: ['5G', 'ไฟเบอร์', ...]
            type_business_found: ['MBB', 'FBB', ...]
            pos_found: [4, 20, ...] (position of the found keyword in tokenized test_string)
            context: list of tokens until the next keyword or until end of news text
            sentences: list of strings, each string a sentence where a keyword was found
    """

# context should be from the current keyword until the end of the sentence that contains the keyword
# not until the end of the entire string. so need to do sentence tokenize first
# if the next keyword is in the same sentence -> context is until next keyword
# if the next keyword is not in the same sentence -> context is until end of sentence

    business_types = dict()
    for b in BUSINESS_TYPES:
        business_types[b] = 'none'

    keywords_dict = get_keywords_all_business()

    test_words = word_tokenize(test_string, engine='newmm', custom_dict=trie)
    test_sentences = sent_tokenize(test_string, engine='crfcut')

    sentence_spans = getSentenceSpans(test_sentences)

    keywords_found = []
    type_business_found = []
    pos_found = [] # position of keywords found, relative to the whole string (positions are word-level, not chars !!!)

    # search keyword for each business type
    for i, w in enumerate( test_words ):
        for b in BUSINESS_TYPES:
            if w in keywords_dict[b]:
                keywords_found.append(w)
                type_business_found.append(b)
                pos_found.append(i)

    # build context for each keyword
    contexts = []
    sentences = []
    for i, (k, b, p) in enumerate( zip(keywords_found, type_business_found, pos_found) ):
        current_sentence = getSentenceThatContainsThisKeyword(sentence_spans=sentence_spans,keyword_pos=p) # sentence that contains a keyword
        if current_sentence == None:
            # no sentence was found that contains the keyword p. (should not happen)
            continue

        # get context for this sentence: from the position of the keyword until the end of the sentence
        words = word_tokenize(current_sentence, engine='newmm', custom_dict=trie)
        for j, w in enumerate(words):
            if w == k:
                context = words[j+1:] # context is from the keyword until the end of the sentence

        contexts.append(context)
        sentences.append(current_sentence)

    return zip(keywords_found, type_business_found, pos_found, contexts, sentences)
# %%
def do_sentiment_one_context(context):
    """
    input: 
        context: list of strings - the words between a keyword until the end of that sentence
    return:
        score: int - total score for this context
    """
    
    # find positive words
    positive_score = 0
    negative_score = 0
    for i, w in enumerate(context):
        for p in positive_words:
            if w == p and context[max(i-1,0)] != 'ไม่':
                positive_score += 1
            elif w == p and context[max(i-1,0)] == 'ไม่':
                negative_score += 1

    # find negative words
    for i, w in enumerate(context):
        for n in negative_words:
            if w == n and context[max(i-1,0)] != 'ไม่':
                negative_score += 1
            elif w == n and context[max(i-1,0)] == 'ไม่':
                positive_score += 1

    # print(context)
    # print(positive_score, negative_score)
    # print('')

    return positive_score - negative_score

# %%
def do_sentiment_whole_news(news: str):
    """
    inputs:
        news: the raw string of news

    return:
        result: list of tuple. each tuple is ('business type', score, sentence)
        positive score = positive news
        negative score = negative news
    """
    contexts = get_contexts(news)
    result = []
    for k,b,p,c,s in contexts:
        score = do_sentiment_one_context(c)
        result.append((b,score,s))

    return result

# %%
if __name__ == "__main__":
    # TODO improve sentence tokenize
    # TODO keyword normalize e.g. 5 จี -> 5G
    # TODO expand sentiment lexicon
    # TODO put positive/negative lexicon in DB

    test_string1 = """
    “เอไอเอสไฟเบอร์” ประคองตัวรอดโควิด-19 เดินหน้าอัพเกรด “เทคโนโลยี-คอนเทนต์-บริการ” เพิ่มดีกรีเขย่าสมรภูมิไฮสปีดเน็ต เร่งเก็บมาร์เก็ตแชร์ทั่วประเทศ มั่นใจกวาดลูกค้าใหม่ทั้งปี 3 แสนราย ผนึก “แอปเปิล” หั่นราคาสมาร์ททีวี 30% กระตุ้นตลาด เล็งดึง 5G เจาะตลาดคอนโดฯ

    นายศรัณย์ ผโลประการ หัวหน้าฝ่ายงานบริหารธุรกิจฟิกซ์ บรอดแบนด์ เอไอเอส เปิดเผยว่า การแข่งขันด้านราคาในธุรกิจอินเทอร์เน็ตบรอดแบนด์ปีนี้เทียบปีที่ผ่านมา “ดูดีขึ้น” มีการแข่งขันกันบนพื้นฐาน “ราคา” ที่สมเหตุสมผลขึ้น ขณะที่สถานการณ์โควิด-19 ส่งผลกระทบต่อภาพรวมตลาดพอสมควร ทั้งในแง่การทำตลาดที่ลำบากขึ้น และการลดค่าใช้จ่ายของผู้บริโภค แต่จากกระแส “เวิร์กฟรอมโฮม” ผลักดันให้ความต้องการในการใช้งานเพิ่มขึ้นมาก

    นายศรัณย์ เชื่อว่าฐานลูกค้าเอไอเอสไฟเบอร์ในปีนี้จะโตไม่น้อยไปกว่าปีที่ผ่านมาที่เพิ่มจาก 7 แสนราย เป็น 1 ล้านราย หรือเพิ่มขึ้น 3 แสนรายโดย ณ ไตรมาสแรก/2563 มีฐานลูกค้า 1.1 ล้านราย มีส่วนแบ่งตลาด 11% โตต่อเนื่อง แต่คงต้องบอกว่าโควิด-19 ส่งผลทั้งในแง่บวกและลบ แง่บวกคือลูกค้าต้องการติดบรอดแบนด์อินเทอร์เน็ตเพิ่ม แต่ในแง่ลบคนส่วนใหญ่หันมาประหยัดค่าใช้จ่าย แม้จะมีความต้องการจึงเลือกบริการที่ราคาไม่แพง
    """

    # context = get_contexts(test_string1)
    # for a,b,c,d in context:
    #     print(a,b,c,d)
    #     print("")

    result = do_sentiment_whole_news(test_string1)
    print(result)

    test_string2 = """
    ทั้งนี้ หลังจากที่คณะกรรมการกิจการกระจายเสียง กิจการโทรทัศน์ และกิจการโทรคมนาคมแห่งชาติ หรือ กสทช. ได้จัดงานประมูลคลื่น 5 จี ขึ้นเมื่อวันที่ 16 ก.พ.2563 เอไอเอสได้คลื่นความถี่แบรนด์ 41 (TDD, 2600 MHz) รวม 100 MHz (10 ใบอนุญาต) และทรูมูฟเอช ได้รวม 90 MHz (9 ใบอนุญาต)
    Opensignal พบว่า ระหว่างวันที่ 1 เม.ย.-30 มิ.ย.2563 ทั้งเอไอเอสและทรูมูฟเอช ได้ใช้คลื่น 2600 MHz ที่ได้มาใหม่จำนวน 20-40 MHz สำหรับให้บริการ 4 จีในบางพื้นที่

    ทำให้ผู้ใช้คลื่นความถี่ Band 41 ได้รับประสบการณ์ความเร็วในการดาวน์โหลด 4 จี ดีกว่าอย่างเห็นได้ชัดทั้งบนเครือข่ายของเอไอเอสและทรูมูฟเอช มีความเร็วดาวน์โหลดเฉลี่ยที่ 14.1 Mbps และ 18.4 Mbps ตามลำดับ โดยผู้ใช้ที่เชื่อมต่อบนคลื่นความถี่สูงกว่า มักจะได้รับประสบการณ์การใช้งานรวดเร็วกว่าผู้ใช้ในย่านความถี่ต่ำ เนื่องจากมีแบนด์วิดท์มากกว่า

    ทั้งนี้ จากการประเมินการถือครองคลื่นความถี่ของผู้ให้บริการโทรศัพท์มือถือในไทยแต่ละราย พบว่าก่อนการประมูลคลื่น 5 จี ดีแทคใช้คลื่นความถี่สูงสุด (90 MHz) สำหรับบริการ 4 จี ตามด้วยเอไอเอส (80 MHz) และทรูมูฟเอช (70 MHz) ตามลำดับ อย่างไร ก็ตาม หลังการประมูลสิ้นสุด เอไอเอสและทรูมูฟเอช นำคลื่นความถี่ Band 41 ใหม่ไปใช้ในการให้บริการ 4 จีเพิ่มเติมระหว่าง 20 ถึง 40 MHz (ปริมาณขึ้นอยู่กับพื้นที่) ทำให้ปริมาณการใช้คลื่นเพื่อให้บริการ 4จีทั้งหมด สูงขึ้นเป็น 120 MHz และ 110MHz ตามลำดับ ขณะที่คลื่น 4จีของดีแทคไม่มีการเปลี่ยนแปลง
    จากการตรวจสอบเพิ่มเติม Opensignal พบอีกว่า เอไอเอสนำคลื่นความถี่ไปใช้เฉพาะในจังหวัดที่มีประชากรหนาแน่น เช่น กรุงเทพมหานคร ขณะที่การใช้งานคลื่นของทรูมูฟเอชมีขอบเขตที่กว้างกว่า

    อย่างไรก็ตาม ขณะนี้ 5 จีในประเทศไทยยังอยู่ในจุดเริ่มต้น จึงน่าจะเร็วเกินไปที่จะสรุป อนาคต แต่การใช้งานเครือข่ายอย่างหนักหน่วง หนาแน่นของคนไทย ยังเป็นปัจจัยสำคัญที่ทำให้ความเร็วในการดาวน์โหลดต่ำ เนื่องจากคลื่นความถี่เป็นทรัพยากรที่มีจำกัด ผู้ให้บริการจึงจำเป็นต้องสร้างสมดุลการใช้ทรัพยากรนี้ ระหว่างผู้ใช้ 5 จีใหม่และผู้ใช้ 4 จี ที่เป็นกลุ่มผู้ใช้ส่วนใหญ่ในปัจจุบัน

    Opensignal รายงานว่า เทคโนโลยี 5 จี ช่วยให้ผู้ให้บริการสามารถเข้าถึงคลื่นความถี่ใหม่ ที่บรรเทาความแออัดของการใช้งาน ตัวอย่างเช่น การประมูลคลื่นความถี่แบบ mmWave ในย่านความถี่ 26 GHz ซึ่งมีสมรรถนะและความเร็วสูงมาก แต่ครอบคลุมพื้นที่ไม่กว้าง เหมาะกับการให้บริการย่านใจกลางเมืองที่มีประชากรหนาแน่น แต่ไม่เหมาะกับการใช้งานในพื้นที่กว้างขวาง หมายความว่าผู้ใช้ 5 จี ในประเทศไทยส่วนใหญ่ มักจะใช้คลื่นความถี่ระดับกลางเช่นคลื่นความถี่ 2600 MHz เพื่อเชื่อมต่อกับ 5 จี แทนที่จะเป็น mmWave.
    """

    result = do_sentiment_whole_news(test_string2)
    print(result)
# %%

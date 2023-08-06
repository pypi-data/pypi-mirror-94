# %%

"""
- read all the positive/negative words from lexicon-thai/
- expect the data to be at ./lexicon-thai/sentiment
- requires: pythainlp

"""

from pythainlp import word_tokenize
import os

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

def check_sentiment(test_string: str) -> str:
    test_words = word_tokenize(test_string)

    # count the number of positive/negative words

    count_pos = 0
    count_neg = 0

    for w in test_words:
        if w in positive_words:
            count_pos += 1
        elif w in negative_words:
            count_neg += 1

    sum_sentiment = count_pos - count_neg

    NEGATIVE_THRES = -5
    POSITIVE_THRES = 5

    if sum_sentiment <= -5:
        result = "negative"
    elif sum_sentiment > -5 and sum_sentiment < 5:
        result = "neutral"
    else:
        result = "positive"

    return result

# %%
# unit test

if __name__ == "__main__":
    test_string = """
    “เอไอเอสไฟเบอร์” ประคองตัวรอดโควิด-19 เดินหน้าอัพเกรด “เทคโนโลยี-คอนเทนต์-บริการ” เพิ่มดีกรีเขย่าสมรภูมิไฮสปีดเน็ต เร่งเก็บมาร์เก็ตแชร์ทั่วประเทศ มั่นใจกวาดลูกค้าใหม่ทั้งปี 3 แสนราย ผนึก “แอปเปิล” หั่นราคาสมาร์ททีวี 30% กระตุ้นตลาด เล็งดึง 5G เจาะตลาดคอนโดฯ

    นายศรัณย์ ผโลประการ หัวหน้าฝ่ายงานบริหารธุรกิจฟิกซ์ บรอดแบนด์ เอไอเอส เปิดเผยว่า การแข่งขันด้านราคาในธุรกิจอินเทอร์เน็ตบรอดแบนด์ปีนี้เทียบปีที่ผ่านมา “ดูดีขึ้น” มีการแข่งขันกันบนพื้นฐาน “ราคา” ที่สมเหตุสมผลขึ้น ขณะที่สถานการณ์โควิด-19 ส่งผลกระทบต่อภาพรวมตลาดพอสมควร ทั้งในแง่การทำตลาดที่ลำบากขึ้น และการลดค่าใช้จ่ายของผู้บริโภค แต่จากกระแส “เวิร์กฟรอมโฮม” ผลักดันให้ความต้องการในการใช้งานเพิ่มขึ้นมาก

    นายศรัณย์ เชื่อว่าฐานลูกค้าเอไอเอสไฟเบอร์ในปีนี้จะโตไม่น้อยไปกว่าปีที่ผ่านมาที่เพิ่มจาก 7 แสนราย เป็น 1 ล้านราย หรือเพิ่มขึ้น 3 แสนรายโดย ณ ไตรมาสแรก/2563 มีฐานลูกค้า 1.1 ล้านราย มีส่วนแบ่งตลาด 11% โตต่อเนื่อง แต่คงต้องบอกว่าโควิด-19 ส่งผลทั้งในแง่บวกและลบ แง่บวกคือลูกค้าต้องการติดบรอดแบนด์อินเทอร์เน็ตเพิ่ม แต่ในแง่ลบคนส่วนใหญ่หันมาประหยัดค่าใช้จ่าย แม้จะมีความต้องการจึงเลือกบริการที่ราคาไม่แพง
    """

    print(check_sentiment(test_string))
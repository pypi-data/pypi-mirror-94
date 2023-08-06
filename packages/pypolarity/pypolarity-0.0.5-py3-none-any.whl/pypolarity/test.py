from pypolarity import do_sentiment_whole_news
text = "อยากถามเอไอเอสว่าเอาเน็ตสมัยไหนมาให้ใช้ช้ามากๆ ทั้งเกมทั้งยูทูป เรียนอีก บางทีหลุดด้วย"
result, sentiment = do_sentiment_whole_news(text)
print(result,sentiment)
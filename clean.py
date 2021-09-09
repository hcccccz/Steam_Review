import json
import re
from datetime import datetime
from redis import StrictRedis
#删掉 "average achievements"
#修改 “price“
#算出推出日期
#算出评论数量
#算出好评率
#增加语言支持


def remove_key(dict_ob,key):
    if key in dict_ob:
        del dict_ob[key]
    return dict_ob
redis = StrictRedis(password="2921038")
keys  = redis.keys()

def clean(before):
    converter = {'Aug':8,'Jan':1,'Dec':12,'Apr':4,'Sep':9,'Mar':3,'Jun':6,'May':5,'Feb':2,'Nov':11,'Oct':10,'Jul':7}
    pattern = re.compile(r'[A-Za-z]{3}\s\d+?,\s\d{4}')
    pattern1 = re.compile(r'\s(\d+?),\s')


    if len(before) == 26:
        before = remove_key(before,"average achievements")
    # print(len(before))
    price = before['price']

    date = before['release_date']
    before['price'] = eval(price)/100
    m = pattern.match(date)
    if not m:
        date_no = True
    else:
        data_no = False
        month = converter[date[0:3]] #month
        day = pattern1.search(date).group(1) #day
        day = eval(day)
        year = eval(date[-4::]) #year
        date = datetime(year,month,day)
        days_from_release  = datetime(2021,8,26) - date
        before['days_from_release'] = days_from_release.days
    before['languages_supports'] = len(before['languages'].split(","))
    review_num = before['positive'] +before['negative']
    before['review_num'] = review_num
    if review_num != 0:
        before['positive_rate'] = round(before['positive']/review_num,2)
    else:
        before['positive_rate'] = 0
    return [before,data_no] #before is dict

for key in keys:
    data = json.loads(redis.get(key).decode("utf-8"))
    if len(data) == 25 or len(data) == 26:
        pack = clean(data)
        if pack[1] == True:
            redis.delete(key)
        else:
            redis.set(key,json.dumps(pack[0]))

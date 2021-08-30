from redis import StrictRedis
import json
import re
from datetime import datetime
import csv
redis = StrictRedis(password = "2921038")

pattern = re.compile(r'[A-Za-z]{3}\s\d+?,\s\d{4}')
pattern1 = re.compile(r'\s(\d+?),\s')
def remove_key(dict_ob,key):
    if key in dict_ob:
        del dict_ob[key]
    return dict_ob

l = redis.keys("*")


converter = {'Aug':8,'Jan':1,'Dec':12,'Apr':4,'Sep':9,'Mar':3,'Jun':6,'May':5,'Feb':2,'Nov':11,'Oct':10,'Jul':7}


with open("data.csv","w") as file:

    fieldnames = list(eval(redis.get(l[0]).decode("utf-8")).keys())
    writer = csv.DictWriter(file,fieldnames = fieldnames)
    writer.writeheader()
    for i in l:
        i = i.decode("utf-8")
        value = redis.get(i).decode("utf-8")
        data = json.loads(value)
        writer.writerow(data)



# s = []
#     print(list(data.keys()))




    # # m = pattern.match(date)
    # # if not m:
    # #     redis.delete(i)
    # month = converter[date[0:3]] #month
    # day = pattern1.search(date).group(1) #day
    # day = eval(day)
    # year = eval(date[-4::]) #year
    # date = datetime(year,month,day)
    #
    # days_from_release  = datetime.today() - date
    # data['days_from_release'] = days_from_release.days
    # redis.set(i,json.dumps(data))



# "average achievements"
# for i in l1:
    # print(i['release_date'].split(" "))
# for i in l:
#     data = redis.get(i.decode("utf-8"))
#     new_data = remove_key(eval(data.decode("utf-8")),"average achievements")
#     new_data = json.dumps(new_data)
#     redis.set(i,new_data)

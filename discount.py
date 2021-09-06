import requests
from bs4 import BeautifulSoup
from redis import StrictRedis
import json
import re
import time
api_key = "cde859f3f3547c8bf77941b2cff1e214884d9d4b"

redis = StrictRedis(password="2921038")

keys = [ i.decode("utf-8") for i in redis.keys()]
i = redis.get(keys[0]).decode("utf-8")

# i = json.loads(i)

url = "https://isthereanydeal.com/game/tomclancysdivision/history/"
#
with open("plain.json") as file:
    plain = file.read()

plain_map = json.loads(plain)['data']['steam']
#

# for key in keys:
#
#     free = False
#     id = "app/" +key
#     if id in plain_map:
#         data = json.loads(redis.get(key).decode("utf-8"))
#         plain = plain_map[id]
#         url = "https://isthereanydeal.com/game/" +plain + "/history/"
#         #https://isthereanydeal.com/game/battlecrewspacepirates/history/
#
#         r = requests.get(url)
#         soup = BeautifulSoup(r.text,"html.parser")
#         soup = soup.find("div",{"id":"historyLogContent"})
#         soup = soup.find_all("div",{"class":"lg2 game","data-shop":"steam"})
#
#         cut_time = 0
#         average_cut = []
#         average_cut_duration = []
#         average_price = []
#         print(plain)
#         for s in soup:
#             pattern = re.compile(r'\d+')
#             duration = s.find("i").get_text()
#
#             initial_price = s.find("span",{"class":"lg2__price"}).get_text()
#             initial_price = eval(initial_price.replace("$",""))
#             after_price = s.find("span",{"lg2__price lg2__price--new"}).get_text()
#             after_price= eval(after_price.replace("$",""))
#
#             if initial_price == 0:
#                 free = True
#             else:
#                 if after_price < initial_price:
#                     cut_time += 1 #cut time
#                     cut_off = 1 - after_price/initial_price
#                     average_cut.append(cut_off) #average_cut
#                     day = pattern.match(duration).group()
#                     average_cut_duration.append(eval(day)) #average_cut_duration
#                     average_price.append(after_price) #average_price
#                 else:
#                     average_price.append(after_price)
#         if not free:
#
#             c = cut_time
#             a = sum(average_cut)/len(average_cut)
#             b= sum(average_cut_duration)/len(average_cut_duration)
#             d = sum(average_price)/len(average_price)
#             print("cut_time: {},average_cut: {}, duration: {}, average_price".format(c,a,b,d))
#             time.sleep(2)

r = requests.get("https://isthereanydeal.com/game/battlecrewspacepirates/history/")
soup = BeautifulSoup(r.text,"html.parser")
soup = soup.find("div",{"id":"historyLogContent"})
soup = soup.find_all("div",{"class":"lg2 game","data-shop":"steam"})
pattern = re.compile(r'\d+')
pattern_price = re.compile(r'\$(\d+\.\d+?)<')
for i in soup:
    day = i.find("i").get_text() #duration
    match = pattern.match(day)
    # if match:
        # print(match.group())
    print(pattern_price.search(str(i)).group(1))

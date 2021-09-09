import requests
from bs4 import BeautifulSoup
from redis import StrictRedis
import json
import re
import time
import math
from tqdm import tqdm
api_key = "cde859f3f3547c8bf77941b2cff1e214884d9d4b"

def average(l):
    if len(l):
        return sum(l)/len(l)
    else:
        return 0


def soup_process(soup):
    soup = soup.find_all("div",{"class":"lg2 game","data-shop":"steam"})
    cut_time = 0
    average_cut = []
    average_cut_duration = []
    average_price = []

    for s in soup:
        pattern = re.compile(r'\d+')
        pattern_price = re.compile(r'\$(\d+\.\d+?)<')
        price_group = [eval(i) for i in pattern_price.findall(str(s))]
        min_price = min(price_group)
        max_price = max(price_group)
        duration = s.find("i").get_text() #singe duration

        if max_price == 0:
            free = True
        else:
            free = False
            if min_price < max_price: #it is a discount
                cut_time += 1 #cut time
                cut_off = 1 - min_price/max_price
                average_cut.append(cut_off) #average_cut
                match = pattern.match(duration)
                if match:
                    day = match.group()
                else:
                    day = "1"
                average_cut_duration.append(eval(day)) #average_cut_duration
                average_price.append(min_price) #average_price
            else:
                average_price.append(min_price)
    price_p = sum(average_price)
    if price_p != 0:

        c = cut_time
        a = round(average(average_cut),2)
        b= math.ceil(average(average_cut_duration))
        d = round(average(average_price),2)
        print("cut_time: {},average_cut: {}, duration: {}, average_price: {}".format(c,a,b,d))
        data = {"cut_time":c,"average_cut":a,"duration":b,"average_price":d}
    else:
        data = {"cut_time":0,"average_cut":0,"duration":0,"average_price":0}
    time.sleep(2)
    return data



redis = StrictRedis(password="2921038")

keys = [ i.decode("utf-8") for i in redis.keys()]
keys_to_remove = []
print("checking keys")
for key in tqdm(keys):
    item = json.loads(redis.get(key).decode("utf-8"))
    if len(item) == 33 or len(item) ==1:

        keys_to_remove.append(key)
for key in keys_to_remove:
    keys.remove(key)
print(len(keys))


# i = json.loads(i)

url = "https://isthereanydeal.com/game/tomclancysdivision/history/"
#
with open("plain.json") as file:
    plain = file.read()

plain_map = json.loads(plain)['data']['steam']
#
#
for idx in (range(len(keys)):

    free = False
    id = "app/" +keys[idx]
    origin_data = json.loads(redis.get(keys[idx]).decode("utf-8"))
    d_len = len(origin_data)
    if id in plain_map and d_len == 29:

        plain = plain_map[id]
        url = "https://isthereanydeal.com/game/" +plain + "/history/"
        #https://isthereanydeal.com/game/driftgearracingfree/history/

        print("{}:{} at {}".format(idx,plain,len(keys)))
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        soup = soup.find("div",{"id":"historyLogContent"})

        if soup:
            data = soup_process(soup)
        else:
            data = {"cut_time":"NA","average_cut":"NA","duration":"NA","average_price":"NA"}


        origin_data['cut_time'] = data['cut_time']
        origin_data['average_cut'] =data['average_cut']
        origin_data['duration'] = data['duration']
        origin_data['average_price'] = data['average_price']
        redis.set(keys[idx],json.dumps(origin_data))

    # r = requests.get("https://isthereanydeal.com/game/dungeonfighteronline/history/")
# soup = BeautifulSoup(r.text,"html.parser")
# soup = soup.find("div",{"id":"historyLogContent"})
# soup_process(soup)

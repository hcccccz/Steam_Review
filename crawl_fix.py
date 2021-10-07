import requests
import tqdm
import json
import random
import time
from bs4 import BeautifulSoup
from redis import StrictRedis
import re
import difflib





def play_tracker_get_url(name:str):

    game = []
    url = "https://playtracker.net/search/?q=" + name
    r = requests.get("https://playtracker.net/search/?q=" + name)
    with open("a.html","wb")as file:
        file.write(r.content)
    soup = BeautifulSoup(r.text, 'html.parser')
    game_list = soup.find_all("div",{"class":"half relative flex-responsive search-result"})
    if game_list:

        for i in game_list:

            game_platform = i.find("div",{"class":"full card-top flex relative"}).find("svg")['data-icon']
            game_name = i.find("div",{"class":"full card-top flex relative"}).find("div",{"class":"full"}).get_text()
            if game_platform == "steam-symbol" and game_name == name:

                game_entry = i.find("a")['href']
                game.append(game_entry)
            if len(game) == 1:
                return game[0]
            else:
                return None

def play_tracker_get_data(url:str):
    data = {}


    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    game_col = soup.find("div",{"class":"relative shoo-top"}).find_all("div",{"class":"figure-total relative wow fadeInLeft"})
    col_value = [ i.find("div",{"class":"superbold wider"}).get_text() for i in game_col]
    col_key = [ i.find("div", {"class":"smaller-text faded"}).get_text() for i in game_col ]
    release_date = soup.find("div",{"class":"full flex white-space-integrated"}).find("div",{"class":"half left-separator"}).get_text()
    if len(col_key) == len(col_value) and release_date:
        for i in range(len(col_key)):
            data[col_key[i]] = col_value[i]
        data['release_date'] = release_date

    if "estimated players" in data:
        fix_str = data["estimated players"].replace("~","")
        fix_str = fix_str.replace("*","")
        if "K" in fix_str:
            fix_str = fix_str.replace("K","")
            temp = float(fix_str)
            data["estimated players"] = temp*1000
        elif "M" in fix_str:
            fix_str = fix_str.replace("M","")
            temp = float(fix_str)
            data["estimated players"] = temp*1000000
    if "estimated active players" in data:

        fix_str = data["estimated active players"].replace("~","")
        fix_str = fix_str.replace("*","")
        fix_str = fix_str.replace("\n","")
        if "K" in fix_str:
            fix_str = fix_str.replace("K","000")
            temp = float(fix_str)
            data["estimated active players"] = temp * 1000
        elif "M" in fix_str:
            fix_str = fix_str.replace("M","000000")
            temp = float(fix_str)
            data["estimated active players"] = temp * 1000000
    return data

def play_tracker_get_url_2(name):
    game = []
    url = "https://playtracker.net/search/?q=" + name
    r = requests.get("https://playtracker.net/search/?q=" + name)
    pattern = re.compile(r'https://playtracker.net/insight/game/\d+')
    soup = BeautifulSoup(r.text, 'html.parser')
    url_all = pattern.findall(r.text)
    d = [soup.find("a", {"href": i})for i in url_all]
    for i in d:
        game_platform = i.find("svg")['data-icon']
        game_name = i.find("div",{"class":"full card-top flex relative"}).find("div",{"class":"full"}).get_text()
        ratio = difflib.SequenceMatcher(None, game_name, name).quick_ratio()

        if game_platform == "steam-symbol" and ratio > 0.90:
            game.append(i['href'])

    return game[0]

redis = StrictRedis(password = "2921038")

keys = redis.keys()
with open("crawl_fix.text", "r") as file:
    fail = file.readlines()
fail = [f.replace("\n","") for f in fail]


with open("Data/App_list.json","r") as file:
    f = json.loads(file.read())
    app_list = f['applist']['apps']

app_dict = {}



for app in app_list:
    app_dict[app['appid']] = app['name']


fix = []
for key in tqdm.tqdm(keys):
    ob = json.loads(redis.get(key).decode("utf-8"))
    if len(ob) == 33:
        name = app_dict[ob['appid']]
        try:
            url = play_tracker_get_url_2(name)

            data = play_tracker_get_data(url)
            eap = data["estimated active players"]
            ep = data["estimated players"]
            ob["estimated active players"] = eap
            ob["estimated players"] = ep
            ob["fix"] = "True"
            redis.set(key,json.dumps(ob))
            time.sleep(2)
        except Exception as e:
            print(e)
            with open("crawl_fix.text", "a") as file:
                file.write(ob['name']+"\n")










# d = play_tracker_get_url_2("King Of Mazes")
# print(d)
# data = play_tracker_get_data(url)

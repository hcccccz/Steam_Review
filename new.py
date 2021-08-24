import requests
from tqdm import tqdm
import json
import random
import time
from bs4 import BeautifulSoup








def sample_app(n:int):

    with open("App_list.json","r") as file:
        f = json.loads(file.read())
        app_list = f['applist']['apps']
        sample = random.sample(app_list,n)

        return sample #


def steam_spy_get(appid:int):

    appid = str(appid)
    cookie = "cf_clearance=10bd62346305b0761445b6862fc08b0ccc080605-1628993799-0-250; __cf_bm=6298fd621af5ba5bdaa079cb5475b09fdb99a5f7-1628995259-1800-AdnvoQRWAGZDBDGMds38h9PJW/XjVw/NYAY3TC/6NQttHrgYWZyXkg/OlJEClth5rETRXaQ8hIFn/TlnbqtV0xs="
    headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 UOS"
    ,"cookie":cookie
    }

    url = "http://steamspy.com/api.php?request=appdetails&appid=" + appid

    response = requests.get(url)
    # print(type(response.text))
    # print(response.text)  v
    return response.status_code


def play_tracker_get_url(name:str):

    game = []
    url = "https://playtracker.net/search/?q=" + name
    r = requests.get("https://playtracker.net/search/?q=" + name)
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
            data["estimated players"] = fix_str.replace("K","000")
        elif "M" in fix_str:
            data["estimated players"] = fix_str.replace("M","000000")
    if "estimated active players" in data:

        fix_str = data["estimated active players"].replace("~","")
        fix_str = fix_str.replace("*","")
        fix_str = fix_str.replace("\n","")
        if "K" in fix_str:
            data["estimated active players"] = fix_str.replace("K","000")
        elif "M" in fix_str:
            data["estimated active players"] = fix_str.replace("M","000000")

    return data
l = sample_app(100)
for i in l:
    print(steam_spy_get(i['appid']))
    time.sleep(2)

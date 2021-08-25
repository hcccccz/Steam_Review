import requests
from tqdm import tqdm
import json
import random
import time
from bs4 import BeautifulSoup
from redis import StrictRedis







def sample_app(n:int):

    with open("App_list.json","r") as file:
        f = json.loads(file.read())
        app_list = f['applist']['apps']
        sample = random.sample(app_list,n)

        return sample #


def steam_spy_get(appid:int):
    try:
        appid = str(appid)

        headers = {
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 UOS"
        }
        url = "http://steamspy.com/api.php?request=appdetails&appid=" + appid
        response = requests.get(url)
        return response.text
    except:
        return None
    # print(type(response.text))
    # print(response.text)  v


def play_tracker_get_url(name:str):

    game = []
    url = "https://playtracker.net/search/?q=" + name
    try:
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
    except:
        return None
def play_tracker_get_data(url:str):
    data = {}
    try:

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
    except:
        return None
# l = sample_app(100)

# for i in l:
#     url = play_tracker_get_url(i['name'])
#     if url:
#         data = play_tracker_get_data(url)
#         redis.hset(i["appid"],mapping=data)
#         print("获取成功，已加入数据库")
#         time.sleep(1)
def log(status_fail,appid):
        with open("time.json","r") as file:
            log = json.loads(file.read())

        if status_fail:
            log['Fail'] += 1
            log['Fail_id'].append(appid)
        else:
            log['Success'] += 1
            print("log!")
        with open("time.json","w") as file:

            file.write(json.dumps(log))
def check_exist(appid,redis):

    with open("time.json","r") as file:

        log = json.loads(file.read())
        if appid in log['Fail_id'] and redis.exists(appid):
            return False
        else:
            return True



def crawl():
    redis = StrictRedis(password="2921038")
    Fail = False
    while True:

        app_list = sample_app(100)
        for app in app_list:
            # steam_spy_get(app['appid'])
            url = play_tracker_get_url(app['name'])
            appid = app['appid']
            if check_exist(appid,redis):
                if not url:
                    Fail = True
                else:
                    data = play_tracker_get_data(url)
                    if not data:
                        Fail = True
                    else:
                        redis.hset(appid,mapping=data)
                        print("success",Fail)

                log(Fail,appid)
                time.sleep(1)
            else:
                pass
            Fail = False

# crawl()

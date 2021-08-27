from bs4 import BeautifulSoup
import requests
import json
from redis import StrictRedis
import aiohttp
import asyncio
import time
from random import choice
def crawl_66():
    start_url = "http://www.66ip.cn/{}.html"
    urls= [start_url.format(page) for page in range(1,4+1)]
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text,'html.parser')
        rows = soup.find("div",{"class":"containerbox boxindex"}).find_all("tr")
        if len(rows) >1:
            for row in rows[1::]:
                ip = row.td.get_text()
                port = row.td.next_sibling.get_text()
                yield ":".join([ip,port])

def crawl_geonode():
    r = requests.get("https://proxylist.geonode.com/api/proxy-list?limit=150&page=1&sort_by=speed&sort_type=asc&protocols=http%2Chttps")
    for i in json.loads(r.text)['data']:
        ip = i['ip']
        port = i['port']
        yield ":".join([ip,port])

def add_proxy(proxy):
    redis = StrictRedis()
    if not redis.zscore("my_proxy",proxy):
        return redis.zadd("my_proxy",{proxy:10})

def get_proxy():
    redis = StrictRedis()
    old = redis.zcard("my_proxy")
    for i in crawl_geonode():
        add_proxy(i)
    new = redis.zcard("my_proxy")
    new_add = new-old
    print("添加了",new_add," 代理")
async def test_single_proxy(proxy):
    proxy = proxy.decode("utf-8")
    try:
        test_url = "http://steamspy.com/api.php?request=appdetails&appid=730"
        async with aiohttp.ClientSession() as session:
            proxy_url = "http://" + proxy
            async with session.get(test_url,proxy=proxy_url,timeout=15) as response:
                if response.status == 200:
                    print(proxy,"代理可用")
                    max_score(proxy)
    except:
        print("代理请求失败",proxy)
        decrease_score(proxy)
def test_proxies():
    redis = StrictRedis()
    proxies = redis.zrange("my_proxy",0,-1)
    loop = asyncio.get_event_loop()
    task = [test_single_proxy(proxy) for proxy in proxies]
    loop.run_until_complete(asyncio.wait(task))


def decrease_score(proxy):
    redis = StrictRedis()
    score = redis.zscore("my_proxy",proxy)
    if score > 0:
        print(proxy,"分数",score,"减一")
        return redis.zincrby("my_proxy",-1,proxy)
    else:
        print(proxy,"分数",score,"移除")
        return redis.zrem("my_proxy",proxy)


def max_score(proxy):
    redis = StrictRedis()
    print("代理可用",proxy,"设置为","100")
    return redis.zadd("my_proxy",{proxy:100})


def random_pool_proxy():
    redis = StrictRedis()
    result = redis.zrangebyscore("my_proxy",100,100)
    if len(result):
        return choice(result)
    else:
        result = redis.zrevrange("my_proxy",0,100)
        if len(result):
            return choice(result)
        else:
            raise PoolEmptyError


# get_proxy()
test_proxies()

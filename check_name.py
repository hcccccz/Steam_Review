import json
from redis import StrictRedis
from tqdm import tqdm
with open("crawl_fix.text", "r") as file:
    fail = file.readlines()
fail = [f.replace("\n","") for f in fail]




redis = StrictRedis(password = 2921038)


keys = redis.keys()

db = [json.loads(redis.get(key)) for key in keys]
f_id = []
double = []
for f in tqdm(fail):
    counter = 1
    for d in db:
        if len(d) == 33:
            if f == d['name']:
                counter -= 1
                if counter < -1:
                    double.append(d['appid'])
                f_id.append(d['appid'])
print(len(f_id))
print(len(fail))
print(double)
for i in double:
    print(redis.get(i))
def sample_app():

    with open("Data/App_list.json","r") as file:
        f = json.loads(file.read())
        app_list = f['applist']['apps']
        # sample = random.sample(app_list,n)

        return app_list #

app_list = sample_app()

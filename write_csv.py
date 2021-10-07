import csv
from redis import StrictRedis
import tqdm
import json
redis = StrictRedis(password = "2921038")
keys = redis.keys()

keys = redis.keys()



o_0 = []


for key in tqdm.tqdm(keys):
    ob = json.loads(redis.get(key).decode("utf-8"))
    if len(ob) == 34:
        o_0.append(ob)

fieldnames = list(o_0[0].keys())
with open("Steam1.csv","w") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i in o_0:
        writer.writerow(i)

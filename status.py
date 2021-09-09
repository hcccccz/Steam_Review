from redis import StrictRedis
import json
# import re
# from datetime import datetime
# import csv

#26-29-33




redis = StrictRedis(password = "2921038")
status = []

keys = redis.keys()
for key in keys:
    ob = json.loads(redis.get(key).decode("utf-8"))
    status.append(len(ob))

freq = {}
for item in status:
    if item in freq:
        freq[item] += 1
    else:
        freq[item] = 1
print(json.dumps(freq,indent=4))

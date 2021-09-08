from redis import StrictRedis
import json
# import re
# from datetime import datetime
# import csv

#26-29-33




redis = StrictRedis(password = "2921038")
status = []
redis.set("123",json.dumps(['fail']))
keys = redis.keys()
for key in keys:
    ob = json.loads(redis.get(key).decode("utf-8"))
    status.append(len(ob))

print(set(status))

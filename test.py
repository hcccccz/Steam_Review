from redis import StrictRedis
import math
import json
redis = StrictRedis(password="2921038")
d = redis.get("717840")
d = json.loads(d.decode("utf-8"))
print(json.dumps(d,indent=4))

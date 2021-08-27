from redis import StrictRedis
import json



redis = StrictRedis(password = "2921038")

def remove_key(dict_ob,key):
    if key in dict_ob:
        del dict_ob[key]
    return dict_ob

l = redis.keys("*")

l = [redis.get(i.decode("utf-8")) for i in l]

l1 = [ remove_key(eval(i.decode("utf-8")),"average achievements") for i in l]

# "average achievements"
# print(json.dumps(l1[110],sort_keys=True,indent=4))
for i in l1:
    print(i['release_date'].split(" "))

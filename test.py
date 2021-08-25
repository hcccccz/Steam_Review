from redis import StrictRedis


redis = StrictRedis(password="2921038")
print(redis.get("a").decode("utf-8"))

import redis
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# cache = redis.Redis(host='127.0.0.1', port=6379)
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
# cache = redis.StrictRedis(connection_pool=pool)
cache = redis.Redis(connection_pool=pool)
# print("chenggong")
# cache = tornadoredis.Client(host="127.0.0.1",port=6379)
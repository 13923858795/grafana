import redis, config

Redis = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)



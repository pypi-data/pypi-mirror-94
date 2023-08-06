import redis

try:
    redis_info = Var.REDIS_URI.split(":")
    udB = redis.StrictRedis(
        host=redis_info[0],
        port=redis_info[1],
        password=Var.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True,
    )
except BaseException:
    print("REDIS_URI or REDIS_PASSWORD is wrong! Recheck!")
    print("Ultroid has shutdown!")
    exit(1)
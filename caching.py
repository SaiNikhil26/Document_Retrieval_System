import redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

RATE_LIMIT = 5
RATE_LIMIT_WINDOW = 60


def get_user_request_count(user_id):
    count = redis_client.get(f"user:{user_id}:count")
    return int(count) if count else 0


def increment_user_request_count(user_id):
    current_count = get_user_request_count(user_id)
    if current_count >= RATE_LIMIT:
        return False
    redis_client.incr(f"user:{user_id}:count")
    redis_client.expire(f"user:{user_id}:count", RATE_LIMIT_WINDOW)
    return True


def cache_search_result(cache_key, results, expiration=3600):
    redis_client.setex(cache_key, expiration, str(results))


def get_cached_result(cache_key):
    cached_result = redis_client.get(cache_key)
    return eval(cached_result) if cached_result else None

import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def get_cache_with_key(key):
    value = r.get(key)
    if value is not None:
        return json.loads(value)


def set_cache_with_key(key, value):
    r.set(key, json.dumps(value))


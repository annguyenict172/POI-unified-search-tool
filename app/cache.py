import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


class Cache:
    @staticmethod
    def get_from_location(location):
        value = r.get(location)
        if value is not None:
            return json.loads(value)

    @staticmethod
    def set_cache_with_location(location, value):
        r.set(location, json.dumps(value))

import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


class Cache:
    @staticmethod
    def get_from_location(location):
        results = r.get(location)
        if results is not None:
            return json.loads(results)

    @staticmethod
    def set_cache_with_location(location, results):
        appeared = {}
        for item in results:
            try:
                if appeared.get(item['id']) is None:
                    appeared[item['id']] = True
                else:
                    results.remove(item)
            except KeyError:
                results.remove(item)
        r.set(location, json.dumps(results))

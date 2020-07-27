import json
import requests

CACHE_SERVER_BASE_URL = 'http://0.0.0.0:5002'
CACHE_QUERY_ENDPOINT = '{}{}'.format(CACHE_SERVER_BASE_URL, '/queries')


def retrieve_from_cache(args):
    params = _transform_arguments(args)
    res = requests.get(CACHE_QUERY_ENDPOINT, params)
    if res.status_code != 200:
        return None, None, None
    data = res.json()
    return data['results'], data['page'], data['total_pages']


def store_to_cache(args, results):
    data = _transform_arguments(args)
    data.update(results=results)
    res = requests.post(CACHE_QUERY_ENDPOINT, json=json.dumps(data))
    if res.status_code != 201:
        return None, None
    data = res.json()
    return data['results'], data['total_pages']


def _transform_arguments(args):
    return {
        'latitude': args['location'].split(',')[0],
        'longitude': args['location'].split(',')[1],
        'radius': args['radius'],
        'categories': args['categories'],
        'page': args.get('page')
    }

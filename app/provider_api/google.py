import time

from config import Config
from .base import ProviderAPI


class GoogleAPI(ProviderAPI):
    endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    _base_params = {
        'key': Config.GOOGLE_PLACE_API_KEY
    }

    def find_places(self, params):
        results = []
        if len(params.get('type')) > 0:
            types = params.pop('type')
            for type in types:
                pagetoken = None
                while True:
                    params['pagetoken'] = pagetoken
                    params['type'] = type
                    res = self._call_api(self.endpoint, params)
                    pagetoken = res.json().get('next_page_token')
                    items = res.json()['results']
                    for item in items:
                        item['unified_category'] = type
                    results.extend(items)
                    time.sleep(2)
                    if pagetoken is None:
                        break
        else:
            pagetoken = None
            while True:
                params['pagetoken'] = pagetoken
                res = self._call_api(self.endpoint, params)
                pagetoken = res.json().get('next_page_token')
                results.extend(res.json()['results'])
                time.sleep(2)
                if pagetoken is None:
                    break
        print('GOOGLE: {}'.format(len(results)))
        return results

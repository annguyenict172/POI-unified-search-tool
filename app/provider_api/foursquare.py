from config import Config
from .base import ProviderAPI


class FoursquareAPI(ProviderAPI):
    endpoint = 'https://api.foursquare.com/v2/venues/explore'
    _base_params = {
        'oauth_token': Config.FOURSQUARE_OAUTH_TOKEN,
        'v': '20190406'
    }

    def find_places(self, params):
        results = []
        if len(params.get('section')) > 0:
            sections = params.pop('section')
            for section in sections:
                temp_results = []
                total_results = 1000000
                last_length = 0
                while len(temp_results) < total_results:
                    params['limit'] = 50
                    params['offset'] = len(temp_results)
                    params['section'] = section
                    res = self._call_api(self.endpoint, params)
                    items = res.json()['response']['groups'][0]['items']
                    for item in items:
                        item['unified_category'] = section
                    temp_results.extend(items)
                    total_results = res.json()['response']['totalResults']
                    if len(temp_results) == last_length:
                        break
                    last_length = len(temp_results)
                results.extend(temp_results)
        else:
            total_results = 1000000
            last_length = 0
            while len(results) < total_results:
                params['limit'] = 50
                params['offset'] = len(results)
                res = self._call_api(self.endpoint, params)
                results.extend(res.json()['response']['groups'][0]['items'])
                total_results = res.json()['response']['totalResults']
                if len(results) == last_length:
                    break
                last_length = len(results)
        print('FOURSQUARE: {}'.format(len(results)))
        return results

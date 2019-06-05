from config import Config
from .base import ProviderAPI


class FacebookAPI(ProviderAPI):
    endpoint = 'https://graph.facebook.com/search'
    _base_params = {
        'type': 'place',
        'access_token': Config.FACEBOOK_ACCESS_TOKEN
    }

    def find_places(self, params):
        after = None
        results = []
        if len(params.get('categories')) > 0:
            for category in params.get('categories'):
                params['categories'] = '["{}"]'.format(category)
                while True:
                    params['after'] = after
                    params['fields'] = 'id,about,description,name,location,phone,picture,website,overall_star_rating,' \
                                       'category_list,checkins'
                    res = self._call_api(self.endpoint, params)
                    data = res.json().get('data')
                    if data:
                        for item in data:
                            item['unified_category'] = category
                        results.extend(data)
                    paging = res.json().get('paging')
                    if paging:
                        after = paging['cursors'].get('after')
                        if after is None:
                            break
                    else:
                        break
        else:
            while True:
                params['after'] = after
                params['fields'] = 'id,about,description,name,location,phone,picture,website,overall_star_rating,' \
                                   'category_list,checkins'
                res = self._call_api(self.endpoint, params)
                data = res.json().get('data')
                if data:
                    results.extend(data)
                paging = res.json().get('paging')
                if paging:
                    after = paging['cursors'].get('after')
                    if after is None:
                        break
                else:
                    break
        print('FACEBOOK: {}'.format(len(results)))
        return results

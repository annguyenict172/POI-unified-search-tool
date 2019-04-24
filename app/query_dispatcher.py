from app.api import FoursquareAPI, GooglePlaceAPI, FacebookAPI
from app.models import Category


class QueryDispatcher:
    foursquare_api = FoursquareAPI()
    google_api = GooglePlaceAPI()
    facebook_api = FacebookAPI()

    def __init__(self, args):
        self.args = args

    def can_dispatch(self):
        if self.args['location'] == '':
            return False
        return True

    def dispatch_query(self):
        res = self.google_api.get_geocoding(self.args['location'])
        geometry = res.json()['results'][0]['geometry']['location']
        # results = self._query_from_google(geometry) + self._query_from_foursquare(geometry)
        # results.sort(key=lambda x: x['core_info']['name'])
        return self._query_from_facebook(geometry)

    def _query_from_facebook(self, geometry):
        after = None
        results = []
        while True:
            res = self.facebook_api.find_places({
                'center': '{},{}'.format(geometry['lat'], geometry['lng']),
                'distance': 1000,
                # 'fields': 'id,about,distance,checkins,description,location,name,overall_star_rating,phone,'
                #           'website,photos,picture',
                'fields': 'id,about,description,name,location,phone,picture,website,overall_star_rating,checkins',
                'after': after,
                'categories': '["FOOD_BEVERAGE"]'
            })
            data = res.json().get('data')
            results.extend(data)
            paging = res.json().get('paging')
            if paging:
                after = paging['cursors'].get('after')
                if after is None:
                    break
            else:
                break
        print(len(results))
        return results

    def _query_from_google(self, geometry):
        results = []
        for type in self._find_matched_categories('Google'):
            pagetoken = None
            while True:
                res = self.google_api.nearby_search({
                    'location': '{},{}'.format(geometry['lat'], geometry['lng']),
                    'radius': 1000,
                    'type': type,
                    'pagetoken': pagetoken
                })
                pagetoken = res.json().get('next_page_token')
                items = res.json()['results']
                for item in items:
                    item['core_info'] = {
                        'name': item['name'],
                        'location': item['geometry']['location']
                    }
                results.extend(items)
                if pagetoken is None:
                    break
        return results

    def _query_from_foursquare(self, geometry):
        results = []
        total_results = 1000000
        last_length = 0
        while len(results) < total_results:
            res = self.foursquare_api.search_venues({
                'll': '{},{}'.format(geometry['lat'], geometry['lng']),
                'limit': 50,
                'offset': len(results),
                'section': 'food',
                'radius': 1000
            })
            items = res.json()['response']['groups'][0]['items']
            for item in items:
                item['core_info'] = {
                    'name': item['venue']['name'],
                    'location': item['venue']['location']
                }
            results.extend(items)
            total_results = res.json()['response']['totalResults']
            if len(results) == last_length:
                break
            last_length = len(results)
        return results

        # results = []
        # categoryId = ','.join(self._find_matched_categories('Foursquare'))
        # total_results = 1000000
        # last_length = 0
        # while len(results) < total_results:
        #     res = self.foursquare_api.search_venues({
        #         'll': '{},{}'.format(geometry['lat'], geometry['lng']),
        #         'limit': 50,
        #         'offset': len(results),
        #         'categoryId': categoryId,
        #         'radius': 1000
        #     })
        #     items = res.json()['response']['venues']
        #     for item in items:
        #         item['core_info'] = {
        #             'name': item['name'],
        #             'location': item['location']
        #         }
        #     results.extend(items)
        #     total_results = res.json()['response'].get('totalResults')
        #     if total_results is None:
        #         total_results = 0
        #     if len(results) == last_length:
        #         break
        #     last_length = len(results)
        # return results

    def _find_matched_categories(self, service):
        types = []
        for type in self.args['types']:
            categories = Category.query.filter(
                Category.service == service,
                Category.formatted_text.like('%{}%'.format(type))
            ).all()
            for category in categories:
                types.append(category.service_identifier)
        return types

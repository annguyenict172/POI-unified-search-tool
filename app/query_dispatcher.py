from app.api import FoursquareAPI, GooglePlaceAPI
from app.models import Category


class QueryDispatcher:
    foursquare_api = FoursquareAPI()
    google_api = GooglePlaceAPI()

    def __init__(self, args):
        self.args = args

    def can_dispatch(self):
        if self.args['location'] == '':
            return False
        return True

    def dispatch_query(self):
        res = self.google_api.get_geocoding(self.args['location'])
        geometry = res.json()['results'][0]['geometry']['location']
        results = self._query_from_foursquare(geometry) + self._query_from_google(geometry)
        return results

    def _query_from_google(self, geometry):
        results = []
        for type in self._find_matched_categories('Google'):
            res = self.google_api.nearby_search({
                'location': '{},{}'.format(geometry['lat'], geometry['lng']),
                'radius': 2000,
                'type': type
            })
            results.extend(res.json()['results'])
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
                'radius': 2000
            })
            results.extend(res.json()['response']['groups'][0]['items'])
            total_results = res.json()['response']['totalResults']
            if len(results) == last_length:
                break
            last_length = len(results)
        return results

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

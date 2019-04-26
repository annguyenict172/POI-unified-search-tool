import json
import os

from app.api import FoursquareAPI, GooglePlaceAPI, FacebookAPI
from app.constants import Service
from app.schemas import FacebookSchema, GoogleSchema, FoursquareSchema


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

    def dispatch_explore_query(self):
        is_demo = os.environ.get('DEMO', False)
        if is_demo:
            foursquare_file = open('files/foursquare.json', 'r')
            facebook_file = open('files/facebook.json', 'r')
            google_file = open('files/google.json', 'r')
            results = {
                Service.GOOGLE: GoogleSchema().dump(json.load(google_file), many=True).data,
                Service.FACEBOOK: FacebookSchema().dump(json.load(facebook_file), many=True).data,
                Service.FOURSQUARE: FoursquareSchema().dump(json.load(foursquare_file), many=True).data
            }
        else:
            results = {
                Service.GOOGLE: self._query_from_google(),
                Service.FACEBOOK: self._query_from_facebook(),
                Service.FOURSQUARE: self._query_from_foursquare()
            }
        return results

    def _query_from_facebook(self):
        after = None
        results = []
        while True:
            params = {
                'center': '{},{}'.format(self.args['geometry']['lat'], self.args['geometry']['lng']),
                'distance': 1000,
                'fields': 'id,about,description,name,location,phone,picture,website,overall_star_rating,checkins',
                'categories': '["FOOD_BEVERAGE"]',
                'after': after
            }
            res = self.facebook_api.find_places(params=params)
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
        return FacebookSchema().dump(results, many=True).data

    def _query_from_google(self):
        results = []
        for type in self.args['types'].get(Service.GOOGLE):
            pagetoken = None
            while True:
                res = self.google_api.nearby_search({
                    'location': '{},{}'.format(
                        self.args['geometry']['lat'],
                        self.args['geometry']['lng']
                    ),
                    'radius': 1000,
                    'type': type,
                    'pagetoken': pagetoken
                })
                pagetoken = res.json().get('next_page_token')
                results.extend(res.json()['results'])
                if pagetoken is None:
                    break
        return GoogleSchema().dump(results, many=True).data

    def _query_from_foursquare(self):
        results = []
        total_results = 1000000
        last_length = 0
        while len(results) < total_results:
            res = self.foursquare_api.search_venues({
                'll': '{},{}'.format(
                    self.args['geometry']['lat'],
                    self.args['geometry']['lng']
                ),
                'limit': 50,
                'offset': len(results),
                'section': 'coffee',
                'radius': 1000
            })
            results.extend(res.json()['response']['groups'][0]['items'])
            total_results = res.json()['response']['totalResults']
            if len(results) == last_length:
                break
            last_length = len(results)
        return FoursquareSchema().dump(results, many=True).data

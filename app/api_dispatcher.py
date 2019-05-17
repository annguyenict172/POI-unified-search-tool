import json
import os
import time
import threading

from app.api import FoursquareAPI, GooglePlaceAPI, FacebookAPI
from app.constants import Service


class APIDispatcher:
    foursquare_api = FoursquareAPI()
    google_api = GooglePlaceAPI()
    facebook_api = FacebookAPI()

    def __init__(self, args):
        self.args = args
        self.results = {
            Service.FOURSQUARE: [],
            Service.FACEBOOK: [],
            Service.GOOGLE: []
        }

    def dispatch_api_calls(self):
        demo_city = os.environ.get('DEMO_CITY', None)
        if demo_city:
            foursquare_file = open('files/foursquare-{}.json'.format(demo_city), 'r')
            facebook_file = open('files/facebook-{}.json'.format(demo_city), 'r')
            google_file = open('files/google-{}.json'.format(demo_city), 'r')
            self.results = {
                Service.GOOGLE: json.load(google_file),
                Service.FACEBOOK: json.load(facebook_file),
                Service.FOURSQUARE: json.load(foursquare_file)
            }
        else:
            threads = [
                threading.Thread(target=self._query_from_google),
                threading.Thread(target=self._query_from_facebook),
                threading.Thread(target=self._query_from_foursquare),
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        return self.results

    def _query_from_facebook(self):
        after = None
        results = []
        params = self.args.get(Service.FACEBOOK)
        if len(params.get('categories')) > 0:
            types = ['"{}"'.format(t) for t in params.get('categories')]
            categories = '[' + ','.join(types) + ']'
            params['categories'] = categories
        while True:
            params['after'] = after
            params['fields'] = 'id,about,description,name,location,phone,picture,website,overall_star_rating,checkins'
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
        with open('files/facebook-Sydney.json', 'w') as outfile:
            json.dump(results, outfile)
        print('FACEBOOK {}'.format(len(results)))
        self.results[Service.FACEBOOK] = results

    def _query_from_google(self):
        results = []
        params = self.args.get(Service.GOOGLE)
        if len(params.get('types')) > 0:
            types = params.pop('types')
            for type in types:
                pagetoken = None
                while True:
                    params['pagetoken'] = pagetoken
                    params['type'] = type
                    res = self.google_api.nearby_search(params=params)
                    pagetoken = res.json().get('next_page_token')
                    results.extend(res.json()['results'])
                    time.sleep(2)
                    if pagetoken is None:
                        break
        else:
            pagetoken = None
            while True:
                params['pagetoken'] = pagetoken
                res = self.google_api.nearby_search(params=params)
                pagetoken = res.json().get('next_page_token')
                results.extend(res.json()['results'])
                if pagetoken is None:
                    break
        with open('files/google-Sydney.json', 'w') as outfile:
            json.dump(results, outfile)
        print('GOOGLE {}'.format(len(results)))
        self.results[Service.GOOGLE] = results

    def _query_from_foursquare(self):
        results = []
        params = self.args.get(Service.FOURSQUARE)
        if len(params.get('sections')) > 0:
            sections = params.pop('sections')
            for section in sections:
                temp_results = []
                total_results = 1000000
                last_length = 0
                while len(temp_results) < total_results:
                    params['limit'] = 50
                    params['offset'] = len(temp_results)
                    params['section'] = section
                    res = self.foursquare_api.search_venues(params=params)
                    temp_results.extend(res.json()['response']['groups'][0]['items'])
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
                res = self.foursquare_api.search_venues(params=params)
                results.extend(res.json()['response']['groups'][0]['items'])
                total_results = res.json()['response']['totalResults']
                if len(results) == last_length:
                    break
                last_length = len(results)
        with open('files/foursquare-Sydney.json', 'w') as outfile:
            json.dump(results, outfile)
        print('FOURSQUARE {}'.format(len(results)))
        self.results[Service.FOURSQUARE] = results

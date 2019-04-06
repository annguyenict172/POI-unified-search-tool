import requests

from config import Config


GOOGLE_BASE_URL = 'https://maps.googleapis.com/maps/api/place'
FOURSQUARE_BASE_URL = 'https://api.foursquare.com/v2/venues'


class GoogleEndpoint:
    FREE_TEXT_SEARCH = '{}/textsearch/json'.format(GOOGLE_BASE_URL)
    FIND_PLACE = '{}/findplacefromtext/json'.format(GOOGLE_BASE_URL)
    NEARBY_SEARCH = '{}/nearbysearch/json'.format(GOOGLE_BASE_URL)
    PLACE_DETAIL = '{}/details/json'.format(GOOGLE_BASE_URL)
    PLACE_PHOTOS = '{}/photo'.format(GOOGLE_BASE_URL)


class FoursquareEndpoint:
    VENUE_RECOMMENDATIONS = '{}/explore'.format(FOURSQUARE_BASE_URL)

    @staticmethod
    def VENUE_DETAIL(venue_id):
        return '{}/{}'.format(FOURSQUARE_BASE_URL, venue_id)

    @staticmethod
    def VENUE_PHOTOS(venue_id):
        return '{}/{}/photos'.format(FOURSQUARE_BASE_URL, venue_id)

    @staticmethod
    def VENUE_TIPS(venue_id):
        return '{}/{}/tips'.format(FOURSQUARE_BASE_URL, venue_id)

    @staticmethod
    def VENUE_MENU(venue_id):
        return '{}/{}/menu'.format(FOURSQUARE_BASE_URL, venue_id)


class BaseAPI:
    _authen_params = {}

    def _call_api(self, endpoint, params):
        return requests.get(endpoint, params={
            **params,
            **self._authen_params
        })


class GooglePlaceAPI(BaseAPI):
    _endpoints = GoogleEndpoint
    _authen_params = {
        'key': Config.GOOGLE_PLACE_API_KEY
    }

    def freetext_search(self, params):
        return self._call_api(self._endpoints.FREE_TEXT_SEARCH, params)

    def find_place(self, params):
        return self._call_api(self._endpoints.FIND_PLACE, params)

    def nearby_search(self, params):
        response = self._call_api(self._endpoints.NEARBY_SEARCH, params)
        return response.json()['results']

    def get_place_detail(self, params):
        return self._call_api(self._endpoints.PLACE_DETAIL, params)

    def get_place_photos(self, params):
        return self._call_api(self._endpoints.PLACE_PHOTOS, params)


class FoursquareAPI(BaseAPI):
    _endpoints = FoursquareEndpoint
    _authen_params = {
        'client_id': Config.FOURSQUARE_CLIENT_ID,
        'client_secret': Config.FOURSQUARE_CLIENT_SECRET,
        'v': '20190406'
    }

    def search_venues(self, params):
        response = self._call_api(self._endpoints.VENUE_RECOMMENDATIONS, params)
        return response.json()['response']['groups'][0]['items']

    def get_venue_detail(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_DETAIL(venue_id), params)

    def get_venue_photos(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_PHOTOS(venue_id), params)

    def get_venue_tips(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_TIPS(venue_id), params)

    def get_venue_menu(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_MENU(venue_id), params)

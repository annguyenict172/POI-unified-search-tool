import requests

from config import Config


GOOGLE_BASE_URL = 'https://maps.googleapis.com/maps/api'
FOURSQUARE_BASE_URL = 'https://api.foursquare.com/v2/venues'
FACEBOOK_BASE_URL = 'https://graph.facebook.com'


class GoogleEndpoint:
    FREE_TEXT_SEARCH = '{}/place/textsearch/json'.format(GOOGLE_BASE_URL)
    FIND_PLACE = '{}/place/findplacefromtext/json'.format(GOOGLE_BASE_URL)
    NEARBY_SEARCH = '{}/place/nearbysearch/json'.format(GOOGLE_BASE_URL)
    PLACE_DETAIL = '{}/place/details/json'.format(GOOGLE_BASE_URL)
    PLACE_PHOTOS = '{}/place/photo'.format(GOOGLE_BASE_URL)
    GET_GEOCODING = '{}/geocode/json'.format(GOOGLE_BASE_URL)


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


class FacebookEndpoint:
    FIND_PLACE = '{}/search'.format(FACEBOOK_BASE_URL)


class BaseAPI:
    _base_params = {}

    def _call_api(self, endpoint, params):
        return requests.get(endpoint, params={
            **params,
            **self._base_params
        })


class GooglePlaceAPI(BaseAPI):
    _endpoints = GoogleEndpoint
    _base_params = {
        'key': Config.GOOGLE_PLACE_API_KEY
    }

    def get_geocoding(self, location):
        return self._call_api(self._endpoints.GET_GEOCODING, {
            'address': location
        })

    def freetext_search(self, params):
        return self._call_api(self._endpoints.FREE_TEXT_SEARCH, params)

    def find_place(self, params):
        return self._call_api(self._endpoints.FIND_PLACE, params)

    def nearby_search(self, params):
        return self._call_api(self._endpoints.NEARBY_SEARCH, params)

    def get_place_detail(self, params):
        return self._call_api(self._endpoints.PLACE_DETAIL, params)

    def get_place_photos(self, params):
        return self._call_api(self._endpoints.PLACE_PHOTOS, params)


class FoursquareAPI(BaseAPI):
    _endpoints = FoursquareEndpoint
    _base_params = {
        'oauth_token': Config.FOURSQUARE_OAUTH_TOKEN,
        'v': '20190406'
    }

    def search_venues(self, params):
        return self._call_api(self._endpoints.VENUE_RECOMMENDATIONS, params)

    def get_venue_detail(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_DETAIL(venue_id), params)

    def get_venue_photos(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_PHOTOS(venue_id), params)

    def get_venue_tips(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_TIPS(venue_id), params)

    def get_venue_menu(self, venue_id, params):
        return self._call_api(self._endpoints.VENUE_MENU(venue_id), params)


class FacebookAPI(BaseAPI):
    _endpoints = FacebookEndpoint
    _base_params = {
        'type': 'place',
        'access_token': Config.FACEBOOK_ACCESS_TOKEN
    }

    def find_places(self, params):
        return self._call_api(self._endpoints.FIND_PLACE, params)

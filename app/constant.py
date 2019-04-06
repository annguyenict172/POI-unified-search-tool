GOOGLE_BASE_URL = 'https://maps.googleapis.com/maps/api/place'
FOURSQUARE_BASE_URL = 'https://api.foursquare.com/v2/venues'


class GoogleEndpoint:
    FREE_TEXT_SEARCH = '{}/textsearch/json'.format(GOOGLE_BASE_URL)
    FIND_PLACE = '{}/findplacefromtext/json'.format(GOOGLE_BASE_URL)
    NEARBY_SEARCH = '{}/nearbysearch/json'.format(GOOGLE_BASE_URL)
    PLACE_DETAIL = '{}/details/json'.format(GOOGLE_BASE_URL)
    PLACE_PHOTOS = '{}/photo'.format(GOOGLE_BASE_URL)
    PLACE_AUTOCOMPLETE = '{}/autocomplete/json'.format(GOOGLE_BASE_URL)
    QUERY_AUTOCOMPLETE = '{}/queryautocomplete/json'.format(GOOGLE_BASE_URL)


class FoursquareEndpoint:
    VENUE_RECOMMENDATIONS = '{}/explore'.format(FOURSQUARE_BASE_URL)
    TRENDING_VENUES = '{}/trending'.format(FOURSQUARE_BASE_URL)

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

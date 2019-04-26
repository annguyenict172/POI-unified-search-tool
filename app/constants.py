class Service:
    GOOGLE = 'google'
    FOURSQUARE = 'foursquare'
    FACEBOOK = 'facebook'

    @classmethod
    def get_list(cls):
        return [cls.GOOGLE, cls.FOURSQUARE, cls.FACEBOOK]

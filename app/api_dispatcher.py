import threading

from app.provider_api.google import GoogleAPI
from app.provider_api.facebook import FacebookAPI
from app.provider_api.foursquare import FoursquareAPI
from app.constants import Provider


class APIDispatcher:
    providers_api = {
        Provider.GOOGLE: GoogleAPI(),
        Provider.FACEBOOK: FacebookAPI(),
        Provider.FOURSQUARE: FoursquareAPI()
    }

    results = {
        Provider.FOURSQUARE: [],
        Provider.FACEBOOK: [],
        Provider.GOOGLE: []
    }

    def __init__(self, parameters):
        self.parameters = parameters

    def dispatch_api_calls(self):
        threads = [threading.Thread(target=self._query_from_provider,
                                    args=(provider,)) for provider in Provider.get_list()]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return self.results

    def _query_from_provider(self, provider):
        results = self.providers_api[provider].find_places(params=self.parameters[provider])
        self.results[provider] = results

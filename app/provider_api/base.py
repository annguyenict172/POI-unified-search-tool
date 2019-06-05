import requests


class ProviderAPI:
    _base_params = {}

    def find_places(self, params):
        raise NotImplementedError

    def _call_api(self, endpoint, params):
        return requests.get(endpoint, params={
            **params,
            **self._base_params
        })

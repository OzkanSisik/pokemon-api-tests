import requests
from config.settings import BASE_URL, API_KEY, TOKEN


class BaseAPI:
    def __init__(self):
        self.base_url = BASE_URL

    def get(self, endpoint, params=None, headers=None):
        if params is None:
            params = {}
        if API_KEY:
            params['key'] = API_KEY
        if TOKEN:
            params['token'] = TOKEN
        url = self.base_url + endpoint
        response = requests.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint, data=None, headers=None):
        if data is None:
            data = {}
        if API_KEY:
            data['key'] = API_KEY
        if TOKEN:
            data['token'] = TOKEN
        url = self.base_url + endpoint
        response = requests.post(url, json=data, headers=headers)
        return response

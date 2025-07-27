import requests
from config.settings import BASE_URL


class BaseAPI:
    def __init__(self):
        self.base_url = BASE_URL

    def get(self, endpoint, params=None, headers=None):
        if params is None:
            params = {}
        url = self.base_url + endpoint
        print(f"URL: {url}")
        response = requests.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint, data=None, headers=None):
        if data is None:
            data = {}
        url = self.base_url + endpoint
        response = requests.post(url, json=data, headers=headers)
        return response

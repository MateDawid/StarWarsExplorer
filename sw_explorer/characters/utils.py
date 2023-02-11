import requests
from urllib.parse import urljoin


class SWAPIConnector:
    BASE_URL = 'https://swapi.dev/api/'

    def get(self, endpoint=''):
        if endpoint.startswith(self.BASE_URL):
            url = endpoint
        else:
            url = urljoin(self.BASE_URL, endpoint)
        response = requests.get(url)
        if response.ok:
            return response.json()
        return {"status_code": response.status_code, 'text': response.text}

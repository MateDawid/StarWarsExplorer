from datetime import datetime

import requests
from urllib.parse import urljoin
import petl as etl


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

    def get_all_pages(self, endpoint=''):
        data = []
        response = self.get(endpoint)
        data += response.get('results', [])
        next_link = response.get('next')
        while next_link is not None:
            response = self.get(next_link)
            data += response.get('results')
            next_link = response.get('next')
        return data

    def get_as_table(self, endpoint=''):
        data = self.get_all_pages(endpoint)
        if not data:
            return data
        headers = [header for header in data[0].keys()]
        rows = [[value for value in person.values()] for person in data]
        return [headers] + rows


def format_people_table(table, connector):
    headers = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'edited']
    planets = {planet.get('url'): planet for planet in connector.get_all_pages('planets')}
    table = (
        etl.wrap(table)
        .cut(*headers)
        .rename('homeworld', 'homeworld_url')
        .addfield('homeworld', lambda row: planets.get(row.homeworld_url))
        .cutout('homeworld_url')
        .addfield('date', lambda row: datetime.strptime(row.edited, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d"))
        .cutout('edited')
    )
    return table

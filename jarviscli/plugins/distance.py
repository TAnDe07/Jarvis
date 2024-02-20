"""
Calculates the haversine distance (distance along Earths surface)
between the centroids of two supplied countries.
"""

import requests
from colorama import Fore
from haversine import haversine
from jarviscli import entrypoint


class Location:
    def __str__(self):
        return self.country_name

    def __init__(self, country_name: str):
        self.country_name = country_name

    def geocode(self):
        url = f'https://restcountries.com/v3.1/name/{self.country_name}'
        payload = requests.get(url)

        if payload.status_code != 200:
            self.coordinates = False

        else:
            response = payload.json()[0]
            self.coordinates = response.get('latlng')
            self.country_name = response.get('name').get('common')


def create_location(order, jarvis, s):
    country_str = input(f'Enter the {order} country: ')
    country = self.Location(country_str)
    country.geocode()
    if not country.coordinates:
        jarvis.say(f'Country {country} not recognized, try again!')

    return country


@entrypoint
def distance(jarvis: "JarvisAPI", s: str):
    country_1 = create_location('first', jarvis, s)
    country_2 = create_location('second', jarvis, s)

    if country_1.coordinates and country_2.coordinates:
        haversine_distance = haversine(
            country_1.coordinates, country_2.coordinates)
        jarvis.say(
            f'The distance between {country_1} and {country_2} is {haversine_distance:.2f} km')

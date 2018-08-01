import googlemaps
import sys
from googlemaps.exceptions import ApiError
from datetime import datetime


class Gsearch():
    '''Used Google Places to searching for a buisiness'''
    def __init__(self, apikey, max_pages):
        self.gmaps = googlemaps.Client(key=apikey)
        self.next = ''
        self.max_pages = max_pages

    def r(self, query):
        result = {}
        try:
            result = self.gmaps.places(query, page_token=self.next)
        except ApiError as err:
            print(f'{err}, exit program')
            sys.exit(-1)
        try:
            self.next = result['next_page_token']
        except KeyError:
            self.next = None
        return result

    def request_data(self, query):
        i = 0
        while self.next is not None and i <= self.max_pages:
            yield self.r(query)
            i += 1

    def get_details(self, id):
        result = {}
        try:
            result =  self.gmaps.place(id, fields=[
                'formatted_address',
                'address_component',
                'formatted_phone_number',
                'website',
                'name',
                'id'
                ])
        except ApiError as err:
            print(f'{err}, exit program')
            sys.exit(-1)
        return result
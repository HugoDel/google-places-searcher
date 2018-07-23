from googlemaps.exceptions import ApiError
import sys
import getopt
import os
import json
import time
from personal_settings import api_key
from datetime import datetime
from gsearch import Gsearch

# Base params used by default
params = {
    'ARGS_OPTIONS_AVAILABLE': 'tf:n:q:',
    'TEST': False,
    'MAX_RES': 20,
    'TEST_FILE': os.path.join(os.getcwd(), 'exemple_data.json'),
    'API_KEY': api_key,
}


def display_array(data):
    rows, columns = os.popen('stty size', 'r').read().split()
    columns = int(columns)
    dash = '-' * columns
    title_centering = columns // 4
    line_centeting = columns // 4
    print(dash)
    print('{:<{title_centering}}{:^{title_centering}}{:>{title_centering}}'
          .format('NAME', 'ADDRESS', 'ID', title_centering=title_centering))
    print(dash)
    for company in data:
        print(f'{company["name"]:<{line_centeting}} \
                {company["formatted_address"]:^{line_centeting}} \
                {company["place_id"]:>{line_centeting}}')


def record_json():
    pass


def get_all_details(g, data):
    companies_details = []
    for company in data:
        details = g.get_details(company['place_id'])
        companies_details.append(details)
    return companies_details


def main(params):
    try:
        opt, args = getopt.getopt(sys.argv[1:],
                                  params['ARGS_OPTIONS_AVAILABLE'])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opt:
        if o == '-t':
            params['TEST'] = True
        if o == '-f':
            params['TEST_FILE'] = os.path.join(os.getcwd(), a)
        if o == '-n':
            params['MAX_RES'] = round(int(a)/20)
        if o == '-q':
            query = a

    if params['TEST']:
        print('Using test data from ', params['TEST_FILE'])
    try:
        gmaps = Gsearch(apikey=params['API_KEY'], max_pages=params['MAX_RES'])
    except ValueError:
        print('Enable to connect : check your API key')
        sys.exit(-1)
    except NotImplementedError:
        print('Enable to connect : check your Google Maps python library')
        sys.exit(-1)
    print('Connected to the Google API')

    if not params['TEST']:
        data = gmaps.request_data(query)
        for page in data:
            display_array(page['results'])
            time.sleep(2)
    else:
        with open(params['TEST_FILE']) as content_file:
            result = json.loads(content_file.read())
            display_array(result['results'])
            get_all_details(gmaps, result['results'])


main(params)

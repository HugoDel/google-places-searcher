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
    'ARGS_OPTIONS_AVAILABLE': 'tf:n:q:o:sk',
    'TEST': False,
    'MAX_RES': 20,
    'TEST_FILE': os.path.join(os.getcwd(), 'exemple_data.json'),
    'API_KEY': api_key,
    'OUTPUT_FILE': os.path.join(os.getcwd(), 'results.json'),
    'SAVE': False,
    'MODE': 'w' # Default writing mode for result file
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


def record_json(file_path, data, mode='w'):
    if mode == 'a':
        print(f'Reading existing data from {file_path}')
        current_data = []
        try:
            with open(file_path, 'r') as f:
                current_data = json.load(f)
            for e in current_data:
                data.append(e)
        except OSError as err:
            print(f"Sorry, {file_path} didn't exist \n{err}")
        except json.JSONDecodeError as err:
            print(f"Can't decode the json file {file_path}. The data will be errase in 5s")
            print('CTRL+C to exit')
            print(f'{err}')
            time.sleep(5)
    print(f'Writing into file {file_path}')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    print('Done.')


def get_all_details(g, data):
    companies_details = []
    for company in data:
        details = g.get_details(company['place_id'])
        companies_details.append(details["result"])
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
        if o == '-o':
            params['OUTPUT_FILE'] = a
        if o == '-s':
            params['SAVE'] = True
        if o == '-k':
            params['MODE'] = 'a'

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
        details_results = []
        for page in data:
            display_array(page['results'])
            if params['SAVE']:
                details_results.append(get_all_details(gmaps, page['results']))
            time.sleep(2)
        if params['SAVE']:
            record_json(params['OUTPUT_FILE'], details_results[0], mode=params['MODE'])

    else:
        with open(params['TEST_FILE']) as content_file:
            result = json.loads(content_file.read())
            display_array(result['results'])
            record_json(params['OUTPUT_FILE'], get_all_details(gmaps, result['results']), mode=params['MODE'])


main(params)

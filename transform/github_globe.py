
import requests
import requests_cache
import json

import fetch_error
import geocode

requests_cache.install_cache('cache/loc_cache')

loc_data_endpoint = 'http://commondatastorage.googleapis.com/github_globe/location_frequencies'

def safe_json_loads(string):
    try:
        string = string.replace('\n', '')
        return json.loads(string)
    except ValueError:
        print('error: %s' % string.encode('utf-8'))
        return None

def fetch_data():
    resp = requests.get(loc_data_endpoint)

    if resp.status_code == requests.codes.ok:
        return resp.text
    else:
        raise FetchError(resp)

def format_data(raw):
    print 'format_data'
    locs = raw.split('}\n{')[:1000]
    locs = map(lambda x: x + '}', locs)
    locs = map(lambda x: '{' + x, locs)
    locs[0] = locs[0].replace('{{', '{')
    locs[-1] = locs[-1].replace('{{', '{')
    json_locs = map(lambda x: safe_json_loads(x), locs)
    return filter(lambda x: x is not None, json_locs)

def add_coords(data):
    data = filter(lambda x: type(x) is dict, data)
    length = len(data)
    new = []

    for x in xrange(len(data)):
        print('processing %s out of %s' % (x, length))
        coords = geocode.address_to_coords(data[x]['actor_attributes_location'])
        if coords is not None:
            data[x]['coords'] = coords
            del data[x]['actor_attributes_location']
            new.append(data[x])

    return new

def normalize_magnitudes(data):
    tmp = map(lambda x: float(x['num_users']), data)
    max_pop = max(tmp)
    
    for x in data:
        x['num_users'] = float(x['num_users']) / max_pop

    return data

def to_globe_format(data):
    data = map(lambda x: [x['coords']['lat'], x['coords']['lng'], x['num_users']], data)
    data = [item for sublist in data for item in sublist]
    data = map(lambda x: float(x), data)
    return data

data = normalize_magnitudes(add_coords(format_data(fetch_data())))
data_globe_format = to_globe_format(data)
data_globe_format = [["now",data_globe_format]]

with open('../visualize/globe/user_locations.json', 'w') as f:
    f.write(json.dumps(data_globe_format))

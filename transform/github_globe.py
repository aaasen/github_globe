
import requests
import requests_cache
import json

import fetch_error
import geocode
from geo_coord import GeoCoord

requests_cache.install_cache('cache/loc_cache')

loc_data_endpoint = 'http://commondatastorage.googleapis.com/github_globe/location_frequencies'

def _safe_json_loads(string):
    try:
        print string
        return json.loads(string)
    except TypeError:
        return None

def _extract_json(text, max_values=None, delimiter='\n'):
    data = text.split('}%s{' % delimiter)[:max_values]
    data = map(lambda x: '{%s}' % x, data)

    data[0] = data[0].replace('{{', '{')
    data[-1] = data[-1].replace('}}', '}')

    return map(lambda x: json.loads(x), data)

def fetch_data():
    resp = requests.get(loc_data_endpoint)

    if resp.status_code == requests.codes.ok:
        return resp.text
    else:
        raise FetchError(resp)

def format_data(raw):
    locs = _extract_json(raw, max_values=1000)
    return filter(lambda x: x is not None, locs)

def add_coords(data):
    data = filter(lambda x: type(x) is dict, data)
    length = len(data)
    new = []

    for x in xrange(len(data)):
        print('processing %s out of %s' % (x, length))
        coords = geocode.address_to_coords(data[x]['actor_attributes_location'])
        if coords is not None:
            coords = GeoCoord(coords['lat'], coords['lng'])
            data[x]['coords'] = coords
            del data[x]['actor_attributes_location']
            new.append(data[x])

    return new

def combine_duplicates(data):
    new = {}

    for el in data:
        el['coords'] = el['coords'].round(2)
        if el['coords'] in new:
            new[el['coords']] += int(el['num_users'])
        else:
            new[el['coords']] = int(el['num_users'])

    return new

def normalize_magnitudes(data):
    max_pop = max(data.values())
    
    for x in data.keys():
        data[x] = float(data[x]) / max_pop

    return data

def to_globe_format(data):
    data = map(lambda x: [x.lat, x.lng, data[x]], data.keys())
    data = [item for sublist in data for item in sublist]
    data = map(lambda x: float(x), data)
    return data

data = normalize_magnitudes(
    combine_duplicates(
    add_coords(
    format_data(
    fetch_data()))))

data_globe_format = to_globe_format(data)
data_globe_format = [["now",data_globe_format]]

with open('../visualize/globe/user_locations.json', 'w') as f:
    f.write(json.dumps(data_globe_format))


import requests
import requests_cache
import json

requests_cache.install_cache('cache/coords_cache')

maps_api_endpoint = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false'
loc_data_endpoint = 'http://commondatastorage.googleapis.com/github_globe/location_frequencies'

class FetchError(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return '%s returned invalid status code %s' % (self.resp.url, self.resp.status_code)

def safe_json_loads(string):
    try:
        return json.loads(string.encode('utf-8'))
    except:
        return None

def fetch_loc_data():
    resp = requests.get(loc_data_endpoint)
    print 'request done'

    if resp.status_code == requests.codes.ok:
        locs = resp.text.split()
        json_locs = map(lambda x: safe_json_loads(x), locs)
        return filter(lambda x: x is not None, json_locs)

    else:
        raise FetchError(resp)

def address_to_coords(loc):
    resp = requests.get(maps_api_endpoint % loc)
    
    if resp.status_code == requests.codes.ok:
        results = resp.json()['results']

        if len(results) > 0:
            return results[0]['geometry']['location']
    else:
        raise FetchError(resp)

    print 'address null!'
    return None

def bulk_address_to_coords(data):
    data = filter(lambda x: type(x) is dict, data)
    length = len(data)
    new = []

    for x in xrange(len(data)):
        print('processing %s out of %s' % (x, length))
        coords = address_to_coords(data[x]['actor_attributes_location'])
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

data = normalize_magnitudes(bulk_address_to_coords(fetch_loc_data()))
data_globe_format = to_globe_format(data)
data_globe_format = [["now",data_globe_format]]

with open('../visualize/globe/user_locations.json', 'w') as f:
    f.write(json.dumps(data_globe_format))

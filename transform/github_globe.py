
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

    print 'address done'

def bulk_address_to_coords(data):
    data = data[:10]
    data = filter(lambda x: type(x) is dict, data)

    for x in data:
        x['coords'] = address_to_coords(x['actor_attributes_location'])
        del x['actor_attributes_location']

    return data


data = bulk_address_to_coords(fetch_loc_data())

with open('../visualize/user_locations.json', 'w') as f:
    f.write(json.dumps(data))

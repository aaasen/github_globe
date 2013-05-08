
import requests
import requests_cache

maps_api_endpoint = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false'

requests_cache.install_cache('cache/coords_cache')

class FetchError(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return '%s returned invalid status code %s' % (self.resp.url, self.resp.status_code)

def address_to_coords(loc):
    resp = requests.get(maps_api_endpoint % loc)
    
    if resp.status_code == requests.codes.ok:
        results = resp.json()['results']

        if len(results) > 0:
            return results[0]['geometry']['location']
    else:
        raise FetchError(resp)

print address_to_coords('seattle')
print address_to_coords('asdasdljsadfoiuru')

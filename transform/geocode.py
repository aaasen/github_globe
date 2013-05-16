
"""A wrapper for the Google Geocoding API

Notes on usage limits:
    The API's courtesy limit is 2,500 requests/day.
    Be nice; it's free.

"""

import requests
import requests_cache
import json
import fetch_error

requests_cache.install_cache('cache/coords_cache')
maps_api_endpoint = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=%s'

"""A generic query method for the Google Geocoding API"""
def _query(address, sensor=False):
    resp = requests.get(maps_api_endpoint % (address, 'true' if sensor else 'false'))

    if resp.status_code == requests.codes.ok:
        return resp.json()
    else:
        raise FetchError(resp)

"""Returns approximate geo coordinates for a given address"""
def address_to_coords(address, sensor=False):
    results = _query(address, sensor)['results']

    if len(results) > 0:
        return results[0]['geometry']['location']

    return None

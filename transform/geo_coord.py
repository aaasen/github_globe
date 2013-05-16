
"""A container for geographic coordinates (latitude and longitude)"""

class GeoCoord:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __eq__(self, other):
        return self.lat == other.lat and self.lng == other.lng

    def __hash__(self):
        return hash((self.lat, self.lng))

    def round(self, ndigits=0):
        return GeoCoord(round(self.lat, ndigits), round(self.lng, ndigits))

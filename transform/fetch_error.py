
class FetchError(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return '%s returned invalid status code %s' % (self.resp.url, self.resp.status_code)

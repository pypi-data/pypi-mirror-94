import urllib.request
import json

class HttpServiceClient:

    def __init__(self, base_url, credentials_headers = {}):
        self._base_url = base_url.rstrip('/')
        self._credentials_headers = credentials_headers

    def send_json_request(self, route, method, json_body, headers = {}):
        body = json.dumps(json_body).encode('utf-8')
        headers['Content-Type'] = 'application/json'

        return self.send_request(route, method, body, headers)

    def send_request(self, route, method, body = None, headers = {}):
        url = self._construct_url(route)
        request = self._generate_request(url, method, body, headers)

        return urllib.request.urlopen(request)

    def _construct_url(self, route):
        return self._base_url + '/' + route.lstrip('/')

    def _generate_request(self, url, method, body, headers):
        for key, value in self._credentials_headers.items():
            headers[key] = value
        
        return urllib.request.Request(url, body, headers, method=method)
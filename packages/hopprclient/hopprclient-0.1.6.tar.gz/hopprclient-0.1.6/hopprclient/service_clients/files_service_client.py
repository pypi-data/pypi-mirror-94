import urllib.error, urllib.parse
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
import json

class FilesServiceClient:

    def __init__(self, http_service_client):
        self._http_service_client = http_service_client
    
    def get_dataset_by_name(self, name):
        route = 'datasets/name/' + urllib.parse.quote(name)

        return self._get_dataset(route)

    def get_dataset(self, dataset_id):
        route = 'datasets/' + dataset_id

        return self._get_dataset(route)

    def create_dataset(self, dataset):
        response = self._http_service_client.send_json_request('datasets', 'POST', dataset)

        return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))['data']
    
    def get_file_hashes(self, client_ids):
        response = self._http_service_client.send_json_request('files/hashes', 'POST', client_ids)

        return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))['data']
    
    def upload_file_metadata_batch(self, metadata_batch):
        response = self._http_service_client.send_json_request('files/metadata/batch', 'POST', metadata_batch)

        return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))['data']

    def upload_file_batch(self, file_batch):
        related = MIMEMultipart('related', 'batch_file', charset='utf-8')

        for f in file_batch.keys():
            file_metadata = file_batch[f]
            
            mimetype, encoding = mimetypes.guess_type(file_metadata['fileName'])
            if mimetype is not None:
                parts = mimetype.split('/')
                majortype = parts[0]; subtype = parts[1]
                if majortype == 'text':
                    part = MIMEText(open(f, 'r').read(), subtype, encoding)
                elif majortype == 'image':
                    part = MIMEImage(open(f, 'rb').read(), subtype)
                elif majortype == 'audio':
                    part = MIMEAudio(open(f, 'rb').read(), subtype)
                elif majortype == 'application':
                    part = MIMEApplication(open(f, 'rb').read(), subtype)
                else:
                    continue
            else:
                part = MIMEApplication(open(f, 'rb').read())
            
            part.add_header('Hashed-Id', file_metadata['hashedId'])
            related.attach(part)
        
        body = related.as_string().split('\n\n', 1)[1].replace('\n', '\r\n') # See https://tools.ietf.org/html/rfc2046#section-4.1.1
        headers = dict(related.items())

        try:
            self._http_service_client.send_request('files/batch', 'PUT', body.encode(), headers)
        except urllib.error.URLError:
            return False
        else:
            return True

    def _get_dataset(self, route):
        try:
            response = self._http_service_client.send_request(route, 'GET')
        
            return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))['data']
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
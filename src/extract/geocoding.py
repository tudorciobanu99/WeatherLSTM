import requests
from src.utils.logger import Logger

class GeocodingAPI:
    def __init__(self, logger:Logger):
        self.BASE_URL = 'https://geocoding-api.open-meteo.com/v1/search'
        self.logger = logger.get_logger()

    def get_endpoint(self, **params):
        url = f'{self.BASE_URL}?' \
            + '&'.join([f'{key}={value}' for key, value in params.items()])
        return url

    def prepare_params(self, location):
        params = {
            'name': location,
            'count': 1,            
        }
        return params
    
    def send_request(self, location):
        params = self.prepare_params(location)
        url = self.get_endpoint(**params)

        try:
            response = requests.get(url, timeout=10)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.warning(f'Request failed for {location}: {e}')
        
    def get_response(self, response):
        try:
            data = response.json()
            code = response.status_code

            self.logger.info(f'Response was received with status code: {code}.')
            return data
        except requests.exceptions.JSONDecodeError:
            self.logger.warning(response.text)
            return response.text
import requests
from typing import Dict
from datetime import datetime
import configparser

class APIHandler:
    def __init__(
            self,
            request_params,
            base_url
    ):
        self.base_url = base_url
        self.request_params = request_params

    def read_api_key(self) -> str:
        config = configparser.ConfigParser()
        config.read(
            '/Users/xxx/xxx/xxx/xxx/xxx/xxx/godata2023/config/config.ini' # use absolute path
        )  # Path to your configuration file
        api_key = config.get('API', 'api_key')
        return api_key
    
    def get_endpoint(self):
        #TODO:
        return url

    def request_date(self, url):
        #TODO:
        return data
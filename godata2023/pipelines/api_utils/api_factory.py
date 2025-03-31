import configparser
from datetime import datetime
from typing import Dict

import requests


class APIHandler:
    def __init__(
        self,
        request_params: Dict[str, str],
        base_url: str = 'https://www.alphavantage.co/query?',
    ):
        self.base_url = base_url
        self.request_params = request_params
        self.api_key = self._read_api_key()

    def _read_api_key(self) -> str:
        """
        This function will read the saved api key in config.ini and return it for later use
        In industry use case, api key (token) will be grabed from external secrets management platform like Vault
        """
        config = configparser.ConfigParser()
        config.read(
            './godata2023/config/config.ini'
        )  # Path to your configuration file
        api_key = config.get('API', 'api_key')
        return api_key

    def get_endpoint(self) -> str:
        # TODO: complete this function to retrieve endpoint url on any given length of request_params
        # Tips 1: loop over request params to get key-value pair and construct url in a dynamic way
        # Tips 2: use _read_api_key() to get the api key for building endpoint url
        params = ""
        for key, value in self.request_params.items():
            params += f"{key}={value}&"
        api_key = self._read_api_key()
        url = self.base_url + params + f"apikey={api_key}"
        return url

    def request_data(self, url: str) -> dict:
        # TODO: Add Error Handling:
        # 1. Check status code of endpoint requests
        # 2. raise error message and coresponding status code if not 200
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Request failed")
        data = r.json()
        return data

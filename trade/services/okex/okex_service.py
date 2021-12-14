from requests.api import request
from .okex_dto import OkexDTO
import requests
import datetime
import json
import base64

class OkexService():

    def __init__(self, data:OkexDTO):
        self.base_rest_url = data.base_rest_url
        self.api_key = data.api_key
        self.secret_key = data.secret_key
        self.passphrase = data.passphrase
        self.instId = data.instId
        
    def get_server_timestamp(self):

        service_name = '/api/v5/public/time'

        return

    def get_account_info(self):

        service_name = '/api/v5/account/balance'

        return

    def get_ticker_info(self):
        instId = self.instId
        url = f'{self.base_rest_url}/api/v5/market/ticker?instId={instId}'
        print(url)
        response = requests.request(
            "GET",
            url=url
        )
        print(response)
        return response.json()

    def order(self):

        service_name = '/api/v5/trade/order'

        return

    
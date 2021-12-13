from .okex_dto import OkexDTO
import requests
import datetime
import json
import base64

class OkexService():

    def __init__(self, data:OkexDTO):
        self.base_rest_url = data.base_rest_url
        self.base_public_websocket_url = data.base_public_websocket_url
        self.base_private_websocket_url = data.base_private_websocket_url
        self.api_key = data.api_key
        self.secret_key = data.secret_key
        self.passphrase = data.passphrase
        self.market = data.market
        
   

    def build_header():
        '''
            header 그리기
        '''
        body = {}
        request = 'GET',
        endpoint = 'api/spot/'
        headers = {
           
        }
        return

    def bid(self):
        '''
            주문
        '''
        _url = self.base_rest_url + "api/v5/trade/order"
        _instId = self.market
        _sz = ""
        _px = ""
        _body = {
            'instId' : _instId,
            'tdMode' : 'cash',
            'side' : 'buy',
            'ordType' : 'limit',
            'sz' : _sz,
            'px' :  _px
        }
        result = requests.request(
            "POST",
            url=_url
        )
        return result.json()

    def get_current_balance(self):
        '''
            현재 잔고
        '''

        return


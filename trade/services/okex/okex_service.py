from time import time
from requests.api import request
from .okex_dto import OkexDTO
import requests
import datetime
import json
import base64
import hmac
import hashlib

class OkexService():

    def __init__(self, data:OkexDTO):
        self.base_rest_url = data.base_rest_url
        self.api_key = data.api_key
        self.secret_key = data.secret_key
        self.passphrase = data.passphrase
        self.instId = data.instId


    def get_range(self):
        '''
            get range
        '''
        range = 0.0
        result = self.get_ticker_info()
        yesterday_higest_price = result['data'][0]['high24h']
        yesterday_lowest_price = result['data'][0]['low24h']
        open_price = result['data'][0]['sodUtc0']

        range = (float(yesterday_higest_price) - float(yesterday_lowest_price)) * 0.5
        range += float(open_price)

        return range

    def get_ticker_info(self):
        '''
            askPx: Best ask price
            askSz: Best ask size
            bidPx: Best bid price
            bidSz: Best bid szie
            open24h: open price in the past 24h
            high24h: highest price in the past 24h
            low24h: lowest price in the past 24h
        '''
        instId = self.instId
        url = f'{self.base_rest_url}/api/v5/market/ticker?instId={instId}'
        response = requests.request(
            "GET",
            url=url
        )
        return response.json()

    def signature(self, timestamp, requestPath, method, body):
        '''
            Making requests
            
            all private rest request must contain the
            following headers:

                OK-ACCESS-KEY : the api_key 
                OK-ACCESS-SIGN : the base64 encoded signature
                OK-ACCESS-TIMESTAMP : the timestamp of your
                request
                OK-ACCESS-PASSPHRASE : passphrase
                Content-Type : application/json

            Signature
            OK-ACCESS-SIGN is generated as follows:

                create a prehash string of timestamp
                + method + requestPath + body(where + 
                represent String concatenation)

                prepare the secret key

                sign the prehash string with the secret key
                using the HMAC SHA256

                encode the signature in the Base64 format
                
                ex) sign = CryptoJS.enc.Base64.stringfy(
                    CryptoJS.HmcSHA256(
                        timestamp + 'GET' + '/users/self/verify',
                        SecretKey
                    )
                )
        '''
        if str(body) == '{}' or str(body) == 'None':
            body=''
        # request의 헤더에 밑의 값을 더 넣으면 됨
        
        OK_ACCESS_SECRET_KEY = self.secret_key
        CONTENT_TYPE = 'application/json'
        message =  str(timestamp) + str.upper(method) + requestPath + body
        mac = hmac.new(
           bytes(OK_ACCESS_SECRET_KEY, encoding='utf8'),
           bytes(message, encoding='utf-8'),
           digestmod='sha256'
        )
        d = mac.digest()
        result = base64.b64encode(d)

        return result

    def build_headers(self, method, requestPath, body:dict=dict()):
        '''
            build headers
        '''
        OK_ACCESS_KEY = self.api_key
        OK_ACCESS_TIMESTAMP = datetime.datetime.utcnow().isoformat()[:-3]+'Z'
        OK_ACCESS_PASSPHRASE = self.passphrase
        header = dict()
        header['CONTENT-TYPE'] = 'application/json'
        header['OK-ACCESS-KEY'] = OK_ACCESS_KEY
        header['OK-ACCESS-SIGN'] = self.signature(
            timestamp=OK_ACCESS_TIMESTAMP,
            method=method,
            requestPath=requestPath,
            body=body
        )
        header['OK-ACCESS-TIMESTAMP'] = str(OK_ACCESS_TIMESTAMP)
        header['OK-ACCESS-PASSPHRASE'] = OK_ACCESS_PASSPHRASE
        return header

    def get_balance(self):
        '''
            Retrieve the balances of all the assets
        '''
        url = f'{self.base_rest_url}/api/v5/asset/balances'
        response = requests.request(
           headers=self.build_headers(
               method='GET',
               requestPath='/api/v5/asset/balances',
               body=''
           ),
           method='GET',
           url=url
    
        )
        return response.json()

    def get_px(self):
        '''
            px: Order Price 구하기
        '''

        return

    def get_sz(self):
        '''
            Quantity to buy OR sell
        '''

        return

    def order(self, side:str):
        instId = self.instId
        url = f'{self.base_rest_url}/api/v5/trade/order'
        _px = 'px'
        _sz = 'sz'
        response = requests.request(
            'POST',
            url=url,
            body={
                'instId':instId,
                'tdMode':'cash',
                'clOrdId': 'b15',
                'side': side,
                'ordType': 'limit',
                'px': _px,
                'sz': _sz
            }
        )
        return response.json()

    def get_orderbook(self):
        '''
        
        '''
        instId = self.instId
        url = f'{self.base_rest_url}/api/v5/market/books?instId={instId}'
        response = requests.request(
            "GET",
            headers=self.build_headers(
                method='GET',
                requestPath='api/v5/market/boods?instId={instId}',
                body=''
            ),
            url=url
        )
        return response.json()
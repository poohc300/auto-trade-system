from django.db import models
import base64
import hashlib
import hmac
import time
import urllib
import requests
import json

from requests.api import head


class PublicApi:
    def __init__(self, access_token, secret_key) -> None:
        self.http = HttpMethod(access_token, secret_key)
        self.base_url = "https://api.coinone.co.kr/v2"

    def orderbook(self, currency):
        _currency=currency
        uri = 'https://api.coinone.co.kr/orderbook/?currency={}&format=json'.format(_currency)
        return self.http.build_get(uri)

class PrivateApi:
    def __init__(self, access_token, secret_key) -> None:
        self.http = HttpMethod(access_token, secret_key)

    def balance(self, **kwargs):
        return self.http.build_post('/account/balance/', **kwargs)

    def complete_orders(self, **kwargs):

        return self.http.build_post('/order/complete_orders/', **kwargs)

    def limit_buy(self, **kwargs):
        
        return self.http.build_post('/order/limit_buy/', **kwargs)

    def limit_sell(self, **kwargs):

        return self.http.build_post('/order/limit_sell/', **kwargs)

    def cancel(self, **kwargs):

        return self.http.build_post('/order/cancel/', **kwargs)

class HttpMethod:
    
    def __init__(self, access_token, secret_key) -> None:
        self.access_token = access_token
        self.secret_key = secret_key
        self.base_url = "https://api.coinone.co.kr/v2"
     

    def _signature(self, encoded_payload):
        secret_key = self.secret_key.encode('utf-8')
        signature = hmac.new(
            secret_key,
            encoded_payload,
            hashlib.sha512
        )
        result = signature.hexdigest()
        return result

    def get_payload(self, **kwargs):
        nonce = str(int(time.time() * 1000))
        payload = kwargs
        payload['nonce'] = nonce
        payload = json.dumps(payload)
        encoded_payload = base64.b64encode(
            payload.encode('utf-8')
        )
        return encoded_payload

    def build_headers(self, **kwargs):
        encoded_payload = self.get_payload(**kwargs)
       
        encoded_secret_key = base64.b64encode(
            self.secret_key.upper().encode('utf-8')
        )
        headers = {
            'Content-type' : 'application/json',
            'X-COINONE-PAYLOAD' : encoded_payload,
            'X-COINONE-SIGNATURE' : self._signature(
                encoded_payload
            )
        }
        print(headers)
        return headers

    def build_post(self, path, **kwargs):

        result = requests.post(
            url=self.base_url+path,
            headers=self.build_headers(**kwargs),
            data=self.get_payload(**kwargs)
        )
        print(result.json())
        return result

    def build_get(self, uri):
        result = requests.get(uri)
        return result

class Oauth:

    def __init__(self, access_token, secret_key):
        self.access_token = access_token
        self.app_id = 'helloworld'
        self.secret_key = secret_key
        self.base_url = "https://coinone.co.kr"
        self.http = HttpMethod(access_token, secret_key)
        #self.request_token = self.request_token()
        #self.access_token = self.request_access_token()
        
    def request_token(self):
        '''
            토큰 요청하기
        '''
        app_id = self.app_id
        uri = f"{self.base_url}/account/login/"
        print(uri)
        return self.http.build_get(uri)

    def request_access_token(self, **kwargs):
        '''
            액세스 토큰 얻기
        
            body
            :request token
            :app_id
            :app_secret

            res
            :result
            :errorCode
            :accessToken
        '''
        app_ip = self.app_id
        app_secret = self.secret_key
        
        kwargs['url'] = f"{self.base_url}/oauth/access_token"
        kwargs['body'] = {
            
            'app_id' : app_ip,
            'app_secret' : app_secret
        }
       
        kwargs['headers'] = "application/x-www-form-urlencoded"
        return self.http.build_post(**kwargs)

    def refresh_access_token(self):
        '''
            토큰 재발행

            body
            :access_token

            res
            :result
            :errorCode
            :accessToken
        '''
        access_token = self.access_token
        url = f"/oauth/refresh_token"
        body = {
            'access_token' : access_token
        }

        return self.http.build_post(url, body)

    def delete_access_token(self):
        '''
            토큰 삭제

            body
            :access_token

            res
            :result
            :errorCode
        '''
        access_token = self.access_token
        url = f"/oauth/delete_token"
        body = {
            'access_token' : access_token
        }

        return self.http.build_post(url, body)


class CoinoneService:
    
    def __init__(self, access_token, secret_key):
        self.api = PrivateApi(access_token, secret_key)
        self.oauth = Oauth(access_token, secret_key)
        self.public_api = PublicApi(access_token, secret_key)

    def get_orderbook(self, currency, limit=5):
        '''
            매수 매도 호가 조회
        '''
        result = None
        try:
            
            result = self.public_api.orderbook(
                currency=currency
                )

            return result

        except Exception as e:
            return e

    def create_order(self, **kwargs):
        '''
            지정가 매수

            order_type 
            0이면 지정가 매수 1이면 지정가 매도
            2이면 시장가 매수 3이면 시장가 매도
        '''
        result = None
        try:
            if kwargs['order_type'] == "0":
                result = self.buy_limit_order(
                    **kwargs
                )
            if kwargs['order_type'] == "1":
                result = self.sell_limit_order(
                    **kwargs
                )
            if kwargs['order_type'] == "2":
                result = self.buy_market_order(
                    **kwargs
                )

            if kwargs['order_type'] == "3":
                result = self.sell_market_order(
                    **kwargs
                )

            return result.json()
        except Exception as e:
            return e

    def get_nonce(self):
        nonce = str(int(time.time() * 1000))

        return nonce

    def buy_limit_order(self, **kwargs):
        '''
            지정가 매수
        '''
        print(kwargs)

        buy_limit_api_path ="/order/limit_buy/"
        url_path = "https://api.coinone.co.kr/v2" + buy_limit_api_path
        payload ={
            "access_token" : kwargs['access_token'],
            "price" : float(kwargs['price']),
            "qty" : float(kwargs['qty']),
            "currency": kwargs['currency'],
            'nonce' : self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}
        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result

    def buy_market_order(self, **kwargs):
        '''
            시장가 매수
        '''
        # 가장 높은 매수 호가
        qty = 0.0
        currency = kwargs['currency']
        target_price = self.get_orderbook(currency)
        target_price = target_price.json()['bid'][0]['price']
        
        # qty 구하기
        balance = self.get_balance(**kwargs)['krw']['avail']
        print(balance)
        
        print(target_price)
        qty = (float(balance) * 0.995) / float(target_price)
        qty = round(qty, 1)
        # 매수하기
        kwargs['qty'] = qty
        kwargs['price'] = target_price
        result = self.buy_limit_order(
            **kwargs
        )
        print(result)
        return result


    def sell_limit_order(self, **kwargs):
        '''
            매도
        '''
        print(kwargs)
        sell_limit_api_path ="/order/limit_sell/"
        url_path = "https://api.coinone.co.kr/v2" + sell_limit_api_path
        payload ={
            "access_token" : kwargs['access_token'],
            "price" : float(kwargs['price']),
            "qty" : float(kwargs['qty']),
            "currency":kwargs['currency'],
            'nonce' : self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result

    def sell_market_order(self, **kwargs):
        qty = 0.0
        # 코인 정보 가져오기
        currency = kwargs['currency'].lower()
        print(currency)
        coins = self.get_balance(**kwargs)
        target_coin_balance = coins.get(currency)['avail']
        qty = target_coin_balance
        # 가장 낮은 매도 호가
        target_price = self.get_orderbook(kwargs['currency']).json()['ask'][0]['price']
        print(target_price)
        
        kwargs['qty'] = qty
        kwargs['price'] = target_price
        print(kwargs)
        result = self.sell_limit_order(
            **kwargs
        )
        print(result)
        return result

    def get_limit_orders(self, **kwargs):
        '''
        지정가 주문 조회
        '''
        limit_order_api_path ="/order/limit_orders/"
        url_path = "https://api.coinone.co.kr/v2" + limit_order_api_path
        payload ={
            "access_token" : kwargs['access_token'],
            "qty" : float(kwargs['qty']),
            "currency":kwargs['currency'],
            'nonce' : self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        print(result)
        return result


    def get_signature(self, encoded_payload, secret_key):
        signature = hmac.new(secret_key, encoded_payload, hashlib.sha512);
        return signature.hexdigest()

    def get_balance(self, **kwargs):
        '''
            계좌 확인
        '''
        result = None
        try:
            nonce = str(int(time.time() * 1000))

            wallet_status_api_path ="/account/balance/"
            url_path = "https://api.coinone.co.kr/v2" + wallet_status_api_path
            payload ={
                "access_token":kwargs['access_token'],
                'nonce':nonce
            }
            dumped_json = json.dumps(payload)
            encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 
            encoded_secret_key = base64.b64encode(kwargs['secret_key'].upper().encode('utf-8')) 

            headers = {'Content-type': 'application/json',
                    'X-COINONE-PAYLOAD': encoded_payload,
                    'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}

            res = requests.post(url_path, headers=headers, data=payload)
            result = res.json()

            return result
        except Exception as e:
            return e

    def cancel_coin_order(self, **kwargs):
        '''
            주문 취소
        '''
        cancel_api_path ="/order/cancel/"
        
        url_path = "https://api.coinone.co.kr/v2" + cancel_api_path
        payload ={
            "access_token" : kwargs['access_token'],
            "price" : float(kwargs['price']),
            "qty" : float(kwargs['qty']),
            "currency":kwargs['currency'],
            'nonce' : self.get_nonce(),
            'is_ask' : kwargs['is_ask'],
            "order_id" : kwargs['order_id']
        }
        print(payload)
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()

        return result

    def get_coin_transaction_history(self, **kwargs):
        '''
            주문 상태 확인

            KRW는 "/v2/transaction/krw/history/
        '''
        list_api_path ="/transaction/history/"
       
        url_path = "https://api.coinone.co.kr/v2" + list_api_path
        payload ={
            "access_token" : kwargs['access_token'],
            "currency":kwargs['currency'],
            'nonce' : self.get_nonce()
        }
        print(payload)
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()

        return result

    def get_krw_transaction_history(self, **kwargs):
        '''
            주문 상태 확인

            KRW는 "/v2/transaction/krw/history/"
        '''
        list_api_path ="/transaction/krw/history/"
       
        url_path = "https://api.coinone.co.kr/v2" + list_api_path
        payload ={
            "access_token" : kwargs['access_token'],
            'nonce' : self.get_nonce()
        }
        print(payload)
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8')) 

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, kwargs['secret_key'].encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()

        return result
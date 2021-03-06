from django.db import models

# Create your models here.
from dataclasses import dataclass
from datetime import date
import base64
import hashlib
import hmac
import time
import urllib
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry




class PublicApi:
  
    @staticmethod
    def orderbook(order_currency, payment_currency="KRW", limit=5):
        uri = f"/public/orderbook/{order_currency}_{payment_currency}?count={limit}"
        return BithumbHttp().get(uri)



class PrivateApi:
    def __init__(self, conkey, seckey):
        self.http = BithumbHttp(conkey, seckey)

    def account(self, **kwargs):
        return self.http.post('/info/account', **kwargs)

    def balance(self, **kwargs):
        return self.http.post('/info/balance', **kwargs)

    def place(self, **kwargs):
        return self.http.post('/trade/place', **kwargs)

    def orders(self, **kwargs):
        return self.http.post('/info/orders', **kwargs)

    def order_detail(self, **kwargs):
        return self.http.post('/info/order_detail', **kwargs)

    def cancel(self, **kwargs):
        return self.http.post('/trade/cancel', **kwargs)

    def market_buy(self, **kwargs):
        return self.http.post('/trade/market_buy', **kwargs)

    def market_sell(self, **kwargs):
        return self.http.post('/trade/market_sell', **kwargs)

    def user_transactions(self, **kwargs):
        return self.http.post('/info/user_transactions', **kwargs)

class HttpMethod:
    def __init__(self):
        self.session = self._requests_retry_session()

    def _requests_retry_session(retries=5, backoff_factor=0.3,
                                status_forcelist=(500, 502, 504), session=None):
        s = session or requests.Session()
        retry = Retry(total=retries, read=retries, connect=retries,
                      backoff_factor=backoff_factor,
                      status_forcelist=status_forcelist)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)
        
        return s

    @property
    def base_url(self):
        return ""

    def update_headers(self, headers):
        self.session.headers.update(headers)

    def post(self, path, timeout=3, **kwargs):
        try:
            uri = self.base_url + path
            return self.session.post(url=uri, data=kwargs, timeout=timeout).\
                json()

        except Exception as e:
            return e

    def get(self, path, timeout=3, **kwargs):
        try:
            uri = self.base_url + path
            return self.session.get(url=uri, params=kwargs, timeout=timeout).\
                json()

        except Exception as e:
            return e


class BithumbHttp(HttpMethod):
    def __init__(self, conkey="", seckey=""):
        self.API_CONKEY = conkey.encode('utf-8')
        self.API_SECRET = seckey.encode('utf-8')
        super(BithumbHttp, self).__init__()

    @property
    def base_url(self):
        return "https://api.bithumb.com"

    def _signature(self, path, nonce, **kwargs):
        query_string = path + chr(0) + urllib.parse.urlencode(kwargs) + \
                       chr(0) + nonce
        print(query_string)
        h = hmac.new(self.API_SECRET, query_string.encode('utf-8'),
                     hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode('utf-8'))

    def post(self, path, **kwargs):
        kwargs['endpoint'] = path
        nonce = str(int(time.time() * 1000))

        self.update_headers({
            'Api-Key': self.API_CONKEY,
            'Api-Sign': self._signature(path, nonce, **kwargs),
            'Api-Nonce': nonce
        })
        return super().post(path, **kwargs)
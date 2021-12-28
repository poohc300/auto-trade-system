from django.db import models

# Create your models here.
from dataclasses import dataclass
from typing import Optional
from datetime import date
import base64
import hashlib
import hmac
import time
import urllib
import requests




class BithumbAPI:

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = 'https://api.bithumb.com'



    def _signature(self, path, nonce, **kwargs):
        query_string = path + chr(0) + urllib.parse.urlencode(kwargs) + \
                       chr(0) + nonce
        h = hmac.new(self.secret_key, query_string.encode('utf-8'),
                     hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode('utf-8'))

    def build_header(self, path, **kwargs):
        nonce = str(int(time.time() * 1000))

        headers={
            'Api-Key': self.api_key,
            'Api-Sign': self._signature(path, nonce, **kwargs),
            'Api-Nonce': nonce
        }
        return headers

    def build_get_form(self, path, timeout=3, **kwargs):

        try:
            uri = self.base_url + path
            result = requests.get(uri)
            print(result)

            return result.json()

        except Exception as e:
            return e

    def build_post_form(self, path, timeout=3, **kwargs):

        try:
            url = self.base_url + path
            result = requests.post(
                url=url,
                headers=self.build_header(path=path),
                data=kwargs['data']
            )
            return result.json()

        except Exception as e:
            return e

    def ticker(self, order_currency, payment_currency="KRW"):
        uri = "/public/ticker/{}_{}".format(order_currency, payment_currency)
        return self.build_get_form(uri)

    
    def transaction_history(self, order_currency, payment_currency="KRW", limit=20):
        uri = "/public/transaction_history/{}_{}?count={}".format(order_currency,
                                                    payment_currency,
                                                    limit)
        return self.build_get_form(uri)

    
    def orderbook(self, order_currency, payment_currency, limit):
        print(order_currency)
        uri = f"/public/orderbook/{order_currency}_{payment_currency}?count={limit}"
        print(uri)
        return self.build_get_form(uri)


    def account(self, **kwargs):
        return self.build_post_form('/info/account', **kwargs)

    def balance(self, **kwargs):
        return self.build_post_form('/info/balance', **kwargs)

    def place(self, **kwargs):
        return self.build_post_form('/trade/place', **kwargs)

    def orders(self, **kwargs):
        return self.build_post_form('/info/orders', **kwargs)

    def order_detail(self, **kwargs):
        return self.build_post_form('/info/order_detail', **kwargs)

    def cancel(self, **kwargs):
        return self.build_post_form('/trade/cancel', **kwargs)

    def market_buy(self, **kwargs):
        return self.build_post_form('/trade/market_buy', **kwargs)

    def market_sell(self, **kwargs):
        return self.build_post_form('/trade/market_sell', **kwargs)


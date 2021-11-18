from __future__ import unicode_literals

from django.db import models
import os

from django.db.models import query
from requests.api import head
import jwt
import uuid
import hashlib
import json
from urllib.parse import urlencode

import requests
import pyupbit
from dotenv import load_dotenv
from abc import ABCMeta, abstractclassmethod


class UpbitManager():
    def __init__(self):
        load_dotenv()
        self.access_key = os.getenv('ACCESS_KEY')
        self.secret_key = os.getenv('SECRET_KEY')
        self.server_url = os.getenv('SERVER_URL')

    def _get_balance(self):

        _upbit = pyupbit.Upbit(
            access=self.access_key,
            secret=self.secret_key
            )
        print(_upbit.get_balances())
        #print(upbit.get_balances())




class StrategyManager():
    def __init__(self, data):
        self.market = data["market"]
        self.k = data["k"]

    def get_today_open(self):
        '''
            오늘 시가
        '''
        
        today_open = pyupbit.get_ohlcv(ticker=self.market)[-1:]['open'][0] # 오늘 시가

        return today_open

    def get_yesterday_high(self):
        '''
            어제 고가
        '''

        yesterday_high = pyupbit.get_ohlcv(ticker=self.market)[-2:-1]['high'][0] # 전날 고가

        return yesterday_high

    def get_yesterday_low(self):
        '''
            어제 저가
        '''

        yesterday_low = pyupbit.get_ohlcv(ticker=self.market)[-2:-1]['low'][0] # 전날 고가

        return yesterday_low

    def get_current(self):
        '''
            현재 {self.market}에 해당하는 코인 가격
        '''

        current = pyupbit.get_current_price(self.market)
        return current

    def get_range(self, today_open, yesterday_high, yesterday_low):
        '''
            양봉 * self.k 에 해당하는 값 구하기
            보통 k는 0.5로 많이 함
            expected_
        '''
       
        range = yesterday_high - yesterday_low
        range *= self.k
        result = today_open + range
        return result

    def is_checked_market_condition(self, range, current):
        '''
            현재 매수 할 타임인지 체크 하는 메소드
            현재 해당 코인 시세가 양봉 * k 한 가격보다 높으면 True
            현재 코인 시세는 self.get_current() 메서드에서 받아옴
            낮으면 False
        '''

        is_checked = None

        if range > current:
            is_checked = True
        else:
            is_checked = False
        return is_checked




upbitManager = UpbitManager()
data = {
    "market" : "USDT-BTC",
    "k" : 0.5
}
strategy = StrategyManager(data)
today = strategy.get_today_open()
high = strategy.get_yesterday_high()
low = strategy.get_yesterday_low()
current = strategy.get_current()
range = strategy.get_range(
    today_open=today,
    yesterday_high=high,
    yesterday_low=low
)
ischk = strategy.is_checked_market_condition(
    range=range,
    current=current
    )
print(ischk)
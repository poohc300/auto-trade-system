# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os

from django.db.models import query
import jwt
import uuid
import hashlib
import json
from urllib.parse import urlencode

import requests

class Upbeat():
    def __init__(self):
        self.access_key = 'wIGEVJC8Acp9BpypTKhlMZf8Z55Nabx9HTQBDaJj'
        self.secret_key = 'JI8alCjBZi4RMObT2sixf2DC9PkpZ8lReeVz50lE'
        self.server_url = 'https://api.upbit.com/v1/'

    def getQuery(self):
        query = {
            'market' :  'KRW-ADA'
        }
        return query

    def getQueryString(self):
        query_string = urlencode(self.getQuery()).encode()
        
        return query_string
    
    def getQueryHash(self):
        m = hashlib.sha512()
        m.update(self.getQueryString())
        query_hash = m.hexdigest()

        return query_hash

    def getPayload(self):
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4()),
            'query_hash' : self.getQueryHash(),
            'query_hash_alg' : 'SHA512'
        }

        return payload

    def getJwtToken(self):
        jwt_token = jwt.encode(self.getPayload(), self.secret_key)

        return jwt_token

    def getAuthorizeToken(self):
        authorize_token = 'Bearer {}'.format(self.getJwtToken())

        return authorize_token

    def getHeaders(self):
        headers = {
            "Authorization" : self.getAuthorizeToken()
        }
        return headers

    def sendForm(
        self,
        route_name,
        ):
        res = requests.get(
            self.server_url + route_name,
            headers=self.getHeaders()
            )
        print(res.json())
        return res.json()

    def sendParamForm(
        self,
        route_name
        ):
        res = requests.get(
            self.server_url +  route_name,
            params=self.getQuery(),
            headers=self.getHeaders()
            )
        print(res.json())

        return res.json()

    def getAllAccount(self):
        '''
            전체 계좌 조회
        '''
        route_name = "accounts"
        res = self.sendParamForm(
            route_name=route_name,
            )

    def getOrderChance(self):
        '''
            주문 가능 정보
        '''
        route_name = "orders/chance"
        query = {
            'state' : 'wait'
        }
        res = self.sendParamForm(
            route_name=route_name,
            )

    def getOrderChanceById(self, id):
        '''
            개별 주문 조회
            
            주문 uuid를 통해 개별 주문건을 조회
            문서에는 params=query로 되어있는데 이게 uuid받아와서 검색하는
            구조인지 아닌지 모르겟음
        '''
        route_name = "order"
        res = self.sendParamForm(
            route_name=route_name,
            params=id,
            headers=self.getHeaders()
            )

        return res.json()

    def getOrderList(self):
        '''
            주문 리스트 조회
        '''
        route_name = "orders"
        res = self.sendParamForm(
            route_name=route_name
            )

    def getDepositList(self):
        '''
            입금 리스트 조회
        '''
        route_name = "deposits"
        res = self.sendParamForm(
            route_name=route_name
            )

    def orderRequest(self, volume, price):
        '''
            주문 하기

                market : 거래 시장
                side : 주문 종류
                    - bid : 매수
                    - ask : 매도
                volume : 주문량(지정가, 시장가 매도 시 필수)
                price : 주문가격
                    ex) KRW-BTC 마켓에서 1BTC 당 1000 KRW 로 거래할 경우, 값은 1000이 됨
                        KRW-BTC 마켓에서 1BTC 당 매도 1호가가 500 KRW 인 경우, 시장가 매수 시
                        값을 1000으로 세팅하면 2BTC 가 매수 된다
                        (수수료가 존재하거나 매도 1호가의 수량에 따라 상이할 수 있음)
                ord_type : 주문 타입
                    - limit : 지정가 주문
                    - price : 시장가 주문(매수)
                    - market : 시장가 주문(매도)
                identifier : 조회용 사용자 지정값
        '''
        route_name = "orders"
        ord_type = "limit"
        query = {
            'market' : 'KRW-ADA',
            'side' : 'ask',
            'volume' : volume,
            'price' : price,
            'ord_type' : ord_type
        }
        print(f"쿼리는: {query}")
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4()),
            'query_hash' : query_hash,
            'query_hash_alg' : 'SHA512'
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {
            "Authorization" : authorize_token
        }
        res = requests.post(
            self.server_url + route_name,
            params = query,
            headers = headers
            )
        print(res.json())

    def orderCancelRequest(self):
        route_name = 'order'
        target_id = '3235d9cf-5e12-45da-8706-80aad6afc9f4'
        query = {
            'uuid' : target_id
        }
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4()),
            'query_hash' : query_hash,
            'query_hash_alg' : 'SHA512'
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {
            "Authorization" : authorize_token
        }
        res = requests.delete(
            self.server_url + route_name,
            params=query,
            headers=headers
            )
        print(res.json())

upbeat = Upbeat()
# 전체 계좌 조회
account = upbeat.getAllAccount()
print(account)
# 주문 가능 정보
order = upbeat.getOrderChance()
print(order)
# 주문하기 (매도)
'''
order = upbeat.orderRequest(
    volume = '2',
    price = '5000'
)
'''
# 주문 리스트 조회
orderList = upbeat.getOrderList()
print(orderList)
# 주문 취소
orderCancel = upbeat.orderCancelRequest()

depositList = upbeat.getDepositList()
print(depositList)

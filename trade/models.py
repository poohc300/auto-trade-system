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
            'market' :  'KRW-ETH'
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
        res = self.sendParamForm(
            route_name=route_name
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

upbeat = Upbeat()
account = upbeat.getAllAccount()
print(account)
order = upbeat.getOrderChance()
print(order)
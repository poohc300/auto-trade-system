# -*- coding: utf-8 -*-
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
from dotenv import load_dotenv
from .upbit_dto import UpbitDTO
'''
    upbit 거래소와 상호작용하는 서비스 레이어
    view로부터 통제를 받아 models 또는 serializer 부터 
    필요한 데이터베이스의 데이터를 처리하고 로직을 수행하는 부분

    'ApiClient'는 view를 통해 외부에서 주입되는 upbit key를 self에 담아 저장하는 클래스이다

    'UpbitService'는 
    전체 계좌 조회, 
    주문 가능 정보 조회, 
    개별 주문 조회,
    주문 리스트 조회, 
    입금 리스트 조회, 
    주문하기, 
    주문 취소 요청,
    출금 가능 정보 조회, 
    코인 출금하기, 
    원화 출금하기, 
    개별 입금 조회,
    입금 주소 생성 요청, 
    전체 입금 주소 조회, 
    개별 입금 주소 조회, 
    원화 입금하기,
    입출금 현황 조회, 
    API 키 리스트 조회 기능이 있다

    view에서 service.py에 있는 서비스 호출하는 방법:

    # views.py
    class UpbitView(generics.GenericAPIView):
        def get(self, request, *args, **kwargs):
            UpbitService().any_business_method()
            return Response(...)
'''

class UpbitService():
    
    def __init__(self, data: UpbitDTO):
        self.access_key = data.access_key
        self.secret_key = data.secret_key
        self.server_url = data.server_url
        self.market = data.market
        self.days_number = data.days_number

    def getQuery(self, query):
        query = query
        return query

    def getQueryString(self, query):
        query_string = urlencode(query).encode()
        
        return query_string
    
    def getQueryHash(self, query_string):
        m = hashlib.sha512()
        m.update(query_string)
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

    def getJwtToken(self, payload):
        jwt_token = jwt.encode(payload, self.secret_key)
        return jwt_token

    def getAuthorizeToken(self, jwt_token):
        authorize_token = 'Bearer {}'.format(jwt_token)

        return authorize_token

    def getHeaders(self, authorize_token):
        headers = {
            "Authorization" : authorize_token
        }
        return headers

    def sendForm(
        self,
        route_name,
        headers
        ):
        res = requests.get(
            self.server_url + route_name,
            headers=headers
            )
        print(res.json())
        return res.json()

    def sendParamForm(
        self,
        route_name,
        query,
        headers
        ):
        print(headers)
        res = requests.get(
            self.server_url +  route_name,
            params=query,
            headers=headers
            )
        print(res.json())

        return res.json()

    def getAllAccount(self):
        '''
            전체 계좌 조회
        '''
        route_name = "accounts"
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4())
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        print(authorize_token)
        headers = self.getHeaders(authorize_token)
        res = self.sendForm(
            route_name=route_name,
            headers=headers
            )
        return res

    def getOrderChance(self):
        '''
            주문 가능 정보
        '''
        route_name = "orders/chance"
        query = {
            'market' : 'KRW-ADA'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            "access_key" : self.access_key,
            'nonce' : str(uuid.uuid4()),
            'query_hash' : query_hash,
            'query_hash_alg' : "SHA512"
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
            )
        return res


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
        query = {
            'state': 'done',
            }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)
        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
            )

    def getDepositList(self):
        '''
            입금 리스트 조회
        '''
        route_name = "deposits"
        query = {
            'currency': 'KRW',
            }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
            )

    def orderRequest(self, volume, price, side_status):
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
        side = 'bid' if side_status == 1 else 'ask'
        route_name = "orders"
        ord_type = "limit"
        query = {
            'market' : 'KRW-ADA',
            'side' : side,
            'volume' : volume,
            'price' : price,
            'ord_type' : ord_type
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
        res = requests.post(
            self.server_url + route_name,
            params = query,
            headers = headers
            )
        print(res.json())

    def orderCancelRequest(self):
        '''
            주문 취소 요청
        '''
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

    def getWithrawsChance(self):
        '''
            출금 가능 정보
        '''
        route_name = 'withdraws/chance'
        query = {
            'currency' : 'ADA'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)
        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
            )

    def withdrawCoin(self):
        '''
            코인 출금하기
        '''
        route_name = 'withdraws/coin'
        query = {
            'currency' : 'ADA',
            'amount' : '0.01',
            'address' : '9187a66e-5edf-427c-9d12-0c21c26ae4b8'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
        )

    def withdrawKrw(self):
        '''
            원화 출금하기
        '''
        route_name = 'withdraws/krw'
        query = {
           'amount' : '10000'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
        )

    def getDeposit(self, uuid_value):
        '''
            개별 입금 조회
        ''' 
        route_name = 'deposit'
        query = {
            'uuid' : uuid_value
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
        )

    def generateCoinAddressForDeposit(self):
        '''
            입금 주소 생성 요청
        '''
        route_name = 'deposits/generate_coin_address'
        query = {
            'currency' : 'ADA'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = requests.post(
            self.server_url + route_name,
            params=query,
            headers=headers
        )

    def getAllCoinAddressForDeposit(self):
        '''
            전체 임금 주소 조회
        '''
        route_name = 'deposits/coin_address'
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4())
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)
        
        res = self.sendForm(
            route_name=route_name,
            headers=headers
        )

    def getCoinAddressForDeposit(self):
        '''
            개별 입금 주소 조회
        '''
        route_name = 'deposits/coin_address'
        query = {
            'currency' : 'ADA'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = self.sendParamForm(
            route_name=route_name,
            query=query,
            headers=headers
        )

    def requestDepositKrw(self):
        '''
            원화 입금하기
        '''
        route_name = 'deposity/krw'
        query = {
            'amount' : '10000'
        }
        query_string = self.getQueryString(query)
        query_hash = self.getQueryHash(query_string)
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)

        res = requests.post(
            self.server_url + route_name,
            params=query,
            headers=headers
        )

    def getWalletStatus(self):
        '''
            입출금 현황
        '''
        route_name = 'status/wallet'
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4())
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)
        
        res = self.sendForm(
            route_name=route_name,
            headers=headers
        )

    def getApiKeys(self):
        '''
            API 키 리스트 조회
        '''
        route_name = 'api_keys'
        payload = {
            'access_key' : self.access_key,
            'nonce' : str(uuid.uuid4())
        }
        jwt_token = self.getJwtToken(payload)
        authorize_token = self.getAuthorizeToken(jwt_token)
        headers = self.getHeaders(authorize_token)
        
        res = self.sendForm(
            route_name=route_name,
            headers=headers
        )

    def get_days_candle(self):
        '''
           일 별 캔들 구하기
        '''
        market=self.market
        days_number=self.days_number
        route_name = 'day_candles'
        url = f"https://api.upbit.com/v1/candles/days?market={market}&count={days_number}"
        headers =  {"Accept" : "application/json"}
        response= requests.request(
            "GET",
            url,
            headers=headers
            )
        return response.text
'''
    테스트 코드
'''
'''
upbeat = Upbeat()
# 전체 계좌 조회
account = upbeat.getAllAccount()
print(f'전체계좌조회: {account}')
# 주문 가능 정보
orderInfo = upbeat.getOrderChance()
print(f'주문가능정보: {orderInfo}')

# 주문하기 
# side_status 가 1이면 매수 
# side_statsu 가 1이 아닌 경우는 매도

order = upbeat.orderRequest(
    volume = 1,
    price = '5000',
    side_status=1
)
print(f'주문하기: {order}')

# 주문 리스트 조회
orderList = upbeat.getOrderList()
print(f'주문리스트 조회: {orderList}')

# 주문 취소
orderCancel = upbeat.orderCancelRequest()
print(f'주문취소: {orderCancel}')


# 출금 가능 정보
withdrawChance = upbeat.getWithrawsChance()
print(f'출금가능 정보: {withdrawChance}')

# 코인 출금하기
withdrawCoin = upbeat.withdrawCoin()
print(f'코인 출금하기: {withdrawCoin}')

# 원화 출금하기
withdrawKrw = upbeat.withdrawKrw()
print(f'원화 출금하기: {withdrawKrw}')

# 입금리스트 조회
depositList = upbeat.getDepositList()
print(f'입금리스트 조회: {depositList}')

# 개별 입금 조회
# 상세 검색이니 입금 uuid 가 파라메타에 필요함
deposit = upbeat.getDeposit(uuid_value='')
print(f'개별 입금 조회: {deposit}')

# 입금 주소 생성 요청
coinAddressForDeposit = upbeat.generateCoinAddressForDeposit()
print(f'입금 주소 생성 요청: {coinAddressForDeposit}')

# 전체 입금 주소 조회
allCoinAddressForDeposit = upbeat.getAllCoinAddressForDeposit()
print(f'전체 입금 주소 조회: {coinAddressForDeposit}')

# 개별 입금 주소 조회
coinAddressForDeposit = upbeat.getCoinAddressForDeposit()
print(f'개별 입금 주소 조회: {coinAddressForDeposit}')

# 원화 입금 하기
depositKrw = upbeat.requestDepositKrw()
print(f'원화 입금 하기: {depositKrw}')

# 입출금 현황
walletStatus = upbeat.getWalletStatus()
print(f'입출금 현황: {walletStatus}')

# API 키 리스트 조회
apiKeys = upbeat.getApiKeys()
print(f'API 키 리스트 조회: {apiKeys}')
'''
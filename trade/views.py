# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABC, abstractclassmethod
from .services.api.upbit_dto import UpbitDTO
from .services.strategies.rarrywilliams_st import Strategy
from .services.strategies.okex_strategy import OkexStrategy
from .services.strategies.auto_trade_strategy import AutotradeStrategy
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
import os
import json
from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from abc import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OrderView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )
    @swagger_auto_schema(
        operation_summary="주문 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ord_type' : openapi.Schema(type=openapi.TYPE_STRING, description='limit: 지정가 market: 시장가'),
                'is_bid' : openapi.Schema(type=openapi.TYPE_STRING, description='1이면 매수 0이면 매도'),
                'price' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 가격'),
                'volume' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 사이즈'),
                'market' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) KRW-BTC'),
            }
        ),
        tags=["trade"],
        operation_description="order",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        '''
            ord_type 따라 다름
            limit: 지정가
            price: 시장가 매수
            market:
        '''
        data = request.data['body']
        ord_type = data['ord_type']
        is_bid = data['is_bid']
        price = data['price'] if data['price'] is not None else 0
        volume = data['volume'] if data['volume'] is not None else 0
        market = data['market']
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        # upbit
        service = Strategy(dto)
        
       
        try:
            side_status = 0
            #result = service.orderRequest()
            print(ord_type)
            if ord_type == "시장가":
                ord_type = 'market'
            elif ord_type == "지정가":
               ord_type = 'limit'
            if is_bid == '매수':
                side_status = 1
            else:
                side_status = 0  
            print(is_bid)
            print(price)
            print(volume)
            print(side_status)
           


            result = service.orderRequest(
                volume=float(volume),
                market=market,
                price=float(price),
                ord_type=ord_type,
                side_status=side_status
            )
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)



class OrderBookView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )
    @swagger_auto_schema(
        operation_summary="오더북 조회 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'market' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) KRW-BTC')
            }
        ),
        tags=["trade"],
        operation_description="orderbook list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        service = Strategy(dto)

        try:
            result = service.get_orderbooks()[0]
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return JsonResponse(result)

class AccountView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )
    @swagger_auto_schema(
        operation_summary="현재 사용자 계좌정보 조회 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_key' : openapi.Schema(type=openapi.TYPE_STRING, description='access key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='secret key'),
                'market' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) KRW-BTC')
            }
        ),
        tags=["trade"],
        operation_description="retrieve current user's balance",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        service = Strategy(dto)

        try:
            result = service.getAllAccount(
            )
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)

class OrderChanceView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        service = Strategy(dto)

        try:
            result = service.getOrderChance(
            )
            print("오더 찬스")
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return JsonResponse(result)

class OrderListView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )

    @swagger_auto_schema(
        operation_summary="완료 & 취소된 주문 내역 조회하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_key' : openapi.Schema(type=openapi.TYPE_STRING, description='access key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='secret key'),
                'market' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) KRW-BTC')
            }
        ),
        tags=["trade"],
        operation_description="retrieve done & canceled order list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        service = Strategy(dto)

        try:
            result = service.getOrderList(
                page=1,
                order_by='asc'
            )
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)

class UnfinishedOrderListView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )
    @swagger_auto_schema(
        operation_summary="미체결 주문 내역 조회하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_key' : openapi.Schema(type=openapi.TYPE_STRING, description='access key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='secret key'),
                'market' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) KRW-BTC')
            }
        ),
        tags=["trade"],
        operation_description="retrieve unfinished order list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        service = Strategy(dto)

        try:
            result = service.getUnfinishedOrderList(
                page=1,
                order_by='asc'
            )
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)

class OrderCancelView(APIView):

    def build_dto(self, access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )
    @swagger_auto_schema(   
        operation_summary="주문 취소하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_key' : openapi.Schema(type=openapi.TYPE_STRING, description='access key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='secret key'),
                'market' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) KRW-BTC'),
                'uuid' : openapi.Schema(type=openapi.TYPE_STRING, description='ex) 주문 uuid')
            }
        ),
        tags=["trade"],
        operation_description="delete order by uuid",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        dto = self.build_dto(
            access_key = data['access_key'],
            secret_key = data['secret_key'],
            server_url="https://api.upbit.com/v1/",
            market = data['market'],
            days=2
        )
        service = Strategy(dto)
        try:
            result = service.orderCancelRequest(
                id=data['order_uuid']
            )
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)


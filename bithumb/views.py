from django.shortcuts import render

# Create your views here.
from .services import BithumbService
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

@permission_classes([AllowAny])
class OrderView(APIView):

    @swagger_auto_schema(   
        operation_summary="주문 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='구매할 코인 통화'),
                'unit' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 수량'),
                'price' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 가격'),
                'api_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'api_secret' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'status' : openapi.Schema(type=openapi.TYPE_STRING, description='0: 지정가 매수 1: 지정가 매도 2: 시장가 매수 3: 시장가 매도')
            }
        ),
        tags=["bithumb"],
        operation_description="order",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        _order_currency = data['order_currency']
        _unit = data['unit']
        _price = data['price']
        _api_key = data['api_key']
        _api_secret = data['api_secret']
        _status = data['status']

        bithumb = BithumbService(
            conkey=_api_key,
            seckey=_api_secret
        )
        result = None
        try:
            # status가 
            # 0이면 지정가 매수 
            # 1이면 지정가 매도
            # 2면 시장가 매수
            # 3이면 시장가 매도

            if _status == "0":
                result = bithumb.buy_limit_order(
                    order_currency=_order_currency,
                    price=_price,
                    unit=_unit
                )
            elif _status == "1":
                result = bithumb.sell_limit_order(
                    order_currency=_order_currency,
                    price=_price,
                    unit=_unit
                )
            elif _status == "2":
                result = bithumb.buy_market_order(
                    order_currency=_order_currency,
                    unit=_unit
                )
            elif _status == "3":
                result = bithumb.sell_market_order(
                    order_currency=_order_currency,
                    unit=_unit
                )
            else:
                return "error"

        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)




@permission_classes([AllowAny])
class OrderBookView(APIView):

    @swagger_auto_schema(   
        operation_summary="오더북 리스트 조회하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'api_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'api_secret' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'order_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='통화 종류'),
                'payment_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='구매할 통화 KRW'),
            }
        ),
        tags=["bithumb"],
        operation_description="retrieve orderbook list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        _order_currency = data['order_currency']
        _payment_currency = data['payment_currency']
        _api_key = data['api_key']
        _api_secret = data['api_secret']    
        bithumb = BithumbService(
            conkey=_api_key,
            seckey=_api_secret
        )
        try:
           
            result = bithumb.get_orderbook(
                order_currency=_order_currency,
                payment_currency=_payment_currency
            )

        except Exception as e:
            return HttpResponse(e)

        return JsonResponse(result)

@permission_classes([AllowAny])
class AccountView(APIView):

    @swagger_auto_schema(   
        operation_summary="계좌 정보 조회 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'api_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'api_secret' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='api currency')
            }
        ),
        tags=["bithumb"],
        operation_description="retrieve order list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
      
        _api_key = data['api_key']
        _api_secret = data['api_secret']    
        _currency = data['currency']
        
        bithumb = BithumbService(
            conkey=_api_key,
            seckey=_api_secret
          
        )
        try:
           
            result = bithumb.get_balance(currency=_currency)
            print(result)

        except Exception as e:
            return HttpResponse(e)

        return JsonResponse(result)


@permission_classes([AllowAny])
class OrderListView(APIView):

    @swagger_auto_schema(   
        operation_summary="주문 내역 조회 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'api_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'api_secret' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'order_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='통화 종류')
            
            }
        ),
        tags=["bithumb"],
        operation_description="retrieve order list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        _api_key = data['api_key']
        _api_secret = data['api_secret']   
        _order_currency = data['order_currency']
        
        bithumb = BithumbService(
            conkey=_api_key,
            seckey=_api_secret
        )
      
        try:
            result = bithumb.get_transaction_history(
                order_currency= _order_currency
            )
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)

@permission_classes([AllowAny])
class UnfinishedOrderListView(APIView):

    @swagger_auto_schema(   
        operation_summary="미체결 주문 내역 조회 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'api_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'api_secret' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'order_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='주문할 통화 종류'),
                'order_id' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 uuid, 공백일 시 전체리스트 조회'),
                'payment_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='구매할 통화 KRW'),
                'type' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 종류')
            }
        ),
        tags=["bithumb"],
        operation_description="retrieve order list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        _api_key = data['api_key']
        _api_secret = data['api_secret']   
        _order_currency = data['order_currency']
        _order_id = data['order_id']
        _payment_currency = data['payment_currency']
        _type = data['type']

        bithumb = BithumbService(
            conkey=_api_key,
            seckey=_api_secret
        )
        _order_desc = {
            'type' : _type,
            'order_currency' : _order_currency,
            'order_id' : _order_id,
            'payment_currency' : _payment_currency
        }
        try:
            result = bithumb.get_outstanding_order(
                order_desc= _order_desc
            )
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)

@permission_classes([AllowAny])
class OrderCancelView(APIView):

    @swagger_auto_schema(   
        operation_summary="주문 취소 하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'api_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'api_secret' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'order_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='주문할 통화 종류'),
                'order_id' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 uuid, 공백일 시 전체리스트 조회'),
                'payment_currency' : openapi.Schema(type=openapi.TYPE_STRING, description='구매할 통화 KRW'),
                'type' : openapi.Schema(type=openapi.TYPE_STRING, description='주문 종류')
            }
        ),
        tags=["bithumb"],
        operation_description="retrieve order list",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        _api_key = data['api_key']
        _api_secret = data['api_secret']   
        _order_currency = data['order_currency']
        _order_id = data['order_id']
        _payment_currency = data['payment_currency']
        _type = data['type']

        bithumb = BithumbService(
            conkey=_api_key,
            seckey=_api_secret
        )
        _order_desc = {
            'type' : _type,
            'order_currency' : _order_currency,
            'order_id' : _order_id,
            'payment_currency' : _payment_currency
        }
        try:
            result = bithumb.cancel_order(
                order_desc= _order_desc
            )

        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)


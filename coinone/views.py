from django.shortcuts import render
from .models import CoinoneService
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json

@permission_classes([AllowAny])
class OrderBookView(APIView):

    @swagger_auto_schema(   
        operation_summary="오더북 리스트 조회하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='currency')
            }
        ),
        tag=['coinone'],
        operation_description='retrieve orderbook list'
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        _access_token = data['access_token']
        _secret_key = data['secret_key']
        _currency = data['currency']
        coinone = CoinoneService(
            access_token=_access_token,
            secret_key=_secret_key
        )
        try:
            result = coinone.get_orderbook(
                currency=_currency
            )
            return HttpResponse(result)
        except Exception as e:
            return HttpResponse(e)

@permission_classes([AllowAny])
class OrderView(APIView):

    @swagger_auto_schema(   
        operation_summary="주문하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'order_type' : openapi.Schema(type=openapi.TYPE_STRING, description='order_type'),
                'price' : openapi.Schema(type=openapi.TYPE_STRING, description='price'),
                'qty' : openapi.Schema(type=openapi.TYPE_STRING, description='qty'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='currency')
            }
        ),
        tag=['coinone'],
        operation_description='create order'
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
       
        kwargs = data

        coinone = CoinoneService(
            access_token=data['access_token'],
            secret_key=data['secret_key']
        )
        try:
            print(kwargs)
            result = coinone.create_order(
               **kwargs
            )
            return HttpResponse(result)
        except Exception as e:
            return HttpResponse(e)

@permission_classes([AllowAny])
class AccountView(APIView):

    @swagger_auto_schema(   
        operation_summary="계좌 정보",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
            }
        ),
        tag=['coinone'],
        operation_description='retrieve balance'
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        print(data)
        kwargs = data

        coinone = CoinoneService(
            access_token=data['access_token'],
            secret_key=data['secret_key']
        )
        try:
            result = coinone.get_balance(
              **kwargs
            )
            return JsonResponse(result)
        except Exception as e:
            return HttpResponse(e)

@permission_classes([AllowAny])
class OrderView(APIView):

    @swagger_auto_schema(   
        operation_summary="주문하기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'order_type' : openapi.Schema(type=openapi.TYPE_STRING, description='order_type'),
                'price' : openapi.Schema(type=openapi.TYPE_STRING, description='price'),
                'qty' : openapi.Schema(type=openapi.TYPE_STRING, description='qty'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='currency')
            }
        ),
        tag=['coinone'],
        operation_description='주문하기 order_type이 0이면 지정가 매수 1이면 지정가 매도\
        2이면 시장가 매수 3이면 시장가 매도 '
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
       
        kwargs = data

        coinone = CoinoneService(
            access_token=data['access_token'],
            secret_key=data['secret_key']
        )
        try:
            print(kwargs)
            result = coinone.create_order(
               **kwargs
            )
            return JsonResponse({"message": "주문이 완료되었습니다"})
        except Exception as e:
            return HttpResponse(e)

@permission_classes([AllowAny])
class OrderCancelView(APIView):

    @swagger_auto_schema(   
        operation_summary="미체결 주문 취소",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'qty' : openapi.Schema(type=openapi.TYPE_STRING, description='qty'),
                'price' : openapi.Schema(type=openapi.TYPE_STRING, description='price'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='currency'),
                'order_id' : openapi.Schema(type=openapi.TYPE_STRING, description='order id'),
                'is_ask' : openapi.Schema(type=openapi.TYPE_STRING, description='1이면 매도 0이면 매수')

            }
        ),
        tag=['coinone'],
        operation_description='cancel order'
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        print(data)
        kwargs = data

        coinone = CoinoneService(
            access_token=data['access_token'],
            secret_key=data['secret_key']
        )
        try:
            result = coinone.cancel_coin_order(
              **kwargs
            )
            return JsonResponse(result)
        except Exception as e:
            return HttpResponse(e)

@permission_classes([AllowAny])
class TransactionHistoryView(APIView):

    @swagger_auto_schema(   
        operation_summary="트랜잭션 정보",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'price' : openapi.Schema(type=openapi.TYPE_STRING, description='price'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='currency'),
                'is_coin' : openapi.Schema(type=openapi.TYPE_STRING, description='1이면 코인 0이면 KRW')
            }
        ),
        tag=['coinone'],
        operation_description='retrieve transaction history'
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        print(data)
        kwargs = data

        coinone = CoinoneService(
            access_token=data['access_token'],
            secret_key=data['secret_key']
        )
        try:
            if kwargs['is_coin'] == "1":
                result = coinone.get_coin_transaction_history(
                **kwargs
                )
            else:
                result = coinone.get_krw_transaction_history(
                **kwargs
                )
            return JsonResponse(result)
        except Exception as e:
            return HttpResponse(e)

@permission_classes([AllowAny])
class OrderlistView(APIView):

    @swagger_auto_schema(   
        operation_summary="지정가 주문 정보",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token' : openapi.Schema(type=openapi.TYPE_STRING, description='api key'),
                'secret_key' : openapi.Schema(type=openapi.TYPE_STRING, description='api secret'),
                'currency' : openapi.Schema(type=openapi.TYPE_STRING, description='currency'),
            }
        ),
        tag=['coinone'],
        operation_description='retrieve orderlist'
    )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        print(data)
        kwargs = data

        coinone = CoinoneService(
            access_token=data['access_token'],
            secret_key=data['secret_key']
        )
        try:
            result = coinone.get_limit_orders(
                **kwargs
            )
            return JsonResponse(result)
        except Exception as e:
            return HttpResponse(e)
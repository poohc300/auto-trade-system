from django.shortcuts import render

# Create your views here.
from .services import Bithumb
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


@permission_classes([AllowAny])
class OrderView(APIView):

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        _order_currency = data['order_currency']
        _unit = data['unit']
        _price = data['price']
        _api_key = data['api_key']
        _api_secret = data['api_secret']
        _status = data['status']

        bithumb = Bithumb(
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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        _order_currency = data['order_currency']
        _payment_currency = data['payment_currency']
        _api_key = data['api_key']
        _api_secret = data['api_secret']    

        bithumb = Bithumb(
            conkey=_api_key,
            seckey=_api_secret
        )
        try:
           
            result = bithumb.get_orderbook(
                order_currency=_order_currency
            )

        except Exception as e:
            return HttpResponse(e)

        return JsonResponse(result)

@permission_classes([AllowAny])
class AccountView(APIView):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        _currency = data['_currency']
        _api_key = data['api_key']
        _api_secret = data['api_secret']    

        bithumb = Bithumb(
            conkey=_api_key,
            seckey=_api_secret
        )
        try:
           
            result = bithumb.get_balance(
                currency=_currency
            )

        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)


@permission_classes([AllowAny])
class OrderListView(APIView):

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        _api_key = data['api_key']
        _api_secret = data['api_secret']   
        _order_currency = data['order_currency']
        _order_id = data['order_id']
        _payment_currency = data['payment_currency']
        _type = data['type']

        bithumb = Bithumb(
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
            result = bithumb.get_order_completed(
                order_desc= _order_desc
            )
            print(result)
        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)

@permission_classes([AllowAny])
class UnfinishedOrderListView(APIView):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        _api_key = data['api_key']
        _api_secret = data['api_secret']   
        _order_currency = data['order_currency']
        _order_id = data['order_id']
        _payment_currency = data['payment_currency']
        _type = data['type']

        bithumb = Bithumb(
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

    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data['body']
        _api_key = data['api_key']
        _api_secret = data['api_secret']   
        _order_currency = data['order_currency']
        _order_id = data['order_id']
        _payment_currency = data['payment_currency']
        _type = data['type']

        bithumb = Bithumb(
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


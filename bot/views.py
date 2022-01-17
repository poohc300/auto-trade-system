from django.shortcuts import render
from trade.services.strategies.auto_trade_strategy import AutotradeStrategy
from trade.services.api.upbit_dto import UpbitDTO
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from .serializers import BotSerializer
from django.shortcuts import render
import os
import json
from rest_framework.decorators import api_view #api
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

@permission_classes([AllowAny])
class BotView(APIView):
    serializer_class = BotSerializer

    @swagger_auto_schema(   
        operation_summary="봇 ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id' : openapi.Schema(type=openapi.TYPE_STRING, description='user_id'),
                'balance' : openapi.Schema(type=openapi.TYPE_NUMBER, description='balance'),
                'profit_percent' : openapi.Schema(type=openapi.TYPE_STRING, description='익절 퍼센트'),
                'loss_percent' : openapi.Schema(type=openapi.TYPE_STRING, description='손절 퍼센트')
            }
        ),
        tags=["bot"],
        operation_description="bot 생성",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        serializer = BotSerializer(data=request.data)
      
        try:
            # 봇 생성
            if serializer.is_valid(raise_exception=True):
                serializer.save()

       
                return JsonResponse({"message" : "200"})

        except Exception as e:
            return JsonResponse({"message" : e})

@permission_classes([AllowAny])
class BotTradeView(APIView):

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
        operation_summary="봇 트레이드 생성",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bot_id' : openapi.Schema(type=openapi.TYPE_STRING, description='봇 아이디')
            }
        ),
        tags=["bot"],
        operation_description="bot 트레이드 생성",
    )  
    def post(self, request, *args, **kwargs) -> HttpResponse:
        data = request.data
        kwargs = data
        dto = self.build_dto(
            access_key = 1,
            secret_key = 1,
            server_url="https://api.upbit.com/v1/",
            market = "",
            days=0
        )
        service = AutotradeStrategy(dto)
        '''
            봇마다 최대 100만원 까지 예산이 주어지는데
            여기서 해당 봇의 예산을 할당할 수 있다
            balance 만큼 금액을 봇이 돌리게 되며 그만큼 봇의 예산에서 차감된다

            :bot_id: :자동 트레이드 시작할 봇 아이디
            :balance: :봇의 자동트레이드 예산 최대 100만원까지 가능
        '''
        try:
            
            
            mvl = service.get_moving_average_line(
                **kwargs
                )
        
            bot = service.check_bid_condition(
                moving_average_line=mvl,
                **kwargs
            )
         
            
            
            
            return JsonResponse({"data" : bot})

        except Exception as e:
            return JsonResponse({"message" : e})

@api_view(['POST'])
@permission_classes([AllowAny])
def create_filtered_coin_list(request):
    '''
        상위 20개 코인 리스트 받아오는 부분
    '''
    def build_dto(access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )

    data = request.data
    kwargs = data
    dto = build_dto(
            access_key = 1,
            secret_key = 1,
            server_url="https://api.upbit.com/v1/",
            market = "",
            days=0
        )
   

    service = AutotradeStrategy(dto)
    coin_list = service.filter_market_status(
                **kwargs
            )
    return JsonResponse({"message" : "success"})

@swagger_auto_schema(method='post', request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'bot_id': openapi.Schema(type=openapi.TYPE_STRING, description='bot id'),
        }
    ))
@api_view(['POST'])
@permission_classes([AllowAny])
def off_bot(request):
    '''
        bot의 status가 false이면 종료
    '''
    def build_dto(access_key, secret_key,server_url, market, days) -> UpbitDTO:
        #load_dotenv()
        return UpbitDTO(
            access_key=access_key,
            secret_key=secret_key,
            server_url=server_url,
            market=market,
            days_number=days
        )

    data = request.data
    kwargs = data
    dto = build_dto(
            access_key = 1,
            secret_key = 1,
            server_url="https://api.upbit.com/v1/",
            market = "",
            days=0
        )
   

    service = AutotradeStrategy(dto)

    sql = "UPDATE bot_bot SET status=%(status)s WHERE id=%(id)s"
    data = {
        "status" : False,
        "id" : request.data['bot_id']
    }
    result = service.conn_where(
        sql,
        data
    )
    return JsonResponse({"message" : "success"})
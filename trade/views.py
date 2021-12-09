# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .services.api.upbit_dto import UpbitDTO
from .services.strategies.rarrywilliams_st import Strategy
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
import os
import json
from dotenv import load_dotenv

# Create your views here.

class OrderAPIView(APIView):

    @staticmethod
    def build_dto() -> UpbitDTO:
        load_dotenv()
        return UpbitDTO(
            access_key=os.getenv('ACCESS_KEY'),
            secret_key=os.getenv('SECRET_KEY'),
            server_url="https://api.upbit.com/v1/",
            market="KRW-ADA",
            days_number=2
        )
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        
        dto = self.build_dto()
        service = Strategy(dto)
        try:
            result = service.get_current_price()

        except Exception as e:
            return HttpResponse(e)

        return HttpResponse(result)


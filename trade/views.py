# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from services.api.upbit_dto import UpbitDTO
from services.api.upbit_service import UpbitService
from services.orders.order_dto import OrderDTO
from services.orders.order_service import OrderService
from drf_service_layer.views import GenericServiceAPIView
from django.shortcuts import render
import os
# Create your views here.

class OrderAPIView(GenericServiceAPIView):

    @property
    def dto(self) -> UpbitDTO:
        return UpbitDTO(
            access=os.getenv('ACCESS_KEY'),
            secret=os.getenv('SECRET_KEY')
        )
    
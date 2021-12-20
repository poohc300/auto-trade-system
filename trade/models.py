# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import os

from django.db.models import query
from urllib.parse import urlencode
import datetime


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField(max_length=100)
    quantity = models.FloatField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=200)
    status = models.BooleanField()
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']
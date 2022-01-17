# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import os

from django.db.models import query
from urllib.parse import urlencode
import datetime
from accounts.models import User

class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(max_length=100)
    market = models.CharField(max_length=200, null=True)
    volume = models.FloatField(max_length=100, null=True)
    is_bid = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    bid_price = models.FloatField(max_length=100, null=True)
    profit_percent = models.FloatField(max_length=50, null=True)
    loss_percent = models.FloatField(max_length=50, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class FilteredMarket(models.Model):
    coin = models.CharField(max_length=200, null=True)
    volume = models.FloatField(max_length=200, null=True)

class TransactionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    uuid = models.TextField()
    side = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    market = models.CharField(max_length=100, null=True)
    volume = models.FloatField(max_length=100)
    price = models.FloatField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


    
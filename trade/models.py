# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
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

class User(models.Model):
    name = models.CharField(max_length=60)
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class Accounts(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    balance = models.FloatField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(default=datetime.datetime.now())

    class Meta:
        ordering = ['created_at']

class Cryptos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField(max_length=100)
    quantity = models.FloatField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=200)
    status = models.BooleanField()
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    crypto_id = models.ForeignKey('Crypto')
    
    class Meta:
        ordering = ['created_at']
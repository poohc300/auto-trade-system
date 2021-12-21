from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
import datetime

class User(AbstractUser):
    objects = UserManager()
    
    # blank=True: 폼(입력양식)에서 빈채로 저장되는 것을 허용, DB에는 ''로 저장
    # CharField 및 TextField는 blank=True만 허용, null=True 허용 X
    username = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=300)
    api_key = models.CharField(blank=True, max_length=100)
    secret_key = models.CharField(blank=True, max_length=100)
    created_at = models.DateField(default=datetime.datetime.now())
    #profile_image = models.ImageField(blank=True, null=True) # null=True: DB에 NULL로 
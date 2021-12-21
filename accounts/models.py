from datetime import timezone
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils import timezone

def get_now():

    return timezone.localtime()

class User(AbstractUser):
    objects = UserManager()
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=300)
    api_key = models.CharField(blank=True, max_length=100)
    secret_key = models.CharField(blank=True, max_length=100)
    created_at = models.DateField(default=get_now())
    #profile_image = models.ImageField(blank=True, null=True) # null=True: DB에 NULL로 
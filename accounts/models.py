from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class User(AbstractBaseUser):

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'user_id'
    class Meta:
        db_table = 'User'
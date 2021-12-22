from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError('id가 없습니다')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(user_id, password, **extra_fields)

    def create_superuser(self, user_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자로 가입하려면 is_staff가 1이어야 함')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자로 가입하려면 is_superuser가 1이어야 함')
        
        return self._create_user(user_id, password, **extra_fields)


class User(AbstractBaseUser):
    object = UserManager()

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'user_id'
    
    class Meta:
        db_table = 'User'
from .base import *

DEBUG = True
import pymysql
pymysql.install_as_MySQLdb()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "auto-trade",
        "USER": 'root',
        "PASSWORD" : 'Gmc@1234!',
        "HOST" : '127.0.0.1',
        "PORT" : '3306'
    }
}

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

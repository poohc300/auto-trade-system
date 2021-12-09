from dataclasses import dataclass
from typing import Optional
from datetime import date
import os
from abc import *

@dataclass
class UpbitDTO:
    access_key: str
    secret_key: str
    server_url: str
    market: str
    days_number: int
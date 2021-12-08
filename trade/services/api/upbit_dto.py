from dataclasses import dataclass
from typing import Optional
from datetime import date
import os

@dataclass
class UpbitDTO:
    access_key: str
    secret_key: str

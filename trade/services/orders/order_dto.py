from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class OrderDTO:
    coin_id: int
    user_id: int
    account_id: int

    
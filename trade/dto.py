from dataclasses import dataclass
from typing import Optional

@dataclass
class UpbitDTO:
    access_key: str
    secret_key: str
    server_url: str

    
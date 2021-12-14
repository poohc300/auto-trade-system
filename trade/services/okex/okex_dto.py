from dataclasses import dataclass

@dataclass
class OkexDTO:
    base_rest_url: str
    api_key: str
    secret_key: str
    passphrase: str
    instId: str
    

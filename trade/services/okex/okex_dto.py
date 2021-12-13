from dataclasses import dataclass

@dataclass
class OkexDTO:
    base_rest_url: str
    base_public_websocket_url: str
    base_private_websocket_url: str
    api_key: str
    secret_key: str
    passphrase: str
    market: str
    

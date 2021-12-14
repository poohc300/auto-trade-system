from ..okex.okex_dto import OkexDTO
from ..okex.okex_service import OkexService
import json
import time
import os
import datetime

class OkexStrategy(OkexService):

    def __init__(self, dto:OkexDTO):
        self.dto = dto
        super().__init__(dto)

    def test(self):
        result = super().get_orderbook()
        print(result)
        return result

        

okex_st = OkexStrategy(
    OkexDTO(
    base_rest_url='https://www.okex.com',
    api_key='b4eaec2d-2655-4a40-a105-84ed2850b9b6',
    secret_key='1D8BEA9C0DA092DFC3C3632B544EBEC1',
    passphrase='mm0819',
    instId='ADA-USD-SWAP'
    )
)
okex_st.test()

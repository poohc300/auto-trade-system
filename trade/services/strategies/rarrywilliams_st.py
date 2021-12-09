from ..api.upbit_service import UpbitService
from ..api.upbit_dto import UpbitDTO
import json

class Strategy(UpbitService):

    def __init__(self, dto: UpbitDTO):
       
       super().__init__(dto)

    def get_range(self):
        '''
            range = (어제 고가 - 어제 저가) * 0.5
            오늘 시가 + range 가 지금 시세보다 낮으면 매도 높으면 보류

            market = "KRW-BTC" 
            days_number = 1 (1이면 오늘 하루동안 정보 2면 어제까지)
        '''
        result = super().get_days_candle()
        range = 0.0
        opening_price = result[0]['opening_price']
        high_price = result[1]['high_price']
        low_price = result[1]['low_price']
        range = (high_price - low_price) * 0.5
        range += opening_price
        return range

    def get_current_price(self):
        '''
            현재 해당하는 코인 시세 구하기
        '''
        result = super().get_ticks()[0]
        result = result['trade_price']

        return result
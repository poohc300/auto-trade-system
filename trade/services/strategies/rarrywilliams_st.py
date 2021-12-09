from ..api.upbit_service import UpbitService
from ..api.upbit_dto import UpbitDTO
import json
import time

class Strategy(UpbitService):

    def __init__(self, dto: UpbitDTO):
       self.dto = dto
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

    def get_my_coin(self):
        '''
            현재 내가 보유한 해당 코인 정보
        '''
        data = super().getAllAccount()
        return data

    def ask(self):
        '''
            전략에 따라 매도하기
            
        '''
        target_price = self.get_range()
        current_price = self.get_current_price()
        volume = self.get_current_target_balance()
        if target_price > current_price:
            print("래리타임")
            result = super().orderRequest(
                volume=volume,
                price=target_price,
                ord_type='limit',
                market=self.dto.market,
                side_status=0
            )
            print(result)
        else:
            print("기다려")
            time.sleep(3000)
            a = self.ask()
            print(a)
            

    def bid(self):
        '''
            해당 코인 매수하기
        
            
        '''
        data = self.get_affordable_order_info()
        result = super().orderRequest(
            volume=data['volume'],
            price=data['current_price'],
            ord_type='limit',
            market=self.dto.market,
            side_status=1
        )
        return result

    def get_affordable_order_info(self):
        '''
            제한된 금액 내에서
            해당하는 코인을
            얼마나 구매할 수 있는지 정보 구하기
        '''
        working_funds = 10000
        volume = 0.0
        current_price = self.get_current_price()
        volume = working_funds / current_price
        return {'volume' : volume, 'current_price' : current_price}

    def get_current_target_balance(self):
        '''
            현재 계좌 정보 중에서
            원하는 코인의 정보에 대한 보유량만 검색
        '''
        market = self.dto.market.split("-")[1]
        result = super().getAllAccount()
        balance = 0.0
        locked = 0.0
        for i in range(0, len(result)):
            if result[i]['currency'] == market:
                balance = result[i]['balance']
        return balance

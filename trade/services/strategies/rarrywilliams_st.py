from ..api.upbit_service import UpbitService
from ..api.upbit_dto import UpbitDTO
import json
import time
import os
import datetime

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

    def get_range_minute(self):
        '''
            range = (어제 고가 - 어제 저가) * 0.5
            오늘 시가 + range 가 지금 시세보다 낮으면 매도 높으면 보류

            market = "KRW-BTC" 
            days_number = 1 (1이면 오늘 하루동안 정보 2면 어제까지)
        '''
        result = super().get_minutes_candle()
        range = 0.0
        high_price = result[0]['high_price']
        low_price = result[0]['low_price']
        range = (float(high_price) - float(low_price)) * 0.5
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
        #target_price = self.get_range()
        current_price = self.get_current_price()
        volume = self.get_current_target_balance()
        result = super().orderRequest(
            volume=volume,
            price=current_price,
            ord_type='limit',
            market=self.dto.market,
            side_status=0
        )
        print(result)
       
            

    def bid(self, units, sell_price):
        '''
            해당 코인 매수하기
        
            
        '''
        _sell_price = sell_price
        _units = units
        
        result = super().orderRequest(
            volume=_units,
            price=_sell_price,
            ord_type='limit',
            market=self.dto.market,
            side_status=1
        )
            
        return result

    def get_affordable_order_info(self, current_money):
        '''
            제한된 금액 내에서
            해당하는 코인을
            얼마나 구매할 수 있는지 정보 구하기
        '''
        working_funds = current_money
        volume = 0.0

                
        current_price = self.get_current_price()
        target_price = self.get_range_minute() + current_price

        current_price = self.get_current_price()
        volume = float(working_funds) / float(target_price)
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

    def rotate(self):
        '''
            매수 매도 반복
            
            가격변동폭 계산: 전일 고가에서 전일 저가를 빼서 변동폭 구함
            매수기준: 당일 시간에서 변동폭 * 0.5 이상 상승하면 해당 가격에 바로 매수하고
            매도는 당일 종가에 매도함 

        '''
       

        # 분 봉 가격 받아오기
        minute_range = self.get_range_minute()
        current_coin_value = self.get_current_price() 
        range = current_coin_value + minute_range
        now = datetime.datetime.now()
        update_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(hours=1)
        while True:
            '''
            주기적으로 현재가 얻어오기
                2초에 한번씩 비트코인의 현재가 화면 출력(거래소마다 API 호출 횟수 제한 때문)

            목표가 계산하기
                전일 가격 정보 얻어온 후 금일 매수 목표가 계산하기

            목표가 갱신하기
                래리 윌리엄스에서는 목표가는 프로그램이 시작할 때 한번, 그리고 매일 자정마다 갱신해야함

            매수 시도
                목표가가 현재가 이상일 경우 잔고를 조회하고 주문 가능한 수량을 계산한 후에 시장가 매수
                현재가가 목표가 보다 크면
                잔고 조회를 해서 보유중인 원화를 얻어오고
                호가창을 조회해서 최우선 매도 호가를 조회함
                원화 잔고를 최우선 매도가로 나눠서 구매가능한 수량 계산하고
                시장가 주문으로 코인 매수
            매도 시도
                다음날 시초에 전량 매도하는데
            '''
            target_price = self.get_range()

            try:
                now = datetime.datetime.now()
                print(now, ":::", update_time)
                if update_time < now < update_time + datetime.timedelta(seconds=10):
                    # 업데이트 할 시간이되면
                    now = datetime.datetime.now()
                    update_time =  datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(hours=1)

                    print("매도 시도")
                    unit = self.get_current_target_balance()
                    result = self.ask()
                    print(result)

                current_price = self.get_current_price()
                print(f"현재가격 {current_price} : 타겟가격 {target_price}")

                if current_price > target_price:
                    print("매수 시도")
                    current_krw_balance = super().getAllAccount()[0]['balance']
                    current_krw_balance = 50000.0
                    orderbook = super().get_orderbooks()
                    sell_price = orderbook[0]['orderbook_units'][0]['ask_price']
                    units = float(current_krw_balance) / float(sell_price)
                    print(units * sell_price)
                    result = self.bid(
                        units=units,
                        sell_price=sell_price
                    )
                    print(result)
                time.sleep(1)
                

            except Exception as e:
                return ({"error" : e})
'''
strategy = Strategy(
    UpbitDTO(
        access_key='agI3Xs74VX8pMPzxCLLdOgWGr5TrFtf7VT5iiFpt',
        secret_key='AxPoPotHZfmxkxyIwjFU1zJREcE1PchSXCDMvcCM',
        server_url="https://api.upbit.com/v1/",
        market="KRW-ADA",
        days_number=2
        )
)
strategy.rotate()
'''
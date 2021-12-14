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
        result = super().get_ticker_info()
        print(result)
        return result

    def rotate(self):
        '''
            래리 윌리엄스 전략 구현
        '''
       
        now = datetime.datetime.now()
        update_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(hours=1)
        
        while True:
            range = super().get_range()
            last_price = super().get_ticker_info()['data'][0]['last']
            try:
                print(f"타겟가격: {range} VS 현재가격: {last_price}")
                now = datetime.datetime.now()
                if update_time < now < update_time + datetime.timedelta(seconds=10):
                # 업데이트 할 시간이되면
                    now = datetime.datetime.now()
                    update_time =  datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(hours=1)

                    print("매도 시도")

                if float(last_price) < range:
                    print("래리 타임")
                time.sleep(1)
            except Exception as e:
                print(e)
        '''
        
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

okex_st = OkexStrategy(
    OkexDTO(
    base_rest_url='https://www.okex.com',
    api_key='b4eaec2d-2655-4a40-a105-84ed2850b9b6',
    secret_key='1D8BEA9C0DA092DFC3C3632B544EBEC1',
    passphrase='mm0819',
    instId='ADA-USD-SWAP'
    )
)
okex_st.rotate()

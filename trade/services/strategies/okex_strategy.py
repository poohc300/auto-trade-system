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
        update_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(seconds=5)
        
        while True:
            range = super().get_range()
            last_price = super().get_ticker_info()['data'][0]['last'][0]
            current_balance=super().get_balance()['data'][0]['details'][0]['availBal']
            current_balance= float(current_balance)-1.0
            bid_target_sz = current_balance / float(last_price)

            best_ask_px=super().get_ticker_info()['data'][0]['askPx'][0]
            current_coin_balance=super().get_balance()['data'][0]['details'][1]['cashBal']
            ask_target_sz=float(current_coin_balance) / float(best_ask_px)
            try:
                print(f"현재시간: {now} | 매도시간: {update_time}")
                print(f"현재가격: {last_price} | 타겟가격: {range}")
                now = datetime.datetime.now()
                if update_time < now < update_time + datetime.timedelta(seconds=10):
                # 업데이트 할 시간이되면
                    now = datetime.datetime.now()
                    update_time =  datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(seconds=5)

                    print("매도 시도")
                    result= super().order(
                        side="sell",
                        px=last_price,
                        sz=ask_target_sz
                    )
                    print(result)
                if float(last_price) > range:
                    print("매수 시도")
                    result = super().order(
                        side="buy",
                        px=last_price,
                        sz=bid_target_sz
                    )
                    print(result)
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
'''
okex_st = OkexStrategy(
    OkexDTO(
    base_rest_url='https://www.okex.com',
    api_key='',
    secret_key='',
    passphrase='',
    instId=''
    )
)
okex_st.rotate()
'''
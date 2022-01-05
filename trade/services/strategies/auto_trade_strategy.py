from ..api.upbit_service import UpbitService
from ..api.upbit_dto import UpbitDTO
import json
import time
import os
import datetime

class AutotradeStrategy(UpbitService):

    def __init__(self, data: UpbitDTO, **kwargs):
        super().__init__(data, **kwargs)

    def filter_market_status(self, **kwargs):
        '''
            코인 종목 필터링

            상위 20개 코인만 선택
        '''
        coin = ""
        volume = ""
        # 마켓 코드 조회
        markets = self.get_all_market()
        # 마켓당 누적 거래량 비교

        filtered_markets = []
        
        kwargs['days_number'] = 1
        
        for market in markets:
            # 일봉 캔들 가져오기
            kwargs['market'] = market['market']
            if market['market'].startswith('KRW'):
                
                market_day_candle = self.get_days_candle(**kwargs)[0]
                acc_trade_volume = float(market_day_candle['candle_acc_trade_volume'])
                data = {
                    'coin' : market['market'],
                    'volume' : acc_trade_volume
                }

                filtered_markets.append(data)
            
            time.sleep(0.1)

        filtered_markets = sorted(filtered_markets, key=lambda x:x['volume'], reverse=True)
        filtered_markets = filtered_markets[0:19]
        return filtered_markets

    
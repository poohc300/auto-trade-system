from ..api.upbit_service import UpbitService
from ..api.upbit_dto import UpbitDTO
import json
import time
import os
import datetime
import asyncio
import pymysql

import uuid

class AutotradeStrategy(UpbitService):

    def __init__(self, data: UpbitDTO, **kwargs):
        super().__init__(data, **kwargs)
    
    def conn(self, sql, data):
        conn = pymysql.connect(
            host='127.0.0.1',
            database='auto-trade',
            user='root',
            password='Gmc@1234!',
            port=3306
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if data is None:
            cursor.execute(sql)
            result = cursor.fetchall()
        else:
            cursor.executemany(sql, data)
            result = "200"
        conn.commit()
        conn.close()

        return result

    def conn_where(self, sql, data):
        conn = pymysql.connect(
            host='127.0.0.1',
            database='auto-trade',
            user='root',
            password='Gmc@1234!',
            port=3306
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

      
        cursor.execute(sql, data)
        result = cursor.fetchall()
       
        conn.commit()
        conn.close()

        return result

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
        start = time.time()
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

           
            time.sleep(0.01)

        filtered_markets = sorted(filtered_markets, key=lambda x:x['volume'], reverse=True)
        filtered_markets = filtered_markets[0:19]
        end = time.time()
        print(f"상위 20개 필터링 걸린시간: {end-start}")
        insert_sql = "INSERT INTO bot_filteredmarket (coin, volume) VALUES (%(coin)s, %(volume)s)"
        reset_sql = "DELETE FROM bot_filteredmarket"
        
        reset = self.conn(
            sql=reset_sql,
            data=filtered_markets
        )
        result = self.conn(
            sql=insert_sql,
            data=filtered_markets
        )
            

        return "200"

    def get_moving_average_line(self, **kwargs):
        '''
            코인의 이동 평균선 찾는 로직

            상위 20개의 코인 목록에서
            최근 5분간의 분봉 캔들을 가져와서 마켓명, 현재가격(종가), 캔들기준시각
            을 저장함
            이때 5분 분봉의 가격 평균이 이동 평균선
        '''
       

        
        get_coin_list_sql = "SELECT * FROM bot_filteredmarket"
        query = self.conn(
            sql=get_coin_list_sql,
            data=None
        )
        coin_list = query
        result = []

        start = time.time()
        
        kwargs['minutes'] = 5
        for coin in coin_list:
            kwargs['market'] = coin['coin']
            candles = self.get_minutes_candle(**kwargs)[0]
            data = {
                'market' : coin['coin'],
                'trade_price' : candles['trade_price'],
                'candle_date_time' : candles['candle_date_time_kst'],
                'candle_acc_trade_volume' : candles['candle_acc_trade_volume']
            }

            result.append(data)
            time.sleep(0.1)
        end = time.time()
        print(f"이동평균선 구하는데 걸린시간: {end-start}")
        return result
    

    def get_coin_ticker(self, filtered_coins, **kwargs):
        '''
            코인별 ticker 구하는 로직
        '''
        coin_list = filtered_coins
        data = []
        for coin in coin_list:
            kwargs['market'] = coin['coin']
            ticker = self.get_ticker(**kwargs)[0]
            data.append(ticker)
            time.sleep(0.1)

        return data

    def check_bid_condition(self, moving_average_line, **kwargs):
        '''
            매수 타이밍 구하는 메서드

            전체 코인들 중에 이동 평균선보다 높은 코인중
            현재가 정보의 change_rate가 가장 높은 코인 정보 반환
        '''
        is_on_bid = False
        now = datetime.datetime.now()
        update_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(minutes=5)

        # 봇 정보
        get_bot_sql = "SELECT * FROM bot_bot where id = %s"
       
        temp_coin = None
        rising_price = 0.0

        get_coin_list_sql = "SELECT * FROM bot_filteredmarket"
        query = self.conn(
            sql=get_coin_list_sql,
            data=None
        )
        filtered_coins=query

        #while update_time > now:
        while True:


            now = datetime.datetime.now()
            #print(now, ":::", update_time)
            query = self.conn_where(
                sql=get_bot_sql,
                data=kwargs['bot_id']
            )
            bot_data = query[0]
            if bot_data['status'] == False:
                break

            time.sleep(0.1)
            if bot_data['is_bid'] == False:
                coin_tickers = self.get_coin_ticker(
                    filtered_coins,
                    **kwargs
                    )

                for i in range(0, 19):
                    
                    a = moving_average_line[i]
                    b = coin_tickers[i]
                    c = float(b['trade_price']) - float(a['trade_price'])
                    status = "매수타임" if a['trade_price'] < b['trade_price'] else "매수타임 아님"

                    print(f"{i+1}번: {a['market']} : {a['trade_price']} || {b['market']} : {b['trade_price']} || 상승가: {c}|| 상태: {status}")
                    if c > rising_price:

                        # 상승가가 같으면 거래량이 더 큰쪽으로 고르는 로직필요
                    
                        rising_price = c
                        temp_coin = b['market']
                        temp_price = float(b['trade_price'])

                if temp_coin is not None:
                    print(f"매수해야할 코인은 {temp_coin} 코인입니다")

                    target_price = temp_price
                    user_balance = float(bot_data['balance'])
                    user_balance = user_balance * 0.95

                    volume = 0.0
                    volume = user_balance / target_price
                    user_balance = user_balance - (target_price * volume)
                    
                    if user_balance < 0.0:
                        print("잔고가 없습니다")
                        break
                    query_string = {
                        "balance" : user_balance,
                        "market" : temp_coin,
                        "volume" : volume,
                        "is_bid" : True,
                        "bid_price" : target_price,
                        "created_at" : datetime.datetime.now(),
                        "id" : bot_data['id'],
                    }
                    print(query_string)
                    update_sql = "UPDATE bot_bot SET balance=%(balance)s, market=%(market)s, volume=%(volume)s, is_bid=%(is_bid)s, bid_price=%(bid_price)s, created_at=%(created_at)s WHERE id=%(id)s"
                    query = self.conn_where(
                        sql=update_sql,
                        data=query_string
                    )

                    # transaction history
                    ts = self.create_transaction_history(
                        query_string=query_string
                    )
                    
                    temp_coin = None
                    print("매수 성공") if query is not None else print("매수 실패")
                else:
                    print("매수할 코인이 없습니다")
            else:
                print("매도하기")
                # 매수한 코인 시세 받아오기
                coin_name = bot_data['market']
                print(f"매수한 코인 이름: {coin_name}")

                kwargs['market'] = coin_name
                current_price = float(self.get_ticker(**kwargs)[0]['trade_price'])
                print(current_price)

                bid_price = float(bot_data['bid_price'])
                plus = bid_price * (1.0 + float(bot_data['profit_percent']))
                minus = bid_price * (1.0 - float(bot_data['loss_percent']))
                # 1.15 0.7
                if current_price > plus or \
                    current_price < minus:
                    #현재 잔고 가져오기
                    query = self.conn_where(
                        sql=get_bot_sql,
                        data=kwargs['bot_id']
                    )
                    bot_data = query[0]

                    volume = float(bot_data['volume'])
                    current_user_balance = float(bot_data['balance'])
                    user_balance = current_price * volume
                    user_balance = (user_balance * 0.95) + current_user_balance
                   
                
                    query_string = {
                        "balance" : user_balance,
                        "market" : coin_name,
                        "volume" : volume,
                        "is_bid" : False,
                        "id" : bot_data['id'],
                        "bid_price" : bid_price,
                        "created_at" : datetime.datetime.now()
                    }

                    ts = self.create_transaction_history(
                        query_string=query_string
                    )

                    volume = 0.0
                    coin_name = ""
                    bid_price = 0.0
                    query_string = {
                        "balance" : user_balance,
                        "market" : coin_name,
                        "volume" : volume,
                        "is_bid" : False,
                        "id" : bot_data['id'],
                        "bid_price" : bid_price,
                        "created_at" : datetime.datetime.now()
                    }

                    update_sql = "UPDATE bot_bot SET balance=%(balance)s, market=%(market)s, volume=%(volume)s, is_bid=%(is_bid)s, bid_price=%(bid_price)s, created_at=%(created_at)s WHERE id=%(id)s"
                    query = self.conn_where(
                        sql=update_sql,
                        data=query_string
                    )
                    print("매도 완료")
                   
                    # 매도 transaction history

                # 현재 코인 시세와 매수했을 때 가격 비교해서 0.15퍼 오르면 익절
                else:
                    
                    print(f"매수금액 {bid_price} : 익절 예상 금액 {plus} : 손절 예상 금액 {minus}")
                    print("매도할 조건이 되지 않습니다")

   
            # 시세 받아온 뒤 계속 계산하기
            time.sleep(1)


        return "200"

    def create_transaction_history(self, query_string):

        sql = "INSERT INTO bot_transactionhistory (uuid, side, state, volume, price, created_at, bot_id, market) VALUES (%(uuid)s, %(side)s, %(state)s, %(volume)s, %(price)s, %(created_at)s, %(bot_id)s, %(market)s)"
        side = ""
        if query_string['is_bid'] == True:
            side = 'bid'
        else:
            side = 'ask'
        data = {
            "uuid" : uuid.uuid4(),
            "side" : side,
            "state" : "done",
            "volume" : query_string['volume'],
            "price" : query_string['bid_price'],
            "created_at" : datetime.datetime.now(),
            "bot_id" : query_string['id'],
            "market" : query_string['market']
        }
        print(data)
        conn = self.conn_where(
            sql,
            data
        )

        result = conn
        return result
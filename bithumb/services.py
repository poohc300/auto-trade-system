from pandas import DataFrame
from .models import BithumbAPI
import pandas as pd
import datetime
import math


class BithumbService:
    def __init__(self, conkey, seckey):
        self.api = BithumbAPI(conkey, seckey)

    def _convert_unit(self, unit):
        try:
            unit = math.floor(unit * 10000) / 10000
            return unit
        except:
            return 0

    
    def get_market_detail(self, order_currency, payment_currency="KRW"):
        """
        거래소 세부 정보 조회 (00시 기준)
        
        """
        result = None
        try:
            result = BithumbAPI.ticker(order_currency, payment_currency)
            
            return result
        except Exception:
            return result


    def get_current_price(self, order_currency, payment_currency="KRW"):
        """
        최종 체결 가격 조회
     
        """
        result = None
        try:
            result = BithumbAPI.ticker(order_currency, payment_currency)
           
            return result
        except Exception:
            return result

    
    def get_orderbook(self, order_currency, payment_currency, limit=5):
        """
        매수/매도 호가 조회
      
        """
        result = None
        _order_currency=order_currency,
        _payment_currency=payment_currency
        
        try:
            limit = min(limit, 30)
            result = self.api.orderbook(
                order_currency=_order_currency[0],
                payment_currency=_payment_currency,
                limit=limit
                )
            return result
        except Exception:
            return result


    def get_transaction_history(self, order_currency, payment_currency="KRW", limit=20):
        result = None
        try:
            limit = min(limit, 100)
            result = BithumbAPI.transaction_history(order_currency, payment_currency, limit)
            
            return result
        except Exception as e:
            print(e)
            return None


    def get_trading_fee(self, order_currency, payment_currency="KRW"):
        """
        거래 수수료 조회
      
        """
        result = None
        try:
            result = self.api.account(order_currency=order_currency,
                                    payment_currency=payment_currency)
            return result
        except Exception:
            return result

    def get_balance(self, currency):
        """
        거래소 회원의 잔고 조회
        
        """
        result = None
        try:
            result = self.api.balance(currency=currency)

            return result
        except Exception:
            return result

    def buy_limit_order(self, order_currency, price, unit,
                        payment_currency="KRW"):
        """
        매수 주문
        
        """
        result = None
        unit = float(unit)
        price = float(price)
        try:
            
            unit = self._convert_unit(unit)
            print(unit)

            price = price if payment_currency == "KRW" else f"{price:.8f}"
            result = self.api.place(type="bid", price=price, units=unit,
                                  order_currency=order_currency,
                                  payment_currency=payment_currency)
            return result
        except Exception:
            return result

    def sell_limit_order(self, order_currency, price, unit,
                         payment_currency="KRW"):
        """
        매도 주문
     
        """
        result = None
        unit = float(unit)
        price = float(price)

        try:
            unit = self._convert_unit(unit)
            price = price if payment_currency == "KRW" else f"{price:.8f}"
            result = self.api.place(type="ask", price=price, units=unit,
                                  order_currency=order_currency,
                                  payment_currency=payment_currency)
            return result
        except Exception:
            return result

    def get_outstanding_order(self, order_desc):
        """
        거래 미체결 수량 조회

        """
        result = None
        try:
            result = self.api.orders(type=order_desc['type'],
                                   order_currency=order_desc['order_currency'],
                                   order_id=order_desc['order_id'],
                                   payment_currency=order_desc['payment_currenct'])
            if result['status'] == '5600':
                return None
            # HACK : 빗썸이 데이터를 리스트에 넣어줌
            return result
        except Exception:
            return result

    def get_order_completed(self, order_desc):
        """
        거래 완료 정보 조회
      
        """
        result = None
        try:
            result = self.api.order_detail(type=order_desc['type'],
                                         order_currency=order_desc['order_currency'],
                                         order_id=order_desc['order_id'],
                                         payment_currency=order_desc['payment_currency'])
            if result['status'] == '5600':
                return None
            # HACK : 빗썸이 데이터를 리스트에 넣어줌
            return result
        except Exception:
            return result

    def cancel_order(self, order_desc):
        """
        매수/매도 주문 취소
       
        """
        result = None
        try:
            result = self.api.cancel(type=order_desc['type'],
                                   order_currency=order_desc['order_currency'],
                                   order_id=order_desc['order_id'],
                                   payment_currency=order_desc['payment_currency'])
            return result
        except Exception:
            return result

    def buy_market_order(self, order_currency, unit, payment_currency="KRW"):
        """
        시장가 매수
       
        """
        result = None
        unit = float(unit)
        try:
            unit = self._convert_unit(unit)
            result = self.api.market_buy(order_currency=order_currency,
                                       payment_currency=payment_currency,
                                       units=unit)
            return result
        except Exception:
            return result

    def sell_market_order(self, order_currency, unit, payment_currency="KRW"):
        """
        시장가 매도
   
        """
        result = None
        unit = float(unit)
        try:
            unit = self._convert_unit(unit)
            result = self.api.market_sell(order_currency=order_currency,
                                        payment_currency=payment_currency,
                                        units=unit)
            return result
        except Exception:
            return result

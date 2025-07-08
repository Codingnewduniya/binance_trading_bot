from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
from config import API_KEY, API_SECRET, TESTNET
from utils import setup_logger

class BasicBot:
    def __init__(self):
        setup_logger()
        self.client = Client(API_KEY, API_SECRET)
        if TESTNET:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price required for LIMIT order.")
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='LIMIT',
                    quantity=quantity,
                    price=price,
                    timeInForce='GTC'
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"Order successful: {order}")
            print("Order placed successfully!")
            print(order)
        except BinanceAPIException as e:
            logging.error(f"Binance API error: {e}")
            print(f"API Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"Unexpected Error: {e}")

import logging
import argparse
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import sys

# Configure logging
logging.basicConfig(
    filename='binance_futures_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.client.FUTURES_WEBSOCKET_URL = 'wss://stream.binancefuture.com/ws'
        logging.info('Initialized BasicBot with testnet=%s', testnet)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            params = {
                'symbol': symbol,
                'side': SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                'type': order_type,
                'quantity': quantity
            }
            if order_type == ORDER_TYPE_LIMIT:
                if price is None:
                    raise ValueError('Limit order requires a price.')
                params['price'] = price
                params['timeInForce'] = TIME_IN_FORCE_GTC
            elif order_type == ORDER_TYPE_STOP_MARKET:
                if stop_price is None:
                    raise ValueError('Stop-Market order requires a stop price.')
                params['stopPrice'] = stop_price
            logging.info('Placing order: %s', params)
            order = self.client.futures_create_order(**params)
            logging.info('Order response: %s', order)
            return order
        except BinanceAPIException as e:
            logging.error('Binance API Exception: %s', e)
            print(f'API Error: {e}')
        except Exception as e:
            logging.error('General Exception: %s', e)
            print(f'Error: {e}')
        return None

def parse_args():
    parser = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot')
    parser.add_argument('--api_key', help='Binance API Key')
    parser.add_argument('--api_secret', help='Binance API Secret')
    parser.add_argument('--symbol', help='Trading pair symbol, e.g., BTCUSDT')
    parser.add_argument('--side', choices=['buy', 'sell'], help='Order side')
    parser.add_argument('--type', choices=['MARKET', 'LIMIT', 'STOP_MARKET'], help='Order type')
    parser.add_argument('--quantity', type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Order price (required for LIMIT orders)')
    parser.add_argument('--stop_price', type=float, help='Stop price (required for STOP_MARKET orders)')
    args = parser.parse_args()
    # If no args provided, return None to trigger UI
    if len(sys.argv) == 1:
        return None
    return args

def menu_input():
    print('--- Binance Futures Testnet Trading Bot ---')
    api_key = input('Enter API Key: ')
    api_secret = input('Enter API Secret: ')
    symbol = input('Enter trading pair symbol (e.g., BTCUSDT): ').upper()
    side = input('Order side (buy/sell): ').lower()
    order_type = input('Order type (MARKET, LIMIT, STOP_MARKET): ').upper()
    quantity = float(input('Order quantity: '))
    price = None
    stop_price = None
    if order_type == 'LIMIT':
        price = float(input('Order price: '))
    if order_type == 'STOP_MARKET':
        stop_price = float(input('Stop price: '))
    return argparse.Namespace(
        api_key=api_key,
        api_secret=api_secret,
        symbol=symbol,
        side=side,
        type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price
    )

def main():
    args = parse_args()
    if args is None:
        args = menu_input()
    bot = BasicBot(args.api_key, args.api_secret, testnet=True)
    order = bot.place_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=getattr(args, 'stop_price', None)
    )
    if order:
        print('Order placed successfully:')
        print(order)
    else:
        print('Order failed. Check logs for details.')

if __name__ == '__main__':
    main() 
import argparse
from bot import BasicBot

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    parser.add_argument('--symbol', required=True, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'])
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'])
    parser.add_argument('--quantity', required=True, type=float)
    parser.add_argument('--price', type=float, help='Price required for LIMIT orders')

    args = parser.parse_args()

    bot = BasicBot()
    bot.place_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price
    )

if __name__ == '__main__':
    main()

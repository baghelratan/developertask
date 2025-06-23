# Binance Futures Testnet Trading Bot

This bot allows you to place market, limit, and stop-market orders on the Binance USDT-M Futures Testnet using the official Binance API via the `python-binance` library.

## Features
- Place market, limit, and stop-market orders (buy/sell)
- Command-line interface (CLI) for input, or interactive menu if no arguments are given
- Logging of all API requests, responses, and errors
- Error handling and input validation
- Uses Binance Futures Testnet (no real funds required)

## Setup

### 1. Register for a Binance Testnet Account
- Go to [Binance Futures Testnet](https://testnet.binancefuture.com/)
- Register and log in
- Generate API Key and Secret from the API Management section

### 2. Clone the Repository
```
git clone <repo-url>
cd <repo-directory>
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

## Usage

### Command-Line Arguments
Run the bot from the command line:

```
python binance_futures_bot.py --api_key <YOUR_API_KEY> --api_secret <YOUR_API_SECRET> --symbol BTCUSDT --side buy --type MARKET --quantity 0.001
```

For a limit order (requires price):
```
python binance_futures_bot.py --api_key <YOUR_API_KEY> --api_secret <YOUR_API_SECRET> --symbol BTCUSDT --side sell --type LIMIT --quantity 0.001 --price 70000
```

For a stop-market order (requires stop_price):
```
python binance_futures_bot.py --api_key <YOUR_API_KEY> --api_secret <YOUR_API_SECRET> --symbol BTCUSDT --side sell --type STOP_MARKET --quantity 0.001 --stop_price 65000
```

### Interactive Menu
If you run the script without any arguments, an interactive menu will prompt you for all required order details.

### Arguments
- `--api_key`: Your Binance Testnet API key
- `--api_secret`: Your Binance Testnet API secret
- `--symbol`: Trading pair symbol (e.g., BTCUSDT)
- `--side`: Order side (`buy` or `sell`)
- `--type`: Order type (`MARKET`, `LIMIT`, or `STOP_MARKET`)
- `--quantity`: Order quantity
- `--price`: Order price (required for LIMIT orders)
- `--stop_price`: Stop price (required for STOP_MARKET orders)

## Logs
- All API requests, responses, and errors are logged to `binance_futures_bot.log`

## Notes
- This bot is for educational and testing purposes only. It uses the Binance Futures Testnet and does not trade real funds.
- For advanced order types or UI enhancements, extend the `BasicBot` class as needed. 
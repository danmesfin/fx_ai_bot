import MetaTrader5 as mt5
import requests
import pandas as pd
import openai
import schedule
import time
import logging
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MT5_LOGIN = int(os.getenv('MT5_LOGIN'))
MT5_PASSWORD = os.getenv('MT5_PASSWORD')
MT5_SERVER = os.getenv('MT5_SERVER')

# Configure logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Connect to MT5
def connect_mt5():
    if not mt5.initialize():
        logging.error("initialize() failed, error code =", mt5.last_error())
        sys.exit()

    authorized = mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    if not authorized:
        logging.error("Failed to connect to MT5, error code:", mt5.last_error())
        mt5.shutdown()
        sys.exit()
    else:
        logging.info("Connected to MetaTrader5")

connect_mt5()

# Fetch live data
def fetch_live_data(symbol='GOLDUSD', interval='1min'):
    url = (
        f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}'
        f'&interval={interval}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact'
    )
    response = requests.get(url)
    data = response.json()
    
    key = f'Time Series ({interval})'
    if key in data:
        df = pd.DataFrame.from_dict(data[key], orient='index')
        df = df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        })
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df
    else:
        logging.error(f"Error fetching data: {data}")
        return None

def fetch_data_multiple_timeframes(symbol):
    timeframes = ['1min', '5min', '60min']
    data = {}
    for tf in timeframes:
        df = fetch_live_data(symbol, interval=tf)
        if df is not None:
            data[tf] = df
    return data

# Get trade recommendation
def get_trade_recommendation(data):
    data_summary = ""
    for tf, df in data.items():
        latest = df.iloc[-1]
        data_summary += f"Time Frame: {tf}\n"
        data_summary += f"Open: {latest['open']}, High: {latest['high']}, Low: {latest['low']}, Close: {latest['close']}, Volume: {latest['volume']}\n\n"

    prompt = f"""
    Analyze the following gold/USD trading data and provide a trade recommendation (BUY, SELL, HOLD) with a brief explanation.

    {data_summary}

    Recommendation:
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        recommendation = response.choices[0].text.strip()
        return recommendation
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "HOLD"

# Place trade
def place_trade(action, symbol, volume, order_type=mt5.ORDER_TYPE_BUY):
    price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": 20,
        "magic": 234000,
        "comment": "AI Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Order failed: {action} {symbol} {volume}, retcode={result.retcode}")
    else:
        logging.info(f"Order executed: {action} {symbol} {volume} @ {result.price}")

# Execute trade based on recommendation
def execute_trade(recommendation, symbol='GOLDUSD', volume=0.1):
    if "BUY" in recommendation.upper():
        place_trade("BUY", symbol, volume, mt5.ORDER_TYPE_BUY)
    elif "SELL" in recommendation.upper():
        place_trade("SELL", symbol, volume, mt5.ORDER_TYPE_SELL)
    else:
        logging.info("No trade action taken (HOLD).")

# Trading modes
MODE_ADVISORY = 'advisory'
MODE_AUTOMATED = 'automated'

current_mode = MODE_ADVISORY  # Change as needed

# Scheduled job
def job():
    try:
        live_data = fetch_data_multiple_timeframes('GOLDUSD')
        if live_data:
            recommendation = get_trade_recommendation(live_data)
            logging.info(f"Trade Recommendation: {recommendation}")

            if current_mode == MODE_AUTOMATED:
                execute_trade(recommendation)
            elif current_mode == MODE_ADVISORY:
                # Example: Print to console or send a notification
                print(f"Advisory Mode: {recommendation}")
    except Exception as e:
        logging.error(f"Error in job execution: {e}")

# Schedule the job every minute
schedule.every(1).minutes.do(job)

print("Trading bot started. Press Ctrl+C to stop.")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Trading bot stopped.")
    mt5.shutdown()

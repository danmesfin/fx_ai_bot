# mt5_data_fetcher.py

import MetaTrader5 as mt5
from config import MT5_ACCOUNT, TIME_FRAMES
from logger import get_logger

logger = get_logger("MT5DataFetcher")

def connect_to_mt5():
    if not mt5.initialize():
        logger.error("Failed to initialize MT5")
        return False
    authorized = mt5.login(MT5_ACCOUNT["login"], password=MT5_ACCOUNT["password"], server=MT5_ACCOUNT["server"])
    if not authorized:
        logger.error("Failed to login to MT5")
        return False
    return True

def fetch_data(symbol, timeframe, bars=100):
    if not mt5.symbol_select(symbol, True):
        logger.error(f"Failed to select symbol {symbol}")
        return None
    timeframe_mapping = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "H1": mt5.TIMEFRAME_H1,
    }
    timeframe = timeframe_mapping.get(timeframe, mt5.TIMEFRAME_H1)
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    return rates

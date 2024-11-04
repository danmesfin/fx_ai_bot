# mt5_data_fetcher.py

import MetaTrader5 as mt5
from config import MT5_ACCOUNT, TIME_FRAMES
from logger import get_logger
from datetime import datetime, timedelta

logger = get_logger("MT5DataFetcher")

def connect_to_mt5():
    if not mt5.initialize():
        logger.error("Failed to initialize MT5")
        return False
        
    # Add debug logging to verify credentials
    logger.info(f"Attempting to connect to server: {MT5_ACCOUNT['server']}")
    logger.info(f"Using login: {MT5_ACCOUNT['login']}")
    
    authorized = mt5.login(
        login=int(MT5_ACCOUNT["login"]),  # Convert login to integer
        password=MT5_ACCOUNT["password"],
        server=MT5_ACCOUNT["server"]
    )
    
    if authorized:
        logger.info("Successfully connected to MT5")
        return True
    else:
        error = mt5.last_error()
        logger.error(f"Failed to login to MT5. Error: {error}")
        return False


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

def get_account_info():
    account_info = mt5.account_info()
    return {
        "login": account_info.login,
        "balance": account_info.balance,
        "profit": account_info.profit,
        "margin": account_info.margin,
        "margin_free": account_info.margin_free,
        "margin_level": account_info.margin_level,
        "server": MT5_ACCOUNT["server"]
    }

def get_open_trades():
    positions = mt5.positions_get()
    return [
        {
            "ticket": position.ticket,
            "symbol": position.symbol,
            "type": "BUY" if position.type == 0 else "SELL",
            "volume": position.volume,
            "price_open": position.price_open,
            "price_current": position.price_current,
            "profit": position.profit
        }
        for position in positions
    ]

def get_trade_history():
    from_date = datetime.now() - timedelta(days=30)
    history = mt5.history_deals_get(from_date)
    return [
        {
            "ticket": deal.ticket,
            "symbol": deal.symbol,
            "type": "BUY" if deal.type == 0 else "SELL",
            "volume": deal.volume,
            "price": deal.price,
            "profit": deal.profit,
            "time": deal.time
        }
        for deal in history
    ]

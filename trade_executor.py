# trade_executor.py

import MetaTrader5 as mt5
from logger import get_logger

logger = get_logger("TradeExecutor")

def place_trade(symbol, action, lot=0.1):
    order_type = mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": mt5.symbol_info_tick(symbol).ask if action == "BUY" else mt5.symbol_info_tick(symbol).bid,
        "deviation": 10,
        "magic": 123456,
        "comment": "TradeBot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        logger.info(f"Trade executed: {action} {symbol}")
        return "Trade Executed"
    else:
        logger.error(f"Trade failed with error code: {result.retcode}")
        return "Trade Failed"

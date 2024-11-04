# trade_executor.py

import MetaTrader5 as mt5
from logger import get_logger

logger = get_logger("TradeExecutor")

def place_trade(symbol: str, action: str, entry_price: float, take_profit: float, stop_loss: float):
    if not mt5.initialize():
        return "Failed to initialize MT5"
        
    lot_size = 0.01
    
    # Get current market price
    symbol_info = mt5.symbol_info(symbol)
    if action == "SELL":
        price = symbol_info.bid
    else:
        price = symbol_info.ask
        
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,  # Using current market price
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 20,
        "magic": 234000,
        "comment": "python trading bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return f"Trade execution result: {result.comment}"
    
    return f"Trade executed successfully: Ticket #{result.order}"

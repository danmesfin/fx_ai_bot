# main.py
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Query
from typing import List
from mt5_data_fetcher import connect_to_mt5, fetch_data, get_account_info, get_open_trades
from signal_processor import generate_signal
from ai_advisor import get_ai_advice
from trade_executor import place_trade

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to MT5
    try:
        if not connect_to_mt5():
            print("Failed to connect to MetaTrader 5 on startup")
        else:
            print("Successfully connected to MetaTrader 5")
        yield
    finally:
        # Shutdown: cleanup operations
        # mt5.shutdown()  # Uncomment if you need to clean up MT5 connection
        print("App shutdown complete")

app = FastAPI(lifespan=lifespan)

@app.get("/trade-recommendation")
async def trade_recommendation(
    symbol: str,
    timeframes: List[str] = Query(default=["M1", "M5", "H1"])
):
    data = {tf: fetch_data(symbol, tf) for tf in timeframes}
    
    # Get current price from latest M1 candle
    current_price = data["M1"][-1][4]  # Close price of last candle
    
    signal = {
        "type": generate_signal(data["M1"]),
        "current_price": current_price
    }
    
    ai_advice = get_ai_advice(signal)
    
    return {
        "symbol": symbol,
        "signal": signal["type"],
        "current_price": current_price,
        "ai_advice": ai_advice,
        "timeframes_analyzed": timeframes
    }

@app.post("/execute-trade")
async def execute_trade(symbol: str, action: str, auto: bool = False):
    if auto:
        result = place_trade(symbol, action)
    else:
        result = f"Manual trade suggestion: {action} on {symbol}"
    return {"status": result}

@app.get("/auto-trade")
async def auto_trade(symbol: str = "XAUUSD"):
    # Get market data and signals
    data = {tf: fetch_data(symbol, tf) for tf in ["M1", "M5", "H1"]}
    current_price = data["M1"][-1][4]
    
    signal = {
        "type": generate_signal(data["M1"]),
        "current_price": current_price
    }
    
    ai_advice = get_ai_advice(signal)
    
    # Parse AI advice to get entry, tp, sl
    lines = ai_advice.split('\n')
    entry = float(lines[0].split('$')[1])
    tp = float(lines[1].split('$')[1])
    sl = float(lines[2].split('$')[1])
    
    # Execute trade automatically
    trade_result = place_trade(
        symbol=symbol,
        action=signal["type"],
        entry_price=entry,
        take_profit=tp,
        stop_loss=sl
    )
    
    return {
        "symbol": symbol,
        "signal": signal["type"],
        "current_price": current_price,
        "ai_advice": ai_advice,
        "trade_status": trade_result,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/account-info")
async def get_account_info():
    return get_account_info()

@app.get("/open-trades")
async def get_open_trades():
    return get_open_trades()

@app.get("/trade-history")
async def get_trade_history():
    return get_trade_history()

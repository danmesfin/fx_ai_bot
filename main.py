# main.py

from fastapi import FastAPI
from mt5_data_fetcher import connect_to_mt5, fetch_data
from signal_processor import generate_signal
from ai_advisor import get_ai_advice
from trade_executor import place_trade

app = FastAPI()

# Lifespan event for startup and shutdown
@app.lifespan
async def app_lifespan(app: FastAPI):
    # Startup event
    if not connect_to_mt5():
        print("Failed to connect to MetaTrader 5 on startup")
    yield
    # Shutdown event (if any teardown logic is needed)
    # e.g., mt5.shutdown() if you need to clean up MT5 connection
    print("App shutdown complete")

@app.get("/trade-recommendation")
async def trade_recommendation(symbol: str, timeframes: list = ["M1", "M5", "H1"]):
    data = {tf: fetch_data(symbol, tf) for tf in timeframes}
    signal = generate_signal(data["M1"])  # Simplified to use one timeframe
    ai_advice = get_ai_advice(signal)
    return {"signal": signal, "ai_advice": ai_advice}

@app.post("/execute-trade")
async def execute_trade(symbol: str, action: str, auto: bool = False):
    if auto:
        result = place_trade(symbol, action)
    else:
        result = f"Manual trade suggestion: {action} on {symbol}"
    return {"status": result}

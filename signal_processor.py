# signal_processor.py

import numpy as np
from logger import get_logger

logger = get_logger("SignalProcessor")

def moving_average(data, period):
    return np.convolve(data, np.ones(period) / period, mode="valid")

def generate_signal(data):
    close_prices = [bar['close'] for bar in data]
    short_ma = moving_average(close_prices, 5)
    long_ma = moving_average(close_prices, 20)
    signal = "BUY" if short_ma[-1] > long_ma[-1] else "SELL"
    logger.info(f"Generated signal: {signal}")
    return signal

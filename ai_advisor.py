# ai_advisor.py

from openai import OpenAI
from config import AI_API_KEY
from logger import get_logger

logger = get_logger("AIAdvisor")

client = OpenAI(api_key=AI_API_KEY)

def get_ai_advice(signal):
    # Get current price from the last candle
    current_price = signal['current_price']  # We'll need to pass this from main.py
    
    prompt = f"""
    Current XAUUSD (Gold) price is ${current_price:.2f}
    Based on the trading signal {signal}, provide:
    
    Format your response exactly like this example:
    ACTION: BUY at $2741.50
    TP: $2745.00
    SL: $2738.00
    
    Use real market prices within 20-30 pips range for Gold.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a precise trading advisor. Use exact market prices for Gold (XAUUSD)."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.3
    )
    
    ai_advice = response.choices[0].message.content.strip()
    logger.info(f"AI trading signal generated: {ai_advice}")
    return ai_advice

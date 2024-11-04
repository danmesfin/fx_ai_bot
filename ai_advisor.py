# ai_advisor.py

import openai
from config import AI_API_KEY
from logger import get_logger

logger = get_logger("AIAdvisor")

openai.api_key = AI_API_KEY

def get_ai_advice(signal):
    prompt = f"The current trading signal is {signal}. What is your recommendation?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    ai_advice = response.choices[0].text.strip()
    logger.info(f"AI advice: {ai_advice}")
    return ai_advice

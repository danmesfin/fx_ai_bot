from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MT5 account configuration
MT5_ACCOUNT = {
    "login": os.getenv("MT5_LOGIN"),
    "password": os.getenv("MT5_PASSWORD"),
    "server": os.getenv("MT5_SERVER")
}

# API key for AI services
AI_API_KEY = os.getenv("AI_API_KEY")

# Time frames from env (split string into list)
TIME_FRAMES = os.getenv("TIME_FRAMES").split(",")

# MT5 Trading Bot

A Python-based trading bot that interfaces with MetaTrader 5 (MT5) to fetch market data and execute trades automatically using FastAPI.

## Features

- Real-time connection to MetaTrader 5 platform
- Automated data fetching for multiple timeframes (M1, M5, H1)
- Account monitoring and management
- Trade execution tracking
- Comprehensive logging system
- RESTful API endpoints for trade management

## API Endpoints

### Trade Management

- `GET /trade-recommendation`: Get trading recommendations for a symbol across multiple timeframes
- `POST /execute-trade`: Execute manual or automated trades
- `GET /auto-trade`: Run fully automated trading with AI-powered advice
- `GET /account-info`: Retrieve current account metrics
- `GET /open-trades`: List all active trading positions
- `GET /trade-history`: Get historical trade data

## Core Functionality

The bot provides the following key capabilities:

- **MT5 Connection Management**: Secure login and connection handling with MT5 servers
- **Market Data Fetching**: Retrieves historical and real-time price data for specified symbols
- **AI-Powered Trading**: Generates trading signals and AI advice for informed decisions
- **Account Information**: Monitors account metrics including balance, profit, margin levels
- **Position Tracking**: Tracks open trades and their current status
- **Trade History**: Maintains detailed records of past trades and their outcomes

## Configuration

The system requires proper MT5 account credentials and server settings in the config file:

- Login credentials
- Server details
- Supported time frames

## Usage

1. Ensure MetaTrader 5 is installed and running
2. Configure your MT5 account details
3. Start the FastAPI server
4. Access endpoints through your preferred HTTP client

## API Examples

```python
# Get trade recommendation
GET /trade-recommendation?symbol=XAUUSD&timeframes=M1,M5,H1

# Execute trade
POST /execute-trade
{
    "symbol": "XAUUSD",
    "action": "BUY",
    "auto": true
}

# Get account information
GET /account-info

```

## Requirements

- Python 3.x
- MetaTrader 5 platform
- FastAPI
- MetaTrader5 Python package

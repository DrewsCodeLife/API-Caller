import datetime
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import yfinance as yf

# Fetch historical data
def get_data(pair, num_days=10000, interval='1d'):
    # Define the end date as today
    end = datetime.datetime.today()

    # Define the start date based on the number of days and interval
    if interval in ['1m', '5m', '15m', '30m', '60m']:
        # For intraday data, you may need to restrict to fewer days
        start = end - datetime.timedelta(days=num_days)
    else:
        # For daily data or higher granularity, 10,000 days might be acceptable
        start = end - datetime.timedelta(days=num_days)
    
    symbol = str(pair)
    df = yf.download(symbol, start=start, end=end, interval=interval)
    return df

# Add TA (Technical Analysis) indicators
def get_indicators(df):
    try:
        # Simple Moving Average
        df['SMA'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()  # Using a 20-period SMA as default

        # RSI
        df['RSI'] = RSIIndicator(close=df['Close']).rsi()

        # MACD
        macd = MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()

        # Bollinger Bands
        bollinger = BollingerBands(close=df['Close'])
        df['bollinger_mavg'] = bollinger.bollinger_mavg()
        df['bollinger_hband'] = bollinger.bollinger_hband()
        df['bollinger_lband'] = bollinger.bollinger_lband()

        # Volume is already present in the original df from yfinance as 'Volume'

        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Save data to a CSV file
def save_to_csv(df, filename):
    try:
        df.to_csv(filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Fetch historical data for AAPL for the past 60 days at 5-minute intervals
    data = get_data('SPY', num_days=10000, interval='5m')
    
    # Add technical indicators to the data
    data_with_indicators = get_indicators(data)
    
    # Save data to a CSV file
    if data_with_indicators is not None:
        save_to_csv(data_with_indicators, 'spy2_with_indicators.csv')

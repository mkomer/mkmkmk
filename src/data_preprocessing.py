"""
Data preprocessing module for stock data.
Handles fetching, cleaning, and preparing stock data for model training.
"""

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import yfinance as yf


def fetch_stock_data(ticker, start_date=None, end_date=None, period='2y'):
    """
    Fetch historical stock data from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        period (str): Time period ('1y', '5y', etc.) if dates not specified
    
    Returns:
        pd.DataFrame: Stock data with OHLCV columns
    """
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date, 
                                period=period, progress=False)
        
        # Handle multi-level columns (common with yfinance)
        if isinstance(stock_data.columns, pd.MultiIndex):
            # Extract single ticker data by selecting first level
            stock_data.columns = stock_data.columns.get_level_values(0)
        
        # Remove any rows with NaN values in Close column
        stock_data = stock_data.dropna(subset=['Close'])
        if len(stock_data) == 0:
            print(f"Error: No valid data retrieved for {ticker}")
            return None
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def preprocess_data(data, lookback=60):
    """
    Preprocess stock data for LSTM model.
    
    Args:
        data (pd.DataFrame): Stock data with Close prices
        lookback (int): Number of previous timesteps to use as input
    
    Returns:
        tuple: (X, y, scaler) - Features, targets, and scaler object
    """
    # Extract closing prices
    prices = data['Close'].values.reshape(-1, 1)
    
    # Verify we have enough data
    if len(prices) < lookback + 1:
        raise ValueError(f"Insufficient data: {len(prices)} rows, need at least {lookback + 1}")
    
    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(prices)
    
    # Create sequences for LSTM
    X, y = [], []
    for i in range(len(scaled_data) - lookback):
        X.append(scaled_data[i:i + lookback])
        y.append(scaled_data[i + lookback])
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"Data shape after preprocessing: X={X.shape}, y={y.shape}")
    return X, y, scaler


def save_data(data, filepath):
    """Save stock data to CSV file."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    data.to_csv(filepath)
    print(f"Data saved to {filepath} ({len(data)} rows)")


def load_data(filepath):
    """Load stock data from CSV file."""
    data = pd.read_csv(filepath, index_col=0, parse_dates=True)
    return data

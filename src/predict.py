"""
Prediction module for generating stock price forecasts.
"""

import numpy as np
from tensorflow import keras


def predict_future_prices(model, last_sequence, scaler, num_predictions=30):
    """
    Predict future stock prices using trained LSTM model.
    
    Args:
        model (keras.Model): Trained LSTM model
        last_sequence (np.ndarray): Last sequence from training data (lookback window)
        scaler: MinMaxScaler object used for training
        num_predictions (int): Number of future days to predict
    
    Returns:
        np.ndarray: Predicted prices (unnormalized)
    """
    predictions = []
    current_sequence = last_sequence.copy()
    
    for _ in range(num_predictions):
        # Predict next value
        next_pred = model.predict(current_sequence.reshape(1, -1, 1), 
                                  verbose=0)
        predictions.append(next_pred[0, 0])
        
        # Update sequence for next prediction
        current_sequence = np.append(current_sequence[1:], next_pred)
    
    # Denormalize predictions
    predictions = np.array(predictions).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)
    
    return predictions.flatten()


def get_forecast_dates(last_date, num_predictions=30):
    """
    Generate future dates for predictions.
    
    Args:
        last_date: Last date from historical data
        num_predictions (int): Number of future dates to generate
    
    Returns:
        list: List of future dates
    """
    from datetime import datetime, timedelta
    
    if isinstance(last_date, str):
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
    
    future_dates = []
    current_date = last_date
    
    for _ in range(num_predictions):
        current_date += timedelta(days=1)
        # Skip weekends
        while current_date.weekday() > 4:
            current_date += timedelta(days=1)
        future_dates.append(current_date)
    
    return future_dates


def calculate_statistics(predictions, historical_prices):
    """
    Calculate prediction statistics.
    
    Args:
        predictions (np.ndarray): Predicted prices
        historical_prices (np.ndarray): Recent historical prices
    
    Returns:
        dict: Statistics including trend, volatility, etc.
    """
    stats = {
        'mean_prediction': np.mean(predictions),
        'min_prediction': np.min(predictions),
        'max_prediction': np.max(predictions),
        'std_prediction': np.std(predictions),
        'current_price': historical_prices[-1],
        'expected_change': predictions[-1] - historical_prices[-1],
        'change_percent': ((predictions[-1] - historical_prices[-1]) / 
                          historical_prices[-1] * 100)
    }
    return stats

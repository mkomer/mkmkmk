"""
LSTM model training module for stock price prediction.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import os


def build_lstm_model(input_shape, units=50, dropout=0.2):
    """
    Build LSTM neural network model.
    
    Args:
        input_shape (tuple): Shape of input data (lookback, num_features)
        units (int): Number of LSTM units
        dropout (float): Dropout rate
    
    Returns:
        keras.Model: Compiled LSTM model
    """
    model = Sequential([
        LSTM(units=units, return_sequences=True, input_shape=input_shape),
        Dropout(dropout),
        LSTM(units=units, return_sequences=True),
        Dropout(dropout),
        LSTM(units=units),
        Dropout(dropout),
        Dense(units=25),
        Dense(units=1)
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model


def train_model(X, y, epochs=50, batch_size=32, validation_split=0.2, 
                model_path='models/lstm_model.h5'):
    """
    Train LSTM model on stock data.
    
    Args:
        X (np.ndarray): Feature data
        y (np.ndarray): Target data
        epochs (int): Number of training epochs
        batch_size (int): Batch size for training
        validation_split (float): Fraction of data for validation
        model_path (str): Path to save trained model
    
    Returns:
        keras.Model: Trained model
    """
    # Create model
    model = build_lstm_model(input_shape=(X.shape[1], 1))
    
    # Train model
    history = model.fit(
        X, y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        verbose=1
    )
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    return model, history


def load_model(model_path='models/lstm_model.h5'):
    """Load trained model from file."""
    return keras.models.load_model(model_path)

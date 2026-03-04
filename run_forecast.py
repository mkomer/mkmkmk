"""
Main script to run the complete stock forecasting pipeline.
Fetches data, trains model, generates predictions, and exports PDF report.
"""

import sys
import os
import argparse
import numpy as np
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_preprocessing import fetch_stock_data, preprocess_data, save_data
from model_training import train_model, load_model
from predict import predict_future_prices, get_forecast_dates, calculate_statistics
from generate_pdf import generate_pdf_report


def main(ticker='AAPL', days_history=365, forecast_days=30, retrain=False, 
         output_pdf='stock_forecast.pdf'):
    """
    Run complete stock forecasting pipeline.
    
    Args:
        ticker (str): Stock ticker symbol
        days_history (int): Number of historical days to fetch
        forecast_days (int): Number of days to forecast
        retrain (bool): Whether to retrain model or use existing
        output_pdf (str): Output PDF filename
    """
    
    # Configuration
    lookback = 60  # Number of previous days for LSTM input
    epochs = 50
    batch_size = 32
    model_path = 'models/lstm_model.h5'
    data_path = f'data/{ticker}_historical.csv'
    
    print(f"Starting stock forecast for {ticker}")
    print(f"Parameters: History={days_history} days, Forecast={forecast_days} days")
    
    # Step 1: Fetch data
    print("\n[1/5] Fetching stock data...")
    stock_data = fetch_stock_data(ticker, period='1y')
    if stock_data is None:
        print(f"Error: Could not fetch data for {ticker}")
        return False
    
    # Save data
    os.makedirs('data', exist_ok=True)
    save_data(stock_data, data_path)
    
    # Step 2: Preprocess data
    print("[2/5] Preprocessing data...")
    try:
        X, y, scaler = preprocess_data(stock_data, lookback=lookback)
        print(f"Prepared {len(X)} training sequences")
    except ValueError as e:
        print(f"Error: {e}")
        return False
    
    # Step 3: Train or load model
    print("[3/5] Training model...")
    os.makedirs('models', exist_ok=True)
    
    if retrain or not os.path.exists(model_path):
        model, history = train_model(X, y, epochs=epochs, batch_size=batch_size,
                                    model_path=model_path)
        print("Model training completed")
    else:
        model = load_model(model_path)
        print("Loaded existing model")
    
    # Step 4: Generate predictions
    print("[4/5] Generating predictions...")
    last_sequence = X[-1]
    predictions = predict_future_prices(model, last_sequence, scaler, 
                                       num_predictions=forecast_days)
    
    forecast_dates = get_forecast_dates(stock_data.index[-1], num_predictions=forecast_days)
    historical_prices = stock_data['Close'].values[-90:].tolist()  # Last 90 days
    
    # Calculate statistics
    stats = calculate_statistics(predictions, stock_data['Close'].values[-30:])
    print(f"Forecast: Current={stats['current_price']:.2f}, "
          f"Expected in {forecast_days} days={stats['mean_prediction']:.2f}, "
          f"Change={stats['change_percent']:.2f}%")
    
    # Step 5: Generate PDF report
    print("[5/5] Generating PDF report...")
    generate_pdf_report(ticker, historical_prices, predictions, forecast_dates, 
                       stats, output_filename=output_pdf)
    
    print(f"\nForecast complete! PDF saved to {output_pdf}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI Stock Forecast to PDF')
    parser.add_argument('--ticker', default='AAPL', help='Stock ticker symbol')
    parser.add_argument('--days', type=int, default=365, help='Days of historical data')
    parser.add_argument('--forecast', type=int, default=30, help='Days to forecast')
    parser.add_argument('--retrain', action='store_true', help='Retrain the model')
    parser.add_argument('--output', default='stock_forecast.pdf', help='Output PDF filename')
    
    args = parser.parse_args()
    
    success = main(
        ticker=args.ticker,
        days_history=args.days,
        forecast_days=args.forecast,
        retrain=args.retrain,
        output_pdf=args.output
    )
    
    sys.exit(0 if success else 1)

"""
Flask web application for AI Stock Forecast to PDF.
Provides a web interface for stock price predictions and PDF report generation.
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.exceptions import BadRequest
import threading

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_preprocessing import fetch_stock_data, preprocess_data, save_data
from model_training import train_model, load_model
from predict import predict_future_prices, get_forecast_dates, calculate_statistics
from generate_pdf import generate_pdf_report

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['TEMP_FOLDER'] = tempfile.gettempdir()

# Store forecasts for download
forecasts = {}


def run_forecast_background(ticker, days_history, forecast_days, job_id):
    """Run forecast in background thread and store result."""
    try:
        lookback = 60
        epochs = 50
        batch_size = 32
        model_path = 'models/lstm_model.h5'
        data_path = f'data/{ticker}_historical.csv'
        
        # Fetch data
        stock_data = fetch_stock_data(ticker, period='2y')
        if stock_data is None:
            forecasts[job_id] = {'error': f'Could not fetch data for {ticker}'}
            return
        
        os.makedirs('data', exist_ok=True)
        save_data(stock_data, data_path)
        
        # Preprocess data
        try:
            X, y, scaler = preprocess_data(stock_data, lookback=lookback)
        except ValueError as e:
            forecasts[job_id] = {'error': str(e)}
            return
        
        # Train or load model
        os.makedirs('models', exist_ok=True)
        if not os.path.exists(model_path):
            model, history = train_model(X, y, epochs=epochs, batch_size=batch_size,
                                        model_path=model_path)
        else:
            model = load_model(model_path)
        
        # Generate predictions
        last_sequence = X[-1]
        predictions = predict_future_prices(model, last_sequence, scaler, 
                                           num_predictions=forecast_days)
        
        forecast_dates = get_forecast_dates(stock_data.index[-1], 
                                           num_predictions=forecast_days)
        historical_prices = stock_data['Close'].values[-90:].tolist()
        
        # Calculate statistics
        stats = calculate_statistics(predictions, stock_data['Close'].values[-30:])
        
        # Generate PDF
        pdf_path = os.path.join(app.config['TEMP_FOLDER'], f'{job_id}.pdf')
        generate_pdf_report(ticker, historical_prices, predictions, forecast_dates, 
                           stats, output_filename=pdf_path)
        
        # Store result
        forecasts[job_id] = {
            'ticker': ticker,
            'current_price': f"${stats['current_price']:.2f}",
            'forecast_price': f"${stats['mean_prediction']:.2f}",
            'change': f"{stats['change_percent']:.2f}%",
            'min_price': f"${stats['min_prediction']:.2f}",
            'max_price': f"${stats['max_prediction']:.2f}",
            'volatility': f"${stats['std_prediction']:.2f}",
            'pdf_path': pdf_path,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        forecasts[job_id] = {'error': str(e)}


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/forecast', methods=['POST'])
def create_forecast():
    """Create stock forecast."""
    try:
        data = request.json
        ticker = data.get('ticker', 'AAPL').upper().strip()
        forecast_days = int(data.get('forecast_days', 30))
        
        # Validate inputs
        if not ticker or len(ticker) > 5:
            return jsonify({'error': 'Invalid ticker symbol'}), 400
        
        if forecast_days < 5 or forecast_days > 365:
            return jsonify({'error': 'Forecast days must be between 5 and 365'}), 400
        
        job_id = f"{ticker}_{datetime.now().timestamp()}"
        
        # Run in background
        thread = threading.Thread(target=run_forecast_background, 
                                 args=(ticker, 365, forecast_days, job_id))
        thread.daemon = True
        thread.start()
        
        return jsonify({'job_id': job_id, 'status': 'processing'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/forecast/<job_id>', methods=['GET'])
def get_forecast(job_id):
    """Get forecast status and results."""
    if job_id not in forecasts:
        return jsonify({'status': 'processing'}), 202
    
    result = forecasts[job_id]
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result), 200


@app.route('/api/download/<job_id>', methods=['GET'])
def download_pdf(job_id):
    """Download generated PDF report."""
    if job_id not in forecasts:
        return jsonify({'error': 'Forecast not found'}), 404
    
    result = forecasts[job_id]
    if 'error' in result:
        return jsonify({'error': result['error']}), 400
    
    pdf_path = result['pdf_path']
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF file not found'}), 404
    
    return send_file(pdf_path, as_attachment=True, 
                     download_name=f"{result['ticker']}_forecast.pdf",
                     mimetype='application/pdf')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

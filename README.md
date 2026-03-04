# AI Prediction Embed Custom App Testing 
# Mike Komer - 03/2/26 -- AI Forecast and Print to PDF Stock Prediction Custom Application

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8+-orange.svg)](https://www.tensorflow.org/)

A machine learning application that predicts stock prices using advanced LSTM neural networks and generates professional PDF reports with forecasts, charts, and visualizations. Features both **CLI and web interface** with real-time forecasting.

## Features

🎯 **Core Capabilities:**
- **Stock Data Fetching**: Automatically retrieves 2 years of historical stock data from Yahoo Finance
- **Data Preprocessing**: Normalizes and prepares data for neural network training
- **LSTM Model**: 3-layer LSTM neural network with dropout for sequence prediction
- **Price Forecasting**: Generates predictions (5-365 days ahead)
- **Professional PDF Reports**: Complete with statistics, charts, and visualizations

🌐 **Web Interface:**
- Beautiful, responsive UI for portfolio/GitHub showcase
- Real-time stock price forecast generation
- **📥 Download PDF Button** for sharing reports
- Live statistics dashboard
- Mobile-friendly design

💻 **CLI Interface:**
- Command-line tool for batch processing
- Model retraining options
- Customizable parameters

## Project Structure

```
ai-stock-forecast-pdf/
├─ data/                       # Saved historical CSV files
├─ models/                     # Trained LSTM model files
├─ src/
│   ├─ data_preprocessing.py   # Data fetching and preprocessing
│   ├─ model_training.py       # LSTM model building and training
│   ├─ predict.py              # Prediction generation and statistics
│   └─ generate_pdf.py         # PDF report generation
├─ templates/
│   └─ index.html              # Web UI template
├─ static/
│   ├─ style.css               # UI styling
│   └─ script.js               # Frontend logic
├─ app.py                      # Flask web application
├─ run_forecast.py             # CLI entry point
├─ requirements.txt            # Python dependencies
└─ README.md                   # Documentation
```

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mkomer/AI-Stock-Forecast-to-PDF.git
   cd AI-Stock-Forecast-to-PDF
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🌐 Web Interface (Recommended for Portfolio)

Start the Flask web server:

```bash
python app.py
```

Then open your browser to **http://localhost:5000**

**Features:**
- Enter any stock ticker (AAPL, TSLA, GOOGL, etc.)
- Adjust forecast period (5-365 days)
- View results instantly
- **📥 Download PDF Report** with one click

### 💻 Command Line Interface

For quick forecasts from the terminal:

```bash
# AAPL with 30-day forecast
python run_forecast.py

# Tesla with 60-day forecast
python run_forecast.py --ticker TSLA --forecast 60

# Microsoft, retrain model, custom output file
python run_forecast.py --ticker MSFT --retrain --output msft_report.pdf
```

**CLI Arguments:**
- `--ticker` (default: AAPL) - Stock symbol
- `--days` (default: 365) - Historical data range
- `--forecast` (default: 30) - Forecast period (days)
- `--retrain` - Force model retraining
- `--output` (default: stock_forecast.pdf) - Output PDF filename

## Module Documentation

### `data_preprocessing.py`
Handles data fetching and preprocessing:
- `fetch_stock_data()`: Fetches historical data from Yahoo Finance
- `preprocess_data()`: Normalizes prices and creates LSTM sequences
- `save_data()` / `load_data()`: CSV file I/O operations

### `model_training.py`
Builds and trains the LSTM model:
- `build_lstm_model()`: Creates 3-layer LSTM architecture
- `train_model()`: Trains on historical data
- `load_model()`: Loads previously trained models

### `predict.py`
Generates forecasts and statistics:
- `predict_future_prices()`: Generates 30-day predictions
- `get_forecast_dates()`: Creates future date sequence
- `calculate_statistics()`: Computes forecast metrics

### `generate_pdf.py`
Creates PDF reports:
- `create_forecast_chart()`: Generates matplotlib visualization
- `generate_pdf_report()`: Creates comprehensive PDF with tables and charts

## Model Architecture

The LSTM model consists of:
- **Input**: 60-day window of normalized closing prices
- **Hidden Layers**: 3 LSTM layers (50 units each) with dropout (0.2)
- **Output**: Single-day price prediction
- **Loss Function**: Mean Squared Error
- **Optimizer**: Adam (learning rate 0.001)

## Output Files

After running the forecast:
- `stock_forecast.pdf`: Main PDF report (customizable name)
- `models/lstm_model.h5`: Trained LSTM model (saved on first run)
- `data/{TICKER}_historical.csv`: Historical stock data
- `forecast_chart.png`: Temporary chart image (embedded in PDF)

## Output Report Contents

The generated PDF includes:
1. **Header**: Stock ticker and report generation timestamp
2. **Summary Statistics**:
   - Current price
   - 30-day forecast price
   - Expected change ($)
   - Expected change (%)
   - Min/Max predicted prices
   - Price volatility
3. **Forecast Chart**: Visual comparison of historical vs. predicted prices

## Requirements

Key dependencies:
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `tensorflow/keras`: Deep learning framework
- `scikit-learn`: Preprocessing and utilities
- `yfinance`: Stock data fetching
- `matplotlib`: Chart generation
- `reportlab`: PDF generation

See `requirements.txt` for complete list with versions.

## Performance Considerations

- **Training Time**: ~2-5 minutes on CPU, <1 minute on GPU
- **Data Size**: Fetches 1 year of data (~250 trading days)
- **Model Size**: ~500KB (lstm_model.h5)
- **PDF Generation**: <10 seconds

## Deployment

### Local Development

```bash
python app.py
```
Access at `http://localhost:5000`

### Heroku Deployment

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Create `runtime.txt`:
```
python-3.9.16
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--timeout", "300", "--workers", "1", "app:app"]
```

Build and run:
```bash
docker build -t stock-forecast .
docker run -p 5000:5000 stock-forecast
```

### GitHub Pages + Backend

1. Host the Flask backend on Heroku or your server
2. Update API endpoint in `static/script.js`:
```javascript
fetch('https://your-backend.herokuapp.com/api/forecast', ...)
```

### Portfolio Integration

Embed the app in your portfolio:
```html
<iframe 
    src="https://your-deployed-app.com" 
    width="100%" 
    height="600px" 
    frameborder="0">
</iframe>
```

Or link directly:
```markdown
[🚀 Live Demo](https://your-deployed-app.com)
```

## Limitations

- Predictions based solely on historical price patterns
- Does not account for external events or market factors
- Performance may vary significantly during market disruptions
- Requires sufficient historical data for accurate training
- Not financial advice; use for research purposes only

## Future Enhancements

- Multi-stock portfolio analysis
- Alternative model architectures (GRU, Transformer)
- Feature engineering (technical indicators, volume)
- Confidence intervals and uncertainty quantification
- Real-time predictions and monitoring
- Web interface for easier access

## Troubleshooting

### "Failed to fetch data"
- Check internet connection
- Verify ticker symbol is correct
- Ensure ticker exists on Yahoo Finance

### "CUDA out of memory"
- Reduce batch size in `model_training.py`
- Use CPU by setting `os.environ['CUDA_VISIBLE_DEVICES'] = '-1'`

### "PDF generation failed"
- Ensure write permissions in project directory
- Check available disk space

## License

MIT License - Feel free to use and modify for educational purposes.

## Disclaimer

This tool is for educational and research purposes only. Stock market predictions are inherently uncertain. Do not make investment decisions based solely on these forecasts. Always consult with a financial advisor before making investment decisions.

---

**Last Updated**: March 2026

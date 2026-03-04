# Quick Start Guide

Get the AI Stock Forecast app running in 2 minutes!

## 🚀 Quickest Way (Web Interface)

### Local Machine

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the web server
python app.py

# 3. Open your browser
# Visit: http://localhost:5000
```

Done! 🎉

### With Docker

```bash
# 1. Build
docker build -t stock-forecast .

# 2. Run
docker run -p 5000:5000 stock-forecast

# 3. Visit http://localhost:5000
```

## 📊 Using the Web App

1. **Enter a stock ticker** (e.g., AAPL, TSLA, GOOGL)
2. **Adjust forecast period** (slider: 5-365 days)
3. **Click "Generate Forecast"** (wait ~30-60 seconds)
4. **View results** with current price, forecast, and statistics
5. **📥 Download PDF Report** with one click!

## 💻 CLI Option (Command Line)

```bash
# Simple forecast - AAPL, 30 days
python run_forecast.py

# Tesla, 60 days
python run_forecast.py --ticker TSLA --forecast 60

# Microsoft, retrain model, custom output name
python run_forecast.py --ticker MSFT --retrain --output msft_report.pdf

# See all options
python run_forecast.py --help
```

## ☁️ Deploy Online (Free Options)

### Render.com (Easiest - Free Tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Deploy! 🚀

**Your app will be available at**: `https://yourapp-name.onrender.com`

### Railway.app (Also Free)

1. Go to [railway.app](https://railway.app)
2. Create project from GitHub
3. Auto-deploys on every push
4. Gets public URL automatically

### Heroku (Paid, but was popular)

```bash
# Install Heroku CLI first
heroku login
heroku create your-app-name
git push heroku main
```

## 🐳 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker + registry deployment
- AWS (Elastic Beanstalk, Lambda, EC2)
- Google Cloud (Cloud Run, App Engine)
- Azure
- DigitalOcean

## ⚙️ Troubleshooting

### Port 5000 already in use?
```bash
# Kill the process
lsof -i :5000
kill -9 <PID>
```

### ModuleNotFoundError?
```bash
pip install -r requirements.txt
```

### "Failed to fetch data"?
- Check internet connection
- Verify ticker symbol is correct
- Make sure ticker exists on Yahoo Finance

### Slow PDF generation?
- First run trains the model (~2-5 min)
- Subsequent runs are faster (~30 sec)
- Uses existing model if available

## 📝 File Structure

```
├── app.py                 # Flask web server
├── run_forecast.py        # CLI entry point
├── src/                   # ML modules
├── templates/index.html   # Web UI
├── static/                # CSS & JavaScript
├── models/                # Trained LSTM model
└── data/                  # Historical CSV files
```

## 🎯 First Steps

1. **Try the web demo locally**
   ```bash
   python app.py
   ```

2. **Generate a forecast for AAPL**
   - Visit http://localhost:5000
   - Enter "AAPL"
   - Click generate
   - Download PDF

3. **Deploy online**
   - Choose platform from above
   - Push to GitHub
   - Follow deployment steps

4. **Share with others**
   - Give them your deployed URL
   - They can use it without installing anything!

## ✨ What You Get

✅ Real-time stock price predictions  
✅ Professional PDF reports with charts  
✅ Live results dashboard  
✅ Works on mobile & desktop  
✅ Shareable link when deployed  

## 📚 Learn More

- [Full README](README.md) - Complete documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Advanced deployment options
- [PORTFOLIO.md](PORTFOLIO.md) - Portfolio showcase guide

## 🆘 Need Help?

1. Check error message carefully
2. See [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section
3. Open an issue on GitHub
4. Check [main README](README.md)

---

**Still stuck?** Make sure you have:
- Python 3.7+
- pip package manager
- Internet connection
- ~2 GB disk space

Ready? Start with: `pip install -r requirements.txt && python app.py`

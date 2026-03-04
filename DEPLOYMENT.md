# Deployment Guide

Complete guide to deploying AI Stock Forecast to PDF on various platforms.

## Table of Contents
1. [Local Development](#local-development)
2. [Heroku](#heroku)
3. [Docker](#docker)
4. [GitHub Pages](#github-pages)
5. [Production Considerations](#production-considerations)

## Local Development

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

Visit `http://localhost:5000` in your browser.

### Environment Variables

Create `.env` file for configuration:
```env
FLASK_ENV=development
FLASK_DEBUG=True
MAX_WORKERS=4
```

## Heroku

### Prerequisites
- Heroku CLI installed
- Heroku account
- Git repository

### Deployment Steps

1. **Create Heroku app:**
```bash
heroku login
heroku create your-app-name
```

2. **Deploy:**
```bash
git push heroku main
```

3. **View logs:**
```bash
heroku logs --tail
```

### Configuration

Heroku automatically uses `Procfile` and `runtime.txt` in the repository.

### Scale Workers (if needed)

```bash
# Scale to 2 dynos
heroku ps:scale web=1 --type=standard-1x

# Check current formation
heroku ps
```

## Docker

### Build & Run Locally

```bash
# Build image
docker build -t stock-forecast:latest .

# Run container
docker run -p 5000:5000 stock-forecast:latest
```

### Docker Hub Deployment

```bash
# Build and tag
docker build -t username/stock-forecast:latest .

# Push to Docker Hub
docker login
docker push username/stock-forecast:latest

# Run from Docker Hub
docker run -p 5000:5000 username/stock-forecast:latest
```

### AWS ECS/ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name stock-forecast

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [account-id].dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag stock-forecast:latest [account-id].dkr.ecr.us-east-1.amazonaws.com/stock-forecast:latest

# Push to ECR
docker push [account-id].dkr.ecr.us-east-1.amazonaws.com/stock-forecast:latest
```

## GitHub Pages

GitHub Pages serves only static content, but you can:

1. **Host backend elsewhere** (Heroku, AWS Lambda, etc.)
2. **Update API endpoint** in `static/script.js`:

```javascript
// Change this line
const response = await fetch('/api/forecast', {
  
// To point to your backend
const response = await fetch('https://your-backend.herokuapp.com/api/forecast', {
```

3. **Deploy static files to GitHub Pages** (optional)

## AWS Deployment Options

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 stock-forecast

# Create environment
eb create prod

# Deploy
eb deploy

# View logs
eb logs
```

### AWS Lambda (Serverless)

Install Zappa:
```bash
pip install zappa
```

Configure `zappa_settings.json`:
```json
{
    "dev": {
        "app_function": "app.app",
        "aws_region": "us-east-1",
        "project_name": "stock-forecast",
        "runtime": "python3.9",
        "s3_bucket": "your-bucket-name"
    }
}
```

Deploy:
```bash
zappa deploy dev
zappa update dev  # For updates
```

### AWS EC2

```bash
# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Install Python & dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# Clone repo and setup
git clone https://github.com/mkomer/AI-Stock-Forecast-to-PDF.git
cd AI-Stock-Forecast-to-PDF
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

# Use systemd for auto-restart
sudo nano /etc/systemd/system/stock-forecast.service
```

## Google Cloud Platform

### Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/stock-forecast

# Deploy
gcloud run deploy stock-forecast \
  --image gcr.io/your-project/stock-forecast \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --timeout 600
```

### App Engine

Create `app.yaml`:
```yaml
runtime: python39

env: standard

entrypoint: gunicorn -b :$PORT app:app

env_variables:
  FLASK_ENV: "production"
```

Deploy:
```bash
gcloud app deploy
```

## Digital Ocean

### App Platform

1. Push code to GitHub
2. Create app on DigitalOcean App Platform
3. Connect GitHub repository
4. Set environment: Python 3.9
5. Build command: `pip install -r requirements.txt`
6. Run command: `gunicorn -b 0.0.0.0:8080 app:app`

### Droplet

```bash
# SSH and setup
ssh root@droplet-ip

# Install dependencies
apt update && apt install python3-pip python3-venv nginx

# Setup app
git clone https://github.com/mkomer/AI-Stock-Forecast-to-PDF.git
cd AI-Stock-Forecast-to-PDF
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx reverse proxy and Gunicorn service
```

## Production Considerations

### Environment Variables

Set in deployment platform:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
MAX_WORKERS=4
```

### Performance

- Use production WSGI server (Gunicorn with multiple workers)
- Enable caching headers in `app.py`
- Compress PDF generation with 5-day delay between same ticker requests

### Security

- Add request rate limiting
- Validate ticker input strictly
- Use HTTPS only
- Add CORS restrictions if needed
- Implement API key authentication for production

### Monitoring

- Set up logging (Cloud Logging, CloudWatch, etc.)
- Monitor error rates and request times
- Alert on failures
- Track resource usage

### Database (Optional)

For production, consider adding a database:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    results = db.Column(db.JSON)
```

## Troubleshooting

### Module not found errors
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it
```

### TensorFlow memory issues
- Reduce `batch_size` in `model_training.py`
- Use smaller workers count
- Deploy with more RAM

### PDF generation timeout
- Reduce forecast period
- Increase deployment timeout (300s recommended)
- Use background job queue (Celery + Redis)

## Support

For issues or questions, check the [main README](README.md) or open an issue on GitHub.

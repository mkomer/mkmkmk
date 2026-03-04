// Update days display when range slider changes
document.getElementById('forecastDays').addEventListener('input', function() {
    const days = this.value;
    document.getElementById('daysDisplay').textContent = `${days} days`;
});

// Handle form submission
document.getElementById('forecastForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const ticker = document.getElementById('ticker').value.trim();
    const forecastDays = document.getElementById('forecastDays').value;
    
    if (!ticker) {
        showError('Please enter a stock ticker');
        return;
    }
    
    // Disable form
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loading = submitBtn.querySelector('.loading');
    
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loading.style.display = 'inline';
    
    try {
        // Create forecast
        const response = await fetch('/api/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ticker: ticker,
                forecast_days: forecastDays
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create forecast');
        }
        
        const result = await response.json();
        const jobId = result.job_id;
        
        // Poll for results
        pollForecast(jobId, ticker);
        
    } catch (error) {
        showError(error.message);
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        loading.style.display = 'none';
    }
});

async function pollForecast(jobId, ticker) {
    const maxAttempts = 60; // Max 60 attempts (2-3 minutes)
    let attempts = 0;
    
    const pollInterval = setInterval(async () => {
        attempts++;
        
        try {
            const response = await fetch(`/api/forecast/${jobId}`);
            
            if (response.status === 202) {
                // Still processing
                console.log(`Processing... (${attempts})`);
                return;
            }
            
            clearInterval(pollInterval);
            
            if (!response.ok) {
                const error = await response.json();
                showError(error.error || 'Forecast failed');
                resetFormUI();
                return;
            }
            
            const result = await response.json();
            
            // Store job ID for download
            window.currentJobId = jobId;
            
            // Display results
            displayResults(result);
            
        } catch (error) {
            clearInterval(pollInterval);
            showError('Error retrieving forecast: ' + error.message);
            resetFormUI();
        }
    }, 2000); // Poll every 2 seconds
    
    // Stop polling after max attempts
    setTimeout(() => {
        if (attempts >= maxAttempts) {
            clearInterval(pollInterval);
            showError('Forecast generation timed out. Please try again.');
            resetFormUI();
        }
    }, maxAttempts * 2000);
}

function displayResults(result) {
    // Hide form and error, show results
    document.getElementById('forecastForm').style.display = 'none';
    document.getElementById('errorCard').style.display = 'none';
    document.getElementById('resultsCard').style.display = 'block';
    
    // Populate results
    document.getElementById('resultTicker').textContent = result.ticker;
    document.getElementById('resultCurrent').textContent = result.current_price;
    document.getElementById('resultForecast').textContent = result.forecast_price;
    
    // Color code the change
    const changeElement = document.getElementById('resultChange');
    const changeValue = parseFloat(result.change);
    changeElement.textContent = result.change;
    changeElement.style.color = changeValue >= 0 ? '#2ca02c' : '#d62728';
    
    document.getElementById('resultMin').textContent = result.min_price;
    document.getElementById('resultMax').textContent = result.max_price;
    document.getElementById('resultVolatility').textContent = result.volatility;
    
    const timestamp = new Date(result.timestamp);
    document.getElementById('generatedTime').textContent = timestamp.toLocaleString();
    
    // Scroll to results
    document.getElementById('resultsCard').scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    document.getElementById('forecastForm').style.display = 'flex';
    document.getElementById('resultsCard').style.display = 'none';
    document.getElementById('errorCard').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
    
    document.getElementById('errorCard').scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    resetFormUI();
    document.getElementById('forecastForm').reset();
    document.getElementById('daysDisplay').textContent = '30 days';
}

function resetFormUI() {
    document.getElementById('forecastForm').style.display = 'flex';
    document.getElementById('resultsCard').style.display = 'none';
    document.getElementById('errorCard').style.display = 'none';
    
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loading = submitBtn.querySelector('.loading');
    
    submitBtn.disabled = false;
    btnText.style.display = 'inline';
    loading.style.display = 'none';
}

// Download PDF button
document.getElementById('downloadBtn')?.addEventListener('click', async function() {
    if (!window.currentJobId) {
        alert('No forecast available for download');
        return;
    }
    
    try {
        const response = await fetch(`/api/download/${window.currentJobId}`);
        
        if (!response.ok) {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Failed to download PDF'));
            return;
        }
        
        // Download the PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${document.getElementById('resultTicker').textContent}_forecast.pdf`;
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        
    } catch (error) {
        alert('Error downloading PDF: ' + error.message);
    }
});

// New forecast button
document.getElementById('newForecastBtn')?.addEventListener('click', resetForm);

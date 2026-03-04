"""
PDF report generation module for stock forecast results.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
from datetime import datetime
import os


def create_forecast_chart(historical_dates, historical_prices, forecast_dates, 
                         forecast_prices, output_path='forecast_chart.png'):
    """
    Create visualization chart for historical and forecast prices.
    
    Args:
        historical_dates: Dates for historical data
        historical_prices: Historical prices
        forecast_dates: Dates for forecast
        forecast_prices: Forecast prices
        output_path (str): Path to save chart image
    
    Returns:
        str: Path to saved chart
    """
    plt.figure(figsize=(12, 6))
    
    # Plot historical prices
    plt.plot(historical_dates, historical_prices, label='Historical Prices', 
             color='blue', linewidth=2)
    
    # Plot forecast prices
    combined_dates = list(historical_dates[-1:]) + forecast_dates
    combined_prices = list(historical_prices[-1:]) + list(forecast_prices)
    plt.plot(combined_dates, combined_prices, label='Forecast', 
             color='red', linewidth=2, linestyle='--')
    
    plt.title('Stock Price Forecast', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_pdf_report(ticker, historical_prices, forecast_prices, forecast_dates, 
                       statistics, output_filename='stock_forecast.pdf'):
    """
    Generate comprehensive PDF report with forecast results.
    
    Args:
        ticker (str): Stock ticker symbol
        historical_prices (list): Recent historical prices
        forecast_prices (np.ndarray): Predicted prices
        forecast_dates (list): Forecast dates
        statistics (dict): Prediction statistics
        output_filename (str): Output PDF filename
    """
    
    # Create PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Title
    title = Paragraph(f"{ticker} Stock Price Forecast", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Report metadata
    report_date = Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                           styles['Normal'])
    elements.append(report_date)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary section
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Current Price', f"${statistics['current_price']:.2f}"],
        ['Forecast Price (30 days)', f"${statistics['mean_prediction']:.2f}"],
        ['Expected Change', f"${statistics['expected_change']:.2f}"],
        ['Expected Change %', f"{statistics['change_percent']:.2f}%"],
        ['Min Predicted Price', f"${statistics['min_prediction']:.2f}"],
        ['Max Predicted Price', f"${statistics['max_prediction']:.2f}"],
        ['Price Volatility (Std Dev)', f"${statistics['std_prediction']:.2f}"],
    ]
    
    table = Table(summary_data, colWidths=[3*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Forecast chart
    elements.append(Paragraph("Price Forecast Chart", heading_style))
    chart_path = create_forecast_chart(
        list(range(len(historical_prices))), 
        historical_prices,
        list(range(len(historical_prices), len(historical_prices) + len(forecast_prices))),
        forecast_prices
    )
    
    if os.path.exists(chart_path):
        img = Image(chart_path, width=6*inch, height=3*inch)
        elements.append(img)
    
    # Build PDF
    doc.build(elements)
    print(f"PDF report saved to {output_filename}")

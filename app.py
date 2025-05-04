from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Sample data for demonstration
def get_stock_data(symbol, days=30):
    """Get stock data for the specified symbol and time period"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # In a real application, you would use an API key from environment variables
    # API_KEY = os.getenv("STOCK_API_KEY")
    
    # For demo purposes, generate random data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Close': [100 + i * (0.5 - 0.1 * (i % 5)) for i in range(len(dates))],
        'Volume': [1000000 + i * 10000 * (i % 3) for i in range(len(dates))]
    })
    
    return df

def get_economic_indicators():
    """Get economic indicators data"""
    # In a real application, you would fetch this from an API
    indicators = {
        'GDP Growth': 2.4,
        'Unemployment': 3.8,
        'Inflation': 3.2,
        'Interest Rate': 5.5,
        'Consumer Confidence': 106.7
    }
    return indicators

def get_industry_performance():
    """Get industry performance data"""
    industries = [
        'Technology', 'Healthcare', 'Finance', 
        'Consumer Goods', 'Energy', 'Utilities',
        'Real Estate', 'Materials', 'Industrials'
    ]
    
    performance = [8.4, 5.2, 3.7, 2.1, -1.3, 1.8, 0.9, 2.5, 4.2]
    
    return industries, performance

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/api/stock/<symbol>')
def stock_data(symbol):
    """API endpoint to get stock data"""
    days = request.args.get('days', default=30, type=int)
    df = get_stock_data(symbol, days)
    
    # Create stock price chart
    fig_price = px.line(df, x='Date', y='Close', 
                        title=f'{symbol} Stock Price',
                        labels={'Close': 'Price ($)', 'Date': ''},
                        template='plotly_dark')
    fig_price.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    # Create volume chart
    fig_volume = px.bar(df, x='Date', y='Volume',
                        title=f'{symbol} Trading Volume',
                        labels={'Volume': 'Volume', 'Date': ''},
                        template='plotly_dark')
    fig_volume.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    # Convert to JSON
    price_chart = json.dumps(fig_price, cls=plotly.utils.PlotlyJSONEncoder)
    volume_chart = json.dumps(fig_volume, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'price_chart': price_chart,
        'volume_chart': volume_chart
    })

@app.route('/api/economic-indicators')
def economic_data():
    """API endpoint to get economic indicators"""
    indicators = get_economic_indicators()
    
    # Create gauge charts for each indicator
    charts = {}
    
    for indicator, value in indicators.items():
        if indicator == 'GDP Growth':
            max_val = 5
            threshold = 2
        elif indicator == 'Unemployment':
            max_val = 10
            threshold = 5
        elif indicator == 'Inflation':
            max_val = 10
            threshold = 3
        elif indicator == 'Interest Rate':
            max_val = 10
            threshold = 5
        else:  # Consumer Confidence
            max_val = 150
            threshold = 100
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': indicator},
            gauge={
                'axis': {'range': [None, max_val]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, threshold], 'color': "lightgray"},
                    {'range': [threshold, max_val], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        charts[indicator.lower().replace(' ', '_')] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(charts)

@app.route('/api/industry-performance')
def industry_data():
    """API endpoint to get industry performance data"""
    industries, performance = get_industry_performance()
    
    # Create bar chart
    fig = px.bar(
        x=industries, 
        y=performance,
        title='Industry Performance (YTD %)',
        labels={'x': 'Industry', 'y': 'Performance (%)'},
        template='plotly_dark',
        color=performance,
        color_continuous_scale='RdBu',
        range_color=[-5, 10]
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=80),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({'chart': chart})

@app.route('/api/portfolio-analysis')
def portfolio_analysis():
    """API endpoint to get portfolio analysis"""
    # Sample portfolio data
    portfolio = {
        'AAPL': 25,
        'MSFT': 20,
        'GOOGL': 15,
        'AMZN': 15,
        'META': 10,
        'TSLA': 10,
        'NVDA': 5
    }
    
    # Create pie chart
    fig = px.pie(
        values=list(portfolio.values()),
        names=list(portfolio.keys()),
        title='Portfolio Allocation',
        template='plotly_dark',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Risk analysis data
    risk_data = {
        'Volatility': 15.2,
        'Beta': 1.2,
        'Sharpe Ratio': 1.8,
        'Alpha': 2.4,
        'Max Drawdown': -12.5
    }
    
    return jsonify({
        'allocation_chart': chart,
        'risk_metrics': risk_data
    })

if __name__ == '__main__':
    app.run(debug=True)
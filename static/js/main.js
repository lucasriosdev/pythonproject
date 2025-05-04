document.addEventListener('DOMContentLoaded', function() {
    // Initial data loading
    loadStockData();
    loadEconomicIndicators();
    loadIndustryPerformance();
    loadPortfolioAnalysis();
    
    // Event listeners
    document.getElementById('update-btn').addEventListener('click', loadStockData);
    document.getElementById('search-btn').addEventListener('click', handleSearch);
    document.getElementById('stock-search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Theme toggle
    document.querySelector('.theme-toggle').addEventListener('click', toggleTheme);
});

function loadStockData() {
    const symbol = document.getElementById('stock-symbol').value;
    const period = document.getElementById('time-period').value;
    
    fetch(`/api/stock/${symbol}?days=${period}`)
        .then(response => response.json())
        .then(data => {
            // Render price chart
            Plotly.newPlot('price-chart', JSON.parse(data.price_chart));
            
            // Render volume chart
            Plotly.newPlot('volume-chart', JSON.parse(data.volume_chart));
        })
        .catch(error => console.error('Error loading stock data:', error));
}

function loadEconomicIndicators() {
    fetch('/api/economic-indicators')
        .then(response => response.json())
        .then(data => {
            // Render each indicator gauge
            Object.keys(data).forEach(key => {
                Plotly.newPlot(key, JSON.parse(data[key]));
            });
        })
        .catch(error => console.error('Error loading economic indicators:', error));
}

function loadIndustryPerformance() {
    fetch('/api/industry-performance')
        .then(response => response.json())
        .then(data => {
            // Render industry performance chart
            Plotly.newPlot('industry-chart', JSON.parse(data.chart));
        })
        .catch(error => console.error('Error loading industry performance:', error));
}

function loadPortfolioAnalysis() {
    fetch('/api/portfolio-analysis')
        .then(response => response.json())
        .then(data => {
            // Render portfolio allocation chart
            Plotly.newPlot('allocation-chart', JSON.parse(data.allocation_chart));
            
            // Update risk metrics
            document.getElementById('volatility').textContent = data.risk_metrics.Volatility + '%';
            document.getElementById('beta').textContent = data.risk_metrics.Beta;
            document.getElementById('sharpe').textContent = data.risk_metrics.['Sharpe Ratio'];
            document.getElementById('alpha').textContent = data.risk_metrics.Alpha;
            document.getElementById('drawdown').textContent = data.risk_metrics.['Max Drawdown'] + '%';
        })
        .catch(error => console.error('Error loading portfolio analysis:', error));
}

function handleSearch() {
    const searchTerm = document.getElementById('stock-search').value.trim().toUpperCase();
    
    if (searchTerm) {
        // In a real application, this would search for the stock
        // For demo purposes, just set the select if it's one of our options
        const select = document.getElementById('stock-symbol');
        for (let i = 0; i < select.options.length; i++) {
            if (select.options[i].value === searchTerm) {
                select.selectedIndex = i;
                loadStockData();
                return;
            }
        }
        
        // If not found
        alert(`Stock symbol ${searchTerm} not found in our demo. Try AAPL, MSFT, GOOGL, AMZN, or META.`);
    }
}

function toggleTheme() {
    // This would toggle between light and dark themes
    // For demo purposes, we'll just show an alert
    alert('Theme toggle functionality would be implemented here. Currently using dark theme by default.');
}

// Fix for the portfolio analysis risk metrics
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/portfolio-analysis')
        .then(response => response.json())
        .then(data => {
            document.getElementById('volatility').textContent = data.risk_metrics.Volatility + '%';
            document.getElementById('beta').textContent = data.risk_metrics.Beta;
            document.getElementById('sharpe').textContent = data.risk_metrics["Sharpe Ratio"];
            document.getElementById('alpha').textContent = data.risk_metrics.Alpha;
            document.getElementById('drawdown').textContent = data.risk_metrics["Max Drawdown"] + '%';
        })
        .catch(error => console.error('Error loading risk metrics:', error));
});
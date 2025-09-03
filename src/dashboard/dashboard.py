"""
AFH Property Scout Dashboard - Web-based dashboard for monitoring and analysis
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger
import pandas as pd
from flask import Flask, render_template, jsonify, request, send_from_directory
import plotly.graph_objs as go
import plotly.utils

class AFHDashboard:
    """Web dashboard for AFH Property Scout"""
    
    def __init__(self, db_manager, config: Dict[str, Any]):
        """Initialize dashboard with database manager and configuration"""
        self.db_manager = db_manager
        self.config = config
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard page"""
            return render_template('dashboard.html')
        
        @self.app.route('/api/summary')
        def api_summary():
            """Get property summary data"""
            try:
                summary = self.db_manager.get_property_summary()
                return jsonify(summary)
            except Exception as e:
                logger.error(f"Error getting summary: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/properties')
        def api_properties():
            """Get properties data"""
            try:
                limit = request.args.get('limit', 50, type=int)
                min_score = request.args.get('min_score', 70.0, type=float)
                
                properties = self.db_manager.get_top_properties(limit=limit, min_score=min_score)
                return jsonify(properties)
            except Exception as e:
                logger.error(f"Error getting properties: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/stats')
        def api_stats():
            """Get database statistics"""
            try:
                stats = self.db_manager.get_database_stats()
                return jsonify(stats)
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/charts/viability')
        def api_charts_viability():
            """Get viability score distribution chart"""
            try:
                chart_data = self._create_viability_chart()
                return jsonify(chart_data)
            except Exception as e:
                logger.error(f"Error creating viability chart: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/charts/county')
        def api_charts_county():
            """Get county distribution chart"""
            try:
                chart_data = self._create_county_chart()
                return jsonify(chart_data)
            except Exception as e:
                logger.error(f"Error creating county chart: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/charts/price')
        def api_charts_price():
            """Get price distribution chart"""
            try:
                chart_data = self._create_price_chart()
                return jsonify(chart_data)
            except Exception as e:
                logger.error(f"Error creating price chart: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/charts/trends')
        def api_charts_trends():
            """Get property trends over time"""
            try:
                chart_data = self._create_trends_chart()
                return jsonify(chart_data)
            except Exception as e:
                logger.error(f"Error creating trends chart: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/property/<int:property_id>')
        def property_detail(property_id):
            """Property detail page"""
            try:
                property_data = self._get_property_detail(property_id)
                if property_data:
                    return render_template('property_detail.html', property=property_data)
                else:
                    return "Property not found", 404
            except Exception as e:
                logger.error(f"Error getting property detail: {e}")
                return "Error loading property", 500
    
    def _create_viability_chart(self) -> Dict[str, Any]:
        """Create viability score distribution chart"""
        try:
            stats = self.db_manager.get_database_stats()
            viability_dist = stats.get('viability_distribution', {})
            
            labels = list(viability_dist.keys())
            values = list(viability_dist.values())
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker_colors=['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6', '#34495e']
            )])
            
            fig.update_layout(
                title="Property Viability Score Distribution",
                font=dict(size=12)
            )
            
            return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
        except Exception as e:
            logger.error(f"Error creating viability chart: {e}")
            return json.dumps({})
    
    def _create_county_chart(self) -> Dict[str, Any]:
        """Create county distribution chart"""
        try:
            summary = self.db_manager.get_property_summary()
            county_dist = summary.get('county_distribution', {})
            
            counties = list(county_dist.keys())
            counts = list(county_dist.values())
            
            fig = go.Figure(data=[go.Bar(
                x=counties,
                y=counts,
                marker_color='#3498db'
            )])
            
            fig.update_layout(
                title="Properties by County",
                xaxis_title="County",
                yaxis_title="Number of Properties",
                font=dict(size=12)
            )
            
            return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
        except Exception as e:
            logger.error(f"Error creating county chart: {e}")
            return json.dumps({})
    
    def _create_price_chart(self) -> Dict[str, Any]:
        """Create price distribution chart"""
        try:
            # Get properties with price data
            properties = self.db_manager.get_top_properties(limit=1000, min_score=0)
            
            prices = [p.get('price', 0) for p in properties if p.get('price', 0) > 0]
            
            if not prices:
                return json.dumps({})
            
            fig = go.Figure(data=[go.Histogram(
                x=prices,
                nbinsx=20,
                marker_color='#9b59b6'
            )])
            
            fig.update_layout(
                title="Property Price Distribution",
                xaxis_title="Price ($)",
                yaxis_title="Number of Properties",
                font=dict(size=12)
            )
            
            return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
        except Exception as e:
            logger.error(f"Error creating price chart: {e}")
            return json.dumps({})
    
    def _create_trends_chart(self) -> Dict[str, Any]:
        """Create property trends over time chart"""
        try:
            # This would require additional data from search history
            # For now, create a mock trend chart
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                                end=datetime.now(), freq='D')
            
            # Mock data - in real implementation, this would come from search history
            total_properties = [10 + i + (i % 3) for i in range(len(dates))]
            viable_properties = [int(t * 0.6) for t in total_properties]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=total_properties,
                mode='lines+markers',
                name='Total Properties',
                line=dict(color='#3498db')
            ))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=viable_properties,
                mode='lines+markers',
                name='Viable Properties',
                line=dict(color='#2ecc71')
            ))
            
            fig.update_layout(
                title="Property Discovery Trends (Last 30 Days)",
                xaxis_title="Date",
                yaxis_title="Number of Properties",
                font=dict(size=12)
            )
            
            return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
        except Exception as e:
            logger.error(f"Error creating trends chart: {e}")
            return json.dumps({})
    
    def _get_property_detail(self, property_id: int) -> Dict[str, Any]:
        """Get detailed property information"""
        try:
            # This would query the database for specific property details
            # For now, return mock data
            return {
                'id': property_id,
                'address': '123 Main St, Seattle, WA',
                'price': 750000,
                'bedrooms': 4,
                'bathrooms': 3,
                'sqft': 2500,
                'county': 'King County',
                'wabo_status': 'approved',
                'viability_score': 85.5,
                'analysis': {
                    'monthly_cash_flow': 4500,
                    'cap_rate': 0.12,
                    'optimal_price': 720000
                }
            }
        except Exception as e:
            logger.error(f"Error getting property detail: {e}")
            return None
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Run the dashboard web server"""
        logger.info(f"Starting AFH Property Scout Dashboard on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def create_dashboard_templates():
    """Create HTML templates for the dashboard"""
    
    # Create templates directory
    os.makedirs('afh-property-scout/templates', exist_ok=True)
    os.makedirs('afh-property-scout/static/css', exist_ok=True)
    os.makedirs('afh-property-scout/static/js', exist_ok=True)
    
    # Main dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFH Property Scout Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
        }
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
        }
        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .property-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            transition: box-shadow 0.3s;
        }
        .property-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .viability-badge {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .viability-excellent { background-color: #2ecc71; color: white; }
        .viability-good { background-color: #f39c12; color: white; }
        .viability-fair { background-color: #e74c3c; color: white; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-home"></i> AFH Property Scout Dashboard
            </span>
            <span class="navbar-text">
                Last Updated: <span id="lastUpdated"></span>
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <!-- Summary Cards -->
        <div class="row" id="summaryCards">
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <div class="metric-value" id="totalProperties">-</div>
                    <div class="metric-label">Total Properties</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <div class="metric-value" id="viableProperties">-</div>
                    <div class="metric-label">Viable Properties</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <div class="metric-value" id="newProperties">-</div>
                    <div class="metric-label">New Properties</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <div class="metric-value" id="avgScore">-</div>
                    <div class="metric-label">Avg Viability Score</div>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="row">
            <div class="col-md-6">
                <div class="chart-container">
                    <h5>Viability Score Distribution</h5>
                    <div id="viabilityChart"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <h5>Properties by County</h5>
                    <div id="countyChart"></div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="chart-container">
                    <h5>Price Distribution</h5>
                    <div id="priceChart"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <h5>Discovery Trends</h5>
                    <div id="trendsChart"></div>
                </div>
            </div>
        </div>

        <!-- Properties Table -->
        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    <h5>Top Properties</h5>
                    <div id="propertiesTable"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Load dashboard data
        async function loadDashboard() {
            try {
                // Load summary
                const summaryResponse = await fetch('/api/summary');
                const summary = await summaryResponse.json();
                updateSummaryCards(summary);

                // Load charts
                loadChart('/api/charts/viability', 'viabilityChart');
                loadChart('/api/charts/county', 'countyChart');
                loadChart('/api/charts/price', 'priceChart');
                loadChart('/api/charts/trends', 'trendsChart');

                // Load properties
                const propertiesResponse = await fetch('/api/properties?limit=20');
                const properties = await propertiesResponse.json();
                updatePropertiesTable(properties);

                // Update last updated time
                document.getElementById('lastUpdated').textContent = new Date().toLocaleString();

            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }

        function updateSummaryCards(summary) {
            document.getElementById('totalProperties').textContent = summary.total || 0;
            document.getElementById('viableProperties').textContent = summary.viable || 0;
            document.getElementById('newProperties').textContent = summary.new || 0;
            document.getElementById('avgScore').textContent = (summary.average_viability_score || 0) + '%';
        }

        async function loadChart(url, containerId) {
            try {
                const response = await fetch(url);
                const chartData = await response.json();
                if (chartData && Object.keys(chartData).length > 0) {
                    Plotly.newPlot(containerId, chartData.data, chartData.layout, {responsive: true});
                }
            } catch (error) {
                console.error(`Error loading chart ${containerId}:`, error);
            }
        }

        function updatePropertiesTable(properties) {
            const container = document.getElementById('propertiesTable');
            if (!properties || properties.length === 0) {
                container.innerHTML = '<p>No properties found.</p>';
                return;
            }

            let tableHTML = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Address</th>
                                <th>Price</th>
                                <th>Beds/Baths</th>
                                <th>Sqft</th>
                                <th>County</th>
                                <th>WABO Status</th>
                                <th>Viability</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            properties.forEach(prop => {
                const viabilityClass = prop.viability_score >= 80 ? 'viability-excellent' : 
                                     prop.viability_score >= 70 ? 'viability-good' : 'viability-fair';
                
                tableHTML += `
                    <tr>
                        <td>${prop.address || 'Unknown'}</td>
                        <td>$${(prop.price || 0).toLocaleString()}</td>
                        <td>${prop.bedrooms || 0}/${prop.bathrooms || 0}</td>
                        <td>${(prop.sqft || 0).toLocaleString()}</td>
                        <td>${prop.county || 'Unknown'}</td>
                        <td>${prop.wabo_status || 'Unknown'}</td>
                        <td><span class="viability-badge ${viabilityClass}">${(prop.viability_score || 0).toFixed(1)}%</span></td>
                        <td><a href="/property/${prop.id}" class="btn btn-sm btn-primary">View Details</a></td>
                    </tr>
                `;
            });

            tableHTML += '</tbody></table></div>';
            container.innerHTML = tableHTML;
        }

        // Load dashboard on page load
        document.addEventListener('DOMContentLoaded', loadDashboard);

        // Refresh dashboard every 5 minutes
        setInterval(loadDashboard, 300000);
    </script>
</body>
</html>
    """
    
    with open('afh-property-scout/templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)
    
    # Property detail template
    property_detail_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Property Details - AFH Property Scout</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-home"></i> AFH Property Scout
            </span>
            <a href="/" class="btn btn-outline-light">Back to Dashboard</a>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <h1>Property Details</h1>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ property.address }}</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Price:</strong> ${{ "{:,}".format(property.price) }}</p>
                                <p><strong>Bedrooms:</strong> {{ property.bedrooms }}</p>
                                <p><strong>Bathrooms:</strong> {{ property.bathrooms }}</p>
                                <p><strong>Square Feet:</strong> {{ "{:,}".format(property.sqft) }}</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>County:</strong> {{ property.county }}</p>
                                <p><strong>WABO Status:</strong> {{ property.wabo_status }}</p>
                                <p><strong>Viability Score:</strong> {{ property.viability_score }}%</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    with open('afh-property-scout/templates/property_detail.html', 'w') as f:
        f.write(property_detail_html)

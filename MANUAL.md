# 📚 AFH Property Scout - Complete User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Basic Usage](#basic-usage)
6. [Advanced Features](#advanced-features)
7. [Understanding Analysis Results](#understanding-analysis-results)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)

---

## Introduction

Welcome to AFH Property Scout, the most comprehensive automated system for finding profitable Adult Family Home (AFH) properties. This manual will guide you through every aspect of the system, from initial setup to advanced configuration and optimization.

### What You'll Learn

- How to set up and configure the system
- Understanding property analysis results
- Customizing search criteria and notifications
- Interpreting financial viability scores
- Troubleshooting common issues
- Maximizing your property search efficiency

---

## System Overview

### Core Components

AFH Property Scout consists of several integrated components:

1. **Property Scrapers**: Search engines for different property sources
2. **Analysis Engine**: Financial and viability analysis system
3. **Filtering System**: Criteria-based property filtering
4. **Notification Manager**: Email and SMS alert system
5. **Database Manager**: Data storage and retrieval
6. **Scheduler**: Automated daily search system
7. **Web Dashboard**: Visual interface for monitoring

### Data Flow

```
Property Sources → Scrapers → Filters → Analysis → Notifications → Dashboard
```

---

## Installation Guide

### Prerequisites

Before installing AFH Property Scout, ensure you have:

- **Python 3.8 or higher**
- **Internet connection**
- **2GB RAM minimum**
- **1GB free disk space**
- **Administrator/sudo access** (for some installations)

### Step 1: Download and Extract

```bash
# Clone the repository
git clone https://github.com/your-repo/afh-property-scout.git
cd afh-property-scout

# Or download and extract ZIP file
unzip afh-property-scout.zip
cd afh-property-scout
```

### Step 2: Run Setup Script

```bash
# Run the automated setup
python setup.py
```

The setup script will:
- Create necessary directories
- Install Python dependencies
- Initialize the database
- Create configuration files
- Set up environment variables

### Step 3: Verify Installation

```bash
# Test the installation
python run_scout.py --summary
```

You should see output similar to:
```
🏠 AFH Property Scout - Starting System
==================================================

System initialized successfully!

📊 Property Summary:
Total properties: 0
Viable properties: 0
New properties: 0
Average viability score: 0.0%
```

---

## Configuration

### Environment Variables

The system uses environment variables for sensitive information. Edit the `.env` file:

```bash
nano .env
```

#### Email Configuration (Required for notifications)

```env
# Gmail settings (recommended)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Recipients
RECIPIENT_EMAIL=your_email@gmail.com
```

**Setting up Gmail App Password:**
1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account → Security → 2-Step Verification → App passwords
3. Generate a password for "Mail"
4. Use this password in the `.env` file

#### SMS Configuration (Optional)

```env
# Twilio settings
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Recipient phone number
RECIPIENT_PHONE=+1234567890
```

**Setting up Twilio:**
1. Sign up at [twilio.com](https://twilio.com)
2. Get your Account SID and Auth Token from the console
3. Purchase a phone number for sending SMS
4. Add credentials to `.env` file

#### Social Media APIs (Optional)

```env
# Facebook API
FACEBOOK_ACCESS_TOKEN=your_facebook_token

# Twitter API
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
```

### Main Configuration

Edit `config/settings.yaml` to customize system behavior:

#### Target Counties and Criteria

```yaml
target_counties:
  - "Lewis County"
  - "Thurston County" 
  - "Pierce County"
  - "King County"

property_criteria:
  property_type: "1st floor rambler"
  min_bedrooms: 3
  min_bathrooms: 2
  min_sqft: 2000
  max_price: 1500000
  min_price: 300000
```

#### Search Sources

```yaml
search_sources:
  real_estate:
    - "nwmls"
    - "zillow"
    - "redfin"
    - "realtor"
  social_media:
    - "facebook"
    - "twitter"
    - "craigslist"
  afh_specific:
    - "afh_council"
    - "facebook_groups"
```

#### AFH Financial Analysis

```yaml
afh_analysis:
  # Revenue assumptions
  medicaid_rate_per_day: 120
  private_pay_rate_per_day: 200
  occupancy_rate: 0.85
  
  # Operating costs (monthly)
  utilities: 800
  insurance: 400
  maintenance: 600
  supplies: 500
  licensing_fees: 200
  
  # Target metrics
  min_cash_flow: 3000
  min_cap_rate: 0.08
  max_debt_ratio: 0.75
```

#### Notification Settings

```yaml
notifications:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
  sms:
    enabled: true
```

#### Schedule Settings

```yaml
schedule:
  daily_search_time: "08:00"  # 8 AM daily
  search_frequency_hours: 24
  notification_check_minutes: 30
```

---

## Basic Usage

### Running Your First Search

```bash
# Run a one-time search
python run_scout.py --search
```

This will:
1. Search all configured sources
2. Filter properties based on your criteria
3. Analyze each property for AFH viability
4. Store results in the database
5. Display a summary

### Starting Daily Automation

```bash
# Start the daily scheduler
python run_scout.py --schedule
```

The system will:
- Run daily searches at 8:00 AM
- Check for notifications every 30 minutes
- Continue running until stopped (Ctrl+C)

### Checking Notifications

```bash
# Check for pending notifications
python run_scout.py --notify
```

### Viewing Property Summary

```bash
# Get current property summary
python run_scout.py --summary
```

### Starting the Web Dashboard

```bash
# Start the web dashboard
python run_dashboard.py
```

Then open your browser to: http://localhost:5000

---

## Advanced Features

### Custom Search Criteria

You can modify the search criteria in `config/settings.yaml`:

```yaml
property_criteria:
  # Adjust minimum requirements
  min_bedrooms: 4        # Increase for larger AFHs
  min_bathrooms: 3       # More bathrooms for better operations
  min_sqft: 2500         # Larger properties
  
  # Adjust price range
  min_price: 400000      # Higher minimum for better properties
  max_price: 2000000     # Increase for premium properties
  
  # Add specific requirements
  property_type: "1st floor rambler"
```

### Financial Analysis Customization

Adjust the financial assumptions to match your market:

```yaml
afh_analysis:
  # Revenue rates (per day)
  medicaid_rate_per_day: 130    # Adjust for your area
  private_pay_rate_per_day: 220 # Higher for premium care
  
  # Occupancy assumptions
  occupancy_rate: 0.90          # Higher for established operators
  
  # Operating costs (monthly)
  utilities: 1000               # Higher for larger properties
  insurance: 500                # Professional liability
  maintenance: 800              # Preventive maintenance
  supplies: 600                 # Medical supplies, food
  licensing_fees: 300           # Annual fees divided by 12
  
  # Target metrics
  min_cash_flow: 4000           # Higher minimum cash flow
  min_cap_rate: 0.10            # 10% minimum cap rate
```

### Notification Customization

Customize when and how you receive notifications:

```yaml
notifications:
  email:
    enabled: true
    # Add multiple recipients
    recipient_emails:
      - "your_email@gmail.com"
      - "partner@example.com"
      - "agent@example.com"
  
  sms:
    enabled: true
    # Add multiple phone numbers
    recipient_phones:
      - "+1234567890"
      - "+0987654321"
```

### Advanced Scheduling

```yaml
schedule:
  daily_search_time: "06:00"    # Earlier morning search
  search_frequency_hours: 12    # Twice daily searches
  notification_check_minutes: 15 # More frequent checks
```

---

## Understanding Analysis Results

### Viability Score Breakdown

The system calculates a viability score from 0-100% based on:

#### Basic Analysis (25% weight)
- **Bedrooms**: 3+ required, 4+ preferred
- **Bathrooms**: 2+ required, 3+ preferred  
- **Square Footage**: 2000+ required, 2500+ preferred
- **Property Type**: Single story/rambler preferred
- **County**: Target counties get bonus points
- **Price Range**: Within target range preferred

#### Financial Analysis (30% weight)
- **Monthly Cash Flow**: Must meet minimum threshold
- **Cap Rate**: Higher rates score better
- **Debt Service Coverage**: Must be above 1.25x
- **Revenue Projections**: Based on occupancy and rates

#### Market Analysis (15% weight)
- **Price per Square Foot**: Compared to market average
- **Market Demand**: High demand areas score better
- **Competition Level**: Lower competition preferred

#### WABO Analysis (20% weight)
- **WABO Status**: Approved > Inspected > Mentioned > None
- **Licensing Timeline**: Shorter timelines score better
- **Estimated Costs**: Lower costs preferred

#### Risk Assessment (10% weight)
- **Price Risk**: Within reasonable range
- **Location Risk**: Target counties preferred
- **Condition Risk**: Turnkey properties preferred

### Sample Analysis Output

```
Property: 123 Main St, Seattle, WA
Price: $750,000
Viability Score: 85.5% ✅ VIABLE

Basic Analysis: 82% (4 beds, 3 baths, 2,500 sqft, rambler)
Financial Analysis: 88% ($4,200/month cash flow, 12% cap rate)
Market Analysis: 75% (Above market price, high demand area)
WABO Analysis: 95% (WABO approved, 1-3 month timeline)
Risk Assessment: 85% (Low risk, good location)

Recommendations:
- Target negotiation price: $720,000
- Use WABO approval as negotiation leverage
- Emphasize quick closing and cash offer
- Budget $5,000 for licensing costs
```

### Understanding Financial Projections

#### Monthly Revenue Calculation
```
Medicaid Residents: 2 × $120/day × 30 days × 85% occupancy = $6,120
Private Pay Residents: 2 × $200/day × 30 days × 85% occupancy = $10,200
Total Monthly Revenue: $16,320
```

#### Monthly Expenses
```
Utilities: $800
Insurance: $400
Maintenance: $600
Supplies: $500
Licensing Fees: $200
Total Operating Expenses: $2,500
```

#### Debt Service
```
Loan Amount: $750,000 × 80% = $600,000
Monthly Payment (6%, 30-year): $3,597
```

#### Cash Flow
```
Monthly Revenue: $16,320
Operating Expenses: $2,500
Debt Service: $3,597
Monthly Cash Flow: $10,223
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors

**Problem**: `ModuleNotFoundError` when running the system

**Solution**:
```bash
# Ensure you're in the correct directory
cd afh-property-scout

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

#### 2. Database Errors

**Problem**: Database connection or permission errors

**Solution**:
```bash
# Check if data directory exists and is writable
ls -la data/
chmod 755 data/

# Reinitialize database
rm data/afh_properties.db
python -c "from src.storage.database import DatabaseManager; import yaml; config = yaml.safe_load(open('config/settings.yaml')); DatabaseManager(config['database'])"
```

#### 3. Email Notifications Not Working

**Problem**: No email notifications received

**Solution**:
```bash
# Check .env file
cat .env | grep EMAIL

# Test email configuration
python -c "
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
print('Email configuration working!')
server.quit()
"
```

#### 4. No Properties Found

**Problem**: System runs but finds no properties

**Solution**:
```bash
# Check internet connection
ping google.com

# Verify search criteria
cat config/settings.yaml | grep -A 10 "property_criteria"

# Test individual scrapers
python -c "
from src.scrapers.property_scraper import PropertyScraper
import yaml
config = yaml.safe_load(open('config/settings.yaml'))
scraper = PropertyScraper(config['search_sources'])
properties = scraper.search_all_sources()
print(f'Found {len(properties)} properties')
"
```

#### 5. High Memory Usage

**Problem**: System uses too much memory

**Solution**:
```yaml
# Reduce search frequency in config/settings.yaml
schedule:
  search_frequency_hours: 48  # Every 2 days instead of daily

# Limit number of properties analyzed
property_criteria:
  max_properties_per_search: 50
```

#### 6. Rate Limiting Issues

**Problem**: Getting blocked by websites

**Solution**:
```yaml
# Increase delays in config/settings.yaml
rate_limiting:
  requests_per_minute: 15  # Reduce from 30
  delay_between_requests: 5  # Increase from 2 seconds
```

### Log Analysis

Check the logs for detailed error information:

```bash
# View recent logs
tail -f logs/afh_scout.log

# Search for errors
grep -i error logs/afh_scout.log

# Search for specific issues
grep -i "email\|sms\|database" logs/afh_scout.log
```

### Performance Optimization

#### For Large-Scale Operations

```yaml
# config/settings.yaml optimizations
database:
  type: "postgresql"  # Use PostgreSQL for better performance
  connection_pool_size: 10

rate_limiting:
  requests_per_minute: 20
  delay_between_requests: 3
  concurrent_requests: 3

search_sources:
  # Disable slower sources if needed
  real_estate:
    - "zillow"
    - "redfin"
  # Remove social_media if not needed
```

---

## Best Practices

### 1. Regular Maintenance

**Weekly Tasks**:
- Check logs for errors
- Review property summary
- Update search criteria if needed
- Backup database

**Monthly Tasks**:
- Review financial assumptions
- Update target counties if expanding
- Analyze success rates
- Update notification preferences

### 2. Database Management

```bash
# Regular backup
cp data/afh_properties.db backups/afh_properties_$(date +%Y%m%d).db

# Clean old data (optional)
python -c "
from src.storage.database import DatabaseManager
import yaml
config = yaml.safe_load(open('config/settings.yaml'))
db = DatabaseManager(config['database'])
# Add cleanup logic here
"
```

### 3. Monitoring and Alerts

Set up external monitoring for:
- System uptime
- Database size
- Error rates
- Notification delivery

### 4. Security Best Practices

- Use app passwords, not regular passwords
- Regularly rotate API keys
- Keep dependencies updated
- Monitor for unusual activity
- Use VPN if accessing from public networks

### 5. Scaling for Multiple Users

For team use:
- Set up shared database (PostgreSQL)
- Configure multiple notification recipients
- Use role-based access control
- Implement audit logging

---

## FAQ

### General Questions

**Q: How often should I run searches?**
A: Daily searches are recommended. The system is designed to run automatically every morning at 8 AM.

**Q: Can I use this for other types of properties?**
A: The system is specifically designed for AFH properties, but you can modify the criteria in the configuration file.

**Q: Is my data secure?**
A: Yes, all data is stored locally on your machine. No property data is shared with third parties.

**Q: Can I run this on multiple computers?**
A: Yes, but each instance will have its own database. For team use, consider setting up a shared database.

### Technical Questions

**Q: What if a website changes its structure?**
A: The scrapers are designed to be resilient, but major changes may require updates. Check the logs for parsing errors.

**Q: How much internet bandwidth does this use?**
A: Minimal. The system makes efficient requests and caches data locally.

**Q: Can I add new property sources?**
A: Yes, you can create new scrapers by extending the BaseScraper class.

**Q: What if I get rate limited?**
A: The system includes built-in rate limiting. If you still get blocked, increase the delays in the configuration.

### Financial Questions

**Q: How accurate are the financial projections?**
A: The projections are based on standard AFH industry assumptions. You should adjust the rates in the configuration to match your local market.

**Q: What if my operating costs are different?**
A: You can customize all financial assumptions in the `afh_analysis` section of the configuration file.

**Q: How do I know if a property is really viable?**
A: The system provides a viability score and detailed analysis. Always conduct your own due diligence before making offers.

### Notification Questions

**Q: Can I get notifications for all properties, not just viable ones?**
A: Yes, you can modify the notification logic in the source code or adjust the viability threshold.

**Q: How do I stop receiving notifications?**
A: Set `enabled: false` in the notification configuration or stop the scheduler.

**Q: Can I customize the notification content?**
A: Yes, you can modify the notification templates in the source code.

---

## Support and Resources

### Getting Help

- **Email Support**: support@afhpropertyscout.com
- **Community Forum**: [Discord Server](https://discord.gg/afhscout)
- **Documentation**: This manual and online docs
- **Video Tutorials**: [YouTube Channel](https://youtube.com/afhscout)

### Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Reporting bugs
- Suggesting features
- Submitting code changes
- Improving documentation

### Updates

The system is regularly updated with:
- New property sources
- Improved analysis algorithms
- Bug fixes and performance improvements
- New features and capabilities

Check the [Releases](https://github.com/your-repo/afh-property-scout/releases) page for updates.

---

*This manual is regularly updated. Check for the latest version at [afhpropertyscout.com/docs](https://afhpropertyscout.com/docs)*

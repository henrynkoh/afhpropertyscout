# AFH Property Scout - Installation Guide

## Quick Start

1. **Clone or download the project**
   ```bash
   cd afh-property-scout
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure your credentials**
   Edit the `.env` file with your actual credentials:
   ```bash
   nano .env
   ```

4. **Run your first search**
   ```bash
   python run_scout.py --search
   ```

## Manual Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Directories

```bash
mkdir -p data logs templates static/css static/js config
```

### Step 3: Configure Environment

Copy the environment template and edit with your credentials:

```bash
cp env_example.txt .env
nano .env
```

### Step 4: Initialize Database

```bash
python -c "from src.storage.database import DatabaseManager; import yaml; config = yaml.safe_load(open('config/settings.yaml')); DatabaseManager(config['database'])"
```

## Configuration

### Email Setup (Gmail)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the app password in your `.env` file

### SMS Setup (Twilio)

1. Sign up for a Twilio account
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase a phone number for sending SMS
4. Add these credentials to your `.env` file

### Social Media APIs

#### Facebook
1. Create a Facebook App at https://developers.facebook.com/
2. Generate an access token
3. Add to `.env` file

#### Twitter/X
1. Create a Twitter Developer account
2. Create a new app and get API keys
3. Add to `.env` file

## Usage

### Basic Commands

```bash
# Run one-time search
python run_scout.py --search

# Run daily search
python run_scout.py --daily

# Start daily scheduler (runs at 8 AM daily)
python run_scout.py --schedule

# Check for new notifications
python run_scout.py --notify

# Show property summary
python run_scout.py --summary

# Start web dashboard
python run_dashboard.py
```

### Web Dashboard

The web dashboard provides a visual interface for monitoring your property searches:

- **URL**: http://localhost:5000
- **Features**:
  - Property summary statistics
  - Interactive charts and graphs
  - Property listings with details
  - Viability score analysis

### Daily Automation

To run the system automatically every day:

1. **Using the built-in scheduler**:
   ```bash
   python run_scout.py --schedule
   ```

2. **Using system cron (Linux/Mac)**:
   ```bash
   # Edit crontab
   crontab -e
   
   # Add this line to run daily at 8 AM
   0 8 * * * cd /path/to/afh-property-scout && python run_scout.py --daily
   ```

3. **Using Windows Task Scheduler**:
   - Create a new task
   - Set trigger to daily at 8:00 AM
   - Set action to run: `python run_scout.py --daily`

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running from the project root directory
   - Check that all dependencies are installed: `pip list`

2. **Database Errors**
   - Ensure the `data` directory exists and is writable
   - Check database permissions

3. **Email/SMS Not Working**
   - Verify credentials in `.env` file
   - Check internet connection
   - Ensure app passwords are used (not regular passwords)

4. **No Properties Found**
   - Check internet connection
   - Verify search criteria in `config/settings.yaml`
   - Some scrapers may need additional configuration

### Logs

Check the logs for detailed error information:

```bash
tail -f logs/afh_scout.log
```

### Configuration Files

- `config/settings.yaml` - Main configuration
- `.env` - Environment variables (credentials)
- `requirements.txt` - Python dependencies

## Advanced Configuration

### Custom Search Criteria

Edit `config/settings.yaml` to customize:

- Target counties
- Property criteria (beds, baths, sqft)
- Price ranges
- Search sources
- Notification settings

### Adding New Sources

To add new property sources:

1. Create a new scraper class in `src/scrapers/`
2. Inherit from `BaseScraper`
3. Implement the `search_afh_properties()` method
4. Add to the sources configuration

### Custom Analysis

Modify `src/analyzers/afh_analyzer.py` to:

- Adjust financial assumptions
- Change viability scoring
- Add new analysis criteria
- Modify recommendation logic

## Support

For issues or questions:

1. Check the logs: `logs/afh_scout.log`
2. Review the configuration files
3. Ensure all dependencies are installed
4. Verify internet connectivity
5. Check API credentials and limits

## Security Notes

- Never commit the `.env` file to version control
- Use app passwords instead of regular passwords
- Regularly rotate API keys and tokens
- Monitor usage to avoid rate limits
- Keep dependencies updated for security patches

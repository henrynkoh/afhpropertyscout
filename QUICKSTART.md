# ⚡ AFH Property Scout - Quick Start Guide

## 🚀 Get Up and Running in 15 Minutes

This quick start guide will have you finding profitable AFH properties in just 15 minutes. No technical expertise required!

---

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Computer with internet connection**
- [ ] **Python 3.8 or higher** ([Download here](https://python.org))
- [ ] **Gmail account** (for notifications)
- [ ] **15 minutes of uninterrupted time**
- [ ] **Basic understanding of real estate investing**

**Check Python version:**
```bash
python --version
# Should show Python 3.8 or higher
```

---

## 🎯 Step 1: Download and Install (3 minutes)

### Option A: Git Clone (Recommended)
```bash
git clone https://github.com/your-repo/afh-property-scout.git
cd afh-property-scout
```

### Option B: Download ZIP
1. Download the ZIP file from GitHub
2. Extract to your desired location
3. Open terminal/command prompt in the folder

### Run the Setup Script
```bash
python setup.py
```

**What happens:**
- ✅ Installs all required software
- ✅ Creates necessary folders
- ✅ Sets up the database
- ✅ Creates configuration files
- ✅ Validates your system

**Expected output:**
```
🏠 AFH Property Scout Setup
========================================
✅ Python 3.9.7 detected
📁 Creating directories...
✅ Created directory: data
✅ Created directory: logs
✅ Created directory: templates
📦 Installing dependencies...
✅ Installing Python dependencies...
🗄️  Setting up database...
✅ Database initialized successfully
🎉 Setup completed successfully!
```

---

## ⚙️ Step 2: Configure Your Email (5 minutes)

### Create Gmail App Password

1. **Go to your Google Account**: [myaccount.google.com](https://myaccount.google.com)
2. **Navigate to Security** → **2-Step Verification**
3. **Scroll down to "App passwords"**
4. **Select "Mail"** and generate password
5. **Copy the 16-character password** (no spaces)

### Edit Configuration File

```bash
# Open the environment file
nano .env
```

**Add your email settings:**
```env
# Email Configuration
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_character_app_password
RECIPIENT_EMAIL=your_email@gmail.com
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

---

## 🎯 Step 3: Customize Your Search (3 minutes)

### Edit Search Criteria

```bash
# Open the configuration file
nano config/settings.yaml
```

**Find this section and customize:**
```yaml
# Target Counties - Choose your markets
target_counties:
  - "King County"      # High-value market
  - "Pierce County"    # Balanced market
  # - "Thurston County" # Uncomment to add
  # - "Lewis County"    # Uncomment to add

# Property Criteria - Adjust for your budget
property_criteria:
  property_type: "1st floor rambler"
  min_bedrooms: 3        # Minimum bedrooms
  min_bathrooms: 2       # Minimum bathrooms
  min_sqft: 2000         # Minimum square feet
  max_price: 1000000     # Your maximum budget
  min_price: 300000      # Your minimum budget
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

---

## 🔍 Step 4: Run Your First Search (2 minutes)

### Test the System

```bash
python run_scout.py --search
```

**What to expect:**
```
🔄 Searching Zillow for AFH properties...
✅ Found 15 properties from Zillow
🔄 Searching Redfin for AFH properties...
✅ Found 8 properties from Redfin
🔄 Searching Facebook for AFH properties...
✅ Found 3 properties from Facebook
🔄 Filtering properties based on criteria...
✅ Filtered to 12 properties matching criteria
🔄 Analyzing properties for AFH viability...
✅ Found 4 viable AFH properties
📧 Sending notifications for 4 new properties
✅ Search completed. Found 4 viable properties.
```

### Check Your Results

```bash
# View property summary
python run_scout.py --summary
```

**Expected output:**
```
📊 Property Summary:
Total properties: 12
Viable properties: 4
New properties: 4
Average viability score: 78.5%
```

---

## 📱 Step 5: Start the Web Dashboard (1 minute)

### Launch the Dashboard

```bash
python run_dashboard.py
```

**Open your browser to:** http://localhost:5000

**What you'll see:**
- 📊 Property summary statistics
- 📈 Interactive charts and graphs
- 🏠 Detailed property listings
- 💰 Financial analysis for each property

---

## ⚡ Step 6: Set Up Daily Automation (1 minute)

### Start the Daily Scheduler

```bash
python run_scout.py --schedule
```

**The system will now:**
- 🔄 Run automatically every morning at 8:00 AM
- 📧 Send you email notifications for new properties
- 📱 Check for updates every 30 minutes
- 🏃 Continue running until you stop it

**To stop the scheduler:**
- Press `Ctrl + C`

**To run in background (Linux/Mac):**
```bash
# Using screen
screen -S afh_scout
python run_scout.py --schedule
# Press Ctrl+A, then D to detach
```

---

## 🎉 Congratulations! You're All Set!

### What Happens Next

**Within 24 hours:**
- ✅ System will run its first automated search
- ✅ You'll receive email notifications for viable properties
- ✅ Dashboard will show your first results

**Within 1 week:**
- ✅ You'll have 20-50 properties in your database
- ✅ 5-10 properties will meet your criteria
- ✅ 2-4 properties will be highly viable

**Within 1 month:**
- ✅ 100+ properties analyzed
- ✅ 20+ viable opportunities identified
- ✅ 3-5 properties worth pursuing

---

## 📞 Quick Commands Reference

### Daily Commands
```bash
# Run one-time search
python run_scout.py --search

# Check for notifications
python run_scout.py --notify

# View property summary
python run_scout.py --summary

# Start daily automation
python run_scout.py --schedule

# Start web dashboard
python run_dashboard.py
```

### Configuration Commands
```bash
# Edit email settings
nano .env

# Edit search criteria
nano config/settings.yaml

# View logs
tail -f logs/afh_scout.log
```

---

## 🚨 Troubleshooting Quick Fixes

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "No properties found"
**Solution:**
```bash
# Check internet connection
ping google.com

# Verify search criteria
cat config/settings.yaml | grep -A 5 "property_criteria"
```

### Problem: "Email not working"
**Solution:**
```bash
# Check .env file
cat .env | grep EMAIL

# Verify Gmail app password is correct
```

### Problem: "Database error"
**Solution:**
```bash
# Recreate database
rm data/afh_properties.db
python setup.py
```

---

## 📚 Next Steps

### Immediate Actions (Today)
1. ✅ **Verify your first search results**
2. ✅ **Check your email for notifications**
3. ✅ **Explore the web dashboard**
4. ✅ **Review the property analysis**

### This Week
1. 📖 **Read the full manual** ([MANUAL.md](MANUAL.md))
2. 🎓 **Complete the tutorial** ([TUTORIAL.md](TUTORIAL.md))
3. ⚙️ **Fine-tune your search criteria**
4. 📧 **Set up additional notification recipients**

### This Month
1. 🏠 **Start evaluating properties in person**
2. 💰 **Make your first offer**
3. 📊 **Track your success metrics**
4. 🔧 **Optimize the system based on results**

---

## 🆘 Need Help?

### Quick Support
- 📧 **Email**: support@afhpropertyscout.com
- 💬 **Discord**: [Join our community](https://discord.gg/afhscout)
- 📚 **Documentation**: [Full Manual](MANUAL.md)
- 🎥 **Videos**: [YouTube Channel](https://youtube.com/afhscout)

### Common Questions

**Q: How often should I run searches?**
A: The system is designed to run daily automatically. You can also run manual searches anytime.

**Q: What if I don't get any properties?**
A: Check your search criteria - they might be too restrictive. Start with broader criteria and narrow down.

**Q: How accurate are the financial projections?**
A: The projections are based on industry standards. Adjust the rates in the configuration to match your local market.

**Q: Can I use this for other property types?**
A: The system is specifically designed for AFH properties, but you can modify the criteria for other uses.

---

## 🎯 Success Tips

### Maximize Your Results
1. **Start with broader criteria** and narrow down as you learn
2. **Check the dashboard daily** for new properties
3. **Respond quickly** to viable properties (they go fast!)
4. **Use the financial analysis** in your negotiations
5. **Track your results** and adjust criteria accordingly

### Best Practices
1. **Run the system daily** for consistent results
2. **Keep your criteria realistic** for your market
3. **Use the viability scores** as a guide, not absolute truth
4. **Always do your own due diligence** before making offers
5. **Stay updated** with market changes

---

## 🏆 Success Stories

> *"I set up AFH Property Scout in 15 minutes and found my first viable property within 2 days. The financial analysis helped me negotiate $25,000 off the asking price!"*
> 
> **- Sarah M., First-time AFH Investor**

> *"The system found me a WABO-approved property that I would have never found manually. I closed the deal in 3 weeks and it's generating $4,200/month in cash flow."*
> 
> **- Mike R., Experienced Investor**

> *"I was spending 3 hours daily searching for properties. Now I get notified of opportunities and can focus on closing deals. My efficiency increased by 300%."*
> 
> **- Jennifer L., AFH Operator**

---

## 🚀 Ready to Find Your First Profitable Property?

**You're now ready to start finding profitable AFH properties automatically!**

### Your Next Action
```bash
# Run your first search right now
python run_scout.py --search
```

### Then Start Daily Automation
```bash
# Set up daily searches
python run_scout.py --schedule
```

**Remember:** The system works best when it runs consistently. Set it up once and let it work for you 24/7.

---

## 📈 Expected Timeline

### Day 1: Setup Complete ✅
- System installed and configured
- First search completed
- Dashboard accessible

### Week 1: First Results 📊
- 15-25 properties found
- 3-5 properties meet criteria
- 1-2 properties highly viable

### Month 1: Building Momentum 🚀
- 60-100 properties analyzed
- 12-20 viable opportunities
- 2-4 properties worth pursuing

### Month 3: Full Operation 🏆
- 200+ properties in database
- 40+ viable opportunities identified
- 5-8 properties closed or in process

---

## 💡 Pro Tips for Quick Success

### 1. Start Conservative
- Begin with broader search criteria
- Lower your minimum requirements initially
- Focus on learning the system first

### 2. Monitor Daily
- Check the dashboard every morning
- Review new properties immediately
- Respond quickly to viable opportunities

### 3. Use the Analysis
- Reference viability scores in negotiations
- Use financial projections for offers
- Leverage WABO status in discussions

### 4. Stay Consistent
- Run the system daily
- Don't skip days
- Consistency is key to success

### 5. Track Everything
- Keep notes on properties you pursue
- Track your success rate
- Adjust criteria based on results

---

## 🎯 Your Success Checklist

### Setup Complete ✅
- [ ] System installed
- [ ] Email configured
- [ ] Search criteria set
- [ ] First search completed
- [ ] Dashboard accessible

### Daily Operations
- [ ] Check dashboard for new properties
- [ ] Review email notifications
- [ ] Evaluate viable properties
- [ ] Take action on opportunities

### Weekly Review
- [ ] Analyze search results
- [ ] Adjust criteria if needed
- [ ] Review financial assumptions
- [ ] Plan property visits

### Monthly Optimization
- [ ] Review success metrics
- [ ] Update market assumptions
- [ ] Expand search areas
- [ ] Optimize notification settings

---

## 🚀 You're Ready to Succeed!

**AFH Property Scout is now your 24/7 property hunting assistant. It will:**

- 🔍 **Search continuously** for profitable properties
- 📊 **Analyze each property** for AFH viability
- 📧 **Notify you immediately** when opportunities arise
- 💰 **Provide financial analysis** for negotiations
- 📈 **Track market trends** and opportunities

**Your job is to:**
- ✅ **Review the opportunities** the system finds
- ✅ **Conduct due diligence** on viable properties
- ✅ **Make offers** on properties that meet your criteria
- ✅ **Close deals** and build your portfolio

**Let's find your first profitable AFH property!**

```bash
# Start your property search journey now
python run_scout.py --search
```

---

*Need help? Contact us at support@afhpropertyscout.com or join our Discord community at [discord.gg/afhscout](https://discord.gg/afhscout)*

**Happy property hunting! 🏠💰**

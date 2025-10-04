# CODPARTNER Automation

Automated inventory download from CODPARTNER website.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip3 install -r requirements.txt

# Install Playwright browsers (one-time setup)
playwright install chromium
```

### 2. Setup Credentials

Create a `.env` file with your CODPARTNER credentials:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

Your `.env` file should look like:
```
CODPARTNER_USERNAME=your_email@example.com
CODPARTNER_PASSWORD=your_password_here
```

### 3. Run the Automation

```bash
python3 download_inventory.py
```

That's it! The script will:
- ✅ Login to CODPARTNER
- ✅ Navigate to inventory page
- ✅ Set view to 100 entries
- ✅ Download and save the HTML
- ✅ Auto-name file with today's date (e.g., `Inventory - OCT05.html`)
- ✅ Clean up old files (keeps last 7 days)

## 📁 Project Structure

```
Stock management/
├── automation/
│   ├── __init__.py
│   ├── config.py          # Settings & credentials
│   ├── codpartner.py      # Main automation class
│   └── utils.py           # Helper functions
├── download_inventory.py   # Run this daily
├── compare_inventory.py    # Compare tool (existing)
├── .env                    # Your credentials (not in git)
└── requirements.txt        # Dependencies
```

## 🎯 Daily Workflow

### Manual Run (Recommended for now)
```bash
python3 download_inventory.py
python3 compare_inventory.py
```

### See the Browser (for debugging)
Edit `automation/config.py` and set:
```python
SHOW_BROWSER = True
```

## 🔧 Configuration

Edit `automation/config.py` to customize:

```python
class Config:
    # Settings
    SHOW_BROWSER = False      # Set True to see browser
    ENTRIES_TO_SHOW = 100     # Number of entries per page
    TIMEOUT = 30000           # 30 seconds
```

## 🚧 Future Features (Ready to Expand)

The structure is built to easily add:

### 1. Download Confirmations/Deliveries
```python
# In download_inventory.py, add:
bot.download_confirmations()
bot.download_deliveries()
```

### 2. Custom Date Ranges
```python
# For products/orders metrics
bot.download_with_date_range(start_date='2025-10-01', end_date='2025-10-05')
```

### 3. Schedule Automation
Use cron (Mac/Linux) or Task Scheduler (Windows)

**Mac/Linux (cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /Users/zak/Downloads/Stock\ management && /usr/local/bin/python3 download_inventory.py
```

## 🛠️ Troubleshooting

### "Credentials not set" error
- Make sure `.env` file exists
- Check that it has your actual credentials
- File should be in the same directory as `download_inventory.py`

### Playwright not found
```bash
pip3 install playwright
playwright install chromium
```

### Login fails
- Check credentials in `.env`
- Try setting `SHOW_BROWSER = True` to see what's happening
- Website might have changed - check selectors in `codpartner.py`

### Timeout errors
- Increase timeout in `config.py`: `TIMEOUT = 60000` (60 seconds)
- Check your internet connection

## 📊 Integration with Compare Tool

The automation creates files that work seamlessly with your existing compare tool:

```bash
# 1. Download inventory (automated)
python3 download_inventory.py

# 2. Compare with previous day (automated)
python3 compare_inventory.py

# Boom! CSV report ready to view
```

## 🔐 Security Notes

- ✅ Credentials stored in `.env` (not in git)
- ✅ `.env` is in `.gitignore`
- ✅ Never commit your `.env` file
- ✅ Use strong passwords

## 📝 To Do

- [ ] Add confirmation/delivery downloads
- [ ] Implement custom date range selector
- [ ] Add email notifications for completion/errors
- [ ] Create dashboard for trends
- [ ] Add scheduling documentation

---

**Built for expansion. Start simple, grow as needed! 🌱**

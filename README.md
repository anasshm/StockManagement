# Stock Management Tool

Complete automation for daily stock management with CODPARTNER inventory tracking.

## What it does

- **Automatically downloads** today's inventory from CODPARTNER
- **Compares** with yesterday's inventory
- **Finds active products** (products where stock changed)
- **Calculates sold products** (old stock - new stock)
- **Sorts by most sold** (highest first)
- **Creates clean CSV report** (`Stock_OCT04.csv`)

## Quick Start

### First Time Setup

See [SETUP.md](SETUP.md) for detailed first-time setup instructions.

Quick version:
```bash
# 1. Install dependencies
pip3 install -r requirements.txt
playwright install chromium

# 2. Set up credentials
cp .env.example .env
# Edit .env and add your CODPARTNER credentials

# 3. Done! Ready to use
```

## Daily Usage

### Automatic (Runs Hourly)

The automation **runs automatically** in the background!

- ✅ **Runs every hour** - Checks if today's report needs to be created
- ✅ **Runs at login** - Also triggers when you log in to your Mac
- ✅ **Smart checking**: Only downloads if today's file doesn't exist yet
- ✅ **No duplicates**: Won't re-run if today's files already exist
- ✅ **Background operation**: Runs invisibly, no browser windows

Your daily report is ready automatically - just check for today's CSV file!

### Manual Run

You can also run it manually anytime:

```bash
python3 stock_update.py
```

This will:
1. ✅ Check if today's report already exists (skips if found)
2. ✅ Download today's inventory (headless/invisible)
3. ✅ Compare with yesterday
4. ✅ Create your CSV report (`Stock_OCT07.csv`)

## Output

CSV file named `Stock_OCT04.csv` (date changes daily) with:
- Product Name
- Warehouse
- Old Expected Stock (e.g., Inventory-OCT03)
- New Expected Stock (e.g., Inventory-OCT04)
- Sold Products (calculated: old - new)

**Results sorted by Sold Products (highest first)**

## Example Output

```bash
$ python3 stock_update.py

============================================================
🚀 STOCK UPDATE - Complete Daily Report
============================================================

📊 STEP 1: Downloading Inventory
✅ Inventory downloaded successfully

📊 STEP 2: Comparing Inventory
✅ Found 24 active products

📈 SUMMARY
============================================================
Top 5 Best Sellers:
  1. Fourleaf Bracelet
     Warehouse: Riyadh warehouse
     Sold: 34 | Remaining: 253
  
  ... (more products)

✅ COMPLETE! Your stock report is ready
📄 Check your Stock_OCT04.csv file
```

## Alternative Scripts

- **`stock_update.py`** - Main script (download + compare)
- **`download_inventory.py`** - Download only (no comparison)
- **`compare_inventory.py`** - Compare only (no download)
- **`daily_report.py`** - Legacy combined script

## Recording & Replay System

**New!** Debug automation issues by recording real browser actions.

When automation fails to find elements you can see, use the recording system:

```bash
# 1. Record your actions
python3 record_session.py

# 2. Edit automation/analytics_recorded.py and paste the generated code

# 3. Test the replay
python3 replay_recorded_session.py

# 4. View visual trace with screenshots
python3 view_trace.py
```

See [RECORDING_GUIDE.md](RECORDING_GUIDE.md) for complete instructions.

**Use cases:**
- Debug date selection issues
- Capture working element selectors
- Create visual reference documentation
- Test new workflows before automating

## Settings

Edit `automation/config.py` to customize:
- `SHOW_BROWSER = False` - Headless (invisible) browser
- `ENTRIES_TO_SHOW = 100` - Products per page
- `TIMEOUT = 30000` - Page load timeout

## Automation Details

The script automatically runs at login via macOS LaunchAgent:
- **Service**: `com.stockmanagement.daily`
- **Config**: `~/Library/LaunchAgents/com.stockmanagement.daily.plist`
- **Logs**: `logs/stock_update.log` and `logs/stock_update_error.log`

To check automation status:
```bash
launchctl list com.stockmanagement.daily
```

To disable automation:
```bash
launchctl unload ~/Library/LaunchAgents/com.stockmanagement.daily.plist
```

To re-enable automation:
```bash
launchctl load ~/Library/LaunchAgents/com.stockmanagement.daily.plist
```

## Future Ideas

- ✅ ~~Automated download~~ (DONE!)
- ✅ ~~Clean CSV output~~ (DONE!)
- ✅ ~~Scheduled automation~~ (DONE! Runs at login)
- 📊 Google Sheets integration
- 📧 Email notifications
- 📈 Historical trends
- ⚠️ Low-stock alerts

---

**Simple. Automated. Effective. 🚀**

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

**One simple command:**

```bash
python3 stock_update.py
```

That's it! This will:
1. ✅ Download today's inventory (headless/invisible)
2. ✅ Compare with yesterday
3. ✅ Create your CSV report (`Stock_OCT04.csv`)

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

## Settings

Edit `automation/config.py` to customize:
- `SHOW_BROWSER = False` - Headless (invisible) browser
- `ENTRIES_TO_SHOW = 100` - Products per page
- `TIMEOUT = 30000` - Page load timeout

## Future Ideas

- ✅ ~~Automated download~~ (DONE!)
- ✅ ~~Clean CSV output~~ (DONE!)
- ⏰ Scheduled automation (cron)
- 📊 Google Sheets integration
- 📧 Email notifications
- 📈 Historical trends
- ⚠️ Low-stock alerts

---

**Simple. Automated. Effective. 🚀**

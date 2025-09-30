# Setup Guide

## First Time Setup

### 1. Check if Python is installed

Open Terminal and type:

```bash
python3 --version
```

If you see something like `Python 3.x.x`, you're good! ✅

If not, install Python from: https://www.python.org/downloads/

### 2. Install BeautifulSoup

Open Terminal, navigate to this folder, and run:

```bash
pip3 install beautifulsoup4
```

That's it! You're ready to go.

## Daily Usage

1. Download today's inventory HTML from CODPARTNER
2. Rename files (or edit script) to match expected names
3. Run:

```bash
python3 compare_inventory.py
```

4. Open `inventory_comparison.csv` to see results

## Troubleshooting

**Problem:** "No module named bs4"
- Solution: Run `pip3 install beautifulsoup4`

**Problem:** "File not found"
- Solution: Make sure HTML files are in the same folder as the script
- Or check the file names in the script match your files

**Problem:** "Permission denied"
- Solution: Run `chmod +x compare_inventory.py` first

---

Need help? Check the error message or ask! 😊

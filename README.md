# Stock Management Tool

Simple Python script to compare daily inventory snapshots and identify active products.

## What it does

- Compares two HTML inventory files (old date vs new date)
- Finds **active products** (products where expected stock changed)
- Calculates **sold products** (old stock - new stock)
- Sorts by **most sold** (highest first)
- Outputs a clean CSV file

## Requirements

Install Python dependencies (only needed once):

```bash
pip install beautifulsoup4
```

## How to Use

### Quick Start

1. Download your inventory HTML files from CODPARTNER
2. Place them in this folder (same folder as `compare_inventory.py`)
3. Run the script:

```bash
python3 compare_inventory.py
```

### File Names

The script looks for these files by default:
- `Inventory - sep28.html` (old)
- `Inventory - SEP30.html` (new)

If your files have different names, either:
- Rename them to match the default names, OR
- Edit `compare_inventory.py` lines 123-124 to use your file names

### Output

The script creates `inventory_comparison.csv` with these columns:
- Product Name
- Warehouse
- Old Expected Stock (e.g., sep28)
- New Expected Stock (e.g., sep30)
- Sold Products (calculated: old - new)

**Results are sorted by Sold Products (highest first)**

## Example

```bash
$ python3 compare_inventory.py

============================================================
📊 Stock Management - Inventory Comparison
============================================================
📂 Reading old inventory: Inventory - sep28.html
   Found 135 products
📂 Reading new inventory: Inventory - SEP30.html
   Found 139 products
✅ Found 45 active products (with stock changes)
💾 Saved results to: inventory_comparison.csv

============================================================
📈 SUMMARY
============================================================
Top 5 Best Sellers:
  1. Fourleaf Bracelet
     Warehouse: Riyadh warehouse
     Sold: 298 | Remaining: 314
  
  ... (more products)

✨ Done! Open the CSV file to view all results.
============================================================
```

## Future Enhancements (Ideas for later)

- Track trends over time
- Set low-stock alerts
- Visualize best sellers
- Web interface for uploading files
- Automated daily reports

---

**Keep it simple for now. Improve as needed! 🚀**

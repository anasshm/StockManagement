#!/usr/bin/env python3
"""
Generate Stock History with 7-day view
Creates a single Stock_History.csv file that gets replaced daily
Shows products with ANY stock changes in the last 7 days
"""

from bs4 import BeautifulSoup
import csv
from pathlib import Path
from datetime import datetime


def parse_inventory_html(html_file):
    """
    Parse inventory HTML file and extract product data
    Returns: dict with key=(product_name, warehouse) and value=expected_stock
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    inventory = {}
    
    # Find all table rows with data
    rows = soup.find_all('tr', role='row')
    
    for row in rows:
        tds = row.find_all('td')
        if len(tds) < 5:  # Skip if not enough columns
            continue
        
        try:
            # Extract product name from h6 tag
            product_name_tag = tds[0].find('h6')
            if not product_name_tag:
                continue
            product_name = product_name_tag.get_text(strip=True)
            
            # Extract warehouse (text after the flag icon)
            warehouse_td = tds[1]
            warehouse = warehouse_td.get_text(strip=True)
            
            # Extract expected remaining stock (5th column, index 4)
            expected_stock_text = tds[4].get_text(strip=True)
            expected_stock = int(expected_stock_text)
            
            # Use (product_name, warehouse) as unique key
            key = (product_name, warehouse)
            inventory[key] = expected_stock
            
        except (ValueError, AttributeError, IndexError):
            # Skip rows that don't have proper data
            continue
    
    return inventory


def extract_date_from_filename(filepath):
    """
    Extract date part from filename
    Example: 'Inventory - OCT12.html' -> 'OCT12'
    """
    import re
    filename = Path(filepath).name
    
    # Try to find date pattern
    pattern = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\s-]?(\d{1,2})'
    match = re.search(pattern, filename, re.IGNORECASE)
    
    if match:
        month = match.group(1).upper()
        day = match.group(2).zfill(2)
        return f"{month}{day}"
    
    # Fallback: use full filename if no date pattern found
    return Path(filepath).stem.replace(' ', '-')


def find_html_files(directory):
    """Find all inventory HTML files and sort by modification time (oldest first)"""
    # Only match inventory files, not orders or analytics
    html_files = list(Path(directory).glob("Inventory*.html"))
    
    if len(html_files) == 0:
        return []
    
    # Sort by modification time (oldest to newest)
    html_files.sort(key=lambda x: x.stat().st_mtime)
    
    return html_files


def generate_history(files):
    """
    Generate 7-day history for all products with stock changes
    Returns: (active_products, date_columns)
    """
    # Parse all files and store inventories
    inventories = []
    date_columns = []
    
    for file in files:
        print(f"📂 Reading inventory: {file.name}")
        inventory = parse_inventory_html(file)
        print(f"   Found {len(inventory)} products")
        
        date = extract_date_from_filename(file)
        inventories.append({'date': date, 'data': inventory})
        date_columns.append(date)
    
    # Get today's and yesterday's inventory for sold calculation
    today_inventory = inventories[-1]['data']
    yesterday_inventory = inventories[-2]['data']
    
    active_products = []
    
    # Find all unique products across all inventories
    all_product_keys = set()
    for inv in inventories:
        all_product_keys.update(inv['data'].keys())
    
    # Check each product to see if it had any stock changes in the last 7 days
    for key in all_product_keys:
        product_name, warehouse = key
        
        # Check if product had any stock changes across the 7 days
        had_changes = False
        stock_values = []
        
        for inv in inventories:
            if key in inv['data']:
                stock_values.append(inv['data'][key])
            else:
                stock_values.append(None)
        
        # Check if stock changed at any point (sales or restocking)
        for i in range(len(stock_values) - 1):
            if stock_values[i] is not None and stock_values[i+1] is not None:
                if stock_values[i] != stock_values[i+1]:  # Any stock change
                    had_changes = True
                    break
        
        # Only include products that had any stock changes in the last 7 days
        if had_changes:
            # Calculate sold products as today vs yesterday
            if key in yesterday_inventory and key in today_inventory:
                sold = yesterday_inventory[key] - today_inventory[key]
            else:
                sold = 0
            
            # Build product entry with history
            product_entry = {
                'Product Name': product_name,
                'Warehouse': warehouse,
            }
            
            # Add stock data for each day in history
            for inv in inventories:
                date = inv['date']
                if key in inv['data']:
                    product_entry[date] = inv['data'][key]
                else:
                    product_entry[date] = '-'
            
            # Add sold products (today vs yesterday)
            product_entry['Sold Products'] = sold
            
            active_products.append(product_entry)
    
    # Sort by Sold Products (highest first)
    active_products.sort(key=lambda x: x['Sold Products'], reverse=True)
    
    print(f"✅ Found {len(active_products)} active products (with stock changes in last 7 days)")
    
    return active_products, date_columns


def save_to_csv(products, output_file, date_columns):
    """Save products to CSV file with history columns"""
    if not products:
        print("⚠️  No active products to save")
        return
    
    # Build fieldnames: Product Name, Warehouse, date columns..., Sold Products
    fieldnames = ['Product Name', 'Warehouse'] + date_columns + ['Sold Products']
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(products)
    
    print(f"💾 Saved results to: {output_file}")


def main():
    print("=" * 60)
    print("📊 Stock History Generator - 7-Day View")
    print("=" * 60)
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Find all HTML files
    html_files = find_html_files(script_dir)
    
    if len(html_files) == 0:
        print("❌ Error: No Inventory HTML files found")
        print(f"   Looking in: {script_dir}")
        return
    
    if len(html_files) == 1:
        print("❌ Error: Only 1 HTML file found. Need at least 2 files.")
        return
    
    # Use up to the last 7 files (or all if less than 7)
    files_to_use = html_files[-7:] if len(html_files) >= 7 else html_files
    
    print(f"\n📁 Using {len(files_to_use)} file(s) for history:")
    for file in files_to_use:
        print(f"   - {file.name}")
    print()
    
    # Generate history
    active_products, date_columns = generate_history(files_to_use)
    
    # Save to Stock_History.csv (gets replaced daily)
    output_file = script_dir / "Stock_History.csv"
    save_to_csv(active_products, output_file, date_columns)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    if active_products:
        print(f"Total products with activity: {len(active_products)}")
        print(f"\nTop 5 Best Sellers:")
        newest_date = date_columns[-1]
        for i, product in enumerate(active_products[:5], 1):
            print(f"  {i}. {product['Product Name'][:50]}")
            print(f"     Warehouse: {product['Warehouse']}")
            print(f"     Sold: {product['Sold Products']} | Remaining: {product[newest_date]}")
            print()
    
    print("✨ Done! Stock_History.csv has been updated.")
    print("=" * 60)


if __name__ == "__main__":
    main()


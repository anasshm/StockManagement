#!/usr/bin/env python3
"""
Stock Management Inventory Comparison Tool
Automatically compares the 2 newest HTML inventory files
"""

from bs4 import BeautifulSoup
import csv
import sys
from pathlib import Path


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


def get_clean_filename(filepath):
    """
    Extract clean filename without extension for column headers
    Example: 'Inventory - sep28.html' -> 'Inventory-sep28'
    """
    # Get filename without extension
    name = Path(filepath).stem
    # Replace spaces with hyphens for cleaner look
    clean_name = name.replace(' ', '-')
    return clean_name


def extract_date_from_filename(filepath):
    """
    Extract just the date part from filename
    Example: 'Inventory - OCT04.html' -> 'OCT04'
    Example: 'Inventory - sep28.html' -> 'SEP28'
    """
    import re
    filename = Path(filepath).name
    
    # Try to find date pattern (month + day)
    # Matches: OCT4, OCT04, sep28, SEP-28, etc.
    pattern = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\s-]?(\d{1,2})'
    match = re.search(pattern, filename, re.IGNORECASE)
    
    if match:
        month = match.group(1).upper()
        day = match.group(2).zfill(2)  # Pad day to 2 digits (4 -> 04)
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


def compare_inventories(files):
    """
    Compare multiple inventory files and return active products with history
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
    
    # Check each product to see if it had any sales in the last 7 days
    for key in all_product_keys:
        product_name, warehouse = key
        
        # Check if product had any stock changes across the 7 days
        had_sales = False
        stock_values = []
        
        for inv in inventories:
            if key in inv['data']:
                stock_values.append(inv['data'][key])
            else:
                stock_values.append(None)
        
        # Check if stock decreased at any point (indicating sales)
        for i in range(len(stock_values) - 1):
            if stock_values[i] is not None and stock_values[i+1] is not None:
                if stock_values[i] > stock_values[i+1]:  # Stock decreased = sales
                    had_sales = True
                    break
        
        # Only include products that had sales in the last 7 days
        if had_sales:
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
    
    print(f"✅ Found {len(active_products)} active products (with sales in last 7 days)")
    
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
    print("📊 Stock Management - Inventory Comparison")
    print("=" * 60)
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Find all HTML files
    html_files = find_html_files(script_dir)
    
    if len(html_files) == 0:
        print("❌ Error: No HTML files found in this directory")
        print(f"   Looking in: {script_dir}")
        print("   Please add your inventory HTML files to this folder")
        return
    
    if len(html_files) == 1:
        print("❌ Error: Only 1 HTML file found. Need at least 2 files to compare.")
        print(f"   Found: {html_files[0].name}")
        print("   Please add another inventory HTML file to compare")
        return
    
    # Use up to the last 7 files (or all if less than 7)
    files_to_use = html_files[-7:] if len(html_files) >= 7 else html_files
    
    print(f"\n📁 Using {len(files_to_use)} file(s) for history:")
    for file in files_to_use:
        print(f"   - {file.name}")
    print()
    
    # Generate output filename using the newest file's date
    new_file = files_to_use[-1]
    new_date = extract_date_from_filename(new_file)
    output_file = script_dir / f"Stock_{new_date}.csv"
    
    # Compare inventories with history
    active_products, date_columns = compare_inventories(files_to_use)
    
    # Save to CSV
    save_to_csv(active_products, output_file, date_columns)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    if active_products:
        print(f"Top 5 Best Sellers:")
        newest_date = date_columns[-1]
        for i, product in enumerate(active_products[:5], 1):
            print(f"  {i}. {product['Product Name'][:50]}")
            print(f"     Warehouse: {product['Warehouse']}")
            print(f"     Sold: {product['Sold Products']} | Remaining: {product[newest_date]}")
            print()
    
    print("✨ Done! Open the CSV file to view all results.")
    print("=" * 60)


if __name__ == "__main__":
    main()

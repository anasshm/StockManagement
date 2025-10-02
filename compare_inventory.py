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


def find_html_files(directory):
    """Find all HTML files and sort by modification time (oldest first)"""
    html_files = list(Path(directory).glob("*.html"))
    
    if len(html_files) == 0:
        return []
    
    # Sort by modification time (oldest to newest)
    html_files.sort(key=lambda x: x.stat().st_mtime)
    
    return html_files


def compare_inventories(old_file, new_file):
    """
    Compare two inventory files and return active products
    Returns: (active_products, old_filename, new_filename)
    """
    old_name = get_clean_filename(old_file)
    new_name = get_clean_filename(new_file)
    
    print(f"📂 Reading old inventory: {old_file.name}")
    old_inventory = parse_inventory_html(old_file)
    print(f"   Found {len(old_inventory)} products")
    
    print(f"📂 Reading new inventory: {new_file.name}")
    new_inventory = parse_inventory_html(new_file)
    print(f"   Found {len(new_inventory)} products")
    
    active_products = []
    
    # Find products that exist in both files
    for key, old_stock in old_inventory.items():
        product_name, warehouse = key
        
        if key in new_inventory:
            new_stock = new_inventory[key]
            
            # Only include if stock changed (active product)
            if old_stock != new_stock:
                sold = old_stock - new_stock
                
                active_products.append({
                    'Product Name': product_name,
                    'Warehouse': warehouse,
                    old_name: old_stock,
                    new_name: new_stock,
                    'Sold Products': sold
                })
    
    # Sort by Sold Products (highest first)
    active_products.sort(key=lambda x: x['Sold Products'], reverse=True)
    
    print(f"✅ Found {len(active_products)} active products (with stock changes)")
    
    return active_products, old_name, new_name


def save_to_csv(products, output_file, old_name, new_name):
    """Save products to CSV file"""
    if not products:
        print("⚠️  No active products to save")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['Product Name', 'Warehouse', old_name, new_name, 'Sold Products']
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
    
    # Use the 2 newest files (last 2 in the sorted list)
    old_file = html_files[-2]  # Second newest (older)
    new_file = html_files[-1]  # Newest
    
    print(f"\n📁 Auto-detected files:")
    print(f"   OLD: {old_file.name}")
    print(f"   NEW: {new_file.name}")
    print()
    
    # Generate output filename
    old_name = get_clean_filename(old_file)
    new_name = get_clean_filename(new_file)
    output_file = script_dir / f"comparison_{old_name}_to_{new_name}.csv"
    
    # Compare inventories
    active_products, old_name, new_name = compare_inventories(old_file, new_file)
    
    # Save to CSV
    save_to_csv(active_products, output_file, old_name, new_name)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    if active_products:
        print(f"Top 5 Best Sellers:")
        for i, product in enumerate(active_products[:5], 1):
            print(f"  {i}. {product['Product Name'][:50]}")
            print(f"     Warehouse: {product['Warehouse']}")
            print(f"     Sold: {product['Sold Products']} | Remaining: {product[new_name]}")
            print()
    
    print("✨ Done! Open the CSV file to view all results.")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Stock Management Inventory Comparison Tool
Compares two HTML inventory files and outputs active products (products with stock changes)
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


def compare_inventories(old_file, new_file):
    """
    Compare two inventory files and return active products
    Returns: list of dicts with product details
    """
    print(f"📂 Reading old inventory: {old_file}")
    old_inventory = parse_inventory_html(old_file)
    print(f"   Found {len(old_inventory)} products")
    
    print(f"📂 Reading new inventory: {new_file}")
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
                    'Old Expected Stock': old_stock,
                    'New Expected Stock': new_stock,
                    'Sold Products': sold
                })
    
    # Sort by Sold Products (highest first)
    active_products.sort(key=lambda x: x['Sold Products'], reverse=True)
    
    print(f"✅ Found {len(active_products)} active products (with stock changes)")
    
    return active_products


def save_to_csv(products, output_file):
    """Save products to CSV file"""
    if not products:
        print("⚠️  No active products to save")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['Product Name', 'Warehouse', 'Old Expected Stock', 
                     'New Expected Stock', 'Sold Products']
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
    
    # You can modify these filenames as needed
    old_file = script_dir / "Inventory - sep28.html"
    new_file = script_dir / "Inventory - SEP30.html"
    output_file = script_dir / "inventory_comparison.csv"
    
    # Check if files exist
    if not old_file.exists():
        print(f"❌ Error: Old file not found: {old_file}")
        print("   Please make sure the file exists in the same directory as this script")
        return
    
    if not new_file.exists():
        print(f"❌ Error: New file not found: {new_file}")
        print("   Please make sure the file exists in the same directory as this script")
        return
    
    # Compare inventories
    active_products = compare_inventories(old_file, new_file)
    
    # Save to CSV
    save_to_csv(active_products, output_file)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    if active_products:
        print(f"Top 5 Best Sellers:")
        for i, product in enumerate(active_products[:5], 1):
            print(f"  {i}. {product['Product Name'][:40]}")
            print(f"     Warehouse: {product['Warehouse']}")
            print(f"     Sold: {product['Sold Products']} | Remaining: {product['New Expected Stock']}")
            print()
    
    print("✨ Done! Open the CSV file to view all results.")
    print("=" * 60)


if __name__ == "__main__":
    main()

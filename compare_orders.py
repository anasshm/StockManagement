#!/usr/bin/env python3
"""
Orders Processing Tool
Extract orders with 'Not Available' shipping status from CODPARTNER
"""

from bs4 import BeautifulSoup
import csv
from pathlib import Path
from datetime import datetime


def parse_orders_html(html_file):
    """
    Parse orders HTML file and extract orders with 'Not Available' shipping status
    Returns: list of dicts with date, reference, link
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    orders = []
    
    # Find all table rows with data
    rows = soup.find_all('tr', role='row')
    
    for row in rows:
        tds = row.find_all('td')
        if len(tds) < 8:  # Need at least 8 columns for status
            continue
        
        try:
            # Column 0: Order reference (#COD5829541)
            reference_text = tds[0].get_text(strip=True)
            if not reference_text.startswith('#COD'):
                continue
            
            reference = reference_text
            
            # Column 2: Order date (2025-10-14 20:47:48)
            date_text = tds[2].get_text(strip=True)
            
            # Column 7: Shipping status
            shipping_status = tds[7].get_text(strip=True)
            
            # Only include orders with "Not Available" or "not available" status
            if "not available" in shipping_status.lower():
                # Generate link from reference
                # #COD5829541 -> https://app.codpartner.com/orders/5829541
                order_id = reference.replace('#COD', '')
                link = f"https://app.codpartner.com/orders/{order_id}"
                
                orders.append({
                    'Date': date_text,
                    'Reference': reference,
                    'Link': link
                })
            
        except (ValueError, AttributeError, IndexError):
            # Skip rows that don't have proper data
            continue
    
    return orders


def save_orders_to_csv(orders, output_file):
    """Save orders to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['Date', 'Reference', 'Link']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        if not orders:
            # Create a row with a positive message when no orders need attention
            writer.writerow({
                'Date': '',
                'Reference': 'Rest easy, all orders have shipping status available',
                'Link': ''
            })
            print("✅ No orders with 'Not Available' status - All good!")
        else:
            writer.writerows(orders)
    
    print(f"💾 Saved results to: {output_file}")


def extract_date_from_filename(filepath):
    """
    Extract date part from filename
    Example: 'Orders - OCT12.html' -> 'OCT12'
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
    
    # Fallback: use today's date
    today = datetime.now().strftime('%b%d').upper()
    if today.startswith('OCT'):
        today = 'OCT' + today[3:]
    return today


def find_latest_orders_html(directory):
    """Find the most recent orders HTML file"""
    html_files = list(Path(directory).glob("Orders*.html"))
    
    if len(html_files) == 0:
        return None
    
    # Sort by modification time (newest first)
    html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return html_files[0]


def main():
    print("=" * 60)
    print("📦 Orders Processing - Not Available Shipping Status")
    print("=" * 60)
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Find latest orders HTML file
    orders_file = find_latest_orders_html(script_dir)
    
    if not orders_file:
        print("❌ Error: No Orders HTML file found")
        print(f"   Looking in: {script_dir}")
        print("   Please run download first")
        return
    
    print(f"\n📁 Processing file: {orders_file.name}")
    print()
    
    # Parse orders
    orders = parse_orders_html(orders_file)
    
    print(f"✅ Found {len(orders)} orders with 'Not Available' shipping status")
    
    # Generate output filename
    date = extract_date_from_filename(orders_file)
    output_file = script_dir / f"Orders_Not_Available_{date}.csv"
    
    # Save to CSV
    save_orders_to_csv(orders, output_file)
    
    # Print summary
    if orders:
        print("\n" + "=" * 60)
        print("📈 SUMMARY")
        print("=" * 60)
        print(f"Total orders needing attention: {len(orders)}")
        print(f"\nFirst 5 orders:")
        for i, order in enumerate(orders[:5], 1):
            print(f"  {i}. {order['Reference']} - {order['Date']}")
        print()
    
    print("✨ Done! Open the CSV file to view all results.")
    print("=" * 60)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Process Product Analytics Data
Extract Saudi Arabia product analytics into CSV
"""

from bs4 import BeautifulSoup
import csv
from pathlib import Path
from datetime import datetime


def parse_analytics_html(html_file):
    """
    Parse analytics HTML file and extract product data
    Returns: list of dicts with product analytics
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    products = []
    
    # Find all table rows with data
    rows = soup.find_all('tr', role='row')
    
    for row in rows:
        tds = row.find_all('td')
        if len(tds) < 10:  # Need at least 10 columns based on structure
            continue
        
        try:
            # Column 0: Product name (has image and text)
            product_td = tds[0]
            product_name = product_td.get_text(strip=True)
            if not product_name or len(product_name) < 2:  # Skip empty/header rows
                continue
            
            # Column 1: Leads
            leads_text = tds[1].get_text(strip=True)
            
            # Column 2: Confirmed
            confirmed_text = tds[2].get_text(strip=True)
            
            # Column 9: Deliv.Rate (Delivery Rate)
            deliv_rate = tds[9].get_text(strip=True)
            
            # Only add if we have valid data
            if leads_text and confirmed_text:
                # Calculate confirmation rate: (Confirmed / Leads) * 100
                try:
                    leads = int(leads_text)
                    confirmed = int(confirmed_text)
                    if leads > 0:
                        conf_rate = f"{(confirmed / leads * 100):.2f}%"
                    else:
                        conf_rate = "0%"
                except (ValueError, ZeroDivisionError):
                    conf_rate = "N/A"
                
                products.append({
                    'Country': 'Saudi Arabia',
                    'Product Name': product_name,
                    'Leads': leads_text,
                    'Confirmed': confirmed_text,
                    'Conf.Rate': conf_rate,
                    'Delivery Rate': deliv_rate
                })
            
        except (ValueError, AttributeError, IndexError) as e:
            # Skip rows that don't have proper data
            continue
    
    return products


def save_to_csv(products, output_file):
    """Save products analytics to CSV file"""
    if not products:
        print("⚠️  No product data found")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['Country', 'Product Name', 'Leads', 'Confirmed', 'Conf.Rate', 'Delivery Rate']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(products)
    
    print(f"💾 Saved results to: {output_file}")


def extract_date_from_filename(filepath):
    """Extract date from filename"""
    import re
    filename = Path(filepath).name
    
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


def find_latest_analytics_html(directory):
    """Find the most recent analytics HTML file"""
    html_files = list(Path(directory).glob("Analytics_Products*.html"))
    
    if len(html_files) == 0:
        return None
    
    # Sort by modification time (newest first)
    html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return html_files[0]


def main():
    print("=" * 60)
    print("📊 Product Analytics Processing - Saudi Arabia")
    print("=" * 60)
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Find latest analytics HTML file
    analytics_file = find_latest_analytics_html(script_dir)
    
    if not analytics_file:
        print("❌ Error: No Analytics HTML file found")
        print(f"   Looking in: {script_dir}")
        print("   Please run download_analytics.py first")
        return
    
    print(f"\n📁 Processing file: {analytics_file.name}")
    print()
    
    # Parse analytics
    products = parse_analytics_html(analytics_file)
    
    print(f"✅ Found {len(products)} products")
    
    # Generate output filename
    date = extract_date_from_filename(analytics_file)
    output_file = script_dir / f"Analytics_Products_Saudi_{date}.csv"
    
    # Save to CSV
    save_to_csv(products, output_file)
    
    # Print summary
    if products:
        print("\n" + "=" * 60)
        print("📈 SUMMARY")
        print("=" * 60)
        print(f"Total products: {len(products)}")
        print(f"\nFirst 5 products:")
        for i, product in enumerate(products[:5], 1):
            print(f"  {i}. {product['Product Name'][:50]}")
            print(f"     Leads: {product['Leads']} | Confirmed: {product['Confirmed']} | Conf.Rate: {product['Conf.Rate']}")
        print()
    
    print("✨ Done! Open the CSV file to view all results.")
    print("=" * 60)


if __name__ == "__main__":
    main()


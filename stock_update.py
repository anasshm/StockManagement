#!/usr/bin/env python3
"""
Complete Stock Update - Download & Compare
Run this daily to get your stock report
"""

from automation.codpartner import CODPartnerAutomation
from automation.utils import clean_old_files
from pathlib import Path
from datetime import datetime
import subprocess
import sys


def download_inventory():
    """Download today's inventory"""
    print("=" * 60)
    print("📊 STEP 1: Downloading Inventory")
    print("=" * 60)
    
    try:
        with CODPartnerAutomation() as bot:
            bot.login()
            filepath = bot.download_inventory()
            clean_old_files(
                directory=Path(__file__).parent,
                pattern="Inventory*.html",
                keep_recent=7
            )
        
        print("✅ Inventory downloaded successfully\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False


def compare_inventory():
    """Run comparison script (daily snapshot)"""
    print("=" * 60)
    print("📊 STEP 2: Comparing Inventory (Daily)")
    print("=" * 60)
    
    try:
        # Run compare_inventory.py
        script_path = Path(__file__).parent / "compare_inventory.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        # Print the output
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"❌ Comparison failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ Comparison failed: {e}")
        return False


def generate_history():
    """Generate 7-day history file"""
    print("=" * 60)
    print("📊 STEP 2b: Generating Stock History (7-day view)")
    print("=" * 60)
    
    try:
        # Run generate_history.py
        script_path = Path(__file__).parent / "generate_history.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        # Print the output
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"⚠️  History generation had issues: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n⚠️  History generation failed: {e}")
        return False


def download_orders():
    """Download today's orders"""
    print("=" * 60)
    print("📦 STEP 3: Downloading Orders")
    print("=" * 60)
    
    try:
        with CODPartnerAutomation() as bot:
            bot.login()
            filepath = bot.download_orders()
            clean_old_files(
                directory=Path(__file__).parent,
                pattern="Orders*.html",
                keep_recent=7
            )
        
        print("✅ Orders downloaded successfully\n")
        return True
        
    except Exception as e:
        print(f"\n⚠️  Orders download failed: {e}")
        print("   Continuing with inventory report...")
        return False


def process_orders():
    """Run orders processing script"""
    print("=" * 60)
    print("📦 STEP 4: Processing Orders (Not Available Status)")
    print("=" * 60)
    
    try:
        # Run compare_orders.py
        script_path = Path(__file__).parent / "compare_orders.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        # Print the output
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"⚠️  Orders processing had issues: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n⚠️  Orders processing failed: {e}")
        return False


def main():
    # Check if today's files already exist
    today = datetime.now().strftime('%b%d').upper()
    if today.startswith('OCT'):
        today = 'OCT' + today[3:]
    
    project_dir = Path(__file__).parent
    today_csv = project_dir / f"Stock_{today}.csv"
    today_html = project_dir / f"Inventory - {today}.html"
    
    if today_csv.exists() and today_html.exists():
        print("\n" + "=" * 60)
        print("✅ Today's report already exists!")
        print("=" * 60)
        print(f"📄 {today_csv.name}")
        print(f"📄 {today_html.name}")
        print("\nSkipping download. Delete these files to force a new download.")
        print("=" * 60)
        print()
        sys.exit(0)
    
    print("\n" + "=" * 60)
    print("🚀 STOCK UPDATE - Complete Daily Report")
    print("=" * 60)
    print()
    
    # Step 1: Download
    if not download_inventory():
        print("\n❌ FAILED at download step")
        sys.exit(1)
    
    # Step 2: Compare (daily snapshot)
    if not compare_inventory():
        print("\n❌ FAILED at comparison step")
        sys.exit(1)
    
    # Step 2b: Generate history (7-day view, non-critical)
    generate_history()
    
    # Step 3: Download Orders (non-critical, continues on failure)
    orders_downloaded = download_orders()
    
    # Step 4: Process Orders (only if download succeeded)
    if orders_downloaded:
        process_orders()
    
    # Success!
    print("\n" + "=" * 60)
    print("✅ COMPLETE! Your stock report is ready")
    print("=" * 60)
    print()
    print("📄 Stock_*.csv - Today's snapshot (changes between yesterday and today)")
    print("📄 Stock_History.csv - 7-day view (all products with activity this week)")
    if orders_downloaded:
        print("📄 Orders_Not_Available_*.csv - Orders needing attention")
    print()


if __name__ == "__main__":
    main()


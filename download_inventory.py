#!/usr/bin/env python3
"""
Download today's inventory from CODPARTNER
Run this daily to get fresh inventory data
"""

from automation.codpartner import CODPartnerAutomation
from automation.utils import clean_old_files
from pathlib import Path


def main():
    print("=" * 60)
    print("📊 CODPARTNER Inventory Downloader")
    print("=" * 60)
    
    try:
        # Use context manager for automatic cleanup
        with CODPartnerAutomation() as bot:
            # Login
            bot.login()
            
            # Download inventory
            filepath = bot.download_inventory()
            
            # Optional: Clean up old files (keep last 7)
            clean_old_files(
                directory=Path(__file__).parent,
                pattern="Inventory*.html",
                keep_recent=7
            )
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Inventory downloaded")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()

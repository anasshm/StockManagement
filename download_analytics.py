#!/usr/bin/env python3
"""
Download Product Analytics from CODPARTNER
Run this to get Saudi Arabia product analytics data
"""

from automation.codpartner import CODPartnerAutomation
from pathlib import Path


def main():
    print("=" * 60)
    print("📊 CODPARTNER Analytics Downloader (Saudi Arabia)")
    print("=" * 60)
    
    try:
        # Use context manager for automatic cleanup
        with CODPartnerAutomation() as bot:
            # Login
            bot.login()
            
            # Download analytics
            filepath = bot.download_analytics(country="Saudi arabia")
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Analytics downloaded")
        print("=" * 60)
        print("\nNext step: Run compare_analytics.py to process the data")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()


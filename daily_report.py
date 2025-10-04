#!/usr/bin/env python3
"""
Complete daily workflow: Download + Compare
Run this once per day for your stock report
"""

import subprocess
import sys

def run_script(script_name):
    """Run a Python script and check if it succeeded"""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print('='*60)
    
    result = subprocess.run([sys.executable, script_name], 
                          capture_output=False)
    
    if result.returncode != 0:
        print(f"\n❌ {script_name} failed!")
        return False
    return True

def main():
    print("=" * 60)
    print("📊 Daily Stock Management Report")
    print("=" * 60)
    
    # Step 1: Download inventory
    if not run_script('download_inventory.py'):
        sys.exit(1)
    
    # Step 2: Compare inventories
    if not run_script('compare_inventory.py'):
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✨ DAILY REPORT COMPLETE!")
    print("=" * 60)
    print("\n📄 Check your CSV file for today's results")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Quick test to see if Playwright works"""

from playwright.sync_api import sync_playwright
import time

print("Testing Playwright...")

with sync_playwright() as p:
    print("✅ Playwright started")
    
    browser = p.chromium.launch(headless=False)
    print("✅ Browser launched")
    
    page = browser.new_page()
    print("✅ Page created")
    
    print("🌐 Going to Google...")
    page.goto('https://www.google.com')
    print("✅ Page loaded")
    
    time.sleep(3)
    
    browser.close()
    print("✅ Test complete!")

#!/usr/bin/env python3
"""
Simple script to replay your recorded session
Just run: python3 run_my_recording.py
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
USERNAME = os.getenv('CODPARTNER_USERNAME', 'anasshm99@gmail.com')
PASSWORD = os.getenv('CODPARTNER_PASSWORD', '@Bihfih123@')


def main():
    print("=" * 60)
    print("🎬 Replaying Your Recorded Session")
    print("=" * 60)
    print()
    
    # Create traces directory
    traces_dir = Path("traces")
    traces_dir.mkdir(exist_ok=True)
    trace_file = traces_dir / "my_recording.zip"
    
    print(f"📹 Recording trace to: {trace_file}")
    print()
    
    try:
        with sync_playwright() as playwright:
            # Launch browser (visible so you can see)
            print("🚀 Starting browser...")
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # Start trace recording
            print("📹 Starting trace recording...")
            context.tracing.start(
                screenshots=True,
                snapshots=True,
                sources=True
            )
            
            page = context.new_page()
            
            print("▶️  Executing your recorded actions...")
            print()
            
            # === YOUR RECORDED ACTIONS ===
            
            # Login
            print("🔐 Logging in...")
            page.goto("https://app.codpartner.com/login")
            time.sleep(3)
            
            page.get_by_role("textbox", name="Enter your email").click()
            time.sleep(3)
            page.get_by_role("textbox", name="Enter your email").fill(USERNAME)
            time.sleep(3)
            
            page.get_by_role("textbox", name="Password cannot exceed 16").click()
            time.sleep(3)
            page.get_by_role("textbox", name="Password cannot exceed 16").fill(PASSWORD)
            time.sleep(3)
            
            page.get_by_role("button", name="Log In").click()
            
            # Wait for login to complete
            print("   ⏳ Waiting for login...")
            time.sleep(3)
            page.wait_for_load_state('networkidle', timeout=30000)
            time.sleep(3)
            
            # Navigate to analytics (skip popup handling, go straight to analytics)
            print("📊 Going to Analytics page...")
            page.goto("https://app.codpartner.com/reports/analytics/products")
            print("   ⏳ Waiting for page to load...")
            time.sleep(3)
            page.wait_for_load_state('networkidle', timeout=30000)
            time.sleep(3)
            
            # Open filter
            print("📅 Opening filter...")
            page.get_by_role("button", name=" Filter").click()
            print("   ⏳ Waiting for filter dialog...")
            time.sleep(3)
            
            # Double click date range input and fill it directly
            print("📅 Double-clicking date range input...")
            page.locator("#daterange").dblclick()
            print("   ⏳ Waiting after double-click...")
            time.sleep(3)
            
            print("📅 Typing date range (2025/10/12 - 2025/10/13)...")
            page.locator("#daterange").fill("2025/10/12 - 2025/10/13")
            print("   ⏳ Waiting after filling dates...")
            time.sleep(3)
            
            # DEEP DIAGNOSTIC: Check button state and clickability
            print("\n🔍 DEEP DIAGNOSTIC: Analyzing Apply buttons...")
            try:
                all_apply = page.get_by_role("button", name="Apply").all()
                print(f"   Total Apply buttons found: {len(all_apply)}")
                
                for i, btn in enumerate(all_apply):
                    print(f"\n   === Button {i} Analysis ===")
                    try:
                        # Basic checks
                        is_visible = btn.is_visible()
                        is_enabled = btn.is_enabled()
                        print(f"   Visible: {is_visible}")
                        print(f"   Enabled: {is_enabled}")
                        
                        # Get attributes
                        classes = btn.get_attribute("class")
                        btn_type = btn.get_attribute("type")
                        print(f"   Class: {classes}")
                        print(f"   Type: {btn_type}")
                        
                        # Check if in viewport
                        box = btn.bounding_box()
                        if box:
                            print(f"   Position: x={box['x']}, y={box['y']}")
                            print(f"   Size: width={box['width']}, height={box['height']}")
                            in_viewport = box['y'] >= 0 and box['y'] < 1000  # rough check
                            print(f"   In viewport: {in_viewport}")
                        else:
                            print(f"   Position: Not in DOM or hidden")
                        
                        # Check if it's the one we want
                        if "applyBtn" in (classes or ""):
                            print(f"   ⭐ THIS IS THE DATE PICKER APPLY!")
                            
                    except Exception as e:
                        print(f"   Error analyzing button {i}: {e}")
                        
            except Exception as e:
                print(f"   ⚠️ Diagnostic failed: {e}")
            
            # Click Apply buttons - there are 2 different ones
            # First: Apply in date picker (after entering dates)
            print("\n✅ ATTEMPTING CLICK: First Apply button (date picker)...")
            
            # Try to find and analyze the button before clicking
            print("   Step 1: Locating button with CSS 'button.applyBtn'...")
            try:
                applyBtn = page.locator("button.applyBtn").first
                print("   ✓ Button located")
                
                print("   Step 2: Checking if button is visible...")
                is_visible = applyBtn.is_visible()
                print(f"   → Visible: {is_visible}")
                
                print("   Step 3: Checking if button is enabled...")
                is_enabled = applyBtn.is_enabled()
                print(f"   → Enabled: {is_enabled}")
                
                print("   Step 4: Getting button position...")
                box = applyBtn.bounding_box()
                if box:
                    print(f"   → Position: ({box['x']}, {box['y']}), Size: {box['width']}x{box['height']}")
                else:
                    print("   → Position: Cannot get bounding box!")
                
                print("   Step 5: Waiting for 'visible' state...")
                applyBtn.wait_for(state="visible", timeout=10000)
                print("   ✓ Wait complete")
                
                print("   Step 6: Scrolling button into view...")
                applyBtn.scroll_into_view_if_needed()
                print("   ✓ Scrolled")
                
                time.sleep(1)
                
                print("   Step 7: Attempting click (force=True)...")
                applyBtn.click(force=True)
                print("   ✓✓✓ FIRST APPLY CLICKED SUCCESSFULLY! ✓✓✓")
                
            except Exception as e:
                print(f"   ❌ CLICK FAILED!")
                print(f"   Error type: {type(e).__name__}")
                print(f"   Error message: {str(e)}")
                print(f"   Full error: {repr(e)}")
            
            print("\n   ⏳ Waiting 3 seconds...")
            time.sleep(3)
            
            # Second: Apply in filter dialog (to apply the filter)
            print("\n✅ ATTEMPTING CLICK: Second Apply button (filter dialog)...")
            
            print("   Step 1: Locating button with CSS 'button.btn-main-primary'...")
            try:
                mainBtn = page.locator("button.btn-main-primary[type='submit']").first
                print("   ✓ Button located")
                
                print("   Step 2: Checking if button is visible...")
                is_visible = mainBtn.is_visible()
                print(f"   → Visible: {is_visible}")
                
                print("   Step 3: Checking if button is enabled...")
                is_enabled = mainBtn.is_enabled()
                print(f"   → Enabled: {is_enabled}")
                
                print("   Step 4: Waiting for 'visible' state...")
                mainBtn.wait_for(state="visible", timeout=10000)
                print("   ✓ Wait complete")
                
                print("   Step 5: Scrolling button into view...")
                mainBtn.scroll_into_view_if_needed()
                print("   ✓ Scrolled")
                
                time.sleep(1)
                
                print("   Step 6: Attempting click (force=True)...")
                mainBtn.click(force=True)
                print("   ✓✓✓ SECOND APPLY CLICKED SUCCESSFULLY! ✓✓✓")
                
            except Exception as e:
                print(f"   ❌ CLICK FAILED!")
                print(f"   Error type: {type(e).__name__}")
                print(f"   Error message: {str(e)}")
                print(f"   Full error: {repr(e)}")
            
            print("   ⏳ Waiting after second Apply...")
            
            print("   ⏳ Waiting for filter to apply...")
            time.sleep(5)
            
            print()
            print("⏸️  Pausing for 5 seconds to see results...")
            time.sleep(5)
            
            # === END RECORDED ACTIONS ===
            
            # Stop trace
            print()
            print("💾 Saving trace...")
            context.tracing.stop(path=str(trace_file))
            
            browser.close()
            
        print()
        print("=" * 60)
        print("✅ Recording Replay Complete!")
        print("=" * 60)
        print()
        print(f"📁 Trace saved to: {trace_file}")
        print()
        print("🔍 To view the trace with screenshots:")
        print(f"   python3 view_trace.py")
        print("   OR")
        print(f"   playwright show-trace {trace_file}")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR: {e}")
        print("=" * 60)
        print()
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()


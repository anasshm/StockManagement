from playwright.sync_api import sync_playwright, Page
from datetime import datetime
from pathlib import Path
import time

from .config import Config


class CODPartnerAutomation:
    """Automate CODPARTNER website tasks"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.config.validate()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def start(self):
        """Initialize Playwright and browser"""
        print("🚀 Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=not self.config.SHOW_BROWSER,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = self.context.new_page()
        print("✅ Browser started")
    
    def stop(self):
        """Close browser and cleanup"""
        try:
            if self.page and not self.page.is_closed():
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("👋 Browser closed")
        except Exception as e:
            print(f"⚠️  Error closing browser: {e}")
    
    def login(self):
        """Login to CODPARTNER"""
        print(f"🔐 Logging in to {self.config.LOGIN_URL}")
        
        try:
            self.page.goto(self.config.LOGIN_URL, wait_until='domcontentloaded')
            
            # Wait for login form
            print("⏳ Waiting for login form...")
            self.page.wait_for_selector('input[name="email"], input[type="email"]', 
                                         timeout=self.config.TIMEOUT)
            
            # Fill in credentials
            print("📝 Filling in credentials...")
            self.page.fill('input[name="email"], input[type="email"]', self.config.USERNAME)
            self.page.fill('input[name="password"], input[type="password"]', self.config.PASSWORD)
            
            # Click login button - try multiple selectors
            print("🖱️  Clicking login button...")
            
            # Try to find and click the login button
            login_clicked = False
            selectors_to_try = [
                'button:has-text("Log In")',
                'button[type="submit"]',
                'button:text("Log In")',
                '//button[contains(text(), "Log In")]'
            ]
            
            for selector in selectors_to_try:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.click(selector)
                        login_clicked = True
                        print(f"✅ Clicked login button using: {selector}")
                        break
                except:
                    continue
            
            if not login_clicked:
                print("⚠️  Could not click login button, trying Enter key...")
                self.page.keyboard.press('Enter')
            
            # Wait for navigation after login
            print("⏳ Waiting for login to complete...")
            time.sleep(3)
            self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
            
            # Check if we're on a different page (successful login)
            current_url = self.page.url
            if 'login' not in current_url.lower():
                print("✅ Logged in successfully")
            else:
                print("⚠️  Still on login page, but continuing...")
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            raise
    
    def download_inventory(self, filename: str = None):
        """Download inventory page with all entries visible"""
        print(f"📦 Downloading inventory from {self.config.INVENTORY_URL}")
        
        try:
            # Navigate to inventory page
            self.page.goto(self.config.INVENTORY_URL, wait_until='domcontentloaded')
            time.sleep(2)
            self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
            
            # Click on "Show entries" dropdown and select 100
            print(f"⚙️  Setting to show {self.config.ENTRIES_TO_SHOW} entries")
            try:
                # Wait for the dropdown
                self.page.wait_for_selector('select[name="inventory_length"]', timeout=5000)
                
                # Select 100 entries
                self.page.select_option('select[name="inventory_length"]', 
                                       str(self.config.ENTRIES_TO_SHOW))
                
                print("⏳ Waiting 30 seconds for table to fully load...")
                
                # Wait for processing indicator to disappear
                try:
                    # Wait for "Processing..." to appear then disappear
                    self.page.wait_for_selector('#inventory_processing[style*="display: block"]', timeout=3000)
                    print("   Loading data...")
                    self.page.wait_for_selector('#inventory_processing[style*="display: none"]', timeout=30000)
                    print("   ✅ Data loaded")
                except:
                    print("   No processing indicator found, continuing...")
                
                # Additional wait to ensure all data is rendered
                time.sleep(5)
                self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
                
                print("✅ Table fully loaded with all entries")
                
            except Exception as e:
                print(f"⚠️  Could not change entries display: {e}")
                print("   Continuing with default view...")
            
            # Generate filename if not provided
            if not filename:
                today = datetime.now().strftime('%b%d').upper()
                # Handle lowercase month abbreviations
                if today.startswith('OCT'):
                    today = 'OCT' + today[3:]
                filename = f"Inventory - {today}.html"
            
            # Get full page HTML
            print("💾 Capturing page content...")
            html_content = self.page.content()
            
            # Save to file
            filepath = self.config.DOWNLOAD_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            raise
    
    def download_orders(self, filename: str = None):
        """Download orders page and return filtered orders with 'Not Available' shipping status"""
        print(f"📦 Downloading orders from {self.config.ORDERS_URL}")
        
        try:
            # Navigate to orders page
            self.page.goto(self.config.ORDERS_URL, wait_until='domcontentloaded')
            time.sleep(2)
            self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
            
            # Click on "Show entries" dropdown and select 100
            print(f"⚙️  Setting to show {self.config.ENTRIES_TO_SHOW} entries")
            try:
                # Wait for the dropdown (assuming similar structure to inventory)
                self.page.wait_for_selector('select[name="orders_length"]', timeout=5000)
                
                # Select 100 entries
                self.page.select_option('select[name="orders_length"]', 
                                       str(self.config.ENTRIES_TO_SHOW))
                
                print("⏳ Waiting 30 seconds for table to fully load...")
                
                # Wait for processing indicator to disappear
                try:
                    self.page.wait_for_selector('#orders_processing[style*="display: block"]', timeout=3000)
                    print("   Loading data...")
                    self.page.wait_for_selector('#orders_processing[style*="display: none"]', timeout=30000)
                    print("   ✅ Data loaded")
                except:
                    print("   No processing indicator found, continuing...")
                
                # Additional wait to ensure all data is rendered
                time.sleep(5)
                self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
                
                print("✅ Table fully loaded with all entries")
                
            except Exception as e:
                print(f"⚠️  Could not change entries display: {e}")
                print("   Continuing with default view...")
            
            # Generate filename if not provided
            if not filename:
                today = datetime.now().strftime('%b%d').upper()
                if today.startswith('OCT'):
                    today = 'OCT' + today[3:]
                filename = f"Orders - {today}.html"
            
            # Get full page HTML
            print("💾 Capturing page content...")
            html_content = self.page.content()
            
            # Save to file
            filepath = self.config.DOWNLOAD_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Orders download failed: {e}")
            raise
    
    def download_analytics(self, country="Saudi arabia", filename: str = None):
        """Download product analytics for specified country with date range filter"""
        print(f"📊 Downloading analytics from {self.config.ANALYTICS_URL}")
        
        try:
            # Navigate to analytics page
            self.page.goto(self.config.ANALYTICS_URL, wait_until='domcontentloaded')
            time.sleep(3)
            self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
            
            # Click on country button
            print(f"🇸🇦 Selecting {country}...")
            try:
                # Click on the country button (e.g., "Saudi arabia")
                self.page.click(f'text="{country}"')
                print(f"✅ Clicked {country}")
                
                # Wait for processing to complete
                print("⏳ Waiting for data processing...")
                time.sleep(3)
                
                # Wait for processing overlay to disappear
                try:
                    self.page.wait_for_selector('text="Processing..."', state='hidden', timeout=10000)
                    print("   ✅ Processing complete")
                except:
                    print("   No processing indicator found, continuing...")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️  Error selecting country: {e}")
                print("   Continuing anyway...")
            
            # Change to show 100 entries
            print(f"⚙️  Setting to show {self.config.ENTRIES_TO_SHOW} entries")
            try:
                # Wait for the dropdown - analytics page uses different name
                # Try multiple possible selectors
                dropdown_found = False
                for selector in ['select[name="products_length"]', 'select']:
                    try:
                        self.page.wait_for_selector(selector, timeout=5000)
                        dropdown_found = True
                        break
                    except:
                        continue
                
                if dropdown_found:
                    # Select 100 entries
                    self.page.select_option(selector, str(self.config.ENTRIES_TO_SHOW))
                    
                    print("⏳ Waiting 30 seconds for table to fully load...")
                    
                    # Wait for processing indicator to disappear (similar to inventory)
                    try:
                        # Wait for "Processing..." to appear then disappear
                        self.page.wait_for_selector('#products_processing[style*="display: block"]', timeout=3000)
                        print("   Loading data...")
                        self.page.wait_for_selector('#products_processing[style*="display: none"]', timeout=30000)
                        print("   ✅ Data loaded")
                    except:
                        print("   No processing indicator found, waiting anyway...")
                        # Even without indicator, wait for the data to load
                        time.sleep(10)
                    
                    # Additional wait to ensure all data is rendered
                    time.sleep(5)
                    self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
                    
                    print("✅ Table fully loaded with all entries")
                else:
                    print("⚠️  Could not find entries dropdown")
                
            except Exception as e:
                print(f"⚠️  Could not change entries display: {e}")
                print("   Continuing with default view...")
            
            # Set date range: 20 days ago to 10 days ago
            print("📅 Setting date range (20 days ago to 10 days ago)...")
            try:
                from datetime import timedelta
                
                # Calculate dates
                today = datetime.now()
                start_date = today - timedelta(days=20)
                end_date = today - timedelta(days=10)
                
                print(f"   Start: {start_date.strftime('%Y-%m-%d')} | End: {end_date.strftime('%Y-%m-%d')}")
                
                # Step 1: Click on the Filter button to open filter dialog
                print("   Step 1: Opening filter dialog...")
                self.page.click('button:has-text("Filter")', timeout=5000)
                time.sleep(2)
                print("   ✅ Filter dialog opened")
                
                # Step 2: Click on the daterange input inside the filter dialog
                print("   Step 2: Clicking daterange input...")
                self.page.click('input#daterange', timeout=5000)
                time.sleep(1)
                print("   ✅ Date dropdown opened")
                
                # Step 3: Click "Custom Range" directly
                print("   Step 3: Clicking 'Custom Range'...")
                self.page.click('text="Custom Range"', timeout=5000)
                time.sleep(2)
                print("   ✅ Custom range calendar opened")
                
                # Step 4: Select start date by clicking on the calendar
                print(f"   Step 4: Selecting start date (day {start_date.day} in {start_date.strftime('%b')})...")
                try:
                    # Click the specific day in the calendar
                    # Find calendar cells that aren't disabled and match our day
                    self.page.evaluate(f"""
                        () => {{
                            // Find all calendar cells
                            const cells = document.querySelectorAll('td.available');
                            for (let cell of cells) {{
                                if (cell.textContent.trim() === '{start_date.day}' && 
                                    !cell.classList.contains('off')) {{
                                    cell.click();
                                    return true;
                                }}
                            }}
                            return false;
                        }}
                    """)
                    time.sleep(0.5)
                    print(f"   ✅ Selected start date: {start_date.strftime('%Y-%m-%d')}")
                except Exception as e:
                    print(f"   ⚠️  Could not click start date: {e}")
                
                # Step 5: Select end date by clicking on the calendar
                print(f"   Step 5: Selecting end date (day {end_date.day} in {end_date.strftime('%b')})...")
                try:
                    # Click the specific day in the calendar for end date
                    # Need to find the second occurrence if different month
                    self.page.evaluate(f"""
                        () => {{
                            // Find all calendar cells
                            const cells = document.querySelectorAll('td.available');
                            let found = false;
                            for (let cell of cells) {{
                                if (cell.textContent.trim() === '{end_date.day}' && 
                                    !cell.classList.contains('off')) {{
                                    // If same month as start date, skip first occurrence
                                    if ({start_date.month} !== {end_date.month} || found) {{
                                        cell.click();
                                        return true;
                                    }}
                                    found = true;
                                }}
                            }}
                            return false;
                        }}
                    """)
                    time.sleep(0.5)
                    print(f"   ✅ Selected end date: {end_date.strftime('%Y-%m-%d')}")
                except Exception as e:
                    print(f"   ⚠️  Could not click end date: {e}")
                
                # Step 6: Click first "Apply" button (in date picker)
                print("   Step 6: Clicking first 'Apply' button...")
                try:
                    # Find and click the Apply button in the date picker popup
                    apply_buttons = self.page.query_selector_all('button:has-text("Apply")')
                    if len(apply_buttons) > 0:
                        apply_buttons[0].click()
                        time.sleep(2)
                        print("   ✅ Clicked Apply in date picker")
                except Exception as e:
                    print(f"   ⚠️  Could not click first Apply: {e}")
                
                # Step 7: Try to click second "Apply" button if it exists (optional)
                print("   Step 7: Checking for second 'Apply' button...")
                try:
                    # Wait a moment for the filter dialog
                    time.sleep(1)
                    # Try to find and click the main Apply button if still visible
                    apply_buttons = self.page.query_selector_all('button:has-text("Apply")')
                    if len(apply_buttons) > 0:
                        # Check if button is visible
                        if apply_buttons[-1].is_visible():
                            apply_buttons[-1].click()
                            time.sleep(2)
                            print("   ✅ Clicked Apply in filter dialog")
                        else:
                            print("   ℹ️  Second Apply not visible (filter already applied)")
                    else:
                        print("   ℹ️  No second Apply button found (filter already applied)")
                except Exception as e:
                    print(f"   ℹ️  Filter already applied: {e}")
                
                # Wait for processing after date change
                print("   ⏳ Waiting for data to reload with new date range...")
                time.sleep(5)
                
                try:
                    self.page.wait_for_selector('text="Processing..."', state='hidden', timeout=15000)
                    print("   ✅ Data reloaded with new date range")
                except:
                    print("   Continuing...")
                
                time.sleep(3)
                self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
                
            except Exception as e:
                print(f"⚠️  Could not set date range: {e}")
                print("   Continuing with current date range...")
            
            # Generate filename if not provided
            if not filename:
                today = datetime.now().strftime('%b%d').upper()
                if today.startswith('OCT'):
                    today = 'OCT' + today[3:]
                filename = f"Analytics_Products_Saudi_{today}.html"
            
            # Get full page HTML
            print("💾 Capturing page content...")
            html_content = self.page.content()
            
            # Save to file
            filepath = self.config.DOWNLOAD_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Analytics download failed: {e}")
            raise
    
    def download_with_date_range(self, start_date: str, end_date: str):
        """
        Download data with custom date range
        Future implementation for Products/Orders pages
        
        Args:
            start_date: Format 'YYYY-MM-DD'
            end_date: Format 'YYYY-MM-DD'
        """
        # TODO: Implement for Products/Orders Metrics pages
        print("🚧 Custom date range feature coming soon...")
        pass
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

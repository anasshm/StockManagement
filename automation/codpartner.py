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
                
                # Wait for table to reload
                time.sleep(3)
                self.page.wait_for_load_state('networkidle', timeout=self.config.TIMEOUT)
                
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

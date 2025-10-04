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
            headless=not self.config.SHOW_BROWSER
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        print("✅ Browser started")
    
    def stop(self):
        """Close browser and cleanup"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("👋 Browser closed")
    
    def login(self):
        """Login to CODPARTNER"""
        print(f"🔐 Logging in to {self.config.LOGIN_URL}")
        
        self.page.goto(self.config.LOGIN_URL)
        
        # Wait for login form
        self.page.wait_for_selector('input[name="email"], input[type="email"]', 
                                     timeout=self.config.TIMEOUT)
        
        # Fill in credentials
        self.page.fill('input[name="email"], input[type="email"]', self.config.USERNAME)
        self.page.fill('input[name="password"], input[type="password"]', self.config.PASSWORD)
        
        # Click login button
        self.page.click('button[type="submit"]')
        
        # Wait for navigation after login
        self.page.wait_for_load_state('networkidle')
        
        print("✅ Logged in successfully")
    
    def download_inventory(self, filename: str = None):
        """Download inventory page with all entries visible"""
        print(f"📦 Downloading inventory from {self.config.INVENTORY_URL}")
        
        # Navigate to inventory page
        self.page.goto(self.config.INVENTORY_URL)
        self.page.wait_for_load_state('networkidle')
        
        # Click on "Show entries" dropdown and select 100
        print(f"⚙️  Setting to show {self.config.ENTRIES_TO_SHOW} entries")
        try:
            # Wait for the dropdown
            self.page.wait_for_selector('select[name="inventory_length"]', timeout=5000)
            
            # Select 100 entries
            self.page.select_option('select[name="inventory_length"]', 
                                   str(self.config.ENTRIES_TO_SHOW))
            
            # Wait for table to reload
            time.sleep(2)
            self.page.wait_for_load_state('networkidle')
            
        except Exception as e:
            print(f"⚠️  Could not change entries display: {e}")
            print("   Continuing with default view...")
        
        # Generate filename if not provided
        if not filename:
            today = datetime.now().strftime('%b%d').upper()
            filename = f"Inventory - {today}.html"
        
        # Get full page HTML
        html_content = self.page.content()
        
        # Save to file
        filepath = self.config.DOWNLOAD_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 Saved to: {filepath}")
        return filepath
    
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

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration for CODPARTNER automation"""
    
    # Credentials
    USERNAME = os.getenv('CODPARTNER_USERNAME', '')
    PASSWORD = os.getenv('CODPARTNER_PASSWORD', '')
    
    # URLs
    BASE_URL = 'https://app.codpartner.com'
    LOGIN_URL = f'{BASE_URL}/login'
    INVENTORY_URL = f'{BASE_URL}/inventory'
    ORDERS_URL = f'{BASE_URL}/orders'
    ANALYTICS_URL = f'{BASE_URL}/reports/analytics/products'
    
    # Paths
    PROJECT_DIR = Path(__file__).parent.parent
    DOWNLOAD_DIR = PROJECT_DIR
    
    # Settings
    SHOW_BROWSER = False  # Headless mode (invisible browser)
    ENTRIES_TO_SHOW = 100  # Number of entries per page
    TIMEOUT = 30000  # 30 seconds
    
    @classmethod
    def validate(cls):
        """Check if credentials are set"""
        if not cls.USERNAME or not cls.PASSWORD:
            raise ValueError(
                "Credentials not set! Please create a .env file with:\n"
                "CODPARTNER_USERNAME=your_username\n"
                "CODPARTNER_PASSWORD=your_password"
            )

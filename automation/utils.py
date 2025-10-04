from datetime import datetime, timedelta
from pathlib import Path


def get_today_filename(prefix="Inventory"):
    """Generate filename with today's date"""
    today = datetime.now().strftime('%b%d').upper()
    return f"{prefix} - {today}.html"


def get_date_range(days_back=7):
    """Get date range for the last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def clean_old_files(directory: Path, pattern: str, keep_recent=7):
    """
    Clean up old HTML files, keep only recent ones
    
    Args:
        directory: Directory to clean
        pattern: File pattern to match (e.g., "Inventory*.html")
        keep_recent: Number of recent files to keep
    """
    files = sorted(directory.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if len(files) > keep_recent:
        for old_file in files[keep_recent:]:
            print(f"🗑️  Removing old file: {old_file.name}")
            old_file.unlink()

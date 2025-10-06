#!/bin/bash

echo "============================================================"
echo "🚀 Stock Management - Daily Automation Setup"
echo "============================================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$SCRIPT_DIR/com.stockmanagement.daily.plist"
DEST_PLIST="$HOME/Library/LaunchAgents/com.stockmanagement.daily.plist"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Copy the plist file
echo "📋 Installing automation..."
cp "$PLIST_FILE" "$DEST_PLIST"

# Load the launch agent
echo "⚙️  Activating daily automation..."
launchctl unload "$DEST_PLIST" 2>/dev/null  # Unload if already loaded
launchctl load "$DEST_PLIST"

echo ""
echo "============================================================"
echo "✅ Automation Installed!"
echo "============================================================"
echo ""
echo "📊 How it works:"
echo "   - Runs ONCE every 24 hours after you log in"
echo "   - Downloads today's inventory"
echo "   - Compares with yesterday"
echo "   - Creates Stock_*.csv report"
echo ""
echo "📁 Logs saved to:"
echo "   $SCRIPT_DIR/logs/"
echo ""
echo "🔧 To disable automation:"
echo "   ./disable_automation.sh"
echo ""
echo "🔧 To manually run anytime:"
echo "   python3 stock_update.py"
echo ""
echo "============================================================"

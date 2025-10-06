#!/bin/bash

echo "============================================================"
echo "🛑 Disabling Stock Management Automation"
echo "============================================================"
echo ""

DEST_PLIST="$HOME/Library/LaunchAgents/com.stockmanagement.daily.plist"

if [ -f "$DEST_PLIST" ]; then
    launchctl unload "$DEST_PLIST"
    rm "$DEST_PLIST"
    echo "✅ Automation disabled and removed"
else
    echo "⚠️  Automation not found (already disabled?)"
fi

echo ""
echo "You can still run manually with: python3 stock_update.py"
echo ""

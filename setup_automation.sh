#!/bin/bash
echo "============================================================"
echo "🚀 CODPARTNER Automation Setup"
echo "============================================================"

# Install Python dependencies
echo ""
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

echo ""
echo "============================================================"
echo "✅ Installation Complete!"
echo "============================================================"
echo ""
echo "📝 Next Steps:"
echo "1. Create your .env file with credentials:"
echo "   cp .env.example .env"
echo "   # Then edit .env and add your credentials"
echo ""
echo "2. Run the automation:"
echo "   python3 download_inventory.py"
echo ""
echo "============================================================"

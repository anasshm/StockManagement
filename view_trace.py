#!/usr/bin/env python3
"""
Trace Viewer Helper
Open the Playwright trace viewer to see your recorded session
"""

import subprocess
import sys
from pathlib import Path


def main():
    trace_file = Path("traces/analytics_session.zip")
    
    if not trace_file.exists():
        print("❌ Trace file not found: traces/analytics_session.zip")
        print()
        print("💡 To create a trace:")
        print("   1. Run: python3 record_session.py (to record actions)")
        print("   2. Run: python3 replay_recorded_session.py (to create trace)")
        print()
        sys.exit(1)
    
    print("=" * 60)
    print("🔍 Opening Playwright Trace Viewer")
    print("=" * 60)
    print()
    print(f"📁 Viewing: {trace_file}")
    print()
    print("🎯 In the viewer you can:")
    print("   - See screenshots of every action")
    print("   - Inspect DOM at each step")
    print("   - View network requests")
    print("   - Check element selectors")
    print()
    print("🚀 Opening viewer...")
    print()
    
    try:
        subprocess.run([
            'playwright',
            'show-trace',
            str(trace_file)
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure Playwright is installed:")
        print("   pip3 install playwright")
        print("   playwright install chromium")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Error: playwright command not found")
        print("\n💡 Install Playwright:")
        print("   pip3 install playwright")
        print("   playwright install chromium")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Viewer cancelled by user")
        sys.exit(0)


if __name__ == "__main__":
    main()


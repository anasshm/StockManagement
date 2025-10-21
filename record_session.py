#!/usr/bin/env python3
"""
Recording Session Helper
Launch Playwright Codegen to record your browser actions
"""

import subprocess
import sys
import time

def main():
    print("=" * 60)
    print("🎬 Starting Playwright Codegen Recording Session")
    print("=" * 60)
    print()
    print("📋 What will happen:")
    print("   1. Browser window opens (interact here)")
    print("   2. Inspector window opens (shows generated code)")
    print("   3. Perform your usual workflow")
    print("   4. Copy the generated code when done")
    print()
    print("💡 Tip: The Inspector shows Python code as you interact")
    print()
    print("🚀 Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Launch Playwright codegen
        subprocess.run([
            'playwright', 
            'codegen', 
            'https://app.codpartner.com/login'
        ], check=True)
        
        print()
        print("=" * 60)
        print("✅ Recording session ended")
        print("=" * 60)
        print()
        print("📝 Next steps:")
        print("   1. Copy the generated code from Inspector")
        print("   2. Paste it into automation/analytics_recorded.py")
        print("   3. Add trace recording wrapper (see template)")
        print("   4. Run: python3 replay_recorded_session.py")
        print()
        
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
        print("\n\n⚠️  Recording cancelled by user")
        sys.exit(0)


if __name__ == "__main__":
    main()


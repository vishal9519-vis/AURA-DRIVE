# ============================================================
#  AURA DRIVE — app.py
#  AI-Powered Adaptive Driver Intelligence & Safety System
#  Entry point — run this file to start the system
#
#  Author: AURA DRIVE Team
#  Version: 1.0.0
#  Date: 2025
# ============================================================

from config import Config

def main():
    print("=" * 55)
    print("   AURA DRIVE — AI Driver Safety System")
    print("   Version:", Config.VERSION)
    print("=" * 55)
    print("  System initializing...")
    print("  Modules: Face Detection | EAR | MAR | Alerts")
    print("  Status : Ready")
    print("=" * 55)
    print("\n  Run each Colab cell in order to start the system.")
    print("  See README.md for full instructions.\n")

if __name__ == "__main__":
    main()

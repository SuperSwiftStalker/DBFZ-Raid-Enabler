"""
DBFZ Raid Enabler - Main Entry Point

Dragon Ball FighterZ Raid Battle Enabler
Automated patching system for enabling offline raid battles.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.tui import DBFZRaidTUI
from utils.logger import logger


def main():
    """Main application entry point."""
    logger.info("=" * 60)
    logger.info("DBFZ Raid Enabler started")
    logger.info("=" * 60)

    try:
        # Create and run TUI
        tui = DBFZRaidTUI()
        tui.run()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n[Operation cancelled]")

    except Exception as e:
        logger.exception("Fatal error in main")
        print(f"\nFatal error: {e}")
        print("Check log file for details")
        input("\nPress Enter to exit...")

    finally:
        logger.info("DBFZ Raid Enabler exited")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()

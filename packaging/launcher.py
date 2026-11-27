"""PyInstaller entry script for OsteoQuant Desktop."""
import multiprocessing
import sys

from osteoquant.desktop.app import main

if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())

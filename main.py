import sys
import os

# Add src to python path so we can import packages from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from notes21 import __version__

def main():
    print(f"Welcome to notes21 version {__version__}")
    print("Music Analysis Toolkit Initialized.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Novelist Desktop - Entry Point"""
import sys
from pathlib import Path

# Add parent dir to path so 'src' is recognized as a package
sys.path.insert(0, str(Path(__file__).parent))

from src.ui import main

if __name__ == "__main__":
    main()

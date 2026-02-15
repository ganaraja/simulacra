"""Pytest configuration and shared fixtures."""
import sys
import os

# Ensure src is on path for backend package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

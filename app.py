"""
Entry point for deployment platforms
This file allows Render and other platforms to find the FastAPI app easily
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the FastAPI app
from main import app

# This is what deployment platforms will use
__all__ = ['app']

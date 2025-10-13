"""
Python Helpers Library

A collection of useful Python utilities and helper functions for common tasks.

Modules:
- file_ops: File and directory operations
- data_processing: Data manipulation and analysis utilities
- web_scraping: Web scraping and HTTP utilities
- automation: Task automation helpers
- utilities: General purpose utility functions
"""

__version__ = "0.1.0"
__author__ = "Serge"
__description__ = "A collection of useful Python utilities and helper functions"

# Import main modules for easy access
from . import file_ops
from . import data_processing
from . import web_scraping
from . import automation
from . import utilities

# Define what gets imported with "from python_helpers import *"
__all__ = [
    "file_ops",
    "data_processing", 
    "web_scraping",
    "automation",
    "utilities"
]
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google-style docstrings
    'sphinx.ext.viewcode',  # Adds links to source code
    'sphinx.ext.todo',      # Optional: For todo notes
]

# Path setup
import os
import sys
sys.path.insert(0, os.path.abspath('../'))  # Adjust this path to point to your project root

# Project information
project = 'Education Tool for ASIC Routing'
author = 'Your Name or Team'
release = '1.0'

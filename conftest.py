import sys
import os

# Add project root to Python path to help pytest find modules
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Rest of the conftest.py content remains the same

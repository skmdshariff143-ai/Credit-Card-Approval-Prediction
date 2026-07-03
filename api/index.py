import os
import sys

# Ensure root directory is on Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.app import app

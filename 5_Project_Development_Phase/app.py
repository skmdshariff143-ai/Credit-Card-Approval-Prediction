import os
import sys

# Ensure root directory is on Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

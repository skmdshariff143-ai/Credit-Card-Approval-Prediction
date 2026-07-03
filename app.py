import os
import sys
import traceback

# Ensure root directory is on Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from app.app import app
except Exception as e:
    print("IMPORT ERROR IN APP.PY:")
    traceback.print_exc()
    raise e

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

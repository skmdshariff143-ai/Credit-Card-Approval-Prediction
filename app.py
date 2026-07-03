import os
import sys
import traceback
from flask import Flask

# Ensure root directory is on Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from app.app import app
except Exception as e:
    print("IMPORT ERROR IN APP.PY:")
    traceback.print_exc()
    
    # Expose dummy app to allow Vercel build phase to complete successfully
    app = Flask(__name__)
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def fallback(path):
        err_msg = traceback.format_exc()
        return f"<h1>Deployment Startup Error</h1><pre>{err_msg}</pre>", 500

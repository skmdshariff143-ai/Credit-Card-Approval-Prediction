import os
import sys

# Add 5_Project_Development_Phase to sys.path so app modules import cleanly
phase5_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "5_Project_Development_Phase")
)
if phase5_dir not in sys.path:
    sys.path.insert(0, phase5_dir)

from app.app import create_app  # noqa: E402

# Create Flask WSGI application instance for Vercel Serverless Function
app = create_app()
handler = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

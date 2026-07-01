import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template

# Ensure root directory is on Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environmental variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))


def create_app() -> Flask:
    """
    Application factory pattern to instantiate the Flask web server.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configure environment configurations
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        from configs.production import ProductionConfig

        app.config.from_object(ProductionConfig)
    elif env == "testing":
        from configs.testing import TestingConfig

        app.config.from_object(TestingConfig)
    else:
        from configs.development import DevelopmentConfig

        app.config.from_object(DevelopmentConfig)

    # Import and register API Blueprints containing routes
    from src.api.routes import api_bp

    app.register_blueprint(api_bp)

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    # Local serving
    app.run(host="0.0.0.0", port=5000, debug=True)  # nosec B201 B104

import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Ensure root directory is on Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Apply sklearn compatibility patch if available
try:
    import src.utils.sklearn_compat  # noqa: F401
except ModuleNotFoundError:
    pass


# Load environmental variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))


# Initialize Flask-Login extension at module level
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please sign in to access this page."
login_manager.login_message_category = "info"


def create_app() -> Flask:
    """
    Application factory pattern to instantiate the Flask web server.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configure environment configurations
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        from config.production import ProductionConfig

        app.config.from_object(ProductionConfig)
    elif env == "testing":
        from config.testing import TestingConfig

        app.config.from_object(TestingConfig)
    else:
        from config.development import DevelopmentConfig

        app.config.from_object(DevelopmentConfig)

    # Initialize Flask extensions
    csrf = CSRFProtect(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login callback to reload user from session cookie."""
        from app.database.database import DatabaseManager
        from app.models.user import User

        db = DatabaseManager()
        row = db.get_user_by_id(int(user_id))
        return User.from_db_row(row)

    # Import and register API Blueprints containing routes
    from app.routes.routes import api_bp

    app.register_blueprint(api_bp)

    # Register Authentication Blueprint
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    # Exempt REST API endpoints from CSRF (they use JSON, not form submissions)
    from app.routes.routes import api_predict

    csrf.exempt(api_predict)

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    # Pre-load ML model and pipeline at startup to optimize response time and warm the container
    try:
        from app.services.predict import _predictor

        _predictor.load_pipeline()
        _predictor.load_model()
        app.logger.info("ML Model and preprocessing pipeline successfully pre-loaded during application startup.")
    except Exception as e:
        app.logger.error(f"Error pre-loading ML model or pipeline during startup: {str(e)}")

    # Register context processors
    @app.context_processor
    def inject_global_variables():
        return {"is_vercel": os.getenv("VERCEL") == "1"}

    return app


app = create_app()

if __name__ == "__main__":
    # Local serving
    app.run(host="0.0.0.0", port=5000, debug=True)  # nosec B201 B104

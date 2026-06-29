import os
import sys
from flask import Flask, render_template
from dotenv import load_dotenv

# Ensure the root directory is on the path for importing src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

def create_app():
    """
    Application factory pattern to create and configure the Flask app.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    # Configure secrets
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_development_secret_key_12345')
    
    # Register blueprints or import routes directly
    with app.app_context():
        import flask_app.routes as routes
        app.register_blueprint(routes.bp)
        
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', content="Error 404: Page not found. Please verify the URL."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', content="Error 500: Internal server error. Please try again later."), 500
        
    return app

if __name__ == "__main__":
    app = create_app()
    # Run server locally on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)

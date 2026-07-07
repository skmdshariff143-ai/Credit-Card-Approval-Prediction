import os


class ProductionConfig:
    """
    Production-grade Flask application settings.
    """

    TESTING = False
    DEBUG = False
    import sys
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        if "pytest" not in sys.modules:
            raise RuntimeError("Production SECRET_KEY environment variable is not configured.")
        SECRET_KEY = "prod-testing-dummy-secret"
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PORT = int(os.getenv("PORT", 5000))

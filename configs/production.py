import os

class ProductionConfig:
    """
    Production-grade Flask application settings.
    """
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "prod-creditguard-fallback-secret-987-xyz")
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PORT = int(os.getenv("PORT", 5000))

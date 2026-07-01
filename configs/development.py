import os


class DevelopmentConfig:
    """
    Local development Flask settings.
    """

    TESTING = False
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_12345")
    WTF_CSRF_ENABLED = True
    PORT = int(os.getenv("PORT", 5000))

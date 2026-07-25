class TestingConfig:
    """
    Unit test and pytest Flask settings.
    """

    TESTING = True
    DEBUG = False
    SECRET_KEY = "test_secret_key_99999"
    WTF_CSRF_ENABLED = False  # Disabled for endpoint post mock testing
    PORT = 5001

import os
from pathlib import Path

from dotenv import load_dotenv

# Load env variables from root directory
root_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=root_dir / ".env")


class ProjectConfig:
    """
    Enterprise Configuration loader using environment variables and YAML settings.
    """

    def __init__(self):
        self.BASE_DIR = root_dir
        self.FLASK_ENV = os.getenv("FLASK_ENV", "development")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_12345")

        # Logging settings
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", str(root_dir / "logs" / "app.log"))

        # IBM Watson Machine Learning Credentials
        self.IBM_API_KEY = os.getenv("IBM_API_KEY")
        self.IBM_URL = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
        self.IBM_INSTANCE_ID = os.getenv("IBM_INSTANCE_ID")
        self.IBM_SPACE_ID = os.getenv("IBM_SPACE_ID")
        self.IBM_SCORING_URL = os.getenv("IBM_SCORING_URL")

        # Create log directories if they don't exist
        os.makedirs(os.path.dirname(self.LOG_FILE_PATH), exist_ok=True)

    def get_paths(self):
        """
        Returns absolute paths to all major data, models, and reports directories.
        """
        return {
            "raw_dir": self.BASE_DIR / "data" / "raw",
            "processed_dir": self.BASE_DIR / "data" / "processed",
            "interim_dir": self.BASE_DIR / "data" / "interim",
            "external_dir": self.BASE_DIR / "data" / "external",
            "models_dir": self.BASE_DIR / "models",
            "reports_dir": self.BASE_DIR / "reports",
            "diagrams_dir": self.BASE_DIR / "diagrams",
            "logs_dir": self.BASE_DIR / "logs",
        }


config = ProjectConfig()

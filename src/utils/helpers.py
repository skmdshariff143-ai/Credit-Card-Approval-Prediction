import os
import yaml
import joblib
from src.utils.logger import get_logger
from src.utils.exceptions import ConfigurationError

logger = get_logger(__name__)

def load_yaml(file_path):
    """
    Safely loads a YAML configuration file.
    """
    if not os.path.exists(file_path):
        logger.error(f"YAML configuration file not found at: {file_path}")
        raise ConfigurationError(f"Configuration file not found: {file_path}")
        
    try:
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)
            logger.debug(f"Loaded YAML configuration from: {file_path}")
            return content
    except Exception as e:
        logger.error(f"Error reading YAML file at {file_path}: {str(e)}")
        raise ConfigurationError(f"Error reading YAML file: {str(e)}")


def save_artifact(obj, file_path):
    """
    Saves an object (model, scaler, encoder) to a file using joblib.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        joblib.dump(obj, file_path)
        logger.info(f"Saved artifact to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save artifact to {file_path}: {str(e)}")
        raise


def load_artifact(file_path):
    """
    Loads an object (model, scaler, encoder) from a file using joblib.
    """
    if not os.path.exists(file_path):
        logger.error(f"Artifact file not found at: {file_path}")
        raise FileNotFoundError(f"Artifact not found: {file_path}")
        
    try:
        obj = joblib.load(file_path)
        logger.debug(f"Loaded artifact from: {file_path}")
        return obj
    except Exception as e:
        logger.error(f"Failed to load artifact from {file_path}: {str(e)}")
        raise

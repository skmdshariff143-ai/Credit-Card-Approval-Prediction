import json
import os

import joblib

from app.utils.exceptions import DataPreprocessingError
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_pkl(file_path):
    """
    Safely loads a serialized pickle/joblib file.
    """
    if not os.path.exists(file_path):
        logger.error(f"Pickle file not found at: {file_path}")
        raise FileNotFoundError(f"Pickle file not found: {file_path}")
    try:
        obj = joblib.load(file_path)
        logger.debug(f"Loaded pickle file from: {file_path}")
        return obj
    except Exception as e:
        logger.error(f"Failed to load pickle file from {file_path}: {str(e)}")
        raise DataPreprocessingError(f"Failed to load pickle file: {str(e)}")


def save_pkl(obj, file_path):
    """
    Safely saves a serialized object to pickle/joblib format.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(obj, file_path)
        logger.info(f"Saved pickle file to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save pickle file to {file_path}: {str(e)}")
        raise DataPreprocessingError(f"Failed to save pickle file: {str(e)}")


def save_json(data_dict, file_path):
    """
    Saves a dictionary as a JSON file.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data_dict, f, indent=4)
        logger.info(f"Saved JSON file to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {str(e)}")
        raise


def load_json(file_path):
    """
    Loads a JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {str(e)}")
        raise

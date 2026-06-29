import os
import pandas as pd
from src.utils.logger import get_logger
from src.utils.exceptions import DataLoadingError, ConfigurationError
from src.utils.helpers import load_yaml

logger = get_logger(__name__)

class DataLoader:
    """
    Handles reading raw datasets, checking file existence, and basic schema checks.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config_path = config_path
        self.config = load_yaml(config_path)
        
        if "paths" not in self.config:
            logger.error("Configuration file missing 'paths' key.")
            raise ConfigurationError("Configuration file missing 'paths' key.")
            
        self.app_path = self.config["paths"].get("raw_application_data")
        self.credit_path = self.config["paths"].get("raw_credit_data")
        
        if not self.app_path or not self.credit_path:
            logger.error("Raw data paths are not configured in the YAML file.")
            raise ConfigurationError("Raw data paths are not configured in the YAML file.")

    def load_application_record(self):
        """
        Loads the application record CSV file.
        """
        logger.info(f"Loading application records from: {self.app_path}")
        if not os.path.exists(self.app_path):
            logger.error(f"Application record file not found: {self.app_path}")
            raise DataLoadingError(f"Application record file not found: {self.app_path}")
            
        try:
            df = pd.read_csv(self.app_path)
            logger.info(f"Successfully loaded application records with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load application records: {str(e)}")
            raise DataLoadingError(f"Failed to load application records: {str(e)}")

    def load_credit_record(self):
        """
        Loads the credit record CSV file.
        """
        logger.info(f"Loading credit records from: {self.credit_path}")
        if not os.path.exists(self.credit_path):
            logger.error(f"Credit record file not found: {self.credit_path}")
            raise DataLoadingError(f"Credit record file not found: {self.credit_path}")
            
        try:
            df = pd.read_csv(self.credit_path)
            logger.info(f"Successfully loaded credit records with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load credit records: {str(e)}")
            raise DataLoadingError(f"Failed to load credit records: {str(e)}")
            
    def load_all(self):
        """
        Loads both datasets and returns them as a tuple (app_df, credit_df).
        """
        app_df = self.load_application_record()
        credit_df = self.load_credit_record()
        return app_df, credit_df

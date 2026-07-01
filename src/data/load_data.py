import os

import pandas as pd

from configs.config import config
from src.utils.exceptions import DataLoadingError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    """
    Ingests and loads raw credit card and application history CSV files.
    """

    def __init__(self):
        paths = config.get_paths()
        self.raw_dir = paths["raw_dir"]
        self.app_path = os.path.join(self.raw_dir, "application_record.csv")
        self.credit_path = os.path.join(self.raw_dir, "credit_record.csv")

    def load_application_records(self) -> pd.DataFrame:
        """
        Loads the application record CSV dataset.
        """
        logger.info(f"Loading application records from: {self.app_path}")
        if not os.path.exists(self.app_path):
            logger.error(f"Application record file not found: {self.app_path}")
            raise DataLoadingError(f"Raw application record not found: {self.app_path}")
        try:
            df = pd.read_csv(self.app_path)
            logger.info(f"Loaded application records with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading application records: {str(e)}")
            raise DataLoadingError(f"Error loading application records: {str(e)}")

    def load_credit_records(self) -> pd.DataFrame:
        """
        Loads the credit record CSV dataset.
        """
        logger.info(f"Loading credit records from: {self.credit_path}")
        if not os.path.exists(self.credit_path):
            logger.error(f"Credit record file not found: {self.credit_path}")
            raise DataLoadingError(f"Raw credit record not found: {self.credit_path}")
        try:
            df = pd.read_csv(self.credit_path)
            logger.info(f"Loaded credit records with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading credit records: {str(e)}")
            raise DataLoadingError(f"Error loading credit records: {str(e)}")

    def load_all(self):
        """
        Returns both loaded DataFrames.
        """
        return self.load_application_records(), self.load_credit_records()

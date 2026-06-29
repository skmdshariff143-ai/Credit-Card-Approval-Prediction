import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DuplicateHandler:
    """
    Identifies and removes duplicate records from DataFrame structures.
    """
    def __init__(self):
        self.duplicate_count = 0
        
    def detect_duplicates(self, df: pd.DataFrame) -> int:
        """
        Calculates number of duplicated rows.
        """
        self.duplicate_count = int(df.duplicated().sum())
        logger.info(f"Duplicate rows detected: {self.duplicate_count}")
        return self.duplicate_count
        
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes duplicates, keeping the first occurrence.
        """
        self.detect_duplicates(df)
        if self.duplicate_count > 0:
            df_cleaned = df.drop_duplicates(keep='first')
            logger.info(f"Successfully removed {self.duplicate_count} duplicate rows.")
            return df_cleaned
        return df

import pandas as pd
from configs.constants import NUMERICAL_COLS, CATEGORICAL_COLS, BINARY_COLS
from src.utils.logger import get_logger
from src.utils.exceptions import DataValidationError

logger = get_logger(__name__)

class DataValidator:
    """
    Validates shapes, schemas, and values of the input datasets.
    """
    def __init__(self):
        self.expected_app_cols = set(NUMERICAL_COLS + CATEGORICAL_COLS + BINARY_COLS)
        
    def validate_application_schema(self, df: pd.DataFrame) -> bool:
        """
        Validates column names and datatypes of the application dataset.
        """
        logger.info("Validating application schema...")
        if df is None or df.empty:
            raise DataValidationError("Application record is empty or None.")
            
        missing_cols = [col for col in self.expected_app_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Application record missing critical columns: {missing_cols}")
            raise DataValidationError(f"Application record missing critical columns: {missing_cols}")
            
        # Verify numeric columns are float/int
        for col in NUMERICAL_COLS:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                logger.error(f"Column '{col}' is expected to be numeric.")
                raise DataValidationError(f"Column '{col}' must be numeric.")
                
        logger.info("Application schema validation passed.")
        return True

    def validate_credit_schema(self, df: pd.DataFrame) -> bool:
        """
        Validates the credit records schema.
        """
        logger.info("Validating credit schema...")
        if df is None or df.empty:
            raise DataValidationError("Credit record is empty or None.")
            
        required_cols = {"ID", "MONTHS_BALANCE", "STATUS"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            logger.error(f"Credit record missing expected columns: {missing_cols}")
            raise DataValidationError(f"Credit record missing expected columns: {missing_cols}")
            
        logger.info("Credit schema validation passed.")
        return True

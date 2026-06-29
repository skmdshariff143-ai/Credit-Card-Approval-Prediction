import pandas as pd
from src.utils.logger import get_logger
from src.utils.exceptions import DataValidationError

logger = get_logger(__name__)

class DataValidator:
    """
    Validates data schemas, column presence, data types, and check ID distributions.
    """
    def __init__(self):
        # Expected columns in the raw files
        self.expected_app_cols = {
            'ID': 'int64',
            'CODE_GENDER': 'object',
            'FLAG_OWN_CAR': 'object',
            'FLAG_OWN_REALTY': 'object',
            'CNT_CHILDREN': 'int64',
            'AMT_INCOME_TOTAL': 'float64',
            'NAME_INCOME_TYPE': 'object',
            'NAME_EDUCATION_TYPE': 'object',
            'NAME_FAMILY_STATUS': 'object',
            'NAME_HOUSING_TYPE': 'object',
            'DAYS_BIRTH': 'int64',
            'DAYS_EMPLOYED': 'int64',
            'FLAG_MOBIL': 'int64',
            'FLAG_WORK_PHONE': 'int64',
            'FLAG_PHONE': 'int64',
            'FLAG_EMAIL': 'int64',
            'CNT_FAM_MEMBERS': 'float64'
        }
        
        self.expected_credit_cols = {
            'ID': 'int64',
            'MONTHS_BALANCE': 'int64',
            'STATUS': 'object'
        }

    def validate_application_record(self, df):
        """
        Validates the application record dataframe.
        """
        logger.info("Validating application record schema...")
        if df is None or df.empty:
            logger.error("Application record DataFrame is empty or None.")
            raise DataValidationError("Application record DataFrame is empty or None.")

        # Check column presence
        missing_cols = [col for col in self.expected_app_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Application record missing expected columns: {missing_cols}")
            raise DataValidationError(f"Application record missing expected columns: {missing_cols}")

        # Check ID uniqueness (we can have duplicate IDs in raw app record but let's check)
        logger.info(f"Unique IDs in application record: {df['ID'].nunique()} out of {len(df)}")
        
        # Check basic ranges
        if (df['CNT_CHILDREN'] < 0).any():
            logger.warning("Found negative values in children count.")
            
        if (df['AMT_INCOME_TOTAL'] <= 0).any():
            logger.error("Found zero or negative values in income.")
            raise DataValidationError("Income values must be strictly positive.")
            
        logger.info("Application record validation passed successfully.")
        return True

    def validate_credit_record(self, df):
        """
        Validates the credit record dataframe.
        """
        logger.info("Validating credit record schema...")
        if df is None or df.empty:
            logger.error("Credit record DataFrame is empty or None.")
            raise DataValidationError("Credit record DataFrame is empty or None.")

        # Check column presence
        missing_cols = [col for col in self.expected_credit_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Credit record missing expected columns: {missing_cols}")
            raise DataValidationError(f"Credit record missing expected columns: {missing_cols}")

        # Validate STATUS values
        valid_statuses = {'0', '1', '2', '3', '4', '5', 'C', 'X'}
        invalid_statuses = df[~df['STATUS'].astype(str).isin(valid_statuses)]['STATUS'].unique()
        if len(invalid_statuses) > 0:
            logger.error(f"Found invalid values in STATUS column: {invalid_statuses}")
            raise DataValidationError(f"Found invalid values in STATUS column: {invalid_statuses}")

        logger.info("Credit record validation passed successfully.")
        return True

    def validate_merge_compatibility(self, app_df, credit_df):
        """
        Checks if there are overlapping IDs between application and credit records.
        """
        logger.info("Checking merge compatibility between datasets...")
        app_ids = set(app_df['ID'])
        credit_ids = set(credit_df['ID'])
        
        overlapping = app_ids.intersection(credit_ids)
        logger.info(f"Overlapping IDs between application and credit: {len(overlapping)}")
        
        if len(overlapping) == 0:
            logger.error("No matching IDs found between application and credit records.")
            raise DataValidationError("No matching IDs found between application and credit records.")
            
        logger.info("Merge compatibility check passed.")
        return True

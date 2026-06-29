import os
import pandas as pd
import numpy as np
from src.utils.logger import get_logger
from src.utils.exceptions import DataCleaningError
from src.utils.helpers import load_yaml

logger = get_logger(__name__)

class DataCleaner:
    """
    Cleans raw application records, aggregates credit records to derive the target variable,
    resolves anomalies, handles missing values, and merges them.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        self.cleaned_path = self.config["paths"].get("processed_clean_data")
        
    def aggregate_credit_history(self, credit_df):
        """
        Aggregates monthly credit records to classify each customer as approved (0) or rejected (1).
        Target definition:
        - Class 1 (Bad): If customer was ever late by 60+ days (STATUS in '2', '3', '4', '5').
        - Class 0 (Good): Otherwise (STATUS in 'C', 'X', '0', '1').
        """
        logger.info("Aggregating credit records to label customers...")
        try:
            # Check if any record is bad
            # Let's map STATUS to a risk level: '2', '3', '4', '5' are bad
            bad_statuses = {'2', '3', '4', '5'}
            
            credit_df['IS_BAD'] = credit_df['STATUS'].astype(str).apply(lambda x: 1 if x in bad_statuses else 0)
            
            # Group by ID and find if they ever had a bad month
            target_df = credit_df.groupby('ID')['IS_BAD'].max().reset_index()
            target_df.rename(columns={'IS_BAD': 'STATUS_TARGET'}, inplace=True)
            
            # Print class distribution
            counts = target_df['STATUS_TARGET'].value_counts()
            logger.info(f"Credit aggregation complete. Good (0): {counts.get(0, 0)}, Bad (1): {counts.get(1, 0)}")
            return target_df
        except Exception as e:
            logger.error(f"Error aggregating credit records: {str(e)}")
            raise DataCleaningError(f"Error aggregating credit records: {str(e)}")

    def clean_application_data(self, app_df):
        """
        Cleans application features: handles missing values, anomalies, duplicates, and signs.
        """
        logger.info("Cleaning application records...")
        try:
            df = app_df.copy()
            
            # 1. Remove duplicate rows based on ID
            num_dups = df.duplicated(subset=['ID']).sum()
            if num_dups > 0:
                logger.info(f"Removing {num_dups} duplicate IDs in application records.")
                df.drop_duplicates(subset=['ID'], keep='first', inplace=True)
                
            # 2. Clean DAYS_BIRTH -> convert negative days to positive age in years
            df['AGE_YEARS'] = np.round(-df['DAYS_BIRTH'] / 365.25, 2)
            
            # 3. Clean DAYS_EMPLOYED -> create UNEMPLOYED flag, convert anomalous value 365243 to 0, 
            # and other negative values to positive years of employment.
            df['FLAG_UNEMPLOYED'] = (df['DAYS_EMPLOYED'] == 365243).astype(int)
            
            # Convert days employed to years
            df['YEARS_EMPLOYED'] = df['DAYS_EMPLOYED'].apply(
                lambda x: 0.0 if x == 365243 else np.round(-x / 365.25, 2)
            )
            
            # Remove raw days variables to keep it clean, or keep them for now.
            # Let's keep them, but AGE_YEARS and YEARS_EMPLOYED are much cleaner features.
            
            # 4. Handle missing values in OCCUPATION_TYPE
            missing_occupations = df['OCCUPATION_TYPE'].isnull().sum()
            logger.info(f"Missing values in OCCUPATION_TYPE: {missing_occupations} ({missing_occupations / len(df) * 100:.2f}%)")
            df['OCCUPATION_TYPE'].fillna('Unknown', inplace=True)
            
            # 5. Fill any family members missing values (impute median if any, though usually none)
            if df['CNT_FAM_MEMBERS'].isnull().any():
                fam_median = df['CNT_FAM_MEMBERS'].median()
                df['CNT_FAM_MEMBERS'].fillna(fam_median, inplace=True)
                
            df['CNT_FAM_MEMBERS'] = df['CNT_FAM_MEMBERS'].astype(int)
            
            logger.info("Application records cleaned.")
            return df
        except Exception as e:
            logger.error(f"Error cleaning application records: {str(e)}")
            raise DataCleaningError(f"Error cleaning application records: {str(e)}")

    def clean_and_merge(self, app_df, credit_df):
        """
        Runs the full clean and merge pipeline, then saves the result.
        """
        logger.info("Starting clean and merge process...")
        try:
            # 1. Clean app records
            clean_app_df = self.clean_application_data(app_df)
            
            # 2. Aggregate credit records
            target_df = self.aggregate_credit_history(credit_df)
            
            # 3. Merge datasets (Inner join to ensure both demographic and status records are present)
            merged_df = pd.merge(clean_app_df, target_df, on='ID', how='inner')
            logger.info(f"Merged dataset shape: {merged_df.shape}")
            
            # 4. Save to processed directory
            os.makedirs(os.path.dirname(self.cleaned_path), exist_ok=True)
            merged_df.to_csv(self.cleaned_path, index=False)
            logger.info(f"Cleaned and merged dataset saved to: {self.cleaned_path}")
            
            return merged_df
        except Exception as e:
            logger.error(f"Error in clean_and_merge: {str(e)}")
            raise DataCleaningError(f"Error in clean_and_merge: {str(e)}")

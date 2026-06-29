import pandas as pd
import numpy as np
from src.data.data_cleaner import DataCleaner

def test_aggregate_credit_history(mock_credit_df):
    """
    Test that credit aggregation correctly labels bad customers (status >= 60 days late).
    """
    cleaner = DataCleaner("e:/Credit-Card-Approval-Prediction/config/config.yaml")
    target_df = cleaner.aggregate_credit_history(mock_credit_df)
    
    # ID 5008804 has only status 'C' and '0' -> Good (0)
    assert target_df[target_df['ID'] == 5008804]['STATUS_TARGET'].values[0] == 0
    
    # ID 5008805 has status '2' (late 60-89 days) -> Bad (1)
    assert target_df[target_df['ID'] == 5008805]['STATUS_TARGET'].values[0] == 1

def test_clean_application_data(mock_app_df):
    """
    Test that application cleaning resolves anomalies, signs, and fills missing values.
    """
    cleaner = DataCleaner("e:/Credit-Card-Approval-Prediction/config/config.yaml")
    clean_app = cleaner.clean_application_data(mock_app_df)
    
    # Check age conversion (negative days to positive years)
    assert clean_app.loc[clean_app['ID'] == 5008804, 'AGE_YEARS'].values[0] == round(12000 / 365.25, 2)
    
    # Check unemployed conversion (365243 to 0 and set unemployed flag to 1)
    pensioner_row = clean_app[clean_app['ID'] == 5008805]
    assert pensioner_row['FLAG_UNEMPLOYED'].values[0] == 1
    assert pensioner_row['YEARS_EMPLOYED'].values[0] == 0.0
    
    # Check employed conversion (negative days to positive years)
    employed_row = clean_app[clean_app['ID'] == 5008804]
    assert employed_row['FLAG_UNEMPLOYED'].values[0] == 0
    assert employed_row['YEARS_EMPLOYED'].values[0] == round(2000 / 365.25, 2)
    
    # Check missing occupation filling
    assert pensioner_row['OCCUPATION_TYPE'].values[0] == 'Unknown'

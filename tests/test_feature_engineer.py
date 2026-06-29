import pytest
import pandas as pd
import numpy as np
from src.features.feature_engineer import FeatureEngineer

def test_feature_creation(mock_app_df):
    """
    Test custom domain features generation.
    """
    engineer = FeatureEngineer("e:/Credit-Card-Approval-Prediction/config/config.yaml")
    
    # Process age/employment manually since it's done in cleaner
    df = mock_app_df.copy()
    df['AGE_YEARS'] = -df['DAYS_BIRTH'] / 365.25
    df['YEARS_EMPLOYED'] = df['DAYS_EMPLOYED'].apply(
        lambda x: 0.0 if x == 365243 else -x / 365.25
    )
    
    df_feats = engineer.create_features(df)
    
    # Income per member check
    assert df_feats.loc[df_feats['ID'] == 5008804, 'INCOME_PER_MEMBER'].values[0] == 120000.0 / 2.0
    
    # Employed to age ratio check
    expected_ratio = (2000/365.25) / (12000/365.25)
    assert df_feats.loc[df_feats['ID'] == 5008804, 'EMPLOYED_TO_AGE_RATIO'].values[0] == expected_ratio

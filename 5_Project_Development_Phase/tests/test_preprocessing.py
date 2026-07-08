import numpy as np
import pandas as pd
import pytest

from src.preprocessing.missing_values import MissingValueImputer
from src.preprocessing.outliers import OutlierCapper


@pytest.fixture
def sample_df():
    """
    Returns a sample DataFrame with missing values and outliers.
    """
    df = pd.DataFrame(
        {"income": [10000.0, np.nan, 30000.0, 1000000.0], "gender": ["M", "F", np.nan, "F"]}  # 1,000,000 is outlier
    )
    return df


def test_missing_value_imputer(sample_df):
    """
    Test missing value median and mode imputations.
    """
    imputer = MissingValueImputer()
    imputer.fit(sample_df, numerical_cols=["income"], categorical_cols=["gender"])

    # Transform
    df_imputed = imputer.transform(sample_df)

    # Missing income should be filled with median: (10000+30000)/2 = 20000
    assert not df_imputed["income"].isnull().any()
    assert df_imputed.loc[1, "income"] == 30000.0  # median of [10k, 30k, 1M] is 30k

    # Missing gender filled with mode: 'F'
    assert not df_imputed["gender"].isnull().any()
    assert df_imputed.loc[2, "gender"] == "F"


def test_outlier_capper(sample_df):
    """
    Test outlier capping.
    """
    capper = OutlierCapper(factor=0.1)
    capper.fit(sample_df, numerical_cols=["income"])
    df_capped = capper.transform(sample_df)

    # 1,000,000 should be capped to upper limit
    assert df_capped.loc[3, "income"] < 1000000.0


def test_preprocessing_pipeline_single_class_edge_case():
    """
    Test that the preprocessing pipeline handles target labels with a single class gracefully.
    """
    from src.preprocessing.pipeline import PreprocessingPipeline
    from unittest.mock import patch
    import pandas as pd
    
    pipeline = PreprocessingPipeline()
    
    # Create mock inputs where y has only a single class
    mock_app_df = pd.DataFrame({
        "ID": [1, 2, 3],
        "CODE_GENDER": ["M", "F", "M"],
        "FLAG_OWN_CAR": ["N", "N", "N"],
        "FLAG_OWN_REALTY": ["N", "N", "N"],
        "CNT_CHILDREN": [0, 0, 0],
        "AMT_INCOME_TOTAL": [50000.0, 60000.0, 70000.0],
        "NAME_INCOME_TYPE": ["Working", "Working", "Working"],
        "NAME_EDUCATION_TYPE": ["Higher education", "Higher education", "Higher education"],
        "NAME_FAMILY_STATUS": ["Single / not married", "Single / not married", "Single / not married"],
        "NAME_HOUSING_TYPE": ["House / apartment", "House / apartment", "House / apartment"],
        "DAYS_BIRTH": [-12000, -13000, -14000],
        "DAYS_EMPLOYED": [-1000, -2000, -3000],
        "FLAG_MOBIL": [1, 1, 1],
        "FLAG_WORK_PHONE": [0, 0, 0],
        "FLAG_PHONE": [0, 0, 0],
        "FLAG_EMAIL": [0, 0, 0],
        "OCCUPATION_TYPE": ["Laborers", "Laborers", "Laborers"],
        "CNT_FAM_MEMBERS": [1, 1, 1]
    })
    
    # A single class target: all "Approved" (0)
    mock_credit_df = pd.DataFrame({
        "ID": [1, 2, 3],
        "MONTHS_BALANCE": [0, 0, 0],
        "STATUS": ["C", "C", "C"]
    })
    
    from pathlib import Path
    mock_paths = {
        "raw_dir": Path("."),
        "processed_dir": Path("."),
        "models_dir": Path("."),
        "reports_dir": Path("."),
        "logs_dir": Path("."),
    }
    
    from config.config import config
    with patch.object(config, "get_paths", return_value=mock_paths):
        with patch("src.preprocessing.pipeline.DataLoader.load_all", return_value=(mock_app_df, mock_credit_df)):
            with patch("pandas.DataFrame.to_csv") as mock_df_csv, \
                 patch("pandas.Series.to_csv") as mock_series_csv, \
                 patch("src.preprocessing.pipeline.save_pkl") as mock_save:
                train_shape, test_shape = pipeline.execute_full_pipeline()
                assert train_shape is not None
                assert test_shape is not None
                assert mock_df_csv.called

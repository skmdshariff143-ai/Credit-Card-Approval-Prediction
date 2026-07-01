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

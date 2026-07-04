import numpy as np
import pandas as pd

from src.utils.exceptions import FeatureEngineeringError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FeatureEngineer:
    """
    Applies mathematical transforms and derives domain indicators (ratios, flags)
    from applicant features.
    """

    def __init__(self):
        pass

    def extract_custom_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates structured engineered variables from raw variables:
        - AGE_YEARS: converts birth days offset to positive age.
        - YEARS_EMPLOYED: converts employment days offset to positive employment years.
        - FLAG_UNEMPLOYED: binary indicator for unemployed status.
        - INCOME_PER_MEMBER: ratios of total income relative to family members.
        - EMPLOYED_TO_AGE_RATIO: proportion of life spent employed.
        """
        logger.info("Extracting custom features...")
        try:
            df_feat = df.copy()

            # Age conversion (DAYS_BIRTH is negative)
            if "DAYS_BIRTH" in df_feat.columns:
                df_feat["AGE_YEARS"] = np.round(-df_feat["DAYS_BIRTH"] / 365.25, 2)

            # Employment conversion
            if "DAYS_EMPLOYED" in df_feat.columns:
                # 365243 represents unemployed in Kaggle dataset
                df_feat["FLAG_UNEMPLOYED"] = (df_feat["DAYS_EMPLOYED"] == 365243).astype(int)
                df_feat["YEARS_EMPLOYED"] = df_feat["DAYS_EMPLOYED"].apply(
                    lambda x: 0.0 if x == 365243 else np.round(-x / 365.25, 2)
                )

            # Income per family member
            if "AMT_INCOME_TOTAL" in df_feat.columns and "CNT_FAM_MEMBERS" in df_feat.columns:
                df_feat["INCOME_PER_MEMBER"] = df_feat["AMT_INCOME_TOTAL"] / df_feat["CNT_FAM_MEMBERS"]

            # Employment ratio
            if "YEARS_EMPLOYED" in df_feat.columns and "AGE_YEARS" in df_feat.columns:
                # Avoid division by zero by clipping AGE_YEARS
                df_feat["EMPLOYED_TO_AGE_RATIO"] = df_feat["YEARS_EMPLOYED"] / df_feat["AGE_YEARS"].clip(lower=1.0)

            # Clean missing values in OCCUPATION_TYPE
            if "OCCUPATION_TYPE" in df_feat.columns:
                df_feat["OCCUPATION_TYPE"] = df_feat["OCCUPATION_TYPE"].fillna("Unknown")

            logger.info("Custom features extraction complete.")
            return df_feat
        except Exception as e:
            logger.error(f"Failed to extract features: {str(e)}")
            raise FeatureEngineeringError(f"Feature extraction failed: {str(e)}")

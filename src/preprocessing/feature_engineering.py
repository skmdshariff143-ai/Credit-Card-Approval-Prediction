import numpy as np
import pandas as pd

from src.utils.exceptions import FeatureEngineeringError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FeatureEngineer:
    """
    Formulates custom domain indicators, bins continuous features into groups,
    and designs risk metrics to improve model prediction power.
    """

    def __init__(self):
        pass

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Derives:
        - AGE_YEARS: positive age.
        - YEARS_EMPLOYED: positive years employed (dummy code handled).
        - INCOME_PER_MEMBER: income relative to family members size.
        - INCOME_GROUP: binned income category.
        - AGE_GROUP: binned age.
        - EXPERIENCE_BUCKET: binned experience duration.
        - FINANCIAL_STABILITY_SCORE: custom stability proxy.
        """
        logger.info("Starting feature engineering transformations...")
        try:
            df_feat = df.copy()

            # Age conversion
            if "DAYS_BIRTH" in df_feat.columns:
                df_feat["AGE_YEARS"] = np.round(-df_feat["DAYS_BIRTH"] / 365.25, 2)

            # Employment conversion
            if "DAYS_EMPLOYED" in df_feat.columns:
                df_feat["FLAG_UNEMPLOYED"] = (df_feat["DAYS_EMPLOYED"] == 365243).astype(int)
                df_feat["YEARS_EMPLOYED"] = df_feat["DAYS_EMPLOYED"].apply(
                    lambda x: 0.0 if x == 365243 else np.round(-x / 365.25, 2)
                )

            # Income per Family Member
            if "AMT_INCOME_TOTAL" in df_feat.columns and "CNT_FAM_MEMBERS" in df_feat.columns:
                df_feat["INCOME_PER_MEMBER"] = df_feat["AMT_INCOME_TOTAL"] / df_feat["CNT_FAM_MEMBERS"].clip(lower=1)

            # Income Groups (Low < 100k, Medium 100k-250k, High > 250k)
            if "AMT_INCOME_TOTAL" in df_feat.columns:
                df_feat["INCOME_GROUP"] = pd.cut(
                    df_feat["AMT_INCOME_TOTAL"], bins=[0, 100000, 250000, np.inf], labels=["low", "medium", "high"]
                ).astype(str)

            # Age Groups (Youth <= 35, Adult 35-55, Senior > 55)
            if "AGE_YEARS" in df_feat.columns:
                df_feat["AGE_GROUP"] = pd.cut(
                    df_feat["AGE_YEARS"], bins=[0, 35, 55, np.inf], labels=["youth", "adult", "senior"]
                ).astype(str)

            # Experience Buckets (Entry <= 3, Mid 3-10, Senior > 10)
            if "YEARS_EMPLOYED" in df_feat.columns:
                df_feat["EXPERIENCE_BUCKET"] = pd.cut(
                    df_feat["YEARS_EMPLOYED"], bins=[-1, 3, 10, np.inf], labels=["entry", "mid", "senior"]
                ).astype(str)

            # Financial Stability Score: Scale 0 to 3
            # +1 if owns property (FLAG_OWN_REALTY == 'Y')
            # +1 if owns car (FLAG_OWN_CAR == 'Y')
            # +1 if income > $150,000
            score = np.zeros(len(df_feat))
            if "FLAG_OWN_REALTY" in df_feat.columns:
                score += (df_feat["FLAG_OWN_REALTY"] == "Y").astype(int)
            if "FLAG_OWN_CAR" in df_feat.columns:
                score += (df_feat["FLAG_OWN_CAR"] == "Y").astype(int)
            if "AMT_INCOME_TOTAL" in df_feat.columns:
                score += (df_feat["AMT_INCOME_TOTAL"] > 150000.0).astype(int)
            df_feat["FINANCIAL_STABILITY_SCORE"] = score

            logger.info("Feature engineering transformations completed successfully.")
            return df_feat
        except Exception as e:
            logger.error(f"Failed feature engineering: {str(e)}")
            raise FeatureEngineeringError(f"Feature engineering failed: {str(e)}")

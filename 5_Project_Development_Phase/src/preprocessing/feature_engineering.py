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
        Derives custom domain indicators, bins continuous features into groups,
        and designs risk metrics to improve model prediction power.
        """
        logger.info("Starting feature engineering transformations...")
        try:
            df_feat = df.copy()
            self._add_demographics(df_feat)
            self._add_ratios(df_feat)
            self._add_buckets(df_feat)
            self._add_stability_score(df_feat)
            logger.info("Feature engineering transformations completed successfully.")
            return df_feat
        except Exception as e:
            logger.error(f"Failed feature engineering: {str(e)}")
            raise FeatureEngineeringError(f"Feature engineering failed: {str(e)}")

    def _add_demographics(self, df: pd.DataFrame):
        # Age conversion
        if "DAYS_BIRTH" in df.columns:
            df["AGE_YEARS"] = np.round(-df["DAYS_BIRTH"] / 365.25, 2)

        # Employment conversion
        if "DAYS_EMPLOYED" in df.columns:
            df["FLAG_UNEMPLOYED"] = (df["DAYS_EMPLOYED"] == 365243).astype(int)
            df["YEARS_EMPLOYED"] = df["DAYS_EMPLOYED"].apply(lambda x: 0.0 if x == 365243 else np.round(-x / 365.25, 2))

    def _add_ratios(self, df: pd.DataFrame):
        # Income per Family Member
        if "AMT_INCOME_TOTAL" in df.columns and "CNT_FAM_MEMBERS" in df.columns:
            df["INCOME_PER_MEMBER"] = df["AMT_INCOME_TOTAL"] / df["CNT_FAM_MEMBERS"].clip(lower=1)

        # Employed to Age Ratio
        if "YEARS_EMPLOYED" in df.columns and "AGE_YEARS" in df.columns:
            df["EMPLOYED_TO_AGE_RATIO"] = df["YEARS_EMPLOYED"] / df["AGE_YEARS"].clip(lower=18.0)

    def _add_buckets(self, df: pd.DataFrame):
        # Income Groups (Low < 100k, Medium 100k-250k, High > 250k)
        if "AMT_INCOME_TOTAL" in df.columns:
            df["INCOME_GROUP"] = pd.cut(
                df["AMT_INCOME_TOTAL"], bins=[0, 100000, 250000, np.inf], labels=["low", "medium", "high"]
            ).astype(str)

        # Age Groups (Youth <= 35, Adult 35-55, Senior > 55)
        if "AGE_YEARS" in df.columns:
            df["AGE_GROUP"] = pd.cut(
                df["AGE_YEARS"], bins=[0, 35, 55, np.inf], labels=["youth", "adult", "senior"]
            ).astype(str)

        # Experience Buckets (Entry <= 3, Mid 3-10, Senior > 10)
        if "YEARS_EMPLOYED" in df.columns:
            df["EXPERIENCE_BUCKET"] = pd.cut(
                df["YEARS_EMPLOYED"], bins=[-1, 3, 10, np.inf], labels=["entry", "mid", "senior"]
            ).astype(str)

    def _add_stability_score(self, df: pd.DataFrame):
        # Financial Stability Score: Scale 0 to 3
        # +1 if owns property (FLAG_OWN_REALTY == 'Y')
        # +1 if owns car (FLAG_OWN_CAR == 'Y')
        # +1 if income > $150,000
        score = np.zeros(len(df))
        if "FLAG_OWN_REALTY" in df.columns:
            score += (df["FLAG_OWN_REALTY"] == "Y").astype(int)
        if "FLAG_OWN_CAR" in df.columns:
            score += (df["FLAG_OWN_CAR"] == "Y").astype(int)
        if "AMT_INCOME_TOTAL" in df.columns:
            score += (df["AMT_INCOME_TOTAL"] > 150000.0).astype(int)
        df["FINANCIAL_STABILITY_SCORE"] = score

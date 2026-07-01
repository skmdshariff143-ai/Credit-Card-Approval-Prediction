import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class OutlierCapper:
    """
    Caps numerical outliers using the Interquartile Range (IQR) method.
    """

    def __init__(self, factor=1.5):
        self.factor = factor
        self.limits = {}

    def fit(self, df: pd.DataFrame, numerical_cols):
        """
        Calculates upper and lower boundaries for each numerical feature.
        """
        logger.info("Fitting outlier capper bounds...")
        for col in numerical_cols:
            if col in df.columns:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower_limit = q1 - self.factor * iqr
                upper_limit = q3 + self.factor * iqr
                self.limits[col] = (lower_limit, upper_limit)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clips feature values using the learned boundaries.
        """
        logger.info("Applying outlier capping...")
        df_capped = df.copy()

        for col, (lower_limit, upper_limit) in self.limits.items():
            if col in df_capped.columns:
                df_capped[col] = df_capped[col].clip(lower=lower_limit, upper=upper_limit)

        return df_capped

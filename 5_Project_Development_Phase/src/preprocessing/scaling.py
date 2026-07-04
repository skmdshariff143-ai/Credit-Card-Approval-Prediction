import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.utils.logger import get_logger

logger = get_logger(__name__)


class NumericalScaler:
    """
    Standardizes numerical columns using scikit-learn StandardScaler.
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.numerical_cols = []

    def fit(self, df: pd.DataFrame, numerical_cols):
        """
        Fits the StandardScaler on the numeric columns.
        """
        logger.info("Fitting numerical scaler...")
        self.numerical_cols = list(numerical_cols)
        present_cols = [col for col in self.numerical_cols if col in df.columns]
        if present_cols:
            self.scaler.fit(df[present_cols])
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scales the numeric columns.
        """
        logger.info("Applying numerical scaling...")
        df_scaled = df.copy()
        present_cols = [col for col in self.numerical_cols if col in df_scaled.columns]

        if not present_cols:
            return df_scaled

        scaled_array = self.scaler.transform(df_scaled[present_cols])
        df_scaled[present_cols] = scaled_array
        return df_scaled

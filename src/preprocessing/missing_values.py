import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MissingValueImputer:
    """
    Imputes missing values in numerical and categorical features.
    """
    def __init__(self):
        self.numerical_medians = {}
        self.categorical_modes = {}
        
    def fit(self, df: pd.DataFrame, numerical_cols, categorical_cols):
        """
        Learns medians and modes of features from the training DataFrame.
        """
        logger.info("Fitting missing value imputer...")
        for col in numerical_cols:
            if col in df.columns:
                self.numerical_medians[col] = df[col].median()
                
        for col in categorical_cols:
            if col in df.columns:
                # Mode might be empty if all NaN, handle fallback
                mode_series = df[col].mode()
                self.categorical_modes[col] = mode_series.iloc[0] if not mode_series.empty else "Unknown"
        return self
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fills missing values with the learned medians and modes.
        """
        logger.info("Applying missing value imputation...")
        df_imputed = df.copy()
        
        for col, val in self.numerical_medians.items():
            if col in df_imputed.columns:
                df_imputed[col] = df_imputed[col].fillna(val)
                
        for col, val in self.categorical_modes.items():
            if col in df_imputed.columns:
                df_imputed[col] = df_imputed[col].fillna(val)
                
        return df_imputed

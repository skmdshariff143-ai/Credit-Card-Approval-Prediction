import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CategoricalEncoder:
    """
    Encodes categorical features using scikit-learn OneHotEncoder.
    """
    def __init__(self):
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.categorical_cols = []
        
    def fit(self, df: pd.DataFrame, categorical_cols):
        """
        Fits the OneHotEncoder on the categorical columns.
        """
        logger.info("Fitting categorical encoder...")
        self.categorical_cols = list(categorical_cols)
        # Verify columns are present
        present_cols = [col for col in self.categorical_cols if col in df.columns]
        if present_cols:
            self.encoder.fit(df[present_cols])
        return self
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encodes the categorical columns and returns a DataFrame with encoded feature names.
        """
        logger.info("Applying categorical encoding...")
        df_encoded = df.copy()
        present_cols = [col for col in self.categorical_cols if col in df_encoded.columns]
        
        if not present_cols:
            return df_encoded
            
        encoded_array = self.encoder.transform(df_encoded[present_cols])
        feature_names = self.encoder.get_feature_names_out(present_cols)
        
        encoded_df = pd.DataFrame(encoded_array, columns=feature_names, index=df_encoded.index)
        
        # Drop raw categorical columns and concatenate encoded ones
        df_encoded.drop(columns=present_cols, inplace=True)
        return pd.concat([df_encoded, encoded_df], axis=1)

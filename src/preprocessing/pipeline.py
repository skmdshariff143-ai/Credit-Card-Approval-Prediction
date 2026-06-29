import os
import pandas as pd
from configs.config import config
from configs.constants import NUMERICAL_COLS, CATEGORICAL_COLS, BINARY_COLS
from src.preprocessing.missing_values import MissingValueImputer
from src.preprocessing.outliers import OutlierCapper
from src.preprocessing.encoding import CategoricalEncoder
from src.preprocessing.scaling import NumericalScaler
from src.utils.logger import get_logger
from src.utils.exceptions import DataPreprocessingError
from src.utils.helper import save_pkl

logger = get_logger(__name__)

class PreprocessingPipeline:
    """
    Unified pipeline wrapping imputer, outlier capper, encoder, and scaler.
    Fits all objects on training data and serializes them.
    """
    def __init__(self):
        self.imputer = MissingValueImputer()
        self.capper = OutlierCapper()
        self.encoder = CategoricalEncoder()
        self.scaler = NumericalScaler()
        self.feature_names = []
        
    def fit(self, df: pd.DataFrame, numerical_cols=None, categorical_cols=None):
        """
        Fits all preprocessors on the input DataFrame.
        """
        logger.info("Fitting preprocessing pipeline...")
        num_cols = numerical_cols if numerical_cols is not None else NUMERICAL_COLS
        cat_cols = categorical_cols if categorical_cols is not None else CATEGORICAL_COLS
        
        try:
            # 1. Fit Imputer
            self.imputer.fit(df, num_cols, cat_cols)
            df_imputed = self.imputer.transform(df)
            
            # 2. Fit Outlier Capper
            self.capper.fit(df_imputed, num_cols)
            df_capped = self.capper.transform(df_imputed)
            
            # 3. Fit Encoder
            self.encoder.fit(df_capped, cat_cols)
            df_encoded = self.encoder.transform(df_capped)
            
            # 4. Fit Scaler
            # Note: After encoding, original cat columns are dropped. We scale numerical columns.
            self.scaler.fit(df_encoded, num_cols)
            
            logger.info("Preprocessing pipeline fitted successfully.")
            return self
        except Exception as e:
            logger.error(f"Failed to fit preprocessing pipeline: {str(e)}")
            raise DataPreprocessingError(f"Preprocessing fit failed: {str(e)}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies imputer, capper, encoder, and scaler transformations.
        """
        logger.info("Running preprocessing pipeline transform...")
        try:
            df_imputed = self.imputer.transform(df)
            df_capped = self.capper.transform(df_imputed)
            df_encoded = self.encoder.transform(df_capped)
            df_scaled = self.scaler.transform(df_encoded)
            
            # Save transformed columns names list
            self.feature_names = list(df_scaled.columns)
            return df_scaled
        except Exception as e:
            logger.error(f"Failed to transform data: {str(e)}")
            raise DataPreprocessingError(f"Preprocessing transform failed: {str(e)}")
            
    def save_artifacts(self, models_dir=None):
        """
        Saves scaler and encoder artifacts to models directory.
        """
        tgt_dir = models_dir if models_dir is not None else config.get_paths()["models_dir"]
        os.makedirs(tgt_dir, exist_ok=True)
        
        logger.info(f"Saving preprocessor artifacts to {tgt_dir}...")
        save_pkl(self.scaler.scaler, os.path.join(tgt_dir, "scaler.pkl"))
        save_pkl(self.encoder.encoder, os.path.join(tgt_dir, "encoder.pkl"))
        save_pkl(self, os.path.join(tgt_dir, "preprocessor_pipeline.pkl"))
        logger.info("Preprocessor artifacts saved.")

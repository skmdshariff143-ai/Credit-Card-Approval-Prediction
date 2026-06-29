import os
import pandas as pd
import numpy as np
from configs.config import config
from src.utils.logger import get_logger
from src.utils.helper import load_pkl
from src.utils.exceptions import ModelTrainingError

logger = get_logger(__name__)

class InferenceEngine:
    """
    Handles single/batch predictions by loading serialized preprocessors and model.
    """
    def __init__(self, models_dir=None):
        paths = config.get_paths()
        self.models_dir = models_dir if models_dir is not None else paths["models_dir"]
        
        self.preprocessor_path = os.path.join(self.models_dir, "preprocessor_pipeline.pkl")
        self.model_path = os.path.join(self.models_dir, "trained_model.pkl")
        
        self.preprocessor = None
        self.model = None
        
    def load_artifacts(self):
        """
        Loads the preprocessor pipeline and trained model from models directory.
        """
        logger.info("Loading inference artifacts...")
        try:
            if self.preprocessor is None:
                self.preprocessor = load_pkl(self.preprocessor_path)
            if self.model is None:
                self.model = load_pkl(self.model_path)
            logger.info("Inference artifacts loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load inference artifacts: {str(e)}")
            raise FileNotFoundError(f"Inference artifacts not loaded: {str(e)}")

    def predict(self, input_df: pd.DataFrame) -> dict:
        """
        Executes preprocessing and model scoring for an input DataFrame.
        """
        self.load_artifacts()
        try:
            # 1. Apply preprocessors
            X_inf = self.preprocessor.transform(input_df)
            
            # Ensure correct columns order
            cols = self.preprocessor.feature_names
            X_inf = X_inf[cols]
            
            # 2. Run prediction
            pred = int(self.model.predict(X_inf)[0])
            
            # 3. Retrieve probability
            if hasattr(self.model, "predict_proba"):
                prob_bad = float(self.model.predict_proba(X_inf)[0][1])
            else:
                prob_bad = 1.0 if pred == 1 else 0.0
                
            approval_probability = (1.0 - prob_bad) * 100.0
            result = "Approved" if pred == 0 else "Rejected"
            
            return {
                "decision": result,
                "class_code": pred,
                "approval_probability_percent": round(approval_probability, 2)
            }
        except Exception as e:
            logger.error(f"Inference scoring failed: {str(e)}")
            raise ModelTrainingError(f"Inference failed: {str(e)}")

import os
import pandas as pd
from configs.config import config
from src.utils.logger import get_logger
from src.utils.helper import load_pkl
from src.utils.exceptions import ModelTrainingError
from src.models.explainability import ExplanationEngine

logger = get_logger(__name__)

class RiskPredictor:
    """
    Handles model predictions, feature standardizations, and JSON schema validations.
    """
    def __init__(self):
        paths = config.get_paths()
        self.models_dir = paths["models_dir"]
        self.pipeline_path = os.path.join(self.models_dir, "preprocessing_pipeline.pkl")
        self.model_path = os.path.join(self.models_dir, "best_model.pkl")
        self.pipeline = None
        self.model = None
        
    def load_pipeline(self):
        """Loads the fitted preprocessing pipeline object."""
        if self.pipeline is None:
            logger.info(f"Loading pipeline from {self.pipeline_path}...")
            self.pipeline = load_pkl(self.pipeline_path)
        return self.pipeline

    def load_model(self):
        """Loads the best trained classifier object."""
        if self.model is None:
            logger.info(f"Loading model from {self.model_path}...")
            self.model = load_pkl(self.model_path)
        return self.model

    def validate_input(self, input_data: dict) -> bool:
        """Validates that input dictionary contains all required fields."""
        required_fields = {
            'code_gender', 'cnt_children', 'cnt_fam_members', 'age_years', 
            'amt_income_total', 'flag_own_car', 'flag_own_realty', 
            'name_income_type', 'name_education_type', 'name_family_status', 
            'name_housing_type', 'years_employed', 'flag_unemployed'
        }
        missing = required_fields - set(input_data.keys())
        if missing:
            logger.error(f"Input verification failed. Missing fields: {missing}")
            return False
        return True

    def predict(self, input_df: pd.DataFrame):
        """
        Runs binary class predictions. If single-sample DataFrame, returns a formatted dictionary
        for REST/client serving compatibility with local explainability outputs.
        """
        pipeline = self.load_pipeline()
        model = self.load_model()
        
        X_trans = pipeline.transform(input_df)
        preds = model.predict(X_trans)
        
        if len(input_df) == 1:
            prob_1 = 0.0
            if hasattr(model, "predict_proba"):
                prob_raw = model.predict_proba(X_trans)
                try:
                    prob_1 = prob_raw[0][1]
                except Exception:
                    try:
                        prob_1 = prob_raw[0]
                    except Exception:
                        prob_1 = 0.0
            decision = "Approved" if preds[0] == 0 else "Rejected"
            try:
                prob_1_val = float(prob_1)
            except Exception:
                prob_1_val = 0.0
            
            approval_prob = (1.0 - prob_1_val) * 100.0
            
            # Generate explanation map
            try:
                explainer = ExplanationEngine(model, pipeline)
                explanation = explainer.explain_instance(input_df)
            except Exception as e:
                logger.error(f"Failed to calculate local explanation: {str(e)}")
                explanation = {"error": str(e)}
                
            return {
                "decision": decision,
                "approval_probability_percent": float(round(approval_prob, 2)),
                "explanation": explanation
            }
        return list(preds)

    def predict_probability(self, input_df: pd.DataFrame) -> list:
        """Runs risk probability calculations."""
        pipeline = self.load_pipeline()
        model = self.load_model()
        
        X_trans = pipeline.transform(input_df)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_trans)[:, 1]
        else:
            preds = model.predict(X_trans)
            probs = [1.0 if p == 1 else 0.0 for p in preds]
        return list(probs)

# Functional API wrapper endpoints for external services
_predictor = RiskPredictor()

def load_pipeline():
    return _predictor.load_pipeline()

def load_model():
    return _predictor.load_model()

def validate_input(input_data: dict) -> bool:
    return _predictor.validate_input(input_data)

def predict(input_df: pd.DataFrame) -> list:
    return _predictor.predict(input_df)

def predict_probability(input_df: pd.DataFrame) -> list:
    return _predictor.predict_probability(input_df)

# Backward compatibility alias
InferenceEngine = RiskPredictor

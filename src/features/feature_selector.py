import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from src.utils.logger import get_logger
from src.utils.helpers import load_yaml

logger = get_logger(__name__)

class FeatureSelector:
    """
    Ranks features by importance using a Random Forest model, and helps in filtering low-importance features.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        
    def analyze_feature_importance(self, X, y):
        """
        Fits a Random Forest model to calculate and print feature importances.
        """
        logger.info("Running feature importance analysis using Random Forest...")
        try:
            random_state = self.config["model_params"].get("random_state", 42)
            rf = RandomForestClassifier(
                n_estimators=100, 
                max_depth=10, 
                random_state=random_state, 
                class_weight='balanced',
                n_jobs=-1
            )
            rf.fit(X, y)
            
            importances = rf.feature_importances_
            feature_names = X.columns
            
            # Create a sorted DataFrame
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances
            }).sort_values(by='Importance', ascending=False).reset_index(drop=True)
            
            logger.info("Top 15 Features by Importance:")
            for idx, row in importance_df.head(15).iterrows():
                logger.info(f"{row['Feature']}: {row['Importance']:.4f}")
                
            return importance_df
        except Exception as e:
            logger.error(f"Failed to calculate feature importances: {str(e)}")
            raise

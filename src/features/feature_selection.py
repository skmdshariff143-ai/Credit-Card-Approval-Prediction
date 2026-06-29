import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from configs.constants import RANDOM_STATE
from src.utils.logger import get_logger
from src.utils.exceptions import FeatureEngineeringError

logger = get_logger(__name__)

class FeatureSelector:
    """
    Ranks features based on Random Forest feature importances.
    """
    def __init__(self, threshold=0.01):
        self.threshold = threshold
        self.importances_df = None
        self.selected_features = []
        
    def fit_selection(self, X: pd.DataFrame, y: pd.Series):
        """
        Fits a Random Forest model on training splits and ranks features.
        """
        logger.info("Running feature selection model...")
        try:
            rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=12,
                class_weight='balanced',
                random_state=RANDOM_STATE,
                n_jobs=-1
            )
            rf.fit(X, y)
            
            importances = rf.feature_importances_
            feature_names = X.columns
            
            self.importances_df = pd.DataFrame({
                "Feature": feature_names,
                "Importance": importances
            }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
            
            # Select features above threshold
            self.selected_features = self.importances_df[
                self.importances_df["Importance"] >= self.threshold
            ]["Feature"].tolist()
            
            logger.info(f"Selected {len(self.selected_features)} features out of {len(feature_names)} using threshold {self.threshold}.")
            return self
        except Exception as e:
            logger.error(f"Feature selection failed: {str(e)}")
            raise FeatureEngineeringError(f"Feature selection run failed: {str(e)}")

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Filters out features below the threshold.
        """
        if not self.selected_features:
            logger.warning("No features selected, returning original DataFrame.")
            return X
        return X[self.selected_features]

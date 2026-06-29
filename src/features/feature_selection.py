import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from configs.config import config
from configs.constants import RANDOM_STATE
from src.utils.logger import get_logger
from src.utils.exceptions import FeatureEngineeringError

logger = get_logger(__name__)

class FeatureSelector:
    """
    Evaluates features utilizing Random Forest Importances and Mutual Information scores.
    Outputs ranking reports and filters features.
    """
    def __init__(self, threshold=0.005):
        self.threshold = threshold
        self.importances_df = None
        self.selected_features = []
        paths = config.get_paths()
        self.reports_dir = paths["reports_dir"]
        
    def fit_selection(self, X: pd.DataFrame, y: pd.Series):
        """
        Calculates Random Forest importance and Mutual Information scores to rank features.
        """
        logger.info("Starting feature ranking and selection...")
        try:
            # 1. Fit Random Forest
            rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=12,
                class_weight='balanced',
                random_state=RANDOM_STATE,
                n_jobs=-1
            )
            rf.fit(X, y)
            rf_importances = rf.feature_importances_
            
            # 2. Compute Mutual Information
            logger.info("Computing Mutual Information scores...")
            mi_scores = mutual_info_classif(X, y, random_state=RANDOM_STATE)
            
            # 3. Build ranking table
            self.importances_df = pd.DataFrame({
                "Feature": X.columns,
                "RF_Importance": rf_importances,
                "Mutual_Information": mi_scores
            }).sort_values(by="RF_Importance", ascending=False).reset_index(drop=True)
            
            # 4. Filter features based on RF importance threshold
            self.selected_features = self.importances_df[
                self.importances_df["RF_Importance"] >= self.threshold
            ]["Feature"].tolist()
            
            # Save ranking table to reports
            os.makedirs(self.reports_dir, exist_ok=True)
            ranking_path = os.path.join(self.reports_dir, "Feature_Selection_Ranking.csv")
            self.importances_df.to_csv(ranking_path, index=False)
            logger.info(f"Feature ranking saved to: {ranking_path}")
            
            logger.info(f"Selected {len(self.selected_features)} features above threshold {self.threshold}.")
            return self
        except Exception as e:
            logger.error(f"Feature selection failed: {str(e)}")
            raise FeatureEngineeringError(f"Feature selection run failed: {str(e)}")

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Slices columns to retain only selected features.
        """
        if not self.selected_features:
            logger.warning("No features selected, returning original DataFrame.")
            return X
        return X[self.selected_features]

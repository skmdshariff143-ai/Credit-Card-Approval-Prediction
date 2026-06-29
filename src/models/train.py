import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from configs.config import config
from configs.constants import RANDOM_STATE
from src.utils.logger import get_logger
from src.utils.exceptions import ModelTrainingError
from src.utils.helper import save_pkl

logger = get_logger(__name__)

class ModelTrainer:
    """
    Handles training of base classifiers and serializes model objects.
    """
    def __init__(self):
        paths = config.get_paths()
        self.models_dir = paths["models_dir"]
        self.random_state = RANDOM_STATE
        
    def get_baseline_models(self):
        """
        Instantiates baseline Logistic Regression, Decision Tree, Random Forest, and XGBoost models.
        """
        models = {
            "logistic_regression": LogisticRegression(
                max_iter=1000, 
                class_weight='balanced', 
                random_state=self.random_state
            ),
            "decision_tree": DecisionTreeClassifier(
                class_weight='balanced', 
                random_state=self.random_state
            ),
            "random_forest": RandomForestClassifier(
                class_weight='balanced', 
                n_jobs=-1, 
                random_state=self.random_state
            ),
            "xgboost": XGBClassifier(
                eval_metric="logloss", 
                random_state=self.random_state
            )
        }
        return models

    def train_model(self, name, model, X_train, y_train):
        """
        Fits a classifier on training dataset splits.
        """
        logger.info(f"Training model '{name}'...")
        try:
            model.fit(X_train, y_train)
            logger.info(f"Model '{name}' trained successfully.")
            return model
        except Exception as e:
            logger.error(f"Failed to train model '{name}': {str(e)}")
            raise ModelTrainingError(f"Model training failed for {name}: {str(e)}")

    def save_model(self, name, model):
        """
        Serializes trained model to the models folder.
        """
        file_path = os.path.join(self.models_dir, f"{name}.pkl")
        save_pkl(model, file_path)

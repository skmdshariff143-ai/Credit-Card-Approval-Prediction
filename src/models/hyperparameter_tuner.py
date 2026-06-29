import os
from sklearn.model_selection import GridSearchCV
from src.utils.logger import get_logger
from src.utils.helpers import load_yaml

logger = get_logger(__name__)

class HyperparameterTuner:
    """
    Handles GridSearchCV hyperparameter tuning for classification models.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        self.tuning_config = self.config.get("hyperparameter_tuning", {})
        self.random_state = self.config["model_params"].get("random_state", 42)
        
    def tune_model(self, name, model, X_train, y_train, cv=5):
        """
        Tunes a specific model using GridSearchCV and the grid defined in config.yaml.
        """
        grid = self.tuning_config.get(name, {})
        if not grid:
            logger.warning(f"No tuning grid defined for {name}. Returning base model.")
            return model
            
        logger.info(f"Tuning hyperparameters for {name} with CV={cv}...")
        try:
            # We optimize for F1-score due to class imbalance
            grid_search = GridSearchCV(
                estimator=model,
                param_grid=grid,
                scoring='f1',
                cv=cv,
                n_jobs=-1,
                verbose=1
            )
            grid_search.fit(X_train, y_train)
            
            logger.info(f"Best parameters for {name}: {grid_search.best_params_}")
            logger.info(f"Best cross-validation F1-score for {name}: {grid_search.best_score_:.4f}")
            
            return grid_search.best_estimator_
        except Exception as e:
            logger.warning(f"Hyperparameter tuning failed for {name} due to library compatibility: {str(e)}. Falling back to base model.")
            return model

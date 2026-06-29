import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from src.utils.logger import get_logger
from src.utils.exceptions import ModelTrainingError
from src.utils.helpers import load_yaml, save_artifact

logger = get_logger(__name__)

class ModelTrainer:
    """
    Manages the training of four classification algorithms:
    Logistic Regression, Decision Tree, Random Forest, and XGBoost.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        self.models_dir = self.config["paths"].get("models_dir")
        self.params = self.config.get("model_params", {})
        
        self.trained_models = {}
        
    def train_logistic_regression(self, X_train, y_train):
        """
        Trains Logistic Regression model using configured parameters.
        """
        logger.info("Training Logistic Regression...")
        try:
            lr_params = self.params.get("logistic_regression", {})
            random_state = self.params.get("random_state", 42)
            
            model = LogisticRegression(
                penalty=lr_params.get("penalty", "l2"),
                solver=lr_params.get("solver", "lbfgs"),
                max_iter=lr_params.get("max_iter", 1000),
                C=lr_params.get("C", 1.0),
                class_weight=lr_params.get("class_weight", "balanced"),
                random_state=random_state
            )
            model.fit(X_train, y_train)
            logger.info("Logistic Regression training complete.")
            self.trained_models["logistic_regression"] = model
            return model
        except Exception as e:
            logger.error(f"Failed to train Logistic Regression: {str(e)}")
            raise ModelTrainingError(f"Logistic Regression training failed: {str(e)}")

    def train_decision_tree(self, X_train, y_train):
        """
        Trains Decision Tree model using configured parameters.
        """
        logger.info("Training Decision Tree Classifier...")
        try:
            dt_params = self.params.get("decision_tree", {})
            random_state = self.params.get("random_state", 42)
            
            model = DecisionTreeClassifier(
                criterion=dt_params.get("criterion", "gini"),
                max_depth=dt_params.get("max_depth", 10),
                min_samples_split=dt_params.get("min_samples_split", 5),
                class_weight=dt_params.get("class_weight", "balanced"),
                random_state=random_state
            )
            model.fit(X_train, y_train)
            logger.info("Decision Tree training complete.")
            self.trained_models["decision_tree"] = model
            return model
        except Exception as e:
            logger.error(f"Failed to train Decision Tree: {str(e)}")
            raise ModelTrainingError(f"Decision Tree training failed: {str(e)}")

    def train_random_forest(self, X_train, y_train):
        """
        Trains Random Forest model using configured parameters.
        """
        logger.info("Training Random Forest Classifier...")
        try:
            rf_params = self.params.get("random_forest", {})
            random_state = self.params.get("random_state", 42)
            
            model = RandomForestClassifier(
                n_estimators=rf_params.get("n_estimators", 100),
                criterion=rf_params.get("criterion", "gini"),
                max_depth=rf_params.get("max_depth", 15),
                min_samples_split=rf_params.get("min_samples_split", 5),
                class_weight=rf_params.get("class_weight", "balanced"),
                n_jobs=rf_params.get("n_jobs", -1),
                random_state=random_state
            )
            model.fit(X_train, y_train)
            logger.info("Random Forest training complete.")
            self.trained_models["random_forest"] = model
            return model
        except Exception as e:
            logger.error(f"Failed to train Random Forest: {str(e)}")
            raise ModelTrainingError(f"Random Forest training failed: {str(e)}")

    def train_xgboost(self, X_train, y_train):
        """
        Trains XGBoost model using configured parameters.
        """
        logger.info("Training XGBoost Classifier...")
        try:
            xgb_params = self.params.get("xgboost", {})
            random_state = self.params.get("random_state", 42)
            
            model = XGBClassifier(
                n_estimators=xgb_params.get("n_estimators", 150),
                max_depth=xgb_params.get("max_depth", 6),
                learning_rate=xgb_params.get("learning_rate", 0.1),
                subsample=xgb_params.get("subsample", 0.8),
                colsample_bytree=xgb_params.get("colsample_bytree", 0.8),
                scale_pos_weight=xgb_params.get("scale_pos_weight", 1),
                eval_metric=xgb_params.get("eval_metric", "logloss"),
                random_state=random_state
            )
            model.fit(X_train, y_train)
            logger.info("XGBoost training complete.")
            self.trained_models["xgboost"] = model
            return model
        except Exception as e:
            logger.error(f"Failed to train XGBoost: {str(e)}")
            raise ModelTrainingError(f"XGBoost training failed: {str(e)}")
            
    def train_all(self, X_train, y_train):
        """
        Trains all 4 models sequentially.
        """
        self.train_logistic_regression(X_train, y_train)
        self.train_decision_tree(X_train, y_train)
        self.train_random_forest(X_train, y_train)
        self.train_xgboost(X_train, y_train)
        return self.trained_models
        
    def save_models(self):
        """
        Saves all trained models to the configured models folder.
        """
        logger.info(f"Saving trained models to: {self.models_dir}")
        try:
            os.makedirs(self.models_dir, exist_ok=True)
            for name, model in self.trained_models.items():
                model_path = os.path.join(self.models_dir, f"{name}.joblib")
                save_artifact(model, model_path)
            logger.info("All models saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save models: {str(e)}")
            raise ModelTrainingError(f"Model saving failed: {str(e)}")

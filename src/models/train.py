import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from configs.constants import RANDOM_STATE
from src.utils.exceptions import ModelTrainingError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelTrainer:
    """
    Handles fitting and timing of baseline risk classifiers.
    """

    def __init__(self):
        self.random_state = RANDOM_STATE

    def get_baseline_models(self) -> dict:
        """
        Instantiates Logistic Regression, Decision Tree, Random Forest, and XGBoost classifiers.
        """
        models = {
            "logistic_regression": LogisticRegression(
                max_iter=1000, class_weight="balanced", random_state=self.random_state
            ),
            "decision_tree": DecisionTreeClassifier(class_weight="balanced", random_state=self.random_state),
            "random_forest": RandomForestClassifier(class_weight="balanced", n_jobs=-1, random_state=self.random_state),
            "xgboost": XGBClassifier(eval_metric="logloss", random_state=self.random_state),
        }
        return models

    def train_and_time_model(self, name: str, model, X_train, y_train) -> tuple:
        """
        Fits a classifier, measuring the training time elapsed.
        """
        logger.info(f"Training model '{name}'...")
        start_time = time.time()
        try:
            model.fit(X_train, y_train)
            train_time = time.time() - start_time
            logger.info(f"Model '{name}' training complete in {train_time:.4f} seconds.")
            return model, train_time
        except Exception as e:
            logger.error(f"Failed to train model '{name}': {str(e)}")
            raise ModelTrainingError(f"Model training failed for {name}: {str(e)}")

    def measure_inference_speed(self, model, X_test) -> tuple:
        """
        Runs predictions on test split and measures total inference duration.
        """
        start_time = time.time()
        y_pred = model.predict(X_test)
        inference_time = time.time() - start_time

        y_prob = None
        if hasattr(model, "predict_proba"):
            y_prob_raw = model.predict_proba(X_test)
            y_prob = (
                y_prob_raw[:, 1] if hasattr(y_prob_raw, "ndim") and y_prob_raw.ndim > 1 else [p[1] for p in y_prob_raw]
            )

        return y_pred, y_prob, inference_time

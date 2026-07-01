from sklearn.model_selection import GridSearchCV

from src.utils.logger import get_logger

logger = get_logger(__name__)


class HyperparameterTuner:
    """
    Executes GridSearchCV parameters search to optimize F1-score for minority default classes.
    """

    def __init__(self, cv=3):
        self.cv = cv
        self.param_grids = {
            "logistic_regression": {"C": [0.1, 1.0, 10.0]},
            "decision_tree": {"max_depth": [5, 10, None], "min_samples_split": [2, 5]},
            "random_forest": {"n_estimators": [50, 100], "max_depth": [10, 15]},
            "xgboost": {"n_estimators": [50, 100], "max_depth": [4, 6], "learning_rate": [0.05, 0.1]},
        }

    def tune(self, name: str, model, X_train, y_train):
        """
        Runs GridSearchCV param search. Integrates robust fallback on sklearn/XGBoost conflicts.
        """
        grid = self.param_grids.get(name, {})
        if not grid:
            logger.warning(f"No grid params found for {name}. Returning base model.")
            return model

        logger.info(f"Tuning hyperparameters for model '{name}'...")
        try:
            grid_search = GridSearchCV(estimator=model, param_grid=grid, scoring="f1", cv=self.cv, n_jobs=-1, verbose=1)
            grid_search.fit(X_train, y_train)

            logger.info(f"Best parameters for {name}: {grid_search.best_params_}")
            logger.info(f"Best CV F1-score for {name}: {grid_search.best_score_:.4f}")
            return grid_search.best_estimator_
        except Exception as e:
            logger.warning(
                f"Hyperparameter tuning failed for {name} due to environment compatibility: {str(e)}. "
                "Returning baseline model."
            )
            return model

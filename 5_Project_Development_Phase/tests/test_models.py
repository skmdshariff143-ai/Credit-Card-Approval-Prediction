import pytest

from src.models.evaluate import ModelEvaluator
from src.models.train import ModelTrainer


def test_model_trainer_baselines():
    """
    Test that ModelTrainer returns the expected base classifiers.
    """
    trainer = ModelTrainer()
    models = trainer.get_baseline_models()

    assert "logistic_regression" in models
    assert "decision_tree" in models
    assert "random_forest" in models
    assert "xgboost" in models


def test_model_evaluation_metrics():
    """
    Test evaluation metric computations.
    """
    evaluator = ModelEvaluator()

    # Mock model
    class MockModel:
        def predict(self, X):
            return [0, 1, 0, 0]

        def predict_proba(self, X):
            return [[0.9, 0.1], [0.3, 0.7], [0.8, 0.2], [0.95, 0.05]]

    y_test = [0, 1, 1, 0]
    metrics = evaluator.evaluate_model("mock_model", MockModel(), [1, 2, 3, 4], y_test)

    # 3 correct predictions out of 4 -> Accuracy = 0.75
    assert metrics["Accuracy"] == 0.75
    assert metrics["Precision"] == 1.0
    assert metrics["Recall"] == pytest.approx(1 / 2)


def test_deployed_best_model():
    """
    Assert that the serialized best_model.pkl is a valid scikit-learn BaseEstimator
    with predict and predict_proba methods.
    """
    import os
    import joblib
    from sklearn.base import BaseEstimator
    from config.config import config

    paths = config.get_paths()
    model_path = os.path.join(paths["models_dir"], "best_model.pkl")
    assert os.path.exists(model_path), f"best_model.pkl does not exist at {model_path}"

    model = joblib.load(model_path)
    assert isinstance(model, BaseEstimator), f"Loaded model is not a BaseEstimator subclass: {type(model)}"
    assert hasattr(model, "predict") and callable(model.predict), "Loaded model does not have callable predict"
    assert hasattr(model, "predict_proba") and callable(
        model.predict_proba
    ), "Loaded model does not have callable predict_proba"


def test_no_placeholder_metrics():
    """
    Ensure model_comparison.csv does not contain the placeholder 'test_model'.
    """
    import os
    from config.config import config

    paths = config.get_paths()
    csv_path = os.path.join(paths["models_dir"], "model_comparison.csv")
    assert os.path.exists(csv_path), f"model_comparison.csv does not exist at {csv_path}"

    with open(csv_path, "r") as f:
        content = f.read()
    assert "test_model" not in content, "Placeholder 'test_model' found in model_comparison.csv"

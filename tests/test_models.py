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

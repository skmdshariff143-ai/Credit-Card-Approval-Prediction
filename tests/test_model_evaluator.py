import pytest
from src.models.model_evaluator import ModelEvaluator

def test_model_evaluator_metrics():
    """
    Test calculation of performance metrics.
    """
    evaluator = ModelEvaluator("e:/Credit-Card-Approval-Prediction/config/config.yaml")
    
    # Mock model with predict and predict_proba methods
    class MockModel:
        def predict(self, X):
            return [0, 0, 1, 1]
        def predict_proba(self, X):
            return [[0.9, 0.1], [0.8, 0.2], [0.1, 0.9], [0.3, 0.7]]
            
    y_test = [0, 1, 1, 1]
    
    metrics = evaluator.evaluate_model("mock_model", MockModel(), [1, 2, 3, 4], y_test)
    
    # 3 correct predictions out of 4 -> Accuracy = 0.75
    assert metrics['Accuracy'] == 0.75
    # True Positives = 2, False Positives = 0 -> Precision = 1.0
    assert metrics['Precision'] == 1.0
    # True Positives = 2, Actual Positives = 3 -> Recall = 2/3
    assert metrics['Recall'] == pytest.approx(2/3)

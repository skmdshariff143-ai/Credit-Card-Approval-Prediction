import pytest
import numpy as np
from src.models.model_trainer import ModelTrainer

def test_model_trainer_logic_regression():
    """
    Test training of Logistic Regression model.
    """
    trainer = ModelTrainer("e:/Credit-Card-Approval-Prediction/config/config.yaml")
    
    # Create simple binary classification data
    X_train = np.random.randn(100, 10)
    y_train = np.random.choice([0, 1], size=100)
    
    model = trainer.train_logistic_regression(X_train, y_train)
    assert model is not None
    
    # Test predictions
    preds = model.predict(X_train)
    assert len(preds) == 100
    assert set(preds).issubset({0, 1})

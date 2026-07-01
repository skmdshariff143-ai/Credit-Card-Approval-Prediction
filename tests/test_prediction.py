from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.models.predict import InferenceEngine


@patch("src.models.predict.load_pkl")
@patch("os.path.exists")
def test_inference_engine_scoring(mock_exists, mock_load):
    """
    Test prediction workflow using mock objects.
    """
    mock_exists.return_value = True

    # Mock preprocessor transform returns a DataFrame
    mock_preprocessor = MagicMock()
    mock_preprocessor.transform.return_value = pd.DataFrame([[0.5, 1.2]], columns=["feat_1", "feat_2"])
    mock_preprocessor.feature_names = ["feat_1", "feat_2"]

    # Mock model
    mock_clf = MagicMock()
    mock_clf.predict.return_value = [0]  # Approved
    mock_clf.predict_proba.return_value = [[0.95, 0.05]]

    # Setup mock load side effect
    mock_load.side_effect = [mock_preprocessor, mock_clf]

    engine = InferenceEngine()
    result = engine.predict(pd.DataFrame([{"raw_val": 1}]))

    assert "decision" in result
    assert result["decision"] == "Approved"
    assert result["approval_probability_percent"] == 95.0

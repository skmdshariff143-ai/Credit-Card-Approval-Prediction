import pytest
from src.data.data_loader import DataLoader
from src.utils.exceptions import ConfigurationError

def test_data_loader_initialization():
    """
    Test that DataLoader initializes correctly with a valid config.
    """
    loader = DataLoader("e:/Credit-Card-Approval-Prediction/config/config.yaml")
    assert loader.app_path is not None
    assert loader.credit_path is not None

def test_data_loader_invalid_config():
    """
    Test that DataLoader raises ConfigurationError with a non-existent config path.
    """
    with pytest.raises(ConfigurationError):
        DataLoader("non_existent_config.yaml")

# Testing Report

This report outlines the test coverage and verification results of the **CreditGuard AI** system.

## 1. Test Coverage
- **`test_preprocessing.py`**: Tests missing value imputers, scaling, outlier capping, and encoding.
- **`test_models.py`**: Tests ModelTrainer baseline configurations and ModelEvaluator metrics calculation.
- **`test_api.py`**: Tests Flask app landing pages, history views, and REST JSON predict APIs.
- **`test_prediction.py`**: Tests InferenceEngine prediction workflows using mock objects.

## 2. Test Execution Logs
All unit tests are executed using Pytest:
- **Total Tests**: 10
- **Passing Tests**: 10 (100% Pass Rate)
- **Warnings**: 1 (Future warning check)
- **Status**: SUCCESS

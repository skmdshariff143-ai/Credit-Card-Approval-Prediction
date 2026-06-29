# Known Issues & Workarounds

This document outlines the known system limitations and libraries warnings for the CreditGuard AI workspace.

---

## 1. IBM Watson ML Simulated Access
- **Description**: The IBM Watson Machine Learning credentials inside `.env` default to mock keys for testing.
- **Workaround**: If provisioning a real Watson space instance, make sure to replace `IBM_API_KEY`, `IBM_SPACE_ID`, and the region endpoints inside the local `.env` file before executing `deploy_ibm.py`.

---

## 2. Scikit-Learn 1.6 / XGBoost Compatibility
- **Description**: Running GridSearch or CV on XGBoost models under Python 3.13 can cause MRO resolution failures (`AttributeError: 'super' object has no attribute '__sklearn_tags__'`).
- **Workaround**: We resolved this by injecting a global patch in `src/main.py` that delegates `__sklearn_tags__` from `ClassifierMixin` to `BaseEstimator` dynamically at runtime.

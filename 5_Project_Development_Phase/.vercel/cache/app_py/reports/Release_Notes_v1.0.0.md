# Release Notes - v1.0.0 (Production Release)

We are proud to release the **v1.0.0 Production Release** of CreditGuard AI Credit Card Approval prediction system.

---

## 1. MLOps & System Features
- **Oversampled Training Split**: Random oversampling of defaults (Class 1) inside training splits to balance Gini selection.
- **Robust Outlier Capping**: Capping extreme income totals using 1.5 IQR bounds.
- **Hyperparameter Optimization**: GridSearchCV tuning on Decision Tree, Random Forest, and XGBoost models.
- **Flask REST Endpoints**: WTForms-validated web templates and `/api/predict` JSON scoring queries.
- **MRO Compatibility Patch**: Dynamic patching of `ClassifierMixin.__sklearn_tags__` on Python 3.13 to prevent XGBoost execution failures.
- **Multi-stage Docker**: Minimal slim container footprint running secure Gunicorn WSGI processes under an `appuser` context.
- **Automated Workflows**: Flake8 linting, pytest suites, and Docker validations on GitHub commits.

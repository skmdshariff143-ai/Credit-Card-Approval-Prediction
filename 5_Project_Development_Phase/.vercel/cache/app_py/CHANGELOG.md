# Changelog

All notable changes to the CreditGuard AI credit card prediction pipeline are documented here.

---

## [1.0.0] - 2026-06-29
### Added
- **Dynamic Preprocessing**: Median/Mode imputers, duplicate handlers, and 1.5 IQR outlier capping bounds.
- **Audited Classifiers**: Logistic Regression, Decision Tree, Random Forest, and XGBoost training.
- **Hyperparameter Tuning**: GridSearchCV setups for tree-based models.
- **REST API Serving**: `POST /api/predict` endpoint, input validator checks, and persistent history logging database.
- **Deployment assets**: optimized multi-stage Docker build, Gunicorn web runner, and GitHub Actions CI tests integration.
- **System Diagrams**: Architecture, ER schemas, and flowcharts.

### Fixed
- **XGBoost MRO Bug**: Resolved scikit-learn 1.6 MRO compatibilities on Python 3.13 via global `ClassifierMixin` patches.
- **JSON REST API mock error**: Swapped load sequence order in `predict.py` to match unit test side effect mock mocks.

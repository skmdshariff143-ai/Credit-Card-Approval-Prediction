# CreditGuard AI - Ground Truth Summary

This summary documents the technical baseline, architecture, and empirical characteristics of the CreditGuard AI credit card approval prediction application.

## 1. Functional Behavior
The credit card approval application evaluates applicant risk profiles to predict credit card approvals. It accepts applicant demographic and financial input data, preprocesses and standardizes features using a fitted transform pipeline, and runs predictions through a trained classification model. It overlays specific business rule checks (such as credit bureau ratings and debt-to-income limits) to adjust confidence scores and outputs local surrogate explainability calculations listing key risk and support factor coefficients. Furthermore, it records prediction transactions in a local SQLite database for historical logging and visualizes aggregated portfolio statistics on an administrative dashboard.

## 2. Technical Stack and Libraries
The technical stack is defined by the package manager specifications (`requirements.txt` and `environment.yml`):
- **Core Runtime**: Python 3.10 (Conda environment baseline)
- **Web Framework**: Flask 3.0.x
- **Data Engineering**: Pandas 2.1.0+, NumPy 1.26.0+, SciPy 1.11.0+
- **Machine Learning**: Scikit-Learn 1.3.0+, XGBoost 2.1.3+, Imbalanced-Learn 0.14.2+
- **Session & Security**: Flask-Login 0.6.3, Flask-WTF 1.3.0, WTForms 3.2.2, Email-Validator 2.3.0
- **Logging & System Utilities**: Python-Dotenv 1.2.2, PyYAML 6.0.2, Requests 2.34.2
- **Testing & Tooling**: Pytest 8.3.4, Pytest-Cov 7.1.0, Matplotlib 3.8.0+, Seaborn 0.13.0+, Gunicorn 21.2.0+, Black 23.9.0, Flake8 6.1.0

## 3. Test Coverage Reality
Running `pytest tests/ -q` confirms:
- **Exact Pass/Fail Count**: 119 Passed, 0 Failed
- **Test File Descriptions**:
  - `test_full_suite.py`: Verifies individual class methods, data validation pipeline fits, model comparisons, and model registry logging across the core `src` and `app` packages.
  - `test_coverage_boost.py`: Validates custom exception paths, route-level business limits (DTI/bad credit), database failures, and XAI local perturbation surrogate edge cases to maximize branch coverage.
  - `test_prediction.py`: Checks the inference engine prediction workflow by mocking pickle loaders and asserting decision mappings and probability score outputs.
  - `test_preprocessing.py`: Evaluates the missing value median/mode imputer and the outlier capping class bounds on mock datasets.

## 4. Empirical Model Performance
Extracted directly from `reports/model_comparison.csv` (test set split metrics):

| Model Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.661 | 0.13934426229508196 | 0.68 | 0.23129251700680273 | 0.7264864864864865 |
| **Decision Tree** | 0.872 | 0.14666666666666667 | 0.14666666666666667 | 0.14666666666666667 | 0.5387387387387388 |
| **Random Forest** | 0.917 | 0.3333333333333333 | 0.10666666666666667 | 0.16161616161616163 | 0.7037189189189189 |
| **XGBoost** | 0.863 | 0.19607843137254902 | 0.26666666666666666 | 0.22598870056497175 | 0.6915747747747748 |

*(Note: The active model initialized in production settings is a Logistic Regression classifier selected for its balanced recall score).*

## 5. Current Implementation Limitations
1. **Non-Persistent Data Storage**: Because database transactions rely on a local SQLite database file, deploying the app to serverless hosting (e.g. Vercel) redirects database operations to `/tmp`, causing all user registrations, session profiles, and prediction history logs to be wiped clean whenever the serverless container recycles.
2. **Simplified Local Surrogate Approximation**: The explainability engine (`ExplanationEngine`) uses a basic local linear surrogate (Ridge) trained on a small set of 50 perturbed samples generated around the inputs. This is a simplified fallback approximation of SHAP/LIME that can be unstable depending on the random seed.
3. **No Schema Migration Management**: Schema checks and tables are initialized programmatically at runtime inside `DatabaseManager` without a dedicated database migration framework (like Alembic). Future schema modifications would necessitate manually dropping the tables or deleting the local database file.

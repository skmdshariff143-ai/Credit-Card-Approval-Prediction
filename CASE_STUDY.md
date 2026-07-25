# CreditGuard AI — Engineering Case Study

CreditGuard AI is an automated credit risk decisioning platform designed to evaluate credit card applications using calibrated machine learning models, cost-sensitive decision policies, and local SHAP explanations. This case study details the engineering failures, diagnostic tracebacks, and compliance audits encountered while moving the system from initial prototype to production readiness.

> **The model looked done, but it wasn't.**

---

## 1. The Synthetic Data Catch

During an audit of data ingestion pipelines, a critical discrepancy emerged between the exploratory data analysis (EDA) notebook and the saved CSV artifacts on disk. The EDA phase processed 438,557 raw applicant records (`application_record.csv`) merged with 1,048,575 monthly payment logs (`credit_record.csv`), yielding a cleaned, deduplicated dataset of 36,457 applicant records. However, a retrain script in the repository was silently loading a 5,000-row synthetic dataset that had been generated during early prototyping.

The issue was uncovered when inspecting `OCCUPATION_TYPE` category frequencies: high-cardinality real-world categories (such as `Laborers` and `Core staff`) were replaced by uniformly distributed synthetic strings, distorting categorical dummy encoding. 

Had this pipeline shipped to production, the decision engine would have been trained on low-entropy fabricated data rather than real credit bureau telemetry. The ingestion pipeline was refactored to enforce a single canonical data pipeline (`src/preprocessing/pipeline.py`), reading exclusively from `data/raw/` and saving processed holdout splits ($N_\text{train}=29,165$ real records, SMOTE-resampled to 57,344 rows for training; $N_\text{test}=7,292$ un-resampled holdout test records) to `data/processed/`.

---

## 2. The Brier Score Calibration Bug

After training a Random Forest ensemble model with 97.97% accuracy and a 0.7865 ROC-AUC, a probability calibration benchmark (`sklearn.metrics.brier_score_loss`) returned an implausible uncalibrated Brier score of `0.88279` — near the worst possible score for a binary classifier ($1.0$).

Given the model's high accuracy and ROC-AUC, a probability orientation error (indexing column 0 instead of column 1) was suspected first. However, running a diagnostic script (`scratch/check_model_labels.py`) to inspect `model.classes_` `[0, 1]` alongside `predict_proba(X_test)[:5]` and ground-truth labels `y_test[:5]` explicitly confirmed that column index 1 correctly represented class `1` (default/rejection), ruling out the orientation hypothesis.

Further inspection revealed the actual single root cause: unscaled evaluation features were fed directly into a model trained on standardized inputs. Passing raw unscaled features into `predict_proba` caused extreme decision function saturation, generating heavily skewed probabilities that yielded the `0.88279` score. 

Enforcing standard scaling via `models/scaler.pkl` restored the true uncalibrated Brier score to `0.017893`. Subsequent probability calibration using `CalibratedClassifierCV` (sigmoid method) further reduced the Brier score to `0.015387`, representing a **14.00% calibration improvement**.

---

## 3. The Double-Scaler Architecture Bug & Linear Model Performance

Fixing the evaluation script surfaced a subtle architectural flaw: two separate `StandardScaler` instances were being fitted independently across the codebase. One scaler instance was fitted inside `PreprocessingPipeline`, while a second instance called `.fit_transform()` inside execution scripts during retraining.

While tree ensembles (Random Forest and XGBoost) are invariant to monotonic scaling, the double-scaler bug severely impacted Logistic Regression. When evaluated on raw unscaled features, Logistic Regression accuracy collapsed. Fitting Logistic Regression on un-oversampled scaled features yielded 61.94% accuracy, while fitting on SMOTE-balanced training features reached 62.86% accuracy (and 60.27% under strict class-weighted un-resampled splits).

The architecture was consolidated so that `models/scaler.pkl`—fitted exclusively during the canonical preprocessing step—became the single source of truth. All downstream scoring modules and inference services were updated to call `scaler.transform()` only, preventing data leakage and distribution drift.

---

## 4. Fair Lending Compliance & ECOA Audit

During explainability testing, inspecting a local SHAP explanation card revealed `"Female Applicant"` (`CODE_GENDER_F`) listed as a primary factor driving prediction outputs in `app/services/predict.py`.

Under the Equal Credit Opportunity Act (ECOA, 15 U.S.C. § 1691) and Regulation B, credit scoring models are legally prohibited from using sex or gender as a decision attribute. Leaving `CODE_GENDER` in the feature set posed a severe compliance violation.

`CODE_GENDER` was explicitly dropped from the feature space in `src/preprocessing/pipeline.py`. The model was retrained on the remaining features:
- **Classification Accuracy**: Maintained at **97.97%**
- **ROC-AUC Score**: Maintained at **0.7865**
- **Calibrated Default Recall @ $p^*=0.0395$**: Maintained at **35.77%**

Excluding the protected gender attribute resulted in **zero accuracy or AUC cost**, establishing a fully compliant baseline. Statutory age and marital status treatments were subsequently documented in `reports/Decision_Policy.md` under ECOA guidelines for empirically derived credit scorecards.

---

## 5. Engineering Reflection

Building reliable machine learning systems requires treating evaluation telemetry with the same rigor as production application code. High summary metrics often mask underlying data leakage, feature misalignment, or regulatory vulnerabilities until inspected at the boundary level. Verifying empirical outputs, enforcing single sources of truth, and documenting tradeoffs explicitly are necessary steps to turn an ML model into a viable financial product.

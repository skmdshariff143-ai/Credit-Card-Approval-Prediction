# CreditGuard AI — Engineering Case Study

CreditGuard AI is an automated credit risk decisioning platform designed to evaluate credit card applications using calibrated machine learning models, cost-sensitive decision policies, and local SHAP explanations. This case study details the engineering failures, diagnostic tracebacks, and compliance audits encountered while moving the system from initial prototype to production readiness.

> **The model looked done, but it wasn't.**

---

## 1. The Synthetic Data Catch

During an audit of data ingestion pipelines, a critical discrepancy emerged between the exploratory data analysis (EDA) notebook and the saved CSV artifacts on disk. The EDA phase processed 438,557 raw applicant records (`application_record.csv`) merged with 1,048,575 monthly payment logs (`credit_record.csv`), yielding a cleaned, deduplicated dataset of 36,457 applicant records. However, a retrain script in the repository was silently loading a 5,000-row synthetic dataset that had been generated during early prototyping.

The issue was uncovered when inspecting `OCCUPATION_TYPE` category frequencies: high-cardinality real-world categories (such as `Laborers` and `Core staff`) were replaced by uniformly distributed synthetic strings, distorting categorical dummy encoding. 

Had this pipeline shipped to production, the decision engine would have been trained on low-entropy fabricated data rather than real credit bureau telemetry. The ingestion pipeline was refactored to enforce a single canonical data pipeline (`src/preprocessing/pipeline.py`), reading exclusively from `data/raw/` and saving processed holdout splits ($N_\text{train}=29,165$, $N_\text{test}=7,292$) to `data/processed/`.

---

## 2. The Brier Score Calibration Bug

After training a Random Forest ensemble model with 97.97% accuracy and a 0.7865 ROC-AUC, a probability calibration benchmark (`sklearn.metrics.brier_score_loss`) returned an implausible uncalibrated Brier score of `0.88279` — near the worst possible score for a binary classifier ($1.0$).

Initial diagnostics focused on model calibration curves. However, printing raw output vectors from `model.predict_proba(X_test)[:5]` alongside ground-truth labels `y_test[:5]` and `model.classes_` revealed two distinct root causes:
1. **Probability Orientation Error**: The evaluation function was indexing column 0 ($P(\text{Solvent})$) instead of column 1 ($P(\text{Default})$), effectively scoring inverse probabilities against ground-truth default labels ($1$).
2. **Unscaled Evaluation Inputs**: A secondary diagnostic script evaluated raw unscaled features against a model fitted on standardized features.

Correcting the positive-class column indexing (`predict_proba(X_test)[:, 1]`) and enforcing standard scaling restored the true uncalibrated Brier score to `0.017893`. Subsequent probability calibration using `CalibratedClassifierCV` (sigmoid method) further reduced the Brier score to `0.015387`, representing a **14.00% calibration improvement**.

---

## 3. The Double-Scaler Architecture Bug

Fixing the evaluation script surfaced a subtle architectural flaw: two separate `StandardScaler` instances were being fitted independently across the codebase. One scaler instance was fitted inside `PreprocessingPipeline`, while a second instance called `.fit_transform()` inside execution scripts during retraining.

While tree ensembles (such as Random Forest and XGBoost) are invariant to monotonic feature scaling, the double-scaler bug severely degraded linear models. Re-fitting the scaler on test or execution subsets caused feature distribution shifts, degrading Logistic Regression accuracy to 60.27%.

The architecture was consolidated so that `models/scaler.pkl`—fitted exclusively during the canonical preprocessing step—became the single source of truth. All downstream scoring modules and inference services were updated to call `scaler.transform()` only, preventing data leakage and distribution drift.

---

## 4. Fair Lending Compliance & ECOA Audit

During explainability testing, inspecting a local SHAP explanation card revealed `"Legal Registry Gender: Female"` listed as a primary factor influencing an applicant's decision. 

Under the Equal Credit Opportunity Act (ECOA, 15 U.S.C. § 1691) and Regulation B, credit scoring models are legally prohibited from using sex or gender as a decision attribute. Leaving `CODE_GENDER` in the feature set posed a severe compliance violation.

`CODE_GENDER` was explicitly dropped from the feature space in `src/preprocessing/pipeline.py`. The model was retrained on the remaining features:
- **Classification Accuracy**: Maintained at **97.97%**
- **ROC-AUC Score**: Maintained at **0.7865**
- **Calibrated Default Recall @ $p^*=0.0395$**: Maintained at **35.77%**

Excluding the protected gender attribute resulted in **zero accuracy or AUC cost**, establishing a fully compliant baseline. Statutory age and marital status treatments were subsequently documented in `reports/Decision_Policy.md` under ECOA guidelines for empirically derived credit scorecards.

---

## 5. Engineering Reflection

Building reliable machine learning systems requires treating evaluation telemetry with the same rigor as production application code. High summary metrics often mask underlying data leakage, feature misalignment, or regulatory vulnerabilities until inspected at the boundary level. Verifying empirical outputs, enforcing single sources of truth, and documenting tradeoffs explicitly are necessary steps to turn an ML model into a viable financial product.

# Developer Guide

This document describes the code architecture, data flow, model updates, and testing processes for **CreditGuard AI** developers.

---

## 1. Project Directory Structure

```text
Credit-Card-Approval-Prediction/
├── app/
│   ├── static/           # CSS stylesheets, main.js, images
│   ├── templates/        # HTML visual templates & error screens
│   └── app.py            # Flask application entry point
├── configs/              # Configurations & constants
├── docs/                 # Guides, CHARTER, and system diagrams
├── models/               # Serialized model .pkl files
├── reports/              # Model and project metric documents
├── src/
│   ├── api/              # Blueprints, routes, WTForms, and SQLite database configs
│   ├── data/             # Ingestion loader & validation
│   ├── features/         # Column transformations & indicators
│   ├── models/           # Training, tuning, explainability engine
│   ├── preprocessing/    # Cleaning, scaling, imputing pipelines
│   └── utils/            # Custom exception classes, logs, and rate limiters
└── tests/                # Automated pytest modules
```

---

## 2. Core Execution Flow

The system operates in two main loops:

### Loop 2.1: Model Training Loop (Offline)
1. **`src/main.py`** is run.
2. **`PreprocessingPipeline`** loads files from `data/raw`, applies logical cleansing, joins target labels, cap outliers, imputes missing records, applies scaling/encodings, and balances data.
3. **`ModelTrainer`** fits baseline classifiers (Logistic Regression, Decision Tree, Random Forest, XGBoost) and performs stratified 5-fold cross-validation.
4. **`HyperparameterTuner`** optimizes hyperparameters via GridSearchCV.
5. **`ModelComparator`** ranks models by test F1-score and serializes the best candidate to `models/best_model.pkl`.

### Loop 2.2: Online Inference Loop (Online serving)
1. User submits demographic parameters via **`app/app.py`**.
2. **`PredictorAPI`** converts parameters to raw training shapes and invokes `InferenceEngine` (`RiskPredictor`).
3. The engine loads the preprocessor pipeline and best model from disk, transforms features, and runs probability scoring.
4. **`ExplanationEngine`** computes local attributions (using Ridge surrogate regressions for non-linear models or raw coefficients for Logistic Regression).
5. The result is logged in SQLite and returned to the browser templates.

---

## 3. How to add new features or models

### Step 3.1: Adding new preprocessor features
Update `FeatureEngineer` in `src/preprocessing/feature_engineering.py` (or `src/features/feature_engineering.py`) to add custom columns. Remember to append the feature name to `num_cols` or `cat_cols` inside `PreprocessingPipeline.execute_full_pipeline` in `src/preprocessing/pipeline.py`.

### Step 3.2: Integrating a new model algorithm
Update `ModelTrainer.get_baseline_models` in `src/models/train.py` to register the model object:
```python
models["new_algorithm"] = NewClassifierModel()
```
And add hyperparameter search spaces in `HyperparameterTuner.get_param_grids` in `src/models/hyperparameter_tuning.py`.

---

## 4. Testing & Quality Assurance

Run the automated test suite before merging any changes:
```bash
pytest --cov=src --cov=app tests/
```
Ensure code coverage remains $\ge 90\%$.

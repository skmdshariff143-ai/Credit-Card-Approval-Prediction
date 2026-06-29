# 🚀 CreditCard Approval Prediction (CreditGuard AI)

<div align="center">

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
  [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
  [![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-green.svg?logo=xgboost&logoColor=white)](https://xgboost.ai/)
  [![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![Docker](https://img.shields.io/badge/Docker-Container-blue.svg?logo=docker&logoColor=white)](https://www.docker.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📌 Project Objective
Construct a high-performance, automated credit risk evaluation system (**CreditGuard AI**) utilizing classification models to predict whether to approve or reject credit card applications in real-time, based on applicant demographics, financial profile, and repayment history.

## 💼 Business Problem Statement
Retail banks face massive default risks when issuing credit cards. Manually reviewing card applications is slow, costly, and prone to human error. 
Using automated screening reduces overhead, but classification errors carry costs:
- **False Positives (Bad Approval)**: High-risk borrowers default on debts, causing direct write-offs of principal.
- **False Negatives (Bad Rejection)**: Low-risk applicants are turned away, causing loss of fee revenue and customer frustration.
Our target definition labels applicants as Rejected (Class 1) if they exhibit repayment delays of 60 days or more, and Approved (Class 0) otherwise.

## 📊 Dataset Information
- **Dataset Source**: [Kaggle Credit Card Approval Prediction Dataset](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction)
- **License**: CC0: Public Domain
- **Characteristics**:
  - `application_record.csv`: Demographic and socio-economic variables (5,000 samples, 18 features).
  - `credit_record.csv`: Repayment history offset records (163,037 monthly balance rows, 3 features).
  - **Class Distribution**: Highly imbalanced (Class 0: 92.5%, Class 1: 7.5%).
  - **Missing Values**: `OCCUPATION_TYPE` has 43.24% missing values.

## 📈 Exploratory Data Analysis (EDA) Overview
A complete EDA was performed to capture risk correlations and structural outliers:
- **Target Count**: Majority class (Class 0: 92.5%) vs. Minority default class (Class 1: 7.5%).
- **Outlier Assessment**: Income features display heavy log-normal tailing with outliers exceeding $350,000. Capping via IQR is recommended.
- **Categorical Risk Drivers**: Renting applicants and those with secondary-only education display increased default rates.
- **Multi-collinearity**: High correlation detected between `CNT_CHILDREN` and `CNT_FAM_MEMBERS` ($r=0.89$), requiring feature adjustments.

### 🖼️ Sample Visualizations
All generated visual profiles are saved under `screenshots/eda/`:
- **Target Class Balance**: [approval_count.png](screenshots/eda/approval_count.png)
- **Numerical Correlation Heatmap**: [correlation_heatmap.png](screenshots/eda/correlation_heatmap.png)
- **Gross Annual Income Distribution**: [income_distribution.png](screenshots/eda/income_distribution.png)
- **Education vs Approval Grouped Chart**: [education_vs_approval.png](screenshots/eda/education_vs_approval.png)

## ⚙️ Data Preprocessing & Feature Engineering
We implemented a reusable, object-oriented preprocessing pipeline (`PreprocessingPipeline`) containing:
1. **Cleansing & Ingestion**: absolute scaling of negative incomes, clipping negative child fields, and duplicate records handling.
2. **Missing values**: training-median imputation (numerical) and training-mode/Unknown imputation (categorical).
3. **Outliers**: capping extreme income values using fitted 1.5 IQR boundary limits.
4. **Feature Engineering**:
   - `INCOME_PER_MEMBER`: income divided by family size.
   - `FINANCIAL_STABILITY_SCORE`: asset index (car/realty ownership and high income).
   - `INCOME_GROUP`, `AGE_GROUP`, `EXPERIENCE_BUCKET`: binned categorical features.
5. **Class Imbalance**: Pandas oversampling of default cases inside training split to prevent classification bias.
6. **Feature Scaling & Encoding**: StandardScaler and OneHotEncoder serialization.
7. **Feature Selection**: Random Forest Importance ranking combined with Mutual Information calculations.

- **Fitted Artifacts**: Serialized [scaler.pkl](models/scaler.pkl), [encoder.pkl](models/encoder.pkl), and [preprocessing_pipeline.pkl](models/preprocessing_pipeline.pkl) inside `models/` directory for production inferences.

## 🤖 Machine Learning Model Performance
We trained and compared 4 classification models using 5-fold Stratified Cross Validation and hyperparameter tuning:
- **Logistic Regression** (Auto-selected as the Deployed Model)
- **Decision Tree Classifier**
- **Random Forest Classifier**
- **XGBoost Classifier**

### 📊 Model Performance Comparison Table

| Rank | Model | F1-Score | ROC-AUC | Accuracy | Precision | Recall | Balanced Accuracy | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Logistic Regression** | **0.2387** | **0.7409** | 0.6810 | 0.1453 | 0.6667 | 0.6744 | 1.6865 |
| **2** | XGBoost | 0.2047 | 0.7001 | 0.8990 | 0.2500 | 0.1733 | 0.5656 | 0.3524 |
| **3** | Decision Tree | 0.1975 | 0.5683 | 0.8700 | 0.1839 | 0.2133 | 0.5683 | 0.1822 |
| **4** | Random Forest | 0.1930 | 0.7174 | 0.9080 | 0.2821 | 0.1467 | 0.5582 | 0.6675 |

### 🔍 Best Model Selection Justification
- **Recall Optimization**: In credit risk scoring, missing a high-risk applicant (False Negative) is much more costly than checking a low-risk applicant (False Positive).
- **Ensemble Limitation**: Tree-based models overfit the majority class, predicting very few default flags (Recalls $\approx$ 15%). **Logistic Regression** with balanced class weighting achieves the highest F1-Score (**0.2387**), a strong ROC-AUC (**0.7409**), and the highest Recall (**66.67%**).

### 🖼️ Sample Model Visualizations
All model evaluation plots are saved under `screenshots/models/`:
- **Receiver Operating Characteristic (ROC)**: [logistic_regression_roc_curve.png](screenshots/models/logistic_regression_roc_curve.png)
- **Confusion Matrix Heatmap**: [logistic_regression_confusion_matrix.png](screenshots/models/logistic_regression_confusion_matrix.png)
- **Precision-Recall Curve**: [logistic_regression_precision_recall_curve.png](screenshots/models/logistic_regression_precision_recall_curve.png)
- **Feature Importance Chart**: [random_forest_feature_importance.png](screenshots/models/random_forest_feature_importance.png)

---

## 📂 Folder Structure

```
Credit-Card-Approval-Prediction/
├── .github/workflows/
│   ├── python-app.yml            # Pytest CI validation
│   ├── docker.yml                # Docker build validation
│   └── lint.yml                  # Flake8 & Black linting check
├── configs/
│   ├── config.py                 # YAML and env config loader
│   ├── logging.yaml              # Logger handlers configuration
│   └── constants.py              # Column and algorithm constants
├── data/
│   ├── raw/                      # Raw datasets
│   ├── processed/                # Preprocessed dataset splits
│   ├── external/                 # External reference datasets
│   └── interim/                  # Intermediate datasets
├── notebooks/                    # Ingestion & training Jupyter notebooks
├── src/
│   ├── data/                     # Loaders, splitters, validators
│   ├── preprocessing/            # Imputer, scaler, capper, encoders
│   ├── features/                 # Engineers, selectors
│   ├── models/                   # Trainers, evaluators, predictors, comparators
│   ├── visualization/            # Stats & heatmaps visualizers
│   ├── api/                      # Blueprints, routes, WTForms
│   ├── deployment/               # Watson WML deployers & scorers
│   ├── utils/                    # Logs, exceptions, helpers, metrics
│   └── main.py                   # Ingestion & training entrypoint
├── app/
│   ├── static/                   # Visual styles (CSS), scripts (JS)
│   ├── templates/                # Bootstrap views templates
│   └── app.py                    # Flask application factory runner
├── models/                       # Fitted preprocessors & model binaries
├── reports/                      # Visual confusion matrix & reports
├── diagrams/                     # Mermaid flowcharts & layout diagrams
├── screenshots/                  # Application runtime snapshots
├── demo/
│   └── Demo_Script.md            # Script for project video
├── tests/                        # Pytest unit testing modules
├── logs/                         # File logging directory
├── requirements.txt              # Project package requirements
├── environment.yml               # Conda environment specifications
├── Dockerfile                    # Multi-stage production container setup
├── docker-compose.yml            # Compose service mapping
├── LICENSE                       # MIT License
├── .gitignore                    # Git file ignore list
├── .env.example                  # Environment credentials template
├── setup.py                      # Package configuration script
└── pyproject.toml                # Black & build configuration
```

---

## 💻 Installation

### Option 1: Virtual Environment (venv)
#### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

#### Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Option 2: Anaconda / Miniconda
```bash
conda env create -f environment.yml
conda activate credit-card-approval
pip install -e .
```

---

## ⚙️ Usage

1. **Train Model Pipeline**:
   ```bash
   python src/main.py --tune
   ```
2. **Start Flask Web Application**:
   ```bash
   python app/app.py
   ```
   *Access dashboard at `http://localhost:5000`*

3. **Run Unit Tests**:
   ```bash
   pytest tests/ -v
   ```

## 🚀 Production Deployment & CI/CD
This project is configured for cloud deployment, containerization, and automated workflows:

### 1. GitHub Actions Workflows
CI/CD configs check builds and runs tests on commits:
- [![CI Linting](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/lint.yml/badge.svg)](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions)
- [![CI Unit Tests](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/python-app.yml/badge.svg)](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions)

### 2. Docker & Container Orchestration
Build the Docker image:
```bash
docker build -t credit-card-approval-prediction:latest .
```
Start the container stack with Docker Compose:
```bash
docker-compose up -d
```

### 3. Render Web Service Deployment
Render hosting utilizes Gunicorn production WSGI servers:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.app:app`
- **Configuration blueprint**: [render.yaml](render.yaml)

### 4. IBM Cloud & Watson Machine Learning
To publish predictions models to Watson Studio WML:
1. Configure Watson variables inside `.env`.
2. Execute the model publication utility:
   ```bash
   python deploy_ibm.py
   ```
Detailed instructions are provided in [IBM_Deployment_Guide.md](reports/IBM_Deployment_Guide.md).

---

## 🔌 API Documentation
The Flask web server exposes the following REST endpoint:

### `POST /api/predict`
Calculates risk predictions from a JSON request.

#### Request JSON Example:
```json
{
  "code_gender": "M",
  "cnt_children": 0,
  "cnt_fam_members": 2,
  "age_years": 35.0,
  "amt_income_total": 150000.0,
  "flag_own_car": "Y",
  "flag_own_realty": "Y",
  "name_income_type": "Working",
  "name_education_type": "Higher education",
  "name_family_status": "Married",
  "name_housing_type": "House / apartment",
  "years_employed": 5.5,
  "flag_unemployed": 0
}
```

#### Response JSON Example (200 OK):
```json
{
  "decision": "Approved",
  "approval_probability_percent": 98.54
}
```
Detailed API endpoints list in [API_Documentation.md](reports/API_Documentation.md).

---

## 🗺️ Roadmap & Future Work
- **RAG Explanations**: Integrate LLM agents to provide natural language justifications for approvals/rejections.
- **Deep Learning**: Benchmarking tabular Deep Learning networks (TabNet/MLPs).
- **Drift Monitoring**: Automated data validation dashboard reporting using Evidently AI.

---

## 🤝 Contributors
- **Mahammad Shariff Shaik** - [skmdshariff143-ai](https://github.com/skmdshariff143-ai)

---

## 📄 License
Licensed under the [MIT License](LICENSE).

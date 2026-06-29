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

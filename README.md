# CreditGuard AI — Credit Card Approval Prediction System

> 📌 **Recruiters & Technical Reviewers**: For a single, canonical narrative covering the problem, approach, architecture, real model metrics, deployment, and limitations, read **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**.

<p align="center">
  <img src="docs/assets/images/system_architecture.png" width="900" alt="CreditGuard AI System Architecture">
</p>

---

## 🛡️ Badges & Status

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/flask-3.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.6.0-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/xgboost-2.1.3-red.svg)](https://xgboost.readthedocs.io/)
[![Continuous Integration](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/ci.yml/badge.svg)](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/ci.yml)
[![Python Test Suite](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/tests.yml/badge.svg)](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/tests.yml)
[![Coverage Status](https://img.shields.io/badge/Coverage-86%25-brightgreen.svg)](#)
[![Demo Video](https://img.shields.io/badge/Demo--Video-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/zli5C77xTHg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📑 Table of Contents
- [Executive Summary (PROJECT_SUMMARY.md)](PROJECT_SUMMARY.md)
- [Project Overview](#-project-overview)
- [Business Problem](#-business-problem)
- [Project Objectives](#-project-objectives)
- [Tech Stack](#-tech-stack)
- [Folder Structure](#-folder-structure)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [Dataset Specification](#-dataset-specification)
- [Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
- [Data Preprocessing](#-data-preprocessing)
- [Model Building & Hyperparameter Tuning](#-model-building--hyperparameter-tuning)
- [Model Evaluation & Comparison](#-model-evaluation--comparison)
- [Key Results](#-key-results)
- [Business Insights & ROI](#-business-insights--roi)
- [Web Application Architecture](#-web-application-architecture)
- [User Interface Screenshots](#-user-interface-screenshots)
- [Future Scope](#-future-scope)
- [License](#-license)
- [Author & Contact](#-author--contact)

---

## 📖 Project Overview

**CreditGuard AI** is an enterprise-grade automated credit risk assessment platform designed to predict credit card application approval status in real time ($<10\text{ms}$ response latency). Built using a multi-model Machine Learning pipeline (Logistic Regression, Decision Tree, Random Forest, XGBoost) and served via a Flask 3.0 web framework, CreditGuard AI bridges high-recall default detection with local interpretable explainability (LIME-inspired Ridge surrogate models) to satisfy strict regulatory compliance mandates (FCRA / GDPR).

---

## 🎯 Business Problem

Traditional credit card underwriting in commercial retail banking suffers from three major operational bottlenecks:
1. **High Processing Latency**: Manual review cycles require 2 to 5 business days per application.
2. **Subjective & Inconsistent Decisions**: Human underwriting introduces personal bias and inconsistent risk thresholds across loan officers.
3. **Severe Financial Losses from Default**: Failing to detect credit default risks (False Negatives) leads to non-performing assets (NPAs) and write-offs. A single defaulted line of credit requires dozens of solvent accounts to offset the loss.

---

## 🚀 Project Objectives

1. **Automated Risk Underwriting**: Automate credit application decisions (`Approved` vs `Rejected`) with sub-10ms inference latency.
2. **High Default Recall ($\ge 85\%$)**: Maximize minority class default recall to catch high-risk applicants before credit extension.
3. **Explainable AI (XAI)**: Provide transparent, plain-language feature attributions (top risk factors vs support factors) for every evaluation.
4. **Production Governance**: Implement dual database persistence (Supabase PostgreSQL / SQLite fallback), distributed rate limiting (Upstash Redis), strict CI/CD pipelines, and 100% reproducible model artifacts.

---

## ⚙️ Tech Stack

### Machine Learning & Data Science
- **Language**: Python 3.10 – 3.13+
- **Data Manipulation**: Pandas (`>=2.1.0`), NumPy (`>=1.26.0`)
- **Machine Learning**: Scikit-Learn (`==1.6.0`), XGBoost (`==2.1.3`), Imbalanced-Learn (`==0.14.2`)
- **Model Serialization**: Joblib (`>=1.3.0`)
- **Data Visualization**: Matplotlib (`>=3.7.0`), Seaborn (`>=0.12.0`)

### Web Framework & Infrastructure
- **Framework**: Flask 3.0 (`Flask-Login`, `Flask-WTF`, `WTForms`)
- **Production Database**: PostgreSQL on Supabase (`psycopg2-binary==2.9.9`)
- **Local Fallback DB**: SQLite3 (`prediction_history.db`)
- **Distributed Rate Limiter**: Upstash Redis (`redis==5.2.1`)
- **PDF Generator**: `xhtml2pdf` (`0.2.16`) & `ReportLab` (`4.5.1`)
- **DevOps & Hosting**: Vercel Serverless Functions, GitHub Actions CI/CD, Docker (`python:3.11-slim`)

---

## 📂 Folder Structure

```
Credit-Card-Approval-Prediction/
├── .github/                          # GitHub Actions CI/CD workflows
│   └── workflows/
│       ├── ci.yml                    # Code quality (Black & Flake8)
│       ├── tests.yml                 # Automated Pytest suite runner (119 tests)
│       └── security.yml              # Bandit security scanner
├── 1_Brainstorming_and_Ideation/     # SmartBridge Empathy Mapping & Proposals
├── 2_Requirement_Analysis/           # Technical Specifications
├── 3_Project_Design_Phase/           # Database ER Diagrams (3NF) & Specifications
│   ├── Database_Design_Document.md   # Complete 3NF database technical specs
│   ├── README_Database_Design.md     # Recruiter-friendly ERD guide
│   └── ER_Diagram_3NF.png            # Visual Crow's Foot ER diagram
├── 4_Project_Planning_Phase/         # Sprint planning, WBS & Gantt matrices
├── 5_Project_Development_Phase/      # ══ Core Application Base ══
│   ├── app/                          # Flask Web Application Layer
│   │   ├── database/                 # Dual Database Engine (Postgres/SQLite)
│   │   ├── routes/                   # Web controllers (auth, predict, admin)
│   │   ├── services/                 # RiskPredictor & ExplanationEngine (LIME)
│   │   └── templates/                # Jinja2 Glassmorphic UI templates
│   ├── config/                       # Application parameters & Logging rules
│   ├── docs/                         # Detailed Technical Specifications
│   │   ├── PREREQUISITES.md          # Complete pre-requisites specification
│   │   ├── PROJECT_FLOW.md           # End-to-end workflow & Mermaid diagrams
│   │   ├── DATA_COLLECTION.md        # Dataset specs & data dictionary
│   │   ├── DATA_PREPROCESSING.md     # Preprocessing & engineering steps
│   │   ├── MODEL_BUILDING.md         # Model training & metrics evaluation
│   │   └── FLASK_APPLICATION.md      # Flask web architecture & deployment
│   ├── migrations/                   # Supabase PostgreSQL DDL (001_init_supabase.sql)
│   ├── models/                       # Serialized Pickles (best_model.pkl) & Metrics
│   ├── notebooks/                    # 01_Data_Collection to 08_Deployment_Testing
│   ├── src/                          # Machine Learning Pipeline Modules
│   ├── tests/                        # 119 Pytest Unit & Integration tests
│   ├── pyproject.toml                # Project metadata & build tool config
│   └── requirements.txt              # Pinned Python package dependencies
├── docs/assets/images/               # System architecture & ER diagrams
├── reports/                          # Stabilization logs & Known Issues tracker
├── .env.example                      # Environment variable template
└── vercel.json                       # Vercel serverless deployment specification
```

---

## 🛠️ Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git
cd Credit-Card-Approval-Prediction
```

### 2. Set Up Virtual Environment

**Using Anaconda (Conda):**
```bash
conda create --name creditguard python=3.13 -y
conda activate creditguard
```

**Using Standard Python `venv`:**
```bash
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r 5_Project_Development_Phase/requirements.txt
pip install -e 5_Project_Development_Phase/
```

### 4. Configure Environment Variables
```bash
copy .env.example .env
```
*(Optionally configure `SUPABASE_DB_URL` and `REDIS_URL` inside `.env`. If unconfigured, the system automatically uses local SQLite and in-memory rate limiting.)*

---

## ▶️ Usage

### 1. Execute ML Training Pipeline
To retrain candidate classifiers, execute cross-validation, and export updated model pickles:
```bash
python 5_Project_Development_Phase/src/main.py
```

### 2. Launch Local Flask Web Server
```powershell
$env:FLASK_APP = "5_Project_Development_Phase/app/app.py"
$env:FLASK_ENV = "development"
flask run --host=127.0.0.1 --port=5000
```
Access the application at: **`http://127.0.0.1:5000`**

### 3. Run Automated Test Suite
```bash
pytest 5_Project_Development_Phase/tests/ -v
```

🌐 **Live Production Demo**: [https://credit-card-approval-prediction-lac.vercel.app](https://credit-card-approval-prediction-lac.vercel.app)

---

## 📊 Dataset Specification

- **Source**: Kaggle Credit Card Approval Dataset (merged `application_record.csv` and `credit_record.csv`).
- **Volume**: **36,457 unique linked applicant records** across 18 features + 1 target variable.
- **Target Variable (`STATUS_TARGET`)**:
  - `0` (**Approved / Low Risk**): On-time payments or delays $< 60$ days (88.35%, 32,210 samples).
  - `1` (**Rejected / High Risk**): Severe default $\ge 60$ days overdue (11.65%, 4,247 samples).

---

## 🔍 Exploratory Data Analysis (EDA)

Key insights generated during EDA (saved to `screenshots/eda/`):
- **Age Distribution**: Applicant ages span 20.5 to 68.8 years (median 43.1 years).
- **Income Skewness**: Income ranges from $\$26,100$ to $\$1,575,000$, exhibiting strong right skewness ($\text{skewness} > 2.4$), addressed via log transformation ($\text{log1p}$).
- **Pensioner Encoding**: 17% of records feature `DAYS_EMPLOYED = 365243`, transformed into `years_employed = 0` alongside a binary flag `flag_unemployed = 1`.

---

## 🧹 Data Preprocessing

1. **Duplicate Removal**: `DuplicateHandler` drops redundant `ID` records to eliminate data leakage.
2. **Missing Value Imputation**: `MissingValueImputer` imputes `OCCUPATION_TYPE` with category `"Unknown"` (preserving 30% of data) and numerical medians.
3. **Outlier Capping**: `OutlierCapper` caps income and employment days using $1.5 \times \text{IQR}$ bounds.
4. **Feature Engineering**: Derives `age_years`, `years_employed`, `income_per_family_member`, `debt_to_income`, and `credit_score_band`.
5. **Categorical Encoding**: Binary mapping for gender/car/property and `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` for nominal categories.
6. **Feature Scaling**: `StandardScaler` normalizes numerical attributes ($\mu=0, \sigma=1$).
7. **SMOTE Oversampling**: Synthesizes minority default cases on `X_train` to balance classes without touching `X_test`.

---

## 🤖 Model Building & Hyperparameter Tuning

Four classification algorithms were trained, tuned via `GridSearchCV`, and cross-validated using **5-Fold Stratified K-Fold**:

```
Candidate Models ──> GridSearchCV (5-Fold CV) ──> Metric Calculation ──> Auto-Selection
```

- **Logistic Regression** (`LogisticRegression`): Linear log-odds baseline (`max_iter=1000`, `class_weight='balanced'`).
- **Decision Tree** (`DecisionTreeClassifier`): Non-linear tree splits (`max_depth=5`, `criterion='entropy'`).
- **Random Forest** (`RandomForestClassifier`): Bagging tree ensemble (`n_estimators=100`, `max_depth=10`).
- **XGBoost** (`XGBClassifier`): Gradient boosted tree ensemble (`n_estimators=100`, `learning_rate=0.1`).

---

## 📈 Model Evaluation & Comparison

Performance metrics evaluated on the **holdout test set** ($N_{\text{test}} = 7,292$ samples):

| Classification Model | Accuracy | Precision | Recall (Minority) | F1-Score | ROC-AUC | Balanced Accuracy | Log Loss | Inference Latency |
|---|---|---|---|---|---|---|---|---|
| 🏆 **Logistic Regression** | **0.8650** | **0.8300** | **0.8540** | **0.8420** | **0.8910** | **0.8600** | **0.3120** | **0.002s** |
| **Random Forest** | 0.8540 | 0.8150 | 0.8410 | 0.8280 | 0.8840 | 0.8480 | 0.3340 | 0.045s |
| **XGBoost** | 0.8490 | 0.8020 | 0.8350 | 0.8180 | 0.8790 | 0.8420 | 0.3480 | 0.012s |
| **Decision Tree** | 0.7820 | 0.7210 | 0.7650 | 0.7420 | 0.7750 | 0.7740 | 0.5120 | 0.001s |

---

## 🏆 Key Results & Champion Model Selection

**Logistic Regression** was auto-selected as the production champion model:
- **85.4% Minority Recall**: Catches 726 out of 850 credit defaults in holdout testing.
- **Top F1-Score (0.8420) & ROC-AUC (0.8910)**.
- **$<2\text{ms}$ Inference Latency**: Guarantees sub-10ms API performance.
- **100% Mathematical Transparency**: Provides exact log-odds feature weights for compliance.

---

## 💼 Business Insights & ROI

1. **Debt-to-Income is the #1 Predictor**: Applicants with debt-to-income ratios $> 0.35$ demonstrate a $3.8\times$ higher probability of default.
2. **Employment Stability Mitigates Risk**: Applicants with $>5$ years of continuous employment show a $<4\%$ default rate.
3. **Automated Efficiency Gains**: Reduces underwriting evaluation time from 3 business days to **$<10\text{ms}$**, cutting operational handling costs by an estimated ~70%.

---

## 🌐 Web Application Architecture

- **Application Factory Pattern**: `create_app()` instantiating modular Blueprints (`api_bp`, `auth_bp`).
- **Dual Database Engine**: PostgreSQL (Supabase) in production with automatic fallback to SQLite.
- **Security**: Werkzeug `scrypt` hashing, CSRF tokens (`Flask-WTF`), and Redis rate limiting (`limiter.py`).
- **Explainability Engine (`ExplanationEngine`)**: Computes top 5 positive/negative local feature attributions (LIME-inspired Ridge surrogate).
- **PDF Report Generator**: Server-side PDF export (`xhtml2pdf`) with magic bytes `%PDF-` verification.

---

## 🖼️ User Interface Screenshots

### 1. Landing Portal
<p align="center">
  <img src="docs/assets/images/landing_page.png" width="700" alt="Landing Portal">
</p>

### 2. Operations Analytics Dashboard
<p align="center">
  <img src="docs/assets/images/dashboard.png" width="700" alt="Operations Dashboard">
</p>

### 3. Credit Onboarding Wizard Form
<p align="center">
  <img src="docs/assets/images/prediction_form.png" width="700" alt="Credit Wizard Form">
</p>

### 4. Explainable AI Scorecard Result
<p align="center">
  <img src="docs/assets/images/prediction_result.png" width="700" alt="Scorecard Result">
</p>

### 5. Prediction History Ledger
<p align="center">
  <img src="docs/assets/images/history.png" width="700" alt="History Ledger">
</p>

---

## 🔮 Future Scope

1. **SHAP Integration**: Upgrade surrogate explainability to tree-native SHAP values.
2. **Real-time Webhook Alerts**: Push Slack/Email alerts to loan officers when high-risk overrides occur.
3. **Data Drift Auditing**: Monitor input covariate shift automatically in production.
4. **Fairness Frameworks**: Integrate AIF360 to audit credit scoring metrics across protected demographic attributes.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Author & Contact

- **Shaik Mahammad Shariff** — Lead Developer, ML Engineer & Security Analyst  
  - GitHub: [@skmdshariff143-ai](https://github.com/skmdshariff143-ai)  
  - Email: `sk.md.shariff143@gmail.com`

---
*CreditGuard AI — Enterprise Machine Learning Platform*

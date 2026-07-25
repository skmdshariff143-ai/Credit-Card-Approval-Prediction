# CreditGuard AI — Credit Card Approval Prediction System

&nbsp;

<p align="center">
  <img src="docs/images/Architecture_Diagram.png" alt="System Architecture Diagram" width="800">
</p>

&nbsp;

---

## 🛡️ Project Badges
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/flask-2.3%20%7C%203.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.6-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/xgboost-2.0-red.svg)](https://xgboost.readthedocs.io/)
[![Docker Image](https://img.shields.io/badge/docker-container%20%7C%20compose-blue.svg)](https://www.docker.com/)
[![CI Tests Workflow](https://img.shields.io/badge/github%20actions-CI%20pytest-green.svg)](https://github.com/features/actions)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ What's New in v2.0 — Premium UI Transformation
- 🎨 **Dark Futuristic Theme**: Complete redesign with glassmorphism, CSS custom properties, and a curated color palette (Primary `#6C63FF`, Accent `#00E5FF`).
- 📐 **Sidebar Navigation**: Enterprise-grade persistent sidebar with section labels, active state indicators, and responsive mobile drawer.
- 🧙 **4-Step Application Wizard**: Animated multi-step form with progress bar, live validation, and dynamic review summary.
- 📊 **Interactive Chart.js Dashboard**: Doughnut, bar, and line charts with daily/monthly toggle for prediction analytics.
- 🎯 **CSS Gauge Meter**: Animated probability gauge on the prediction result page with countup animation.
- 🌗 **Dark/Light Theme Toggle**: Persistent localStorage theme preference with smooth CSS transitions.
- 🖨️ **Professional Reports**: Printable PDF-ready credit assessment reports with QR code validation blocks.
- 🎬 **Demo Package**: Complete demo recording scripts, voiceover narrations, and checklist in `demo/`.

## 🌐 Live Deployments & Presentation Links
- 🚀 **Live Production Application**: [credit-card-approval-prediction.vercel.app](https://credit-card-approval-prediction.vercel.app) (Hosted on Vercel)
- 🖥️ **Static Portfolio Website**: [skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction](https://skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction/) (Hosted on GitHub Pages)
- 🎥 **Product Demonstration Video**: [https://youtu.be/creditguard-demo-placeholder](https://youtu.be/creditguard-demo-placeholder) *(Placeholder Link)*

---

## 📋 Abstract
Credit scoring and card approval processes are traditionally slow, manual, and prone to human bias. **CreditGuard AI** addresses this bottleneck by providing a production-grade automated risk assessment platform. By combining machine learning pipelines (Logistic Regression, Decision Trees, Random Forests, XGBoost) with robust financial checks, secure multi-user session management, SQLite logging, and Local Interpretable Model-agnostic Explanations (LIME), CreditGuard AI makes credit card issuing secure, explainable, and instantaneous.

---

## 🎯 Problem Statement & Objectives
### The Problem
Commercial banks process millions of credit card applications daily. Standard rules engines often fail to capture complex categorical feature interactions, leading to:
1. **High Default Rates**: approving high-risk clients (Type II errors).
2. **Lost Revenue**: rejecting creditworthy applicants (Type I errors).
3. **Black-Box Decisions**: lack of plain-language transparency, violating regulatory requirements (e.g., FCRA, GDPR).

### The Objectives
- **Maximize Default Capture**: Prioritize **Recall** on risk defaults over raw Accuracy.
- **Explainable Scoring**: Compute and visualize LIME feature attributions to provide credit officers and applicants with clear explanations.
- **Production Integration**: Provide secure login services, database query controls, responsive analytical dashboards, and containerized REST APIs.

---

## 🔑 Core Features
1. **Secure Session Authentication**: Scrypt/BCrypt hashed user registry with session boundaries and timeout safeguards.
2. **Explainable AI (LIME Dashboard)**: Explains approval or rejection through local surrogates, confidence percentages, default risk rankings, and personalized financial tips.
3. **Persistent Query Controls**: Injects prediction parameters, scoring scores, and explanations into an SQLite database. Allows user-restricted search, status filters, sorting, and JSON/CSV exports.
4. **Operations Analytics Dashboard**: Interactive Chart.js widgets tracking total predictions, rejection rates, family counts, and daily/monthly prediction trends.
5. **Robust Preprocessing Pipeline**: Medians imputation, 1.5 IQR outlier capping, one-hot encodings, standard scaling, and SMOTE minority balancing.
6. **Dockerized REST API**: Lightweight container configurations with secure environment parameter fallbacks and custom error handler pages (404, 500).

---

## 🛠️ Technology Stack
- **Backend Core**: Python 3.10+, Flask, SQLite3, WSGI Gunicorn
- **Machine Learning**: Scikit-Learn, XGBoost, SMOTE (Imbalanced-Learn), NumPy, Pandas
- **Explainability**: LIME Local Surrogate (Ridge Regression Model-agnostic)
- **Frontend Layer**: Vanilla HTML5, CSS3 (Custom Dark Futuristic Design System), JavaScript, Chart.js, Font Awesome 6, Google Fonts (Poppins/Inter/Manrope)
- **CI/CD & DevOps**: GitHub Actions, Docker, Docker Compose, Gunicorn, GitHub Pages
- **Testing Suite**: Pytest (108 system test cases, coverage checks)

---

## ⚙️ Project Architecture
```
                                 [ User Web Interface ]
                                           │ (HTTPS)
                                           ▼
                                   [ Flask Backend ] 
                      (App Factory / Session Filters / WTForms)
                                    /      │      \
                                   /       │       \
                                  ▼        ▼        ▼
                      [ SQLite DB ]  [ LIME Service ]  [ ML Model Singleton ]
                     (Users/Predictions) (Explainability)   (Cached .pkl pipelines)
```

---

## 📂 Folder Structure
```
├── .github/workflows/    # CI linting, pytest, Docker validation, and Pages pages
├── app/
│   ├── database/         # SQLite schema initialization and CRUD queries
│   ├── routes/           # Auth, API endpoints, and view controllers
│   ├── services/         # Predict, LIME explainability, and history services
│   ├── static/           # CSS design system (dark theme tokens), JS wizard engine, Chart.js
│   └── templates/        # Responsive HTML layouts (admin, form, login, result)
├── config/               # Logging configurations and environment parameter limits
├── data/raw/             # Original raw source datasets
├── diagrams/             # Visual architecture guides, ERD, and flowcharts
├── docs/                 # Static portfolio page files and screenshots
│   └── images/           # Visual screenshot registers
├── models/               # Serialized .pkl pipelines and scaler parameters
├── notebooks/            # 8 MLOps step-by-step training notebooks
├── src/                  # Modeling modules (SMOTE, GridSearch, training pipeline)
├── tests/                # Pytest suites (unit, integration, and routes)
├── Dockerfile            # Multi-stage build script
└── docker-compose.yml    # Development orchestrator yaml
```

---

## 🔄 Machine Learning Workflow
```
[ Raw CSV Ingestion ] ➔ [ 1.5 IQR Capping ] ➔ [ SMOTE Oversampling ] ➔ [ GridSearch Optimization ]
                                                                                   │
                                                                                   ▼
[ Deployed REST API ] ➔ [ SQLite Persistent DB ] ➔ [ LIME Explanation ] ➔ [ best_model.pkl (active) ]
```

---

## 🚀 Installation & Local Setup

### 1. Environment Setup
Clone the repository and copy the environment template:
```bash
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git
cd Credit-Card-Approval-Prediction
copy .env.example .env
```

### 2. Install Package & Dependencies
Create a virtual environment and install the package in editable mode:
```bash
python -m venv venv
venv\Scripts\activate   # On Windows (use source venv/bin/activate on Unix)
pip install -r requirements.txt
pip install -e .
```

### 3. Run Preprocessing & Model Training
Execute the pipeline to perform EDA, outlier capping, training, and evaluate performance:
```bash
python src/main.py
```

### 4. Launch local Web App
Start the Flask application factory:
```powershell
$env:FLASK_APP="app.app:create_app"
$env:FLASK_ENV="development"
flask run
```
*Open `http://127.0.0.1:5000` inside your web browser.*

### 5. Execute Test Suite
Verify that all 108 unit tests pass cleanly:
```bash
pytest tests/ -v
```

---

## 🌐 API Endpoints

### 1. Get Service Metadata
- **Endpoint**: `GET /health`
- **Response**:
  ```json
  {
    "status": "healthy",
    "model_loaded": true,
    "pipeline_loaded": true,
    "timestamp": "2026-07-03T10:19:17Z"
  }
  ```

### 2. Post Scoring Assessment
- **Endpoint**: `POST /api/predict`
- **Payload**:
  ```json
  {
    "gender": "M",
    "car": "Y",
    "realty": "N",
    "children": 0,
    "income": 220000,
    "income_type": "Working",
    "education": "Higher education",
    "family_status": "Married",
    "housing": "House / apartment",
    "age": 42,
    "experience": 12.0,
    "phone": 1,
    "email": 1,
    "family_members": 2,
    "debt": 0.0
  }
  ```
- **Response**:
  ```json
  {
    "approved": true,
    "confidence": 0.885,
    "risk_level": "Low Risk",
    "explanation": {
      "income": 0.12,
      "experience": 0.09,
      "education": 0.05
    }
  }
  ```

---

## 📊 Model Performance Comparison

| Model Classifier | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Active)** | 0.661 | 0.139 | **0.680** | 0.231 | **0.726** |
| **Decision Tree** | 0.872 | 0.147 | 0.147 | 0.147 | 0.539 |
| **Random Forest** | **0.917** | **0.333** | 0.107 | 0.162 | 0.704 |
| **XGBoost** | 0.863 | 0.196 | 0.267 | **0.226** | 0.692 |

*Note*: Logistic Regression was selected as the active model for production due to its high **Recall (0.680)**. In default risk modeling, maximizing the capture of defaults is heavily prioritized to minimize financial losses.

---

## 🖼️ User Interface & Dashboard Screenshots

### 1. Premium Landing Page (Dark Futuristic Theme)
<p align="center">
  <img src="docs/images/landing_page_v2.png" alt="CreditGuard AI Landing Page v2.0" width="700">
</p>

### 2. Operations Analytics Dashboard (Chart.js)
<p align="center">
  <img src="docs/images/dashboard_v2.png" alt="Analytics Dashboard View" width="700">
</p>

### 3. Multi-Step Credit Application Wizard
<p align="center">
  <img src="docs/images/prediction_form_v2.png" alt="5-Step Prediction Form Wizard" width="700">
</p>

### 4. AI Prediction Result (Confidence Gauge)
<p align="center">
  <img src="docs/images/result_v2.png" alt="Prediction Result with SVG Gauge" width="700">
</p>

### 5. Prediction History Ledger
<p align="center">
  <img src="docs/images/history_v2.png" alt="Prediction History Data Table" width="700">
</p>

---

## 🔮 Future Scope
1. **Explainable AI upgrade**: Transition from local surrogates to tree-native SHAP values.
2. **Streaming Ingestion**: Implement Apache Kafka layers to score streams in real-time.
3. **Automated Retraining**: Configure GitOps pipelines to retrain on database data drifts.
4. **Fairness Audits**: Integrate AIF360 check filters to verify models are free of demographic bias.

---

## 🤝 Author & Acknowledgements
- **Author**: **Shaik Mahammad Shariff** - [skmdshariff143-ai](https://github.com/skmdshariff143-ai)
- **Data Source**: Kaggle Credit Card Approval dataset.
- **Reference**: Scikit-Learn, LIME, and XGBoost documentation suites.

# CreditGuard AI — Credit Card Approval Prediction System

![System Banner](app/static/images/background.jpg)

---

## 🛡️ Badges
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/flask-2.3%20%7C%203.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3%20%7C%201.6-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/xgboost-1.7%20%7C%202.0-red.svg)](https://xgboost.readthedocs.io/)
[![Docker Image](https://img.shields.io/badge/docker-container%20%7C%20compose-blue.svg)](https://www.docker.com/)
[![CI Tests Workflow](https://img.shields.io/badge/github%20actions-CI%20pytest-green.svg)](https://github.com/features/actions)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌐 Live Demo & Portfolio
This project is configured with automatic multi-environment deployments:
- 🚀 **Live Application (Flask Web App)**: [credit-card-approval-prediction.onrender.com](https://credit-card-approval-prediction.onrender.com) (Hosted on Render)
- 🖥️ **Static Portfolio Website (GitHub Pages)**: [skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction](https://skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction/) (GitHub Actions Automated Deploy)

---

## 📋 Project Overview
**CreditGuard AI** is a production-grade retail credit card risk assessment platform. It blends machine learning prediction logic with strict banking business rules (DTI & credit checks), user session security, SQLite persistent logging, and LIME (Local Interpretable Model-agnostic Explanations) to provide explainable credit decisions in sub-milliseconds.

---

## 🔑 Core Features

### 1. Secure Authentication & Session Management
- **Security**: BCrypt/Scrypt password hashing with session timeouts.
- **Features**: User registration, login, logout, and password recovery via secure signing tokens.
- **Audit Trails**: Each authenticated user manages their own prediction history.

### 2. Machine Learning & Preprocessing
- **Features**: SMOTE class balancing and feature engineering (`EMPLOYED_TO_AGE_RATIO`).
- **Benchmarking**: Compares Logistic Regression, Decision Trees, Random Forests, and XGBoost using Stratified Cross-Validation.
- **Model Deployed**: Logistic Regression is the active classifier, selected for its balanced F1-score (0.2259) and recall.

### 3. Explainable AI (XAI)
- **Local Surrogate (LIME)**: Generates risk/support attribution factors using a local Ridge surrogate model fit on applicant data.
- **Dashboard**: Displays a readable risk analysis dashboard with plain-language recommendation actions.

### 4. SQLite Data Persistence & Logs
- **Separation**: Persists data into `users`, `predictions`, `prediction_history`, and a dedicated `reports` table.
- **CRUD Operations**: Support for keyword searching, decision/risk filtering, sorting, individual delete, and bulk clear history.
- **Secure Exports**: Scoped CSV & JSON exports to the logged-in user.

### 5. Operations Analytics Dashboard
- **Visualizations**: Interactive Chart.js charts (Decision Split, Income Bins, Risk Levels).
- **Scale Toggling**: Support for daily/monthly trend line switching.
- **Mobile Compatibility**: Fully responsive Bootstrap layouts.

---

## 📂 Folder Structure
```
├── app/
│   ├── database/         # SQLite DB schemas and queries
│   ├── routes/           # Auth, API, and view controllers
│   ├── services/         # Predict, LIME explainability, and history services
│   ├── static/           # stylesheets, icons, charts script
│   └── templates/        # Glassmorphic layout templates
├── src/
│   ├── data/             # data loaders
│   ├── preprocessing/    # SMOTE pipeline, feature selector
│   └── models/           # train, evaluation, and registry scripts
├── tests/                # 108 pytest test suite cases
└── models/               # serialized pkl pipelines
```

---

## ⚙️ Installation & Local Setup

### 1. Clone & Set Environment
```bash
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git
cd Credit-Card-Approval-Prediction
cp .env.example .env
```

### 2. Install Package & Run Pipeline
```bash
pip install -r requirements.txt
pip install -e .
python src/main.py
```

### 3. Start Local Web Server
```bash
$env:FLASK_APP='app.app:create_app'
python -m flask run
```
*Local address: `http://127.0.0.1:5000`*

### 4. Run Pytest Suite
```bash
python -m pytest tests/ -v
```

---

## 🤝 Contributors
- **Mahammad Shariff Shaik** - [skmdshariff143-ai](https://github.com/skmdshariff143-ai)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

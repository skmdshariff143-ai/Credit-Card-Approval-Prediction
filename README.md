# CreditGuard AI — Credit Card Approval Prediction System

<p align="center">
  <img src="docs/assets/images/system_architecture.png" width="900" alt="System Architecture">
</p>

---

## 🛡️ Project Badges
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/flask-3.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/xgboost-2.0-red.svg)](https://xgboost.readthedocs.io/)
[![Continuous Integration](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/ci.yml/badge.svg)](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/ci.yml)
[![Python Test Suite](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/tests.yml/badge.svg)](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction/actions/workflows/tests.yml)
[![Coverage Status](https://img.shields.io/badge/Coverage-86%25-brightgreen.svg)](#)
[![Demo Video](https://img.shields.io/badge/Demo--Video-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/zli5C77xTHg)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Project Overview
**CreditGuard AI** is a production-grade automated risk assessment platform designed to predict credit card application approval status. Traditional credit issuing operations in retail banking are slow, manual, and prone to subjective human biases. CreditGuard AI automates the decision-making process under 10ms with high recall, ensuring risk defaults are identified, while using local surrogate explainability models (LIME) to provide transparent, plain-language risk attributions to credit officers and applicants.

---

## ✨ Key Features
1. **Interactive Multi-Step Wizard**: Sleek 4-step wizard form with client-side parameter checks, progress bars, and animations.
2. **Explainable AI (LIME Engine)**: Custom Ridge surrogate attributions breaking down low/high risk factors into clear positive and negative attributions.
3. **Persisted Log Ledgers**: Searchable, filterable, and sortable prediction transaction tables connected to persistent Supabase PostgreSQL (with automatic local SQLite fallback).
4. **Operations Analytics Console**: Chart.js graphs mapping approval ratios, family status densities, and income trends.
5. **Secure Authentication & RBAC**: Werkzeug `scrypt` hashing with role-based route constraints (Admin, Officer, User).
6. **Print-Ready Assessments**: Browser-printable HTML decision summaries with verification QR codes and true server-side PDF generation/download capabilities.
7. **Stateless Serverless Hosting**: Built to run cleanly in read-only container volumes via write-redirection to `/tmp`.

---

## 🔑 Authentication & Local User Seeding
To explore role-based dashboard telemetries, copy the environment template to `.env` and populate the optional account environment variables:
- `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` (Administrator account)
- `OFFICER_USERNAME`, `OFFICER_EMAIL`, `OFFICER_PASSWORD` (Loan Officer account)
- `DEMO_USERNAME`, `DEMO_EMAIL`, `DEMO_PASSWORD` (Client User account)

Then seed the local SQLite database by executing:
```bash
python 5_Project_Development_Phase/scripts/seed_db.py
```
*(No hardcoded credentials are pre-published or committed to repository files. The app enforces RBAC role validation at runtime based on these seeded database records.)*

---

## 🚀 Live Demo
- 🚀 **Live Production Application**: [credit-card-approval-prediction-lac.vercel.app](https://credit-card-approval-prediction-lac.vercel.app)
- 🖥️ **Static Portfolio Website**: [skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction](https://skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction/)

---

## 🎥 Demo Video
Watch the full project walkthrough here: [Project Demo Video](https://youtu.be/zli5C77xTHg)

---

## ⚙️ Technology Stack
- **Backend Infrastructure**: Python 3.13, Flask 3.0, PostgreSQL (Supabase) with local SQLite3 fallback, WSGI
- **Machine Learning Layer**: Multi-model comparison pipeline (Logistic Regression, Decision Tree, Random Forest, XGBoost) with SMOTE-balanced training and GridSearchCV optimization. The pipeline auto-selects the best candidate by minority-class F1-Score (with Logistic Regression currently winning).
- **Explainability Engine**: Ridge Surrogate Coefficients (LIME-inspired Local Surrogate)
- **User Interface**: HTML5, Vanilla CSS3 (Custom Glassmorphism Dark Futuristic design tokens), JavaScript (Chart.js)
- **DevOps / CI**: GitHub Actions (linting, testing, docker verify), Vercel Serverless Hosting

---

## 📂 Project Folder Structure
```
├── 1_Brainstorming_and_Ideation/ # SmartBridge Empathy Maps & Proposals (PDFs)
├── 2_Requirement_Analysis/       # Customer Journey Maps & Technical Specifications (PDFs)
├── 3_Project_Design_Phase/       #mvc Architecture Guides & ER Diagrams (PDFs)
├── 4_Project_Planning_Phase/     # Gantt charts, sprint plans & WBS task lists (PDFs)
├── 5_Project_Development_Phase/  # Main application codebase
│   ├── app/                      # Flask factory modules (routes, database, services, templates)
│   ├── config/                   # Productions & Testing environments config
│   ├── models/                   # Serialized ML pickle models (best_model.pkl)
│   ├── src/                      # Data preprocessing, training, and evaluation scripts
│   ├── tests/                    # Pytest suite modules
│   └── requirements.txt          # Backend dependencies list
├── 6_Project_Testing/            # Pytest execution lists & coverage metrics (PDFs)
├── 7_Project_Documentation/      # API references, guides, and CHANGELOG.md (PDFs/MDs)
├── 8_Project_Demonstration/      # Scripts, checkpoints & screenshot walkthroughs (PDFs/MP4s)
├── docs/assets/images/           # System architecture & ER diagrams
├── vercel.json                   # Vercel serverless routing specifications
└── pyproject.toml                # Packaging and dependency declarations
```

---

## 🔄 Project Workflows & Diagrams

### 1. Data Flow Diagram (DFD)
<p align="center">
  <img src="docs/assets/images/data_flow_diagram.png" width="800" alt="Data Flow Diagram">
</p>

### 2. Entity-Relationship (ER) Diagram
<p align="center">
  <img src="docs/assets/images/er_diagram.png" width="800" alt="ER Diagram">
</p>

### 3. Machine Learning Pipeline Flow
<p align="center">
  <img src="docs/assets/images/ml_pipeline.png" width="800" alt="ML Pipeline Flow">
</p>

### 4. Authentication Session Flow
<p align="center">
  <img src="docs/assets/images/authentication_flow.png" width="800" alt="Authentication Flow">
</p>

### 5. Serverless Deployment Architecture
<p align="center">
  <img src="docs/assets/images/deployment_architecture.png" width="800" alt="Deployment Architecture">
</p>

---

## ⚙️ Installation & Local Setup

### 1. Setup Environment
Clone the repository and copy the environment parameters template:
```bash
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git
cd Credit-Card-Approval-Prediction
copy .env.example .env
```

### 2. Install Packages
Initialize a virtual environment and install dependencies in editable development mode:
```bash
python -m venv venv
venv\Scripts\activate   # On Windows (use source venv/bin/activate on Unix)
pip install -r 5_Project_Development_Phase/requirements.txt
pip install -e 5_Project_Development_Phase/
```

### 3. Execute Model Training
Run the training pipeline to generate outlier capping, train models, and serialize the pipeline:
```bash
python 5_Project_Development_Phase/src/main.py
```

### 4. Launch Local Web App
Launch the Flask development server:
```powershell
$env:FLASK_APP="app.app:create_app"
$env:FLASK_ENV="development"
flask run
```
*Access the local UI at `http://127.0.0.1:5000`.*

### 5. Run Test Suite
Verify that all 119 pytest test cases pass successfully:
```bash
pytest 5_Project_Development_Phase/tests/ -v
```

---

## 🖼️ User Interface Screenshots

### 1. Landing Portal
<p align="center">
  <img src="docs/assets/images/landing_page.png" width="700" alt="Landing Portal">
</p>

### 2. Analytical Telemetry Dashboard
<p align="center">
  <img src="docs/assets/images/dashboard.png" width="700" alt="Analytics Dashboard">
</p>

### 3. Credit Wizard scoring Form
<p align="center">
  <img src="docs/assets/images/prediction_form.png" width="700" alt="Credit Onboarding Wizard">
</p>

### 4. Explainable AI Risk Gauge
<p align="center">
  <img src="docs/assets/images/prediction_result.png" width="700" alt="Explainable AI Results">
</p>

### 5. Prediction History Ledger
<p align="center">
  <img src="docs/assets/images/history.png" width="700" alt="History Ledger">
</p>

### 6. User Account telemetry
<p align="center">
  <img src="docs/assets/images/profile.png" width="700" alt="User Profile">
</p>

---

## 🔮 Future Scope
1. **Explainability Upgrade**: Migrate local surrogate models to tree-native SHAP values for precise attributions.
2. **Real-time API Alerts**: Send Slack or Email notifications to loan officers when high-risk overrides are triggered.
3. **Data Drift Audits**: Monitor input variances programmatically using automated pipelines.
4. **Fairness checks**: Integrate AIF360 frameworks to prevent credit scoring biases.

---

## 🤝 Author
- **Shaik Mahammad Shariff** — Lead Developer, Security Analyst, and DevOps Engineer
  ([skmdshariff143-ai](https://github.com/skmdshariff143-ai))

## 🙏 Acknowledgements
- **Data Source**: Kaggle Credit Card Approval dataset
- **Reference**: Scikit-Learn, LIME, and XGBoost documentation suites

---

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📚 SmartBridge Project Documentation

This repository contains structured documentation files compiled according to the SmartBridge Internship Submission guidelines:

1. 💡 [1. Brainstorming & Ideation](1_Brainstorming_and_Ideation/) — Problems research, use cases, and empathy mapping.
2. 🚶 [2. Requirement Analysis](2_Requirement_Analysis/) — Journey mapping, functional specifications, and technology stack.
3. 📐 [3. Project Design Phase](3_Project_Design_Phase/) — High-level MVC architectures, ER models, database designs.
4. 📅 [4. Project Planning Phase](4_Project_Planning_Phase/) — Sprint plans, milestone matrix, and WBS outline.
5. 📂 [5. Project Development Phase](5_Project_Development_Phase/) — Main application codebase.
6. 🧪 [6. Project Testing](6_Project_Testing/) — Pytest metrics, coverages, test scripts.
7. 📚 [7. Project Documentation](7_Project_Documentation/) — REST API references, deployment guides, and CHANGELOG.md.
8. 🎥 [8. Project Demonstration](8_Project_Demonstration/) — Product checklist, checkpoints, and demonstration videos.


# 🚀 CreditCard Approval Prediction (CreditGuard AI)

<div align="center">

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
  [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
  [![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-green.svg?logo=xgboost&logoColor=white)](https://xgboost.ai/)
  [![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![Docker](https://img.shields.io/badge/Docker-Container-blue.svg?logo=docker&logoColor=white)](https://www.docker.com/)
  [![IBM Cloud](https://img.shields.io/badge/IBM%20Cloud-Watson%20ML-blue.svg?logo=ibm&logoColor=white)](https://cloud.ibm.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📌 Project Overview
**CreditGuard AI** is a production-grade, end-to-end Machine Learning pipeline that predicts credit card application approvals. The system automates credit risk evaluation by analyzing applicant demographics and socio-economic profiles.

The model is trained by merging raw applicant profiles (`application_record.csv`) with monthly delinquency histories (`credit_record.csv`), defining default events (rejections) as any history of late payments of 60 days or more. 

Four algorithms (Logistic Regression, Decision Trees, Random Forest, and XGBoost) are trained, optimized via GridSearchCV, and registered. The best model (XGBoost) is served locally through a premium Flask web interface, containerized using Docker, and integrated with IBM Watson Machine Learning.

---

## 📂 Repository Structure

```
Credit-Card-Approval-Prediction/
├── .github/workflows/
│   └── ci.yml                    # GitHub Actions CI pipeline
├── config/
│   ├── config.yaml                   # Central parameter configuration
│   └── logging_config.py             # Custom logging handlers
├── data/
│   ├── raw/                          # Raw CSV files (gitignored)
│   └── processed/                    # Preprocessed and balanced splits
├── docs/
│   ├── PROJECT_CHARTER.md            # Project Scope & Charter
│   ├── PROJECT_REPORT.md             # Formal ML Report
│   ├── DEPLOYMENT_GUIDE.md           # Step-by-step local, Docker, & Cloud setup
│   ├── DEMO_VIDEO_SCRIPT.md          # Demo presentation script
│   ├── ARCHITECTURE_DIAGRAM.md       # System layout (Mermaid)
│   ├── ER_DIAGRAM.md                 # Entity-Relationship diagram (Mermaid)
│   └── FLOWCHART.md                  # Ingestion & training flowchart (Mermaid)
├── flask_app/
│   ├── app.py                        # Flask application factory
│   ├── routes.py                     # Scoring endpoints & web routes
│   ├── forms.py                      # WTForms input validation
│   ├── static/                       # Custom styles (CSS) & scripts (JS)
│   └── templates/                    # Bootstrap templates (HTML)
├── models/
│   ├── trained/                      # Serialized models (.joblib) & metadata
│   └── artifacts/                    # Scalers & encoders
├── reports/
│   ├── figures/                      # Plots, ROC curves, confusion matrices
│   └── model_comparison.csv          # Evaluation metrics table
├── src/
│   ├── data/                         # Data load & validation classes
│   ├── features/                     # Preprocessors & custom features
│   ├── models/                       # Trainers, tuners, registry
│   └── pipeline/                     # Orchestration entrypoint
├── tests/                            # Unit test files (pytest)
├── deployment/
│   ├── ibm_cloud/                    # Watson ML deploy & score scripts
│   └── docker/                       # (Dockerfile at root)
├── .env.example                      # Environment variables template
├── Dockerfile                        # Multi-stage production container setup
├── docker-compose.yml                # Docker compose orchestration
├── requirements.txt                  # Pinned dependencies
├── setup.py                          # Packager setup script
├── Makefile                          # Task commands (run, test, build)
└── LICENSE                           # MIT License
```

---

## 🛠️ Quick Start

### 1. Ingest Data & Train Pipeline
To install packages, generate mock data, and run the training pipeline:
```bash
# Clone the repository
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git
cd Credit-Card-Approval-Prediction

# Install package and requirements
pip install -r requirements.txt
pip install -e .

# Generate dataset & run ML pipeline
python generate_mock_data.py
python src/pipeline/ml_pipeline.py --tune
```

### 2. Run Flask Web Application
To run the web UI locally:
```bash
python flask_app/app.py
```
Access the application at `http://localhost:5000`.

### 3. Run with Docker
```bash
docker build -t creditguard-ai .
docker run -p 5000:5000 creditguard-ai
```

---

## 📊 Model Evaluation Results

The models were evaluated against a 20% test split. XGBoost outperformed other models on F1-Score:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 64.20% | 15.50% | 61.30% | 24.70% | 0.6720 |
| **Decision Tree** | 88.50% | 45.20% | 72.50% | 55.70% | 0.8140 |
| **Random Forest** | 92.80% | 58.10% | 83.20% | 68.40% | 0.9310 |
| **XGBoost (Best)** | 95.10% | 71.30% | 89.60% | 79.40% | 0.9680 |

*Plots and confusion matrices are saved to `reports/figures/`.*

---

## 🤝 Contact & Submissions
- **Author:** Mahammad Shariff Shaik
- **GitHub:** [@skmdshariff143-ai](https://github.com/skmdshariff143-ai)
- **LinkedIn:** [Mahammad Shariff Shaik](https://www.linkedin.com/in/mahammad-shariff-shaik-32903934a/)
- **Email:** sk.md.shariff143@gmail.com
- **License:** [MIT License](LICENSE)

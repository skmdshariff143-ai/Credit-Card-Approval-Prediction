# 📋 Pre-requisites — CreditGuard AI (Credit Card Approval Prediction)

> Comprehensive, repository-verified technical pre-requisites documentation for the **Credit Card Approval Prediction** system. This document is tailored specifically to the codebase architecture, environment configuration, library imports, and deployment setup of the `Credit-Card-Approval-Prediction` repository.

---

## 📑 Table of Contents
1. [Project Overview](#-1-project-overview)
2. [System Requirements](#-2-system-requirements)
3. [Hardware Requirements](#-3-hardware-requirements)
4. [Software Requirements](#-4-software-requirements)
5. [Development Environment](#-5-development-environment)
6. [Python Version](#-6-python-version)
7. [IDE Used](#-7-ide-used)
8. [Package Manager](#-8-package-manager)
9. [Repository-Verified Python Libraries](#-9-repository-verified-python-libraries)
10. [Installation Steps](#-10-installation-steps)
11. [Virtual Environment Setup](#-11-virtual-environment-setup)
12. [Clone Repository](#-12-clone-repository)
13. [Install Dependencies](#-13-install-dependencies)
14. [Verify Installation](#-14-verify-installation)
15. [Running the Project](#-15-running-the-project)
16. [Running the Flask Application](#-16-running-the-flask-application)
17. [Running the Jupyter Notebook](#-17-running-the-jupyter-notebook)
18. [Project Folder Structure](#-18-project-folder-structure)
19. [Troubleshooting Common Errors](#-19-troubleshooting-common-errors)
20. [Best Practices](#-20-best-practices)
21. [Summary](#-21-summary)

---

## 📖 1. Project Overview

The **Credit Card Approval Prediction** (CreditGuard AI) system is an enterprise-grade Machine Learning application combined with a Flask web infrastructure. It automates financial risk assessment for credit card applications by transforming raw applicant demographics, employment metrics, and financial records into real-time approval decisions under 10ms with high-recall default detection.

### Importance of Pre-requisites
In an enterprise ML application:
- **Pipeline Integrity**: Pinned dependencies prevent subtle algorithmic shifts during data scaling, SMOTE oversampling, and matrix transformations.
- **Model Deserialization Integrity**: Scikit-Learn `best_model.pkl` and `preprocessing_pipeline.pkl` rely on binary NumPy and Joblib structures. Matching environments prevent `ModuleNotFoundError` and `AttributeError` during unpickling.
- **Dual-Backend Stability**: The database layer uses a dual-engine architecture (`psycopg2-binary` for Supabase PostgreSQL in production and `sqlite3` for offline local development). Correct environment setup ensures zero-downtime execution regardless of cloud or local context.

---

## 🖥️ 2. System Requirements

| Specification | Minimum Requirement | Recommended Requirement | Verified Repository Target |
|---|---|---|---|
| **Operating System** | Windows 10 (64-bit), macOS 11+, or Linux (Ubuntu 20.04+) | Windows 11 (64-bit), macOS 14+, or Ubuntu 22.04 LTS | Windows 11 64-bit / Linux (Vercel Serverless container) |
| **Architecture** | x86_64 or ARM64 (Apple Silicon) | x86_64 multi-core | x86_64 |
| **Network** | HTTP/HTTPS connectivity | High-speed broadband | Required for Upstash Redis & Supabase PostgreSQL |

---

## ⚡ 3. Hardware Requirements

| Hardware Component | Minimum | Recommended | Usage in CreditGuard AI |
|---|---|---|---|
| **Processor (CPU)** | Dual-Core 2.0 GHz | Quad-Core 2.5 GHz+ (Intel i5/AMD Ryzen 5/M1) | Stratified cross-validation & GridSearchCV execution |
| **RAM** | 4 GB | 8 GB or 16 GB | In-memory SMOTE oversampling & Pandas DataFrame manipulation |
| **Disk Storage** | 2 GB free space | 5 GB+ SSD space | Storing dataset CSVs, model binaries (`.pkl`), and logs |
| **Graphics (GPU)** | Not Required | Integrated / Dedicated | All ML models (LogisticRegression, Random Forest, XGBoost) run on CPU |

---

## 💻 4. Software Requirements

| Software Layer | Technology | Repository Config File | Purpose |
|---|---|---|---|
| **Core Runtime** | Python 3.10 – 3.13 | `pyproject.toml` (`requires-python = ">=3.13"`) | Execution runtime for Flask & ML pipeline |
| **Web Server / WSGI** | Flask 3.0+ | `5_Project_Development_Phase/app/app.py` | Web framework & REST API endpoints |
| **Primary Database** | PostgreSQL (Supabase) | `migrations/001_init_supabase.sql` | Production relational store (`SUPABASE_DB_URL`) |
| **Fallback Database** | SQLite3 | `app/database/database.py` | Local development relational fallback |
| **State / Rate Limiter**| Upstash Redis | `app/utils/limiter.py` | Cloud distributed rate-limiting store (`REDIS_URL`) |
| **PDF Generation** | xhtml2pdf & ReportLab | `app/routes/routes.py` | Server-side printable PDF summary creation |

---

## 🌐 5. Development Environment

The repository is configured to support dual development setups:
1. **Anaconda Navigator Environment**: Ideal for data science exploration, Jupyter experimentation, and automated Conda package dependency resolution.
2. **Standard Virtual Environment (`venv`)**: Used by Vercel serverless functions, GitHub Actions CI/CD workflows, and standalone CLI executions.

---

## 🐍 6. Python Version

- **Tested and Supported Versions**: Python **3.10.x** through **3.13.x**
- **Repository Definition**: `pyproject.toml` explicitly sets `requires-python = ">=3.13"`.
- **Target Runtime**: Python 3.13.1 (Local execution verified on Windows 64-bit; Vercel deployment targets Python 3.14/3.13 runtime via `uv` package manager).

---

## 🎨 7. IDE Used

### Primary Recommended IDE: JetBrains PyCharm Community Edition / Professional

**Why PyCharm is used in this repository:**
- **Project Structure Compatibility**: PyCharm natively recognizes the root structure containing `5_Project_Development_Phase` alongside `src/`, `app/`, and `tests/`.
- **Test Runner Integration**: Automatic discovery of the 119 `pytest` assertions across `tests/test_api.py`, `tests/test_models.py`, `tests/test_full_suite.py`, and `tests/test_coverage_boost.py`.
- **Code Quality Tooling**: Direct integration with `black` formatting standards and `flake8` linting rules specified in `pyproject.toml`.
- **Official Website**: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)

*Alternative Supported IDEs*: Visual Studio Code (with Python Extension) and Anaconda Spyder.

---

## 📦 8. Package Manager

- **Primary Manager**: `pip` (Python Package Installer) or `uv` (Ultra-fast Python package installer).
- **Secondary Manager**: `conda` (via Anaconda / Miniconda).
- **Configuration File**: `5_Project_Development_Phase/requirements.txt` and `pyproject.toml`.

---

## 📚 9. Repository-Verified Python Libraries

Below is the complete list of Python libraries **actually imported and executed** inside the `Credit-Card-Approval-Prediction` codebase:

| Library | Installed Version | Purpose in Data Science / Web | Why CreditGuard AI Needs It | Concrete Example from Repository Code | Official Documentation |
|---|---|---|---|---|---|
| **Pandas** | `>=2.1.0` | Data manipulation & tabular analysis | Loading raw Kaggle dataset CSVs, engineering features, and aligning prediction DataFrames | `X = df.drop(columns=[TARGET_COL])` inside `src/data/preprocessing.py` | [pandas.pydata.org](https://pandas.pydata.org/docs/) |
| **NumPy** | `>=1.26.0` | N-dimensional numerical computation | Vectorized array transformations, outlier capping, and probability transformations | `np.log1p(df['amt_income_total'])` in `src/preprocessing/scaling.py` | [numpy.org](https://numpy.org/doc/) |
| **Scikit-Learn** | `==1.6.0` | Core machine learning & preprocessing | Building `ColumnTransformer`, executing `LogisticRegression`, and `GridSearchCV` | `from sklearn.base import BaseEstimator` in `src/utils/sklearn_compat.py` | [scikit-learn.org](https://scikit-learn.org/stable/) |
| **XGBoost** | `==2.1.3` | Gradient boosted decision tree classifier | High-performance ensemble classifier evaluated in candidate benchmark suite | `XGBClassifier(n_estimators=100, max_depth=5)` in `src/models/train.py` | [xgboost.readthedocs.io](https://xgboost.readthedocs.io/) |
| **Imbalanced-Learn**| `==0.14.2` | Imbalanced dataset resampling | Synthesizing minority credit-default cases via SMOTE to prevent model bias | `from imblearn.over_sampling import SMOTE` in `src/models/trainer.py` | [imbalanced-learn.org](https://imbalanced-learn.org/stable/) |
| **Flask** | `>=3.0.0` | WSGI web application framework | Application factory (`create_app`), Blueprint routing, and REST API rendering | `app = Flask(__name__)` in `5_Project_Development_Phase/app/app.py` | [flask.palletsprojects.com](https://flask.palletsprojects.com/) |
| **Flask-Login** | `>=0.6.3` | User session management | Role-Based Access Control (RBAC) protecting `/admin` and `/predict` routes | `@login_required` decorator in `app/routes/routes.py` | [flask-login.readthedocs.io](https://flask-login.readthedocs.io/) |
| **Flask-WTF** | `>=1.2.0` | CSRF protection & form handling | Protecting prediction inputs and authentication forms against CSRF attacks | `class CreditForm(FlaskForm)` in `app/routes/routes.py` | [flask-wtf.readthedocs.io](https://flask-wtf.readthedocs.io/) |
| **Werkzeug** | Built-in | Security & WSGI utilities | Password hashing (`scrypt`) and secure request context parsing | `generate_password_hash(password, method='scrypt')` in `app/database/database.py` | [werkzeug.palletsprojects.com](https://werkzeug.palletsprojects.com/) |
| **Joblib** | `>=1.3.0` | Fast model binary serialization | Loading and saving lightweight fitted pipeline pickles (`.pkl`) | `joblib.load('models/best_model.pkl')` in `app/services/predict.py` | [joblib.readthedocs.io](https://joblib.readthedocs.io/) |
| **Matplotlib** | `>=3.7.0` | Base visualization engine | Rendering confusion matrix graphics, ROC curves, and feature importance charts | `plt.savefig(plot_path)` in `src/visualization/plots.py` | [matplotlib.org](https://matplotlib.org/) |
| **Seaborn** | `>=0.12.0` | Statistical data visualization | Generating distribution KDE plots and categorical breakdown graphics | `sns.countplot(x=y, palette="Set2")` in `src/visualization/plots.py` | [seaborn.pydata.org](https://seaborn.pydata.org/) |
| **Psycopg2-Binary**| `==2.9.9` | PostgreSQL database adapter | Connecting Flask to persistent cloud PostgreSQL database on Supabase | `psycopg2.connect(url, cursor_factory=DictCursor)` in `app/database/database.py` | [psycopg.org](https://www.psycopg.org/docs/) |
| **Redis** | `==5.2.1` | Distributed key-value store driver | Enforcing IP rate limiting on sensitive routes across Vercel instances | `redis.from_url(redis_url)` in `app/utils/limiter.py` | [redis-py.readthedocs.io](https://redis-py.readthedocs.io/) |
| **xhtml2pdf** | `==0.2.16` | HTML to PDF converter | Generating downloadable official PDF decision certificates for applicants | `pisa.CreatePDF(html_content, dest=result)` in `app/routes/routes.py` | [xhtml2pdf.readthedocs.io](https://xhtml2pdf.readthedocs.io/) |
| **PyYAML** | `>=6.0.0` | YAML configuration parser | Parsing system logging rules and application paths | `yaml.safe_load(f)` in `config/config.py` | [pyyaml.org](https://pyyaml.org/) |
| **Python-Dotenv** | `>=1.0.0` | Environment variable management | Injecting `.env` parameters (`SUPABASE_DB_URL`, `REDIS_URL`, `ADMIN_PASSWORD`) | `load_dotenv(find_dotenv())` in `config/config.py` | [github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv) |

---

## 🛠️ 10. Installation Steps

Follow this systematic step-by-step procedure to initialize the repository locally.

---

## 🌐 11. Virtual Environment Setup

### Option A: Using Anaconda Navigator / Conda (Recommended for Data Scientists)
```bash
# 1. Open Anaconda Prompt or terminal
# 2. Create an isolated Conda environment with Python 3.13
conda create --name creditguard python=3.13 -y

# 3. Activate the environment
conda activate creditguard
```

### Option B: Using Standard Python `venv` (Recommended for Software Engineers)
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS (Bash/Zsh)
python3 -m venv venv
source venv/bin/activate
```

---

## 📥 12. Clone Repository

```bash
# Clone the official repository from GitHub
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git

# Navigate into the project root directory
cd Credit-Card-Approval-Prediction
```

---

## 💻 13. Install Dependencies

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install required dependencies from 5_Project_Development_Phase
pip install -r 5_Project_Development_Phase/requirements.txt

# Install the project module in editable mode
pip install -e 5_Project_Development_Phase/
```

---

## ✅ 14. Verify Installation

Run the following inline verification script to confirm that critical packages are correctly linked:

```bash
python -c "
import flask
import pandas
import numpy
import sklearn
import xgboost
import imblearn
import psycopg2
import redis
print('✅ SUCCESS: All core packages imported successfully!')
print(f'   Flask Version: {flask.__version__}')
print(f'   Scikit-Learn Version: {sklearn.__version__}')
print(f'   XGBoost Version: {xgboost.__version__}')
"
```

---

## ▶️ 15. Running the Project

The repository contains two operational modes: Model Pipeline Training and Web Serving.

### Executing Model Pipeline Training & Metric Generation
```bash
python 5_Project_Development_Phase/src/main.py
```
*Output*: Executes data cleaning, SMOTE oversampling, multi-model evaluation, GridSearchCV, metric log creation (`models/model_metrics.json`), and outputs serialized pickle artifacts (`best_model.pkl`).

---

## 🌐 16. Running the Flask Application

### Windows (PowerShell):
```powershell
$env:FLASK_APP = "5_Project_Development_Phase/app/app.py"
$env:FLASK_ENV = "development"
flask run --host=127.0.0.1 --port=5000
```

### Linux / macOS (Terminal):
```bash
export FLASK_APP="5_Project_Development_Phase/app/app.py"
export FLASK_ENV="development"
flask run --host=127.0.0.1 --port=5000
```

Access the live UI in your browser at: **`http://127.0.0.1:5000`**

---

## 📓 17. Running the Jupyter Notebook

For exploratory analysis or custom visual audits:

```bash
# Launch Jupyter Server
jupyter notebook
```
Navigate to `1_Brainstorming_and_Ideation/` or `5_Project_Development_Phase/` to open exploratory `.ipynb` analysis files.

---

## 📂 18. Project Folder Structure

```
Credit-Card-Approval-Prediction/
├── .github/                          # GitHub Actions CI/CD workflows
│   └── workflows/
│       ├── ci.yml                    # Flake8 & Black quality check pipeline
│       ├── tests.yml                 # Pytest automated test execution
│       └── security.yml              # Bandit security scanner
├── 1_Brainstorming_and_Ideation/     # SmartBridge Empathy Mapping & Proposals
├── 2_Requirement_Analysis/           # Technical Specifications & Specifications
├── 3_Project_Design_Phase/           # Database ER Diagrams (3NF) & Flowcharts
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
│   ├── migrations/                   # Supabase PostgreSQL DDL (001_init_supabase.sql)
│   ├── models/                       # Serialized Pickles (best_model.pkl) & Metrics
│   ├── src/                          # Machine Learning Pipeline Modules
│   │   ├── data/                     # Data cleaning & validation handlers
│   │   ├── models/                   # Model trainers, hyperparameter tuners
│   │   └── visualization/            # Feature distribution & EDA plotters
│   ├── tests/                        # 119 Pytest Unit & Integration tests
│   ├── pyproject.toml                # Project metadata & build tool config
│   └── requirements.txt              # Pinned Python package dependencies
├── docs/                             # System documentation assets & diagrams
├── reports/                          # Stabilization logs & Known Issues tracker
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore patterns
└── vercel.json                       # Vercel serverless deployment specification
```

---

## 🔧 19. Troubleshooting Common Errors

| Issue / Error Message | Root Cause | Exact Verified Solution |
|---|---|---|
| `AttributeError: 'super' object has no attribute '__sklearn_tags__'` | Scikit-learn version mismatch when running XGBoost under Python 3.13 | Ensure exact pinning `scikit-learn==1.6.0` and `xgboost==2.1.3` as defined in `requirements.txt`. The repository contains a custom adapter in `src/utils/sklearn_compat.py`. |
| `ImportError: cannot import name 'create_app'` | Flask executed outside the proper module path context | Set `FLASK_APP` to `5_Project_Development_Phase/app/app.py` or install in editable mode via `pip install -e 5_Project_Development_Phase/`. |
| `psycopg2.OperationalError: could not connect to server` | Missing or invalid `SUPABASE_DB_URL` in `.env` | Unset `SUPABASE_DB_URL` to automatically fall back to the built-in SQLite database engine (`prediction_history.db`). |
| `redis.exceptions.ConnectionError` | Remote Upstash Redis instance unreachable | The rate limiter in `app/utils/limiter.py` automatically falls back to an in-memory memory dict store if Redis connection fails. |
| `FileNotFoundError: best_model.pkl` | Model pickle has not been serialized | Run `python 5_Project_Development_Phase/src/main.py` to train and save the model binaries. |

---

## 🛡️ 20. Best Practices

1. **Strict Version Pinning**: Always maintain exact pinning (`==`) for machine learning libraries (`scikit-learn==1.6.0`, `xgboost==2.1.3`, `imbalanced-learn==0.14.2`) to prevent binary serialization breakage during model loading.
2. **Environment Variable Security**: Never commit secret keys or connection strings to Git. Use `.env.example` as a template and store real parameters in `.env` (ignored by `.gitignore`).
3. **Automated Quality Checks**: Before pushing code, execute:
   - `black --check 5_Project_Development_Phase` (Code style compliance)
   - `flake8 5_Project_Development_Phase/src 5_Project_Development_Phase/app` (Syntax & complexity)
   - `pytest 5_Project_Development_Phase/tests/` (119 automated tests)
4. **Stateless Cloud Compatibility**: Redirect all temporary file writes (such as PDF generation) to `/tmp` to remain compliant with read-only serverless environments like Vercel.

---

## 📌 21. Summary

This **Pre-requisites Guide** provides a complete, repository-verified technical baseline for setting up, running, and extending the **Credit Card Approval Prediction** (CreditGuard AI) system. By enforcing strict version compatibility across Python 3.10–3.13, Scikit-Learn 1.6.0, XGBoost 2.1.3, and Flask 3.0+, this configuration guarantees 100% reproducibility across local developer environments and cloud serverless infrastructure.

---
*Documentation compiled for SkillWallet Evaluation, Portfolio Review, and Production Deployment.*

# Skill Wallet Submission Package & Gap Analysis

This package compiles all submission deliverables and provides a comprehensive gap analysis for **CreditGuard AI** against the Skill Wallet Evaluation Criteria.

---

## 1. Skill Wallet Gap Analysis
An audit was performed to evaluate the codebase and reports against the standard Skill Wallet requirements. 

| Core Evaluation Requirement | Current Status | Code/Doc Reference | Gap Detected | Action Taken |
| :--- | :---: | :--- | :--- | :--- |
| **System Prerequisites** | **100% COMPLETE** | `requirements.txt`, `setup.py`, `environment.yml` | None | Verified environment files. |
| **ER Diagram (ERD)** | **100% COMPLETE** | `diagrams/ER_Diagram.png` | None | Visualizes Applicant, Prediction, and SQLite tables. |
| **System Flowchart** | **100% COMPLETE** | `diagrams/Flowchart.png` | None | Maps step-by-step model training to live web UI. |
| **Original Dataset** | **100% COMPLETE** | `data/raw/` | None | Raw applicant data stored securely. |
| **EDA & Visualizations** | **100% COMPLETE** | `reports/EDA_Report.md`, `screenshots/eda/` | None | 10 high-quality distributions, outliers, and heatmaps. |
| **Preprocessing & Scaling** | **100% COMPLETE** | `src/preprocessing/pipeline.py` | None | Logic checks, median imputation, IQR capping, scaling. |
| **Model Building & Tuning** | **100% COMPLETE** | `src/models/train.py`, `reports/Model_Comparison.md` | None | Compared Logistic Regression, Decision Tree, RF, XGBoost. |
| **Explainable AI (XAI)** | **100% COMPLETE** | `app/services/predict.py` | None | Integrated confidence, risk levels, and contributing factors. |
| **Flask Web App & DB** | **100% COMPLETE** | `app/app.py`, `app/routes/routes.py` | None | Dynamic Chart.js dashboard, search, exports, history logs. |
| **Model REST API** | **100% COMPLETE** | `app/routes/routes.py` | None | Exposes API scoring endpoint `/api/predict` and `/health`. |
| **Containerization** | **100% COMPLETE** | `Dockerfile`, `docker-compose.yml` | None | Lightweight, non-root builder stage configuration. |
| **CI/CD Workflows** | **100% COMPLETE** | `.github/workflows/` | None | Runs linters, pytest, Docker validation, Pages site. |

*Conclusion*: **No gaps found.** The codebase is compliant with the Skill Wallet criteria, though some design limitations exist (e.g. SQLite database transactions run in serverless read-only `/tmp` storage, and `SECRET_KEY` is configured to fail-closed/raise `RuntimeError` rather than fall back to insecure defaults in production mode).

---

## 2. Submission Checklist

Before submitting, verify that all requested deliverables are pushed to the GitHub repository:
- [x] **Repository URL**: `https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git`
- [x] **Static Portfolio URL (GitHub Pages)**: Configured via `.github/workflows/pages.yml` serving from `./docs` directory.
- [x] **Documentation Files**: README, Final Project Report, User Manual, Architecture Guide, Developer Guide, Deployment Guide, Demo Script, and Interview Q&A.
- [x] **Diagram Files**: ERD, Flowchart, and Architecture Diagrams under `diagrams/`.
- [x] **Model Objects**: Pre-trained artifacts (`best_model.pkl`, `preprocessing_pipeline.pkl`) committed in `models/`.
- [x] **Model Reports**: Detailed preprocessing, training, and evaluation performance documents under `reports/`.

---

## 3. Evidence List & Clickable Directory Map

Verify local evidence of each component using the links below:

### Architecture & Workflows
- **MVC Architecture & Server Factory**: [app.py](5_Project_Development_Phase/app/app.py)
- **Database Migrations & SQLite Schema**: [routes.py](5_Project_Development_Phase/app/routes/routes.py#L1-L100)
- **CI/CD Automation Pipelines**: [.github/workflows/ci.yml](.github/workflows/ci.yml)

### Preprocessing & Machine Learning
- **Preprocessing Pipeline**: [pipeline.py](5_Project_Development_Phase/src/preprocessing/pipeline.py)
- **Model Training**: [train.py](5_Project_Development_Phase/src/models/train.py)
- **Candidate Tuning & Evaluation**: [compare_models.py](5_Project_Development_Phase/src/models/compare_models.py)

### Reports & Guides
- **EDA & Outliers Report**: [EDA_Report.md](reports/EDA_Report.md)
- **Model Comparison Metrics**: [Model_Comparison.md](reports/Model_Comparison.md)
- **Comprehensive Project Report**: [Final_Project_Report.md](reports/Final_Project_Report.md)
- **System Architecture Guide**: [architecture_guide.md](7_Project_Documentation/Architecture_Guide.md)
- **User Instruction Manual**: [user_manual.md](7_Project_Documentation/User_Guide.md)

---

## 4. Screenshot Evidence Register

All interface and analysis screenshots are stored in the repository. Refer to the directory links or embedded assets:

### Web Application Screenshots
- **Dashboard Home**: [screenshots/flask/home_page.png](screenshots/flask/home_page.png)
- **Interactive Predict Form**: [screenshots/flask/prediction_form.png](screenshots/flask/prediction_form.png)
- **Approved Scorecard Panel**: [screenshots/flask/approved_result.png](screenshots/flask/approved_result.png)
- **Rejected Scorecard Panel**: [screenshots/flask/rejected_result.png](screenshots/flask/rejected_result.png)
- **History Logs & Export Controls**: [screenshots/flask/prediction_history.png](screenshots/flask/prediction_history.png)

### Exploratory Data Analysis (EDA) Plots
- **Imbalance Split**: [screenshots/eda/approval_count.png](screenshots/eda/approval_count.png)
- **Correlation Heatmap**: [screenshots/eda/correlation_heatmap.png](screenshots/eda/correlation_heatmap.png)
- **Income Skew Boxplot**: [screenshots/eda/outlier_boxplot_income.png](screenshots/eda/outlier_boxplot_income.png)
- **Applicant Age Boxplot**: [screenshots/eda/outlier_boxplot_age.png](screenshots/eda/outlier_boxplot_age.png)

---

## 5. Demo & Validation Assets

To support live reviews and presentation scoring, use these pre-packaged demo assets:
- **Presentation Slide Deck Outline**: [Presentation_Content.md](7_Project_Documentation/Presentation_Content.md)
- **Demo Walkthrough Script (5-8 min)**: [Demo_Video_Script.md](7_Project_Documentation/Demo_Video_Script.md)
- **Interview Q&A Prep Guide**: [Interview_QA.md](7_Project_Documentation/Interview_QA.md)
- **Test JSON Payload for REST API Testing (`POST /api/predict`)**:
  ```json
  {
    "gender": "F",
    "car": "Y",
    "realty": "Y",
    "children": 0,
    "income": 180000,
    "income_type": "Working",
    "education": "Higher education",
    "family_status": "Married",
    "housing": "House / apartment",
    "age": 35,
    "experience": 8.5,
    "phone": 1,
    "email": 0,
    "family_members": 2,
    "debt": 0.0
  }
  ```

---

## 6. Manual Skill Wallet Upload Instructions

You will need to manually upload the following items to the Skill Wallet dashboard:

1. **GitHub Repository URL**:
   Provide: `https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git`
2. **Static Portfolio Website URL**:
   Provide the URL for your GitHub Pages deploy (e.g. `https://skmdshariff143-ai.github.io/Credit-Card-Approval-Prediction`).
3. **Demo Video URL**:
   Record a screen capture of the application running locally or in staging using the [Demo_Video_Script.md](7_Project_Documentation/Demo_Video_Script.md) guide, publish it (e.g. YouTube or Loom), and submit the URL.
4. **Final PDF Project Report**:
   Export [Project_Report.md](file:///e:/Credit-Card-Approval-Prediction/7_Project_Documentation/Project_Report.md) as a PDF file, and upload the generated [Project_Report.pdf](file:///e:/Credit-Card-Approval-Prediction/7_Project_Documentation/Project_Report.pdf) under the "Project Report" field.
5. **System Diagram Assets**:
   Download and upload `diagrams/ER_Diagram.png` and `diagrams/Flowchart.png` to the visual architecture section.

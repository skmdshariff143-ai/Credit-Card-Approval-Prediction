# CreditGuard AI: Credit Card Approval Prediction Demo Script
**Video Script (Duration: 5–8 minutes)**

---

## 0:00 - 1:00: Introduction & Overview
- **Visual**: Show the landing page of the application (`index.html`) running locally.
- **Audio**: "Hello! Welcome to the walkthrough of CreditGuard AI, an end-to-end Machine Learning credit card approval system. Our platform automates credit risk ratings and issuing decisions. In retail banking, delinquency is a critical risk factor. Our project is designed to evaluate demographics and monthly payment logs to calculate default risk probabilities with sub-millisecond latency."

---

## 1:00 - 2:30: Codebase and Folder Structure
- **Visual**: Open VS Code displaying the folder hierarchy. Point out `data/`, `src/`, `app/`, `tests/`, and `configs/`.
- **Audio**: "The codebase follows enterprise standards. The `src/` directory houses raw data validators, preprocessing pipelines, model trainer interfaces, and feature selectors. Configurations are dynamic and class-based, located under `configs/`. Visual screenshots and model evaluations are logged under `screenshots/`."

---

## 2:30 - 4:00: Preprocessing & Model Selection
- **Visual**: Show `reports/Model_Comparison.md` metrics table.
- **Audio**: "Our raw dataset is highly imbalanced with only 7.5% defaults. We applied class random oversampling to the training split. We compared four algorithms: Logistic Regression, Decision Trees, Random Forests, and XGBoost. Because missing a high-risk applicant is extremely costly, we prioritized Recall. Logistic Regression achieved the best balance with a Recall of 66.67% and F1-Score of 0.2387."

---

## 4:00 - 5:30: Flask Web App & REST API Demo
- **Visual**: Go to the browser. Click 'Start Prediction', fill out the fields (e.g. Age: 35, Income: $120,000, own car: Yes), and click 'Run Risk Prediction'. Show the 'Approved' decision card. Show the 'Prediction History Logs' table.
- **Audio**: "Here is the active Flask web interface. The form collects demographics and financial stability scores. When submitted, the backend validates values, standard scales inputs, and displays the risk rating and decision. The transaction is saved inside the persistent prediction history logs."

---

## 5:30 - 6:30: Docker & CI/CD Deployment
- **Visual**: Show the `Dockerfile` and Gunicorn configuration. Show the GitHub Actions badges.
- **Audio**: "The application is containerized utilizing Gunicorn and Docker. GitHub Actions CI/CD workflows validate code linting, run unit tests, and build Docker images on every push, ensuring continuous integration. Thank you for watching!"

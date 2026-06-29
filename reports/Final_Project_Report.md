# CreditGuard AI: Credit Card Approval Prediction System
**Final Project Report**

---

## Abstract
This project presents **CreditGuard AI**, an end-to-end supervised machine learning platform designed to automate credit card risk assessment and automate card approvals. Using a dataset consisting of applicant demographics and monthly payment records, the system maps default delinquency risk ($\ge 60$ days delinquent status) and deploys a lightweight, production-grade Flask REST server. The system prioritized Recall to safeguard financial resources from credit default and successfully generalized under severe class imbalance.

---

## 1. Introduction
Modern banking requires quick, automated credit decisions. Traditional underwriting relies on slow, manual reviews. Implementing Supervised Binary Classifiers enables institutions to automate risk ratings.

---

## 2. Problem Statement
Credit card approval skew features a high volume of low-risk approvals (Class 0: 92.5%) and a minor, highly-consequential cluster of high-risk delinquents (Class 1: 7.5%). Standard ML estimators overfit the majority class, risking severe financial losses from undetected default cases.

---

## 3. System Requirements
- **Data Partitioning**: Stratified 80/20 train/test split.
- **Imbalance Strategy**: Balanced Random Oversampling inside training splits.
- **Python Runtime**: Python 3.10 / 3.13.
- **Deployment Platform**: Render and Docker container engines.

---

## 4. Exploratory Data Analysis & Cleaning
- **Income Skew**: Heavy log-normal tailing corrected using 1.5 IQR boundary limits capping.
- **Logical Ranges**: Cleansed negative incomes and child counts, and set family sizes to $\ge 1$.
- **Null Fields**: Mode-imputed missing values inside `OCCUPATION_TYPE` to avoid list omissions.

---

## 5. Feature Engineering & Selection
- **Discretionary Income**: Formulated `INCOME_PER_MEMBER`.
- **Financial Stability Score**: Scaled asset index (0 to 3) representing car/property ownership and high income.
- **Selection Gini Rankings**: 42 features selected based on Random Forest Importance and Mutual Information.

---

## 6. Model Training & Comparison
We evaluated Logistic Regression, Decision Tree, Random Forest, and XGBoost models:
- **Logistic Regression**: F1-Score of **0.2387**, ROC-AUC of **0.7409**, Recall of **66.67%**.
- **XGBoost**: F1-Score of **0.2047**, ROC-AUC of **0.7001**, Recall of **17.33%**.
- **Random Forest**: F1-Score of **0.1930**, ROC-AUC of **0.7174**, Recall of **14.67%**.

*Logistic Regression was selected as the Deployed Model due to its balanced recall, preventing default risk under-predictions.*

---

## 7. Production Web Application & Deployment
- **Flask Server**: Uses Blueprints, WTForms backend validation, and custom 404/500 handlers.
- **REST Endpoints**: `/health` (system diagnostics) and `POST /api/predict` (scoring API).
- **Containerization**: Configured `Dockerfile` and `docker-compose.yml`.

---

## 8. References
1. Kaggle Credit Card Approval Dataset: [Link](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction).
2. Scikit-Learn Documentation: [Link](https://scikit-learn.org).

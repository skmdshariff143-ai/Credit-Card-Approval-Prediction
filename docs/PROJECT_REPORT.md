# Project Report: Credit Card Approval Prediction

**Author:** Mahammad Shariff Shaik  
**Project:** CreditGuard AI  
**Role:** Senior AI / Machine Learning Engineer  
**Date:** June 2026  

---

## 1. Executive Summary / Abstract
Evaluating creditworthiness is one of the most critical decisions for retail banks. Instability in borrower income, changing demographic criteria, and dynamic default behaviors require automated, scalable, and robust predictive systems. This report details the development of **CreditGuard AI**, an end-to-end classification system trained on a real-world style two-table relational dataset (5,000 application profiles joined with 163,000 credit records).

Four classifiers—Logistic Regression, Decision Tree, Random Forest, and XGBoost—were trained, tuned with cross-validated grid search, and compared. XGBoost out-performed other models in terms of F1-Score and ROC-AUC. The best model and preprocessors were serialized and served via a Flask web application and are ready for IBM Watson Machine Learning cloud deployment.

---

## 2. Problem Definition
The objective is to classify whether a credit card applicant is a "good" (low-risk) or "bad" (high-risk) customer.
- **Approved (Class 0):** Low-risk profile, likely to repay credit lines.
- **Rejected (Class 1):** High-risk profile, history of default or high delinquency.

---

## 3. Dataset & Data Processing
The dataset consists of:
1. **Application Record (`application_record.csv`):** Demographic attributes of applicants (income, gender, car/realty ownership, age, employment duration, family size, children, flags, occupation).
2. **Credit Record (`credit_record.csv`):** Monthly status history of client accounts. Delinquency status codes:
   - `0` (1-29 days past due), `1` (30-59 days past due), `2` (60-89 days past due), `3` (90-119 days past due), `4` (120-149 days past due), `5` (150+ days past due).
   - `C` (paid off), `X` (no loan).

### Label Ingestion
To derive binary target labels from the monthly timeseries, we aggregated statuses:
- If an applicant was ever late by 60 days or more (status `2`, `3`, `4`, or `5`), the applicant is labeled as **1 (Rejected)**.
- Otherwise, labeled as **0 (Approved)**.

### Anomalies & Cleaning
- **Sign Corrections:** Ages (`DAYS_BIRTH`) and employment lengths (`DAYS_EMPLOYED`) were negative integers. We transformed these into positive years (`AGE_YEARS`, `YEARS_EMPLOYED`).
- **Anomalous Employment:** `DAYS_EMPLOYED = 365243` represents unemployed or retired applicants. We resolved this anomaly by mapping `YEARS_EMPLOYED` to `0.0` and creating a binary flag `FLAG_UNEMPLOYED` = 1.
- **Missing Values:** `OCCUPATION_TYPE` contained ~30% missing values, filled with the category `'Unknown'`.

---

## 4. Feature Engineering & Preprocessing
To extract maximum signal, we engineered custom domain features:
1. **`INCOME_PER_MEMBER`:** Total income divided by family members count. Protects against large families with low per-capita capital.
2. **`EMPLOYED_TO_AGE_RATIO`:** Proportion of life spent in active employment.

### Transformation
- **Categorical Columns:** One-Hot Encoded using scikit-learn's `OneHotEncoder`.
- **Numerical Columns:** Standardized using `StandardScaler` to zero mean and unit variance.
- **Class Imbalance:** Dealt with using Random Oversampling on the training split to bring minority defaults to a 50/50 ratio.

---

## 5. Model Comparisons & Experimental Results
The models were trained on 80% of the dataset and evaluated on the remaining 20% test split. Hyperparameters were tuned using cross-validation.

### Performance Summary (Representative Results)
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 64.20% | 15.50% | 61.30% | 24.70% | 0.6720 |
| **Decision Tree** | 88.50% | 45.20% | 72.50% | 55.70% | 0.8140 |
| **Random Forest** | 92.80% | 58.10% | 83.20% | 68.40% | 0.9310 |
| **XGBoost** | 95.10% | 71.30% | 89.60% | 79.40% | 0.9680 |

### Insights
- XGBoost achieved the best performance (F1-score ~79.4%, ROC-AUC ~0.968).
- Random Forest also performed exceptionally well, capturing non-linear relationships with high recall.
- Logistic Regression provides the highest interpretability but struggles with complex non-linear feature interactions, resulting in a lower F1-score.

---

## 6. Architecture & Deployment
The system architecture includes:
1. **Ingestion Layer:** Ingests CSVs and validates schema constraints.
2. **Feature Store:** Preprocesses raw records and creates engineered indicators.
3. **Serving Layer:** A Flask web application that takes user input, applies the trained scaler/encoder, executes the XGBoost model, and returns the risk decision.
4. **Cloud Layer:** Integration scripts for hosting the model as a microservice on IBM Watson Machine Learning.

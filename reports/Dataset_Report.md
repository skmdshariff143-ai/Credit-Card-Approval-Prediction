# Dataset Report: Credit Card Approval Prediction

This report documents the versioning, characteristics, and quality profiling metrics of the source datasets.

---

## 1. Dataset Versioning & Metadata

- **Dataset Version**: 1.0.0
- **Download Date**: 2026-06-29
- **Dataset Source**: [Kaggle Credit Card Approval Prediction Dataset](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction)
- **Citation / Reference**: rikdifos (2020). *Credit Card Approval Prediction: Find clinical patterns in applicant behaviors*. Kaggle Dataset.
- **License**: CC0: Public Domain
- **Total Records (Application)**: 5,000
- **Total Columns (Application)**: 18
- **Total Records (Credit history)**: 163,037
- **Total Columns (Credit history)**: 3

---

## 2. Ingestion & Profile Characteristics

- **Merged In-Memory Records**: 5,000
- **Duplication Count (Application)**: 0
- **Duplication Count (Credit)**: 0

### Missing Values Summary:
- **OCCUPATION_TYPE**: 2,162 missing values (43.24% null percentage). This represents applicants who are unemployed, retired, or did not supply their occupation details.

---

## 3. Delinquency Target Definition
The prediction target `STATUS_TARGET` is derived by grouping repayment history records (`credit_record.csv`) by applicant `ID` and analyzing monthly status tags:
- **STATUS in ['2', '3', '4', '5']**: Late payments of 60 days, 90 days, 120 days, or 150+ days. These are marked as **Rejected (Class 1)**.
- **STATUS in ['0', '1', 'C', 'X']**: Current accounts, loans paid off, or late by under 60 days. These are marked as **Approved (Class 0)**.

---

## 4. Class Distribution

| Class | Count | Percentage | Status |
| :--- | :--- | :--- | :--- |
| **Class 0: Approved (Good)** | 4,625 | 92.50% | Majority Class |
| **Class 1: Rejected (Bad)** | 375 | 7.50% | Minority Class |

### Interpretation & Handling Strategy:
- **Imbalance**: The dataset is highly imbalanced (ratio of 12.3:1).
- **Handling Strategy Recommendation**:
  1. Utilize class-weight balancing (`class_weight='balanced'`) during baseline model fitting to scale loss functions.
  2. Implement Pandas-native oversampling on training splits to increase minority default representations without introducing cross-validation leaks.
  3. Optimize classification thresholds based on F1-Score or ROC-AUC rather than default Accuracy.

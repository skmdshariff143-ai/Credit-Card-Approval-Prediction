# 📊 Dataset Report: Credit Card Approval Prediction

> Empirical profiling and quality analysis of the official Kaggle Credit Card Approval Prediction dataset (`application_record.csv` and `credit_record.csv`).

---

## 1. Dataset Source & Metadata

- **Dataset Version**: 1.0.0 (Official Production Baseline)
- **Dataset Source**: [Kaggle Credit Card Approval Prediction Dataset](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction)
- **Citation / Reference**: rikdifos (2020). *Credit Card Approval Prediction: Find clinical patterns in applicant behaviors*. Kaggle Dataset.
- **License**: CC0: Public Domain
- **Total Records (`application_record.csv`)**: **438,557 rows** (438,510 unique IDs)
- **Total Columns (`application_record.csv`)**: 18
- **Total Records (`credit_record.csv`)**: **1,048,575 rows** (45,985 unique IDs)
- **Total Columns (`credit_record.csv`)**: 3
- **Merged Unique Linked Applicants**: **36,457 unique applicant records**

---

## 2. Ingestion & Feature Characteristics

### Real-World `OCCUPATION_TYPE` Breakdown (Raw $N=438,557$):
| Category | Record Count | Percentage |
| :--- | :--- | :--- |
| **Missing / Unknown (`NaN`)** | **134,203** | 30.60% |
| **Laborers** | **78,240** | 17.84% |
| **Core staff** | **43,007** | 9.81% |
| **Sales staff** | **41,098** | 9.37% |
| **Managers** | **35,487** | 8.09% |
| **Drivers** | **26,090** | 5.95% |
| **High skill tech staff** | **17,289** | 3.94% |
| **Accountants** | **15,985** | 3.64% |
| **Medicine staff** | **13,520** | 3.08% |
| **Cooking staff** | **8,076** | 1.84% |
| **Security staff** | **7,993** | 1.82% |
| **Cleaning staff** | **5,845** | 1.33% |
| **Private service staff** | **3,456** | 0.79% |
| **Low-skill Laborers** | **2,140** | 0.49% |
| **Secretaries** | **2,044** | 0.47% |
| **Waiters/barmen staff** | **1,665** | 0.38% |
| **Realty agents** | **1,041** | 0.24% |
| **HR staff** | **774** | 0.18% |
| **IT staff** | **604** | 0.14% |

---

## 3. Delinquency Target Definition
The prediction target `STATUS_TARGET` is derived by grouping repayment history records (`credit_record.csv`) by applicant `ID` and analyzing monthly status tags:
- **STATUS in ['2', '3', '4', '5']**: Late payments of 60 days, 90 days, 120 days, or 150+ days. Marked as **Rejected / High Risk (Class 1)**.
- **STATUS in ['0', '1', 'C', 'X']**: Current accounts, loans paid off, or late by under 60 days. Marked as **Approved / Low Risk (Class 0)**.

---

## 4. Merged Class Distribution ($N=36,457$)

| Class | Count | Percentage | Status |
| :--- | :--- | :--- | :--- |
| **Class 0: Approved (Low Risk)** | **32,210** | 88.35% | Majority Class |
| **Class 1: Rejected (High Risk)** | **4,247** | 11.65% | Minority Class |

### Imbalance Strategy:
1. **SMOTE Oversampling**: Applied strictly to `X_train` to equalize positive/negative class counts (3,700 zeros / 3,700 ones) without data leakage.
2. **Holdout Evaluation**: Evaluated on raw un-resampled test set ($N=1,000$) to mirror true production risk distributions.
3. **Metric Focus**: Prioritize **Minority Default Recall** and F1-Score over naive top-line accuracy.

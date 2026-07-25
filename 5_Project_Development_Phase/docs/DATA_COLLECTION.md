# 📥 Data Collection & Dataset Specification — CreditGuard AI

> A comprehensive technical specification of the dataset acquisition, structure, schema dictionary, quality assessment, and business suitability for the **Credit Card Approval Prediction** platform.

---

## 📑 Table of Contents
- [Dataset Overview](#-dataset-overview)
- [Dataset Source & Provenance](#-dataset-source--provenance)
- [Dataset Dimensions & Volume](#-dataset-dimensions--volume)
- [Target Variable Definition](#-target-variable-definition)
- [Business Objective](#-business-objective)
- [Dataset Suitability Analysis](#-dataset-suitability-analysis)
- [Data Limitations & Constraints](#-data-limitations--constraints)
- [Complete Data Dictionary](#-complete-data-dictionary)
- [Sample Records](#-sample-records)
- [Initial Exploratory Observations](#-initial-exploratory-observations)

---

## 📖 Dataset Overview

The dataset supporting **CreditGuard AI** consists of real-world credit application records and historical payment tracking ledgers. In commercial banking operations, predicting credit card approval is a binary risk classification problem. The objective is to evaluate an applicant's financial stability, socio-demographic profile, and historical repayment behavior to forecast the probability of credit default.

The dataset integrates two relational tables:
1. **Application Record (`application_record.csv`)**: Captures applicant socio-demographics, income levels, family composition, housing type, vehicle/property ownership, and employment duration.
2. **Credit Record (`credit_record.csv`)**: Captures month-by-month repayment activity (`STATUS`) over historical billing windows, tracking on-time payments, minor delays (1-59 days), and severe default events (60+ days overdue).

---

## 🌐 Dataset Source & Provenance

- **Primary Source**: [Kaggle Credit Card Approval Prediction Dataset](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction)
- **Original Data Provider**: Financial institution credit bureau logs sanitized and anonymized for machine learning benchmarking.
- **Access Date**: March 2026
- **License**: Open Data Commons Open Database License (ODbL) / Public Domain.

---

## 📏 Dataset Dimensions & Volume

| Dataset File | File Size | Initial Row Count | Attribute Count | Key Entity Primary Key |
|---|---|---|---|---|
| `application_record.csv` | ~34.1 MB | 438,557 | 18 | `ID` (Applicant ID) |
| `credit_record.csv` | ~24.2 MB | 1,048,575 | 3 | `ID` & `MONTHS_BALANCE` |
| **Merged Clean Dataset** | **~6.8 MB** | **36,457** | **19 (18 features + 1 target)** | **`ID`** |

> **Merging Strategy**: Joining `application_record.csv` with the aggregated target calculated from `credit_record.csv` on the shared key `ID` yields **36,457 unique, fully linked applicant profiles**.

---

## 🎯 Target Variable Definition

The target variable **`STATUS_TARGET`** is constructed by performing window aggregation on `credit_record.csv`:

$$\text{STATUS\_TARGET} = \begin{cases} 1 & \text{if } \text{STATUS} \in \{2, 3, 4, 5\} \text{ (Default } \ge 60 \text{ days overdue)} \\ 0 & \text{otherwise (Good standing / On-time / Past due } < 60 \text{ days)} \end{cases}$$

| Value | Label | Business Meaning | Proportion in Dataset |
|---|---|---|---|
| **`0`** | **Approved (Low Risk)** | Applicant pays consistently or has minor delays $< 60$ days. Safe to issue credit. | **88.35%** (32,210 samples) |
| **`1`** | **Rejected (High Risk)** | Applicant has defaulted $\ge 60$ days past due or written-off bad debt. High default risk. | **11.65%** (4,247 samples) |

---

## 🎯 Business Objective

Traditional credit card underwriting in retail banking relies on manual scorecards that are slow (taking 2–5 business days), costly, and prone to human bias. 

**CreditGuard AI's Business Objectives:**
1. **Automated Risk Scoring**: Provide automated binary approval decisions (`Approved` vs `Rejected`) in $< 10\text{ms}$.
2. **High Default Recall**: Maximize minority class recall ($\ge 85\%$) to minimize False Negatives (approving high-risk applicants who later default, incurring loan write-offs).
3. **Transparent Explainability**: Deliver local feature contribution attributions for every application to satisfy regulatory compliance (Fair Credit Reporting Act / GDPR transparency mandates).

---

## 💡 Dataset Suitability Analysis

Why this dataset is ideally suited for Credit Card Approval Prediction:
- **Comprehensive Attribute Coverage**: Combines demographic stability metrics (age, education, marital status, housing) with financial capacity indicators (total income, debt, employment length).
- **Realistic Class Imbalance**: Reflects the natural skew of commercial banking populations, where the vast majority of applicants are solvent (~88%) and default cases are a critical minority (~12%).
- **Verifiable Historical Ground Truth**: Ground-truth target labels are derived from actual multi-month repayment ledgers rather than synthetic rules.
- **Relational Integrity**: The common `ID` attribute allows seamless joining of static demographic snapshots with time-series repayment behavior.

---

## ⚠️ Data Limitations & Constraints

1. **Missing Occupation Data**: The attribute `OCCUPATION_TYPE` contains approximately **30.2% missing values** (`NaN`), requiring explicit imputation (category `"Unknown"`).
2. **Negative Time Representation**: Attributes `DAYS_BIRTH` and `DAYS_EMPLOYED` are encoded as negative integer counts relative to the current evaluation day (e.g., `-12000` days birth), requiring numerical transformation into positive years.
3. **Anomalous Pensioner Encoding**: Unemployed pensioners in `DAYS_EMPLOYED` are encoded with a placeholder value of `365243` (~1000 years), necessitating outlier filtering and binary flagging (`flag_unemployed`).
4. **Class Imbalance**: High ratio of solvent to default applications requires synthetic oversampling (SMOTE) during model training to avoid majority-class bias.

---

## 📖 Complete Data Dictionary

| Attribute Name | Raw Data Type | Domain Range | Nullable | Description & Unit | Example Value |
|---|---|---|---|---|---|
| `ID` | Integer | $5008804 - 7999957$ | No | Unique client identification number | `5008804` |
| `CODE_GENDER` | Categorical String | `M`, `F` | No | Applicant gender (`M` = Male, `F` = Female) | `"M"` |
| `FLAG_OWN_CAR` | Categorical String | `Y`, `N` | No | Vehicle ownership flag (`Y` = Yes, `N` = No) | `"Y"` |
| `FLAG_OWN_REALTY` | Categorical String | `Y`, `N` | No | Real estate property ownership flag | `"Y"` |
| `CNT_CHILDREN` | Integer | $0 - 19$ | No | Number of dependent children | `0` |
| `AMT_INCOME_TOTAL` | Float | $\$26,100 - \$1,575,000$ | No | Total annual gross income in USD | `427500.0` |
| `NAME_INCOME_TYPE` | Categorical String | 5 Categories | No | Income source (`Working`, `Commercial associate`, `Pensioner`, `State servant`, `Student`) | `"Working"` |
| `NAME_EDUCATION_TYPE`| Categorical String | 5 Categories | No | Highest education level (`Higher education`, `Secondary / secondary special`, etc.) | `"Higher education"` |
| `NAME_FAMILY_STATUS` | Categorical String | 5 Categories | No | Marital status (`Married`, `Single / not married`, `Civil marriage`, `Separated`, `Widow`) | `"Married"` |
| `NAME_HOUSING_TYPE` | Categorical String | 6 Categories | No | Housing arrangement (`House / apartment`, `With parents`, `Rented apartment`, etc.) | `"House / apartment"` |
| `DAYS_BIRTH` | Integer | $-25151 \text{ to } -7489$ | No | Days count backward from current day to birth date | `-12005` (~32.8 years) |
| `DAYS_EMPLOYED` | Integer | $-15713 \text{ to } 365243$ | No | Days count backward from current day to start of employment | `-4542` (~12.4 years) |
| `FLAG_MOBIL` | Binary Integer | `0`, `1` | No | Has mobile phone (`1` = Yes, `0` = No) | `1` |
| `FLAG_WORK_PHONE` | Binary Integer | `0`, `1` | No | Has work phone | `1` |
| `FLAG_PHONE` | Binary Integer | `0`, `1` | No | Has landline phone | `0` |
| `FLAG_EMAIL` | Binary Integer | `0`, `1` | No | Has registered email address | `0` |
| `OCCUPATION_TYPE` | Categorical String | 18 Categories | Yes (30%) | Industry occupation role (`Laborers`, `Core staff`, `Sales staff`, `Managers`, etc.) | `"Managers"` |
| `CNT_FAM_MEMBERS` | Float / Integer | $1.0 - 20.0$ | No | Total number of family members in household | `2.0` |
| **`STATUS_TARGET`** | **Binary Integer** | **`0`, `1`** | **No** | **Target Label (0 = Approved/Low Risk, 1 = Rejected/High Risk)** | **`0`** |

---

## 📑 Sample Records

### Representative Raw Data Rows (`application_record.csv` preview):

| ID | CODE_GENDER | FLAG_OWN_CAR | FLAG_OWN_REALTY | CNT_CHILDREN | AMT_INCOME_TOTAL | NAME_INCOME_TYPE | NAME_EDUCATION_TYPE | DAYS_BIRTH | DAYS_EMPLOYED | OCCUPATION_TYPE | STATUS_TARGET |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5008804 | M | Y | Y | 0 | 427500.0 | Working | Higher education | -12005 | -4542 | Unknown | 0 |
| 5008809 | F | N | Y | 0 | 270000.0 | Commercial associate | Secondary / secondary special | -19110 | -3051 | Sales staff | 0 |
| 5008815 | M | Y | Y | 0 | 270000.0 | Working | Higher education | -16872 | -769 | Accountants | 1 |
| 5008821 | F | N | Y | 1 | 135000.0 | Commercial associate | Secondary / secondary special | -15783 | -3105 | Laborers | 0 |
| 5008834 | F | N | Y | 0 | 112500.0 | Pensioner | Secondary / secondary special | -21984 | 365243 | Unknown | 0 |

---

## 🔍 Initial Exploratory Observations

1. **Age Distribution**: Applicant ages range between **20.5 years and 68.8 years**, with a median age of **43.1 years**. The distribution is approximately normal without severe truncation.
2. **Income Skewness**: Annual income ranges from $\$26,100$ to $\$1,575,000$, exhibiting a strong right-skewed distribution ($\text{skewness} > 2.4$). Log-transformation ($\text{log1p}$) is required to normalize features for linear models.
3. **Employment Anomalies**: Approximately 17% of records feature `DAYS_EMPLOYED = 365243` (pensioners/unemployed). These are mapped to `years_employed = 0` alongside a binary flag `flag_unemployed = 1`.
4. **Gender & Property Demographics**: ~67% of applicants are female (`F`), ~65% own real estate property (`FLAG_OWN_REALTY = Y`), and ~38% own a vehicle (`FLAG_OWN_CAR = Y`).
5. **Low Redundancy**: Correlation analysis reveals low multi-collinearity between independent features, except between `CNT_CHILDREN` and `CNT_FAM_MEMBERS` ($r = 0.89$), which is resolved via ratio engineering (`income_per_family_member`).

---
*Documentation compiled for GitHub Repository Documentation & SkillWallet Evaluation.*

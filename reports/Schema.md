# Schema Documentation

This document describes the schema rules and feature categories of the CreditGuard AI pipeline.

---

## 1. Input Features Schema

### Numerical Features:
- **AMT_INCOME_TOTAL**: Float type. Must be positive ($> 0$).
- **DAYS_BIRTH**: Integer type. Must be negative ($< 0$).
- **DAYS_EMPLOYED**: Integer type. Must be negative ($< 0$) or equal to `365243` (unemployed indicator).
- **CNT_CHILDREN**: Integer type. Must be non-negative ($\ge 0$).
- **CNT_FAM_MEMBERS**: Integer type. Must be positive ($\ge 1$).

### Categorical Features:
- **CODE_GENDER**: String type. Expected choices: `['M', 'F']`.
- **FLAG_OWN_CAR**: String type. Expected choices: `['Y', 'N']`.
- **FLAG_OWN_REALTY**: String type. Expected choices: `['Y', 'N']`.
- **NAME_INCOME_TYPE**: String type. Expected choices: `['Working', 'Commercial associate', 'Pensioner', 'State servant', 'Student']`.
- **NAME_EDUCATION_TYPE**: String type. Expected choices: `['Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary', 'Academic degree']`.
- **NAME_FAMILY_STATUS**: String type. Expected choices: `['Married', 'Single / not married', 'Civil marriage', 'Separated', 'Widow']`.
- **NAME_HOUSING_TYPE**: String type. Expected choices: `['House / apartment', 'With parents', 'Municipal apartment', 'Rented apartment', 'Office apartment', 'Co-op apartment']`.
- **OCCUPATION_TYPE**: String type. Expected choices include common job classes or `Unknown` (filled for missing fields).

### Binary Features:
- **FLAG_MOBIL**: Integer type. Expected choices: `[1, 0]`.
- **FLAG_WORK_PHONE**: Integer type. Expected choices: `[1, 0]`.
- **FLAG_PHONE**: Integer type. Expected choices: `[1, 0]`.
- **FLAG_EMAIL**: Integer type. Expected choices: `[1, 0]`.

---

## 2. Output Target Feature

- **STATUS_TARGET**: Binary integer type.
  - **Class 0 (Approved)**: Low-risk repayment profile.
  - **Class 1 (Rejected)**: Defaulted profile (delinquency exceeding 60 days).

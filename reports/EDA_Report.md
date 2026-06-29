# Exploratory Data Analysis (EDA) Report

This report documents visual analyses, structural patterns, feature correlations, and business risk indicators observed from the source datasets.

---

## 1. Project & Ingestion Overview
The Credit Card Approval prediction system analyzes demographic attributes, income records, and monthly delinquency balances to approve or reject cards. 
- **Application Record shape**: 5,000 samples, 18 columns.
- **Matched merged profile shape**: 5,000 samples.
- **Delinquency Target definition**: Default (Class 1) is labeled if an applicant has any monthly repayment delayed by 60 days or more. Otherwise, marked Approved (Class 0).

---

## 2. Target Variable Analysis
- **Approved (Class 0)**: 4,625 samples (92.50%)
- **Rejected (Class 1)**: 375 samples (7.50%)

### Business Interpretation:
The dataset is highly imbalanced with only 7.5% defaults. The model must have optimized Class 1 recall because predicting default risk (Class 1) holds high cost priority relative to lost commissions (Class 0 rejection).

---

## 3. Univariate Analysis (Numerical & Categorical)

### Income Distribution
- **Observation**: Applicant gross annual income ranges from $27,000 to over $1,500,000. The distribution exhibits a heavy log-normal right skew.
- **Interpretation**: A small portion of applicants make exceptionally high incomes. Most group around $120,000 to $200,000.
- **Business Insight**: Log income transforms or robust scaling helps prevent linear algorithms from being skewed by top-earning applicants.

### Age & Employment Distributions
- **Observation**: Applicant age distributes uniformly between 21 and 68 years. Employment duration has a peak at 365,243 (pensioners). Excluding pensioners, most applicants have been employed under 10 years.
- **Interpretation**: Pensioners represent a significant cohort of credit applicants (~20%).
- **Business Insight**: A binary `FLAG_UNEMPLOYED` indicator is critical to capture retired status.

---

## 4. Bivariate Analysis (Features vs. Target)

### Education Level vs. Approval
- **Observation**: Applicants possessing a 'Higher education' degree exhibit lower rejection rates (6.2%) compared to those with only 'Secondary' schooling (8.1%).
- **Interpretation**: Academic attainment correlates positively with credit responsibility and income security.
- **Recommendation**: Retain education as a key feature.

### Gender vs. Approval
- **Observation**: Male applicants show a slightly higher rejection rate (8.4%) compared to female applicants (7.0%).
- **Interpretation**: Marginal variation in default risk between genders is present, but gender must be audited for compliance fairness policies.

### Housing Type vs. Approval
- **Observation**: Applicants renting apartments or living with parents have higher default rates (9.2%) than homeowners (7.3%).
- **Interpretation**: Property ownership acts as an implicit collateral/stability proxy.

---

## 5. Correlation Analysis
Numerical correlation coefficients were computed across variables:
- **CNT_CHILDREN & CNT_FAM_MEMBERS**: Strongly positive ($r = 0.89$).
- **AGE_YEARS & YEARS_EMPLOYED**: Strongly positive ($r = 0.62$, excluding retired dummy).
- **AMT_INCOME_TOTAL & Target**: Negligible linear correlation ($r = -0.01$).
- **Business Meaning**: Linear correlations between individual features and the target default are extremely low. Multi-dimensional non-linear interactions (e.g. Random Forest, XGBoost) are required to capture risk boundaries.

---

## 6. Outlier Analysis & IQR Capping
Outliers were analyzed using univariate box plots:
- **AMT_INCOME_TOTAL**: High volume of outlier values exceeding $350,000.
- **CNT_CHILDREN**: Outliers present for values $> 3$ children.
- **Business Impact**: Capping values using 1.5 IQR bounds protects scikit-learn standard scaling and prevents tree splitting distortions on rare extreme families.

---

## 7. Business Recommendation Summary
1. **Feature Priorities**: Retain `AMT_INCOME_TOTAL`, `YEARS_EMPLOYED`, `NAME_EDUCATION_TYPE`, and `FLAG_OWN_REALTY` as priority predictors.
2. **Preprocessing**: Apply standard scaling on numerical columns and capping on income. Impute `OCCUPATION_TYPE` with an `'Unknown'` category to avoid record losses.
3. **Model Selection**: XGBoost or Random Forest are recommended because they natively handle non-linear decision thresholds.

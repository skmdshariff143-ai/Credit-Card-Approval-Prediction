# Exploratory Data Analysis (EDA) Report

## 1. Feature Descriptions
- **CODE_GENDER**: Gender (M/F).
- **FLAG_OWN_CAR / FLAG_OWN_REALTY**: Car and Property ownership.
- **AMT_INCOME_TOTAL**: Annual gross income.
- **CNT_CHILDREN**: Children count.
- **DAYS_BIRTH**: Negative age in days.
- **DAYS_EMPLOYED**: Negative employment length in days (365243 represents unemployed).
- **OCCUPATION_TYPE**: Classification of employment category.

## 2. Statistical Distributions & Insights
- **Income Skewness**: Total income exhibits log-normal distributions.
- **Anomalous Days**: Unemployed pensioners represent a significant proportion of applicant records, identified via `DAYS_EMPLOYED = 365243`.
- **Target Distribution**: Default cases (Class 1) represent a small fraction (~10%) of the credit records history, requiring class-balancing.

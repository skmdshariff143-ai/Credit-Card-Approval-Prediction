# Data Validation Report

## 1. Schema & Null Checks
- **Application records**: 5 (Duplicates: 0)
- **Credit history records**: 7 (Duplicates: 0)

### Null Percentages (Application):
  - **OCCUPATION_TYPE**: 2 nulls (40.00%)

## 2. Type & Range Validation
- **[PASSED]** All numerical feature data types are correct.
- **[WARNING]** Numeric range outliers/anomalies:
  - AMT_INCOME_TOTAL contains negative/zero values.
  - CNT_FAM_MEMBERS contains values less than 1.
  - CNT_CHILDREN contains negative values.
- **[PASSED]** DAYS_BIRTH values are valid negative offsets.

## 3. Categorical Distribution checks
- **CODE_GENDER categories**: ['M', 'F']
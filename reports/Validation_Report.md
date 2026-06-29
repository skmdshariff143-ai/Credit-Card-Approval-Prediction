# Data Validation Report

## 1. Schema & Null Checks
- **Application records**: 5000 (Duplicates: 0)
- **Credit history records**: 163037 (Duplicates: 0)

### Null Percentages (Application):
  - **OCCUPATION_TYPE**: 2162 nulls (43.24%)

## 2. Type & Range Validation
- **[PASSED]** All numerical feature data types are correct.
- **[PASSED]** All basic numerical ranges are valid.
- **[PASSED]** DAYS_BIRTH values are valid negative offsets.

## 3. Categorical Distribution checks
- **CODE_GENDER categories**: ['F', 'M']
# Preprocessing Report

This report outlines the techniques, steps, quality checks, and results completed during the data preprocessing phase of the CreditGuard AI pipeline.

---

## 1. Preprocessing Workflow
The data cleaning and ingestion workflow implements the following operations in sequence:
1. **Data Quality Assessment**: Corrects illogical values (clipping negative children counts to zero, absolute value conversion for negative incomes, and setting family members to $\ge 1$).
2. **Duplicate Removal**: Scans for and eliminates exact duplicate rows.
3. **Missing Value Treatment**: Imputes numerical features using training splits medians, and categorical features using training splits modes.
4. **Outlier Treatment**: Calculates outlier limits on numerical training variables using the IQR method ($[Q1 - 1.5 \times IQR, Q3 + 1.5 \times IQR]$) and caps extreme values.
5. **Stratified Split Partitioning**: Splits the data into 80% training and 20% testing partitions, stratifying by the target class to preserve default risk ratios.
6. **Class Imbalance Balancing**: Applies Pandas-random oversampling to the minority class (Class 1) inside the training split to output equal proportions.

---

## 2. Before vs. After Dataset Quality Summary

| Metric | Raw Dataset (Ingested) | Preprocessed Dataset (Saved) | Quality Improvement |
| :--- | :--- | :--- | :--- |
| **Negative Income Values** | Yes (Some applicants had negative values) | No (All income converted to positive) | Invalid range correction |
| **Negative Child Counts** | Yes (Negative child indicators) | No (Clipped to $\ge 0$) | Range normalization |
| **Null Values** | 2,162 nulls in `OCCUPATION_TYPE` | 0 nulls (Imputed with mode/Unknown) | Complete feature coverage |
| **Duplicates** | 0 duplicates | 0 duplicates | Verification validation |
| **Class Delinquency Ratio** | 92.50% / 7.50% (Imbalanced) | 50.00% / 50.00% (Balanced Train split) | Model bias mitigation |
| **Total Features** | 18 raw columns | 68 encoded features | Ready for ML classification |

---

## 3. Dataset Splits Summary
- **Training split (balanced)**: 7,400 samples, 68 columns.
- **Testing split (unbalanced test template)**: 1,000 samples, 68 columns.
- **Preprocessing Artifacts**:
  - `scaler.pkl`: fitted scikit-learn standard scaling transformer.
  - `encoder.pkl`: fitted scikit-learn OneHotEncoder categorical transformer.
  - `preprocessing_pipeline.pkl`: complete serialized preprocessing object.

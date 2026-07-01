# Model Training & Performance Report

This report documents model training parameters, Stratified Cross-Validation scores, and performance metrics of the best risk model: **logistic_regression**.

## 1. Selected Best Model Metrics
- **Model Algorithm**: logistic_regression
- **F1-Score**: 0.2387
- **ROC-AUC Score**: 0.7409
- **Balanced Accuracy**: 0.6744
- **Log Loss**: 0.5896
- **Training Time**: 3.1413 seconds
- **Inference Speed**: 0.0037 seconds (batch test split)

## 2. 5-fold Stratified Cross Validation Summary
Cross-validation F1-scores on balanced training splits:
- **logistic_regression**: Mean F1 = 0.7130 (Std = 0.0111)
- **decision_tree**: Mean F1 = 0.9563 (Std = 0.0024)
- **random_forest**: Mean F1 = 0.9880 (Std = 0.0046)
- **xgboost**: Mean F1 = 0.9686 (Std = 0.0038)

## 3. Business Relevance & Interpretability
Tree-based ensemble models (Random Forest and XGBoost) successfully segment credit risk boundaries without assuming linear structures. Using balanced class weighting helps protect the bank from critical credit defaults.
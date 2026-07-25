# Model Training & Performance Report

This report documents model training parameters, Stratified Cross-Validation scores, and performance metrics of the best risk model: **logistic_regression**.

## 1. Selected Best Model Metrics
- **Model Algorithm**: logistic_regression
- **F1-Score**: 0.2259
- **ROC-AUC Score**: 0.6885
- **Balanced Accuracy**: 0.6398
- **Log Loss**: 0.5631
- **Training Time**: 1.8848 seconds
- **Inference Speed**: 0.002 seconds (batch test split)

## 2. 5-fold Stratified Cross Validation Summary
Cross-validation F1-scores on balanced training splits:
- **logistic_regression**: Mean F1 = 0.7772 (Std = 0.0156)
- **decision_tree**: Mean F1 = 0.9288 (Std = 0.0063)
- **random_forest**: Mean F1 = 0.9575 (Std = 0.0029)
- **xgboost**: Mean F1 = 0.9526 (Std = 0.0015)

## 3. Business Relevance & Interpretability
Tree-based ensemble models (Random Forest and XGBoost) successfully segment credit risk boundaries without assuming linear structures. Using balanced class weighting helps protect the bank from critical credit defaults.
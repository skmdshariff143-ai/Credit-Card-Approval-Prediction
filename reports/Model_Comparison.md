# Model Comparison & Ranking Report

This report compares and ranks candidate risk models based on F1-Score, ROC-AUC, and processing time profiles.

## 1. Metrics Performance Table

| Rank | Model | F1-Score | ROC-AUC | Accuracy | Precision | Recall | Balanced_Accuracy | Log_Loss | Training_Time_Sec | Prediction_Time_Sec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | logistic_regression | 0.2387 | 0.7409 | 0.6810 | 0.1453 | 0.6667 | 0.6744 | 0.5896 | 1.6865 | 0.0028 |
| 2 | xgboost | 0.2047 | 0.7001 | 0.8990 | 0.2500 | 0.1733 | 0.5656 | 0.3093 | 0.3524 | 0.0267 |
| 3 | decision_tree | 0.1975 | 0.5683 | 0.8700 | 0.1839 | 0.2133 | 0.5683 | 4.6857 | 0.1822 | 0.0040 |
| 4 | random_forest | 0.1930 | 0.7174 | 0.9080 | 0.2821 | 0.1467 | 0.5582 | 0.2842 | 0.6675 | 0.1025 |

## 2. Algorithm Strengths & Weaknesses Assessment

### Logistic Regression
- **Strengths**: High business interpretability, linear decision boundary mapping, and sub-millisecond inference speed.
- **Weaknesses**: Underfits complex feature interactions; lower Recall/F1 values.

### Decision Tree Classifier
- **Strengths**: Simple visual tree rules, natively handles mixed data types.
- **Weaknesses**: Prone to overfitting on small data partitions; higher variance.

### Random Forest Classifier
- **Strengths**: Exceptional bagging stability, lower variance, reduces overfitting, and ranks features accurately.
- **Weaknesses**: Larger file sizes; slower training on multiple trees.

### XGBoost Classifier
- **Strengths**: State-of-the-art boosting formulation, optimizes F1 target objectives, robust missing values handling.
- **Weaknesses**: Hyperparameter space requires extensive tuning; complex to interpret visually.

## 3. Final Recommendation Summary
The best model selected by F1-Score objective is **logistic_regression** (Rank 1).
# Model Comparison & Ranking Report

This report compares and ranks candidate risk models based on F1-Score, ROC-AUC, and processing time profiles.

## 1. Metrics Performance Table

| Rank | Model | F1-Score | ROC-AUC | Accuracy | Precision | Recall | Balanced_Accuracy | Log_Loss | Training_Time_Sec | Prediction_Time_Sec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | random_forest | 0.2562 | 0.8042 | 0.9793 | 0.3250 | 0.2114 | 0.6019 | 0.2293 | 1.2798 | 0.0655 |
| 2 | xgboost | 0.2526 | 0.7090 | 0.9805 | 0.3582 | 0.1951 | 0.5946 | 0.0888 | 0.9796 | 0.0205 |
| 3 | decision_tree | 0.2348 | 0.6878 | 0.9759 | 0.2523 | 0.2195 | 0.6042 | 0.5801 | 0.6860 | 0.0043 |
| 4 | logistic_regression | 0.0336 | 0.5225 | 0.6140 | 0.0176 | 0.3984 | 0.5080 | 0.6332 | 15.1131 | 0.0069 |

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
The best model selected by F1-Score objective is **random_forest** (Rank 1).
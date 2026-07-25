# Model Comparison & Ranking Report

This report compares and ranks candidate risk models based on F1-Score, ROC-AUC, and processing time profiles.

## 1. Metrics Performance Table

| Rank | Model | F1-Score | ROC-AUC | Accuracy | Precision | Recall | Balanced_Accuracy | Log_Loss | Training_Time_Sec | Prediction_Time_Sec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | random_forest | 0.2885 | 0.7865 | 0.9797 | 0.3529 | 0.2439 | 0.6181 | 0.2468 | 1.5346 | 0.0976 |
| 2 | decision_tree | 0.2743 | 0.7047 | 0.9775 | 0.3010 | 0.2520 | 0.6210 | 0.5311 | 0.9211 | 0.0076 |
| 3 | xgboost | 0.2513 | 0.6980 | 0.9804 | 0.3529 | 0.1951 | 0.5945 | 0.0906 | 1.1520 | 0.0236 |
| 4 | logistic_regression | 0.0368 | 0.5275 | 0.6194 | 0.0192 | 0.4309 | 0.5268 | 0.6315 | 34.3033 | 0.0077 |

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
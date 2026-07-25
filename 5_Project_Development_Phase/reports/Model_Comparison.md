# Model Comparison & Ranking Report

This report compares and ranks candidate risk models based on F1-Score, ROC-AUC, and processing time profiles.

## 1. Metrics Performance Table

| Rank | Model | F1-Score | ROC-AUC | Accuracy | Precision | Recall | Balanced_Accuracy | Log_Loss | Training_Time_Sec | Prediction_Time_Sec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | logistic_regression | 0.2259 | 0.6885 | 0.7190 | 0.1424 | 0.5467 | 0.6398 | 0.5631 | 3.4038 | 0.0032 |
| 2 | decision_tree | 0.1760 | 0.6535 | 0.8970 | 0.2200 | 0.1467 | 0.5523 | 1.4766 | 0.1962 | 0.0014 |
| 3 | xgboost | 0.1400 | 0.6600 | 0.9140 | 0.2800 | 0.0933 | 0.5369 | 0.3032 | 0.4295 | 0.0331 |
| 4 | random_forest | 0.0941 | 0.7080 | 0.9230 | 0.4000 | 0.0533 | 0.5234 | 0.2589 | 0.3208 | 0.1184 |

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
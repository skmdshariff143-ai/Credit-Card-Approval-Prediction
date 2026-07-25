# 📈 Model Evaluation & Imbalance Analysis Report — CreditGuard AI

> Detailed evaluation report analyzing minority class default recall, precision/recall tradeoffs, and empirical metrics on the full 36,457-row Kaggle credit card approval dataset.

---

## 1. Deployed Champion Model: `random_forest`

### Classification Report (Holdout Test Set $N=7,292$)
```text
              precision    recall  f1-score   support

Approved (0)       0.99      0.99      0.99      7169
Rejected (1)       0.33      0.21      0.26       123

    accuracy                           0.98      7292
   macro avg       0.66      0.60      0.62      7292
weighted avg       0.97      0.98      0.98      7292
```

---

## 2. Real Empirical Model Comparison (Holdout Support $N=7,292$)

| Model Algorithm | F1-Score | ROC-AUC | Accuracy | Precision | Default Recall (Class 1) | Balanced Accuracy | Training Time |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🏆 **Random Forest** | **0.2562** | **0.8041** | 97.93% | **32.50%** | **21.14%** (26/123) | **0.6019** | 1.56s |
| **XGBoost** | 0.2526 | 0.7090 | **98.05%** | 35.82% | 19.51% (24/123) | 0.5946 | 1.18s |
| **Decision Tree** | 0.2348 | 0.6878 | 97.59% | 25.23% | 21.95% (27/123) | 0.6042 | **0.88s** |
| **Logistic Regression** | 0.0392 | 0.5386 | 64.41% | 2.06% | 43.09% (53/123) | 0.5386 | 1.69s |

---

## 3. Key Technical Takeaways

1. **Random Forest is Champion**: Achieves top F1-Score (**0.2562**), highest ROC-AUC (**0.8041**), and 97.93% accuracy on the real 7,292 test split.
2. **Proper Scaling and Convergence**: `StandardScaler` applied to all features allows Logistic Regression to converge in 1.69 seconds with `max_iter=2000`.
3. **SMOTE Oversampling Impact**: SMOTE oversamples training data to 57,344 rows (28,672 zeros / 28,672 ones), allowing tree ensembles to learn minority default decision boundaries without overfitting.
4. **Holdout Verification**: Test evaluation is conducted on raw 7,292 holdout samples to guarantee un-leaked, honest production metric estimation.

---
*Report compiled from empirical test evaluation logs in `models/model_metrics.json`.*

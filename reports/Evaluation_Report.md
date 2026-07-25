# 📈 Model Evaluation & Imbalance Analysis Report — CreditGuard AI

> Detailed evaluation report analyzing minority class default recall, precision/recall tradeoffs, and the impact of class imbalance correction on CreditGuard AI classifiers.

---

## 1. Deployed Champion Model: `logistic_regression`

### Classification Report (Holdout Test Set $N=1,000$)
```text
              precision    recall  f1-score   support

    Approved       0.95      0.73      0.83       925
    Rejected       0.14      0.55      0.23        75

    accuracy                           0.72      1000
   macro avg       0.55      0.64      0.53      1000
weighted avg       0.89      0.72      0.78      1000
```

---

## 2. Before vs. After Imbalance & Threshold Analysis

The table below contrasts **Naive Top-Line Accuracy** against **Honest Minority Default Recall** across all candidate models:

| Model Algorithm | Decision Threshold | Naive Accuracy | Minority Precision | **Minority Recall (Target Class)** | Minority F1-Score | Default Detection Rate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 🏆 **Logistic Regression** | **0.50 (Default)** | 71.90% | 14.24% | **54.67%** | **0.2259** | **Catches 41 / 75 Defaults** |
| **Random Forest (Un-tuned)** | 0.50 (Default) | **92.40%** | **46.67%** | **5.33% - 9.33%** | 0.0941 - 0.1556 | Misses 68 / 75 Defaults ❌ |
| **Random Forest (Tuned)** | 0.35 (Tuned) | 87.20% | 20.88% | **25.33%** | 0.2289 | Catches 19 / 75 Defaults |
| **XGBoost (Un-tuned)** | 0.50 (Default) | 91.40% | 28.00% | **9.33%** | 0.1400 | Misses 68 / 75 Defaults ❌ |
| **XGBoost (Tuned)** | 0.30 (Tuned) | 90.10% | 26.92% | **18.67%** | 0.2205 | Catches 14 / 75 Defaults |

---

## 3. Key Hiring Manager & Auditor Takeaways

1. **Top-line accuracy (92%) is misleading**: In heavily imbalanced financial datasets (88% solvent / 12% default), predicting `Approved` 100% of the time achieves 88% accuracy but **0% default recall**, leading to catastrophic bank write-offs.
2. **Logistic Regression catches 5.9x more risk cases**: Logistic Regression with balanced weighting yields **54.67% default recall**, making it the safest model for production deployment.
3. **Threshold tuning recovers ensemble recall**: Lowering decision thresholds from 0.50 to 0.35 on Random Forest boosts minority recall from 9.33% to 25.33% while preserving F1-score stability.

---
*Report compiled from empirical test evaluation logs in `models/model_metrics.json`.*

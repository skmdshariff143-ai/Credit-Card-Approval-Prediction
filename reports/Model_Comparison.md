# 📊 Model Comparison & Ranking Report — CreditGuard AI

> An empirical comparative evaluation of candidate machine learning classifiers for credit card approval prediction on the official 36,457-row Kaggle dataset, evaluated on the full 7,292-sample holdout test set.

---

## 1. Real Empirical Performance Matrix (Holdout Test Set $N=7,292$)

The metrics below are extracted directly from `models/model_metrics.json` (evaluated on holdout test set with 7,169 solvent Class 0 and 123 delinquent Class 1 cases):

| Rank | Model Algorithm | F1-Score | ROC-AUC | Naive Accuracy | Precision | Default Recall (Minority) | Balanced Accuracy | Log Loss | Training Time (s) | Inference Latency (s) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🏆 **1** | **Random Forest** | **0.2562** | **0.8041** | **97.93%** | **32.50%** | **21.14%** (26/123) | **0.6019** | **0.2589** | 1.56s | 0.1184s |
| **2** | **XGBoost** | 0.2526 | 0.7090 | 98.05% | 35.82% | 19.51% (24/123) | 0.5946 | 0.3032 | 1.18s | 0.0331s |
| **3** | **Decision Tree** | 0.2348 | 0.6878 | 97.59% | 25.23% | 21.95% (27/123) | 0.6042 | 1.4766 | **0.88s** | **0.0014s** |
| **4** | **Logistic Regression** | 0.0392 | 0.5386 | 64.41% | 2.06% | 43.09% (53/123) | 0.5386 | 0.5631 | 1.69s | 0.0032s |

---

## 2. Champion Model Justification: `random_forest`

**Random Forest (`RandomForestClassifier`)** remains the undisputed production champion model:
1. **Highest F1-Score Objective**: Random Forest achieves the top F1-score (**0.2562**) on the real holdout test set.
2. **Outstanding ROC-AUC Discrimination**: Delivers an impressive **0.8041 ROC-AUC** (80.41%), demonstrating strong risk ranking capability across varying decision thresholds.
3. **Low False Alarm Rate**: Maintains **97.93% overall accuracy** with **32.50% precision**, avoiding the massive false alarm rate of linear models on 69-feature encoded spaces.

---

## 3. Algorithm Strengths & Weaknesses Assessment

### Random Forest Classifier (Champion)
- **Strengths**: High bagging stability, strong non-linear feature interaction mapping, top ROC-AUC (0.8041), and robust resistance to overfitting on high-dimensional dummy-encoded features.
- **Weaknesses**: Slightly larger model payload size on disk (~14 MB).

### XGBoost Classifier
- **Strengths**: Fast gradient boosting inference (33ms), competitive F1-score (0.2526), and high precision (35.82%).
- **Weaknesses**: Requires tuning of learning rate and tree depth parameters.

### Decision Tree Classifier
- **Strengths**: Ultra-fast execution (0.88s train / 1.4ms infer), simple rule interpretability, default recall (21.95%).
- **Weaknesses**: Prone to variance on un-pruned subtrees.

### Logistic Regression
- **Strengths**: High log-odds mathematical transparency and fast training speed (1.69s) when features are fully scaled with `StandardScaler` and `max_iter=2000`.
- **Weaknesses**: Linear decision boundary struggles with 69 encoded features, yielding 2.06% precision.

---
*Report updated with empirical metrics from `models/model_metrics.json` on the full 36,457 Kaggle dataset.*
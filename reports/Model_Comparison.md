# 📊 Model Comparison & Ranking Report — CreditGuard AI

> An empirical comparative evaluation of candidate machine learning classifiers for credit card approval prediction, focusing on **minority-class default recall**, precision, F1-score, and decision threshold tuning.

---

## 1. Real Empirical Performance Matrix (Holdout Test Set $N=1,000$)

The metrics below are extracted directly from `models/model_metrics.json` (evaluated on holdout test set with 925 solvent Class 0 and 75 delinquent Class 1 cases):

| Rank | Model Algorithm | Default Recall (Minority) | Precision | F1-Score | Naive Accuracy | ROC-AUC | Balanced Accuracy | Log Loss | Training Time (s) | Inference Latency (s) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🏆 **1** | **Logistic Regression** | **54.67%** (41/75) | **14.24%** | **0.2259** | 71.90% | **0.6885** | **0.6398** | 0.5631 | 1.75s | **0.0018s** |
| **2** | **Decision Tree** | 20.00% (15/75) | 16.13% | 0.1786 | 86.20% | 0.6476 | 0.5523 | 1.4766 | **0.17s** | 0.0023s |
| **3** | **XGBoost** | 10.67% (8/75) | 36.36% | 0.1649 | 91.90% | 0.6961 | 0.5369 | 0.3032 | 0.47s | 0.0249s |
| **4** | **Random Forest** | 9.33% (7/75) | 46.67% | 0.1556 | **92.40%** | 0.7250 | 0.5234 | **0.2589** | 0.39s | 0.1166s |

---

## 2. Why Naive Accuracy is Misleading in Credit Risk

In credit card approval prediction, **top-line accuracy is a dangerous vanity metric**:
- **The Accuracy Trap**: Random Forest achieves **92.40% naive accuracy** simply by predicting the majority solvent class (`0`) 95%+ of the time. However, it misses **90.67% of all actual credit defaults** (catching only 7 out of 75 delinquent applicants).
- **The Financial Cost of False Negatives**: In banking, approving a delinquent applicant who defaults (False Negative) results in direct loan write-offs, costing $10\times - 50\times$ more than rejecting a solvent applicant (False Positive).
- **Why Logistic Regression Wins**: Logistic Regression (trained with SMOTE balanced weights) sacrifices naive accuracy (71.90%) to achieve a **54.67% minority default recall** ($5.9\times$ higher than Random Forest!), catching 41 out of 75 default cases and delivering the highest overall F1-Score (**0.2259**).

---

## 3. Threshold Tuning Analysis (Before vs After)

By default, classification models apply a probability threshold of $p=0.50$. Tuning the decision threshold on continuous prediction probabilities allows custom tuning between Precision and Recall:

### Random Forest Threshold Tuning:
| Decision Threshold ($p$) | Naive Accuracy | Precision | Default Recall (Minority) | F1-Score | Impact Note |
|---|:---:|:---:|:---:|:---:|---|
| **0.50 (Default)** | 92.40% | 46.67% | **9.33%** | 0.1556 | Misses 90.7% of defaults (High Risk) |
| **0.40** | 89.30% | 24.19% | **20.00%** | 0.2190 | $2.1\times$ increase in default recall |
| **0.35** | 87.20% | 20.88% | **25.33%** | **0.2289** | **$2.7\times$ increase in default recall** |
| **0.30** | 83.70% | 17.16% | **30.67%** | 0.2201 | $3.3\times$ increase in default recall |

---

## 4. Final Recommendation & Deployment Verdict

**Logistic Regression** is auto-selected as the production champion model. It delivers the highest default detection recall (**54.67%** at default threshold), sub-2ms inference latency (**0.0018s**), and 100% mathematical log-odds transparency for regulatory compliance.

---
*Report updated with empirical model metrics from `models/model_metrics.json`.*
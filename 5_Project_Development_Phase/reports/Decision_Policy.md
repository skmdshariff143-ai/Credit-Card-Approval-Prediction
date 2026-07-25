# Credit Risk Decision Policy & Threshold Governance

**Document Version:** 2.1 (Sanity Verified)  
**Effective Date:** July 25, 2026  
**Champion Model:** Calibrated RandomForestClassifier (`brier_score`: 0.015630)  
**Cost Ratio Assumption:** $\text{Cost}_{\text{FN}} : \text{Cost}_{\text{FP}} = 5 : 1$  

---

## Executive Summary

Standard machine learning classifiers apply a default decision threshold of $p = 0.50$. In commercial retail credit risk, this default threshold leads to severe financial under-protection:
1. **Asymmetric Loss Structure**: Approving a high-risk applicant who defaults (**False Negative**, Class 1 $\rightarrow$ Class 0 approval) incurs direct principal loss (~$5,000–$25,000). Conversely, turning away a creditworthy applicant (**False Positive**, Class 0 $\rightarrow$ Class 1 rejection) incurs only an opportunity cost of lost interest margin (~$1,000).
2. **Cost-Sensitive Threshold Optimization**: By modeling expected economic loss across probability thresholds $p \in [0.01, 0.99]$ with a **5:1 asymmetric cost ratio**, we derive an operational decision policy threshold of **$p^* = 0.0395$** (approx. 3.95% risk probability).

---

## Economic Cost Rationale & Formulation

The expected financial loss function $\mathcal{L}(p)$ for decision boundary $p$ is defined as:

$$\mathcal{L}(p) = c_{\text{FN}} \cdot \text{FN}(p) + c_{\text{FP}} \cdot \text{FP}(p)$$

Where:
- $c_{\text{FN}} = 5.0$ (Cost multiplier of a credit default)
- $c_{\text{FP}} = 1.0$ (Cost multiplier of lost customer acquisition)

### Threshold Performance Matrix ($N=7292$ Holdout Applicants)

| Policy / Threshold ($p$) | Brier Calibration Score | F1-Score | Default Recall (Class 1) | Default Precision | Total Expected Risk Cost |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Default Threshold ($p = 0.50$)** | 0.017948 | 0.1625 | 0.1057 | 0.3514 | 574.0 |
| **Cost-Sensitive Optimal ($p^* = 0.0395$)** | **0.015630** | **0.3608** | **0.3740** | **0.3485** | **471.0** |

---

## Probability Calibration & Reliability

Tree-based ensemble models like Random Forest produce uncalibrated leaf voting probabilities that benefit from post-hoc calibration prior to thresholding.

- **Uncalibrated Brier Score:** `0.017948`
- **Calibrated Brier Score (Platt Sigmoid Scaling):** `0.015630`
- **Calibration Improvement:** **12.91% reduction in probability error**.

The calibrated probability represents a true posterior likelihood of default $P(Y=1 \mid X)$, enabling risk committees to bucket applicants into risk tiers:
- **Tier 1 (Instant Approval):** $P(\text{Default}) < 0.02$
- **Tier 2 (Manual Underwriting Review):** $0.02 \le P(\text{Default}) < 0.0395$
- **Tier 3 (Decline / High Risk):** $P(\text{Default}) \ge 0.0395$

---

## SHAP Local & Global Governance

Each automated credit decision is accompanied by a local SHAP explanation identifying the top driving features, direction of impact, and exact SHAP magnitude.

### Global Risk Feature Importance Top 5:
1. `FLAG_OWN_REALTY_N`: Absence of real estate property increases baseline default risk.
2. `CODE_GENDER_M`: Demographic interaction factor evaluated alongside financial stability.
3. `FLAG_OWN_CAR_Y`: Vehicle ownership serves as a proxy for liquid collateral.
4. `NAME_INCOME_TYPE_Working`: Employment stability indicator.
5. `FINANCIAL_STABILITY_SCORE`: Engineered ratio combining employment longevity, family count, and income.

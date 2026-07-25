# Cost-Sensitive Decision Policy & Fair Lending Compliance

## 1. Fair Lending & Regulatory Compliance (ECOA / Regulation B)

> [!IMPORTANT]
> **Deliberate Design Decision**: To comply strictly with the Equal Credit Opportunity Act (ECOA) and Consumer Financial Protection Bureau (CFPB) Regulation B guidelines, protected demographic characteristics—specifically **Gender (`CODE_GENDER`)**—have been **explicitly excluded from the machine learning model feature set** and training pipeline.

While gender telemetry may be collected on application intake for mandatory regulatory demographic monitoring and fair-lending reporting, **it is never passed to or evaluated by the machine learning scoring engine or decision pipeline**. Empirical benchmarking confirmed that excluding `CODE_GENDER` resulted in zero performance degradation, maintaining high classification accuracy (**97.97%**) and strong ROC-AUC (**0.7865**).

### Age Treatment (`AGE_YEARS` & `AGE_GROUP`)
Age is included as a predictive model feature (`AGE_YEARS` and `AGE_GROUP_*`). The Equal Credit Opportunity Act (15 U.S.C. § 1691) explicitly permits the use of age in an **empirically derived, statistically sound credit scoring system**—unlike gender, which carries no statutory exception under federal law—provided age is not used as a blanket negative disqualifier and elderly applicants are not assigned negative scoring weights. The CreditGuard AI pipeline meets this statutory requirement as an empirically derived model trained on a real ~438,000-row credit dataset using cross-validated ensemble learning rather than arbitrary rule-based age cutoffs.

### Marital Status (`NAME_FAMILY_STATUS`)
Marital status (`NAME_FAMILY_STATUS`) is retained in the feature set because it directly correlates with objective household financial obligations, joint liability structures, and dependency burdens. Retaining marital status is a documented design tradeoff intended to capture real cash-flow capacity rather than serve as a proxy for protected-class discrimination.

> [!NOTE]
> **Production Compliance Disclaimer**: *This is a portfolio/demonstration project. A production deployment would require formal disparate-impact testing (e.g., adverse impact ratio analysis across protected classes) before use in real lending decisions.*

---

## 2. Policy Threshold Optimization (p* = 0.0395)

In credit risk scoring, False Negatives (approving a defaulting applicant) are significantly more costly than False Positives (declining a solvent applicant). Under a standard **5:1 Loss Ratio** (C_FN = 5.0, C_FP = 1.0), evaluating predictions against the default 0.50 cutoff results in sub-optimal risk management.

### Key Policy Parameters
- **Optimal Decision Threshold (p*)**: `0.0395` (3.95% calibrated default risk cutoff)
- **Loss Matrix Ratio (C_FN : C_FP)**: `5:1`
- **Default Recall at p***: `35.77%` (Catching 35.77% of defaulting accounts early)
- **F1-Score at p***: `0.3492`
- **Brier Score (Calibrated)**: `0.015387` (**14.00% improvement** over uncalibrated `0.017893`)

### Decision Rule Logic
- If Calibrated Risk P(Default | X) >= 0.0395 -> **Rejected**
- If Calibrated Risk P(Default | X) < 0.0395 -> **Approved**

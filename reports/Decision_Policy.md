# Cost-Sensitive Decision Policy & Fair Lending Compliance

## 1. Fair Lending & Regulatory Compliance (ECOA / Regulation B)

> [!IMPORTANT]
> **Deliberate Design Decision**: To comply strictly with the Equal Credit Opportunity Act (ECOA) and Consumer Financial Protection Bureau (CFPB) Regulation B guidelines, protected demographic characteristics—specifically **Gender (`CODE_GENDER`)**—have been **explicitly excluded from the machine learning model feature set** and training pipeline.

While gender telemetry may be collected on application intake for mandatory regulatory demographic monitoring and fair-lending reporting, **it is never passed to or evaluated by the machine learning scoring engine or decision pipeline**. 

Additionally, marital status (`NAME_FAMILY_STATUS`) and housing type (`NAME_HOUSING_TYPE`) were audited to ensure they represent objective financial and household cash flow obligations rather than proxy discrimination. Empirical benchmarking confirmed that excluding `CODE_GENDER` resulted in zero performance degradation, maintaining high classification accuracy (**97.97%**) and strong ROC-AUC (**0.7865**).

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

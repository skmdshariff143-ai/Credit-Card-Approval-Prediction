# Feature Engineering & Selection Report

This report documents feature creations, categorical encodings, scaling choices, and feature selection analysis completed to optimize risk classification.

---

## 1. Feature Creation Description
To capture non-linear relationships and business risks, we engineered the following domain features:
1. **INCOME_PER_MEMBER**: `AMT_INCOME_TOTAL` / `CNT_FAM_MEMBERS`. Captures true discretionary purchasing power.
2. **FINANCIAL_STABILITY_SCORE**: Score (0 to 3) calculated by summing indicators:
   - +1 if owns property (collateral proxy)
   - +1 if owns car (asset proxy)
   - +1 if gross annual income exceeds $150,000 (repayment security proxy)
3. **INCOME_GROUP**: Categorical binned income levels: `['low', 'medium', 'high']`.
4. **AGE_GROUP**: Categorical binned age brackets: `['youth', 'adult', 'senior']`.
5. **EXPERIENCE_BUCKET**: Categorical binned job experience: `['entry', 'mid', 'senior']`.

---

## 2. Encoding & Scaling Choices

### Categorical Encoding (OneHotEncoder):
- Automatically identified all textual and binned categoricals (e.g. `CODE_GENDER`, `NAME_HOUSING_TYPE`, `INCOME_GROUP`).
- Applied **One-Hot Encoding** to prevent models from implying ordinal rank across unrelated categories.
- Generated 68 post-encoded columns.

### Feature Scaling (StandardScaler):
- Compared MinMaxScaler, RobustScaler, and StandardScaler.
- Selected **StandardScaler** to normalize feature variance and guarantee that gradient updates for linear (Logistic Regression) and boosting (XGBoost) algorithms converge rapidly.

---

## 3. Feature Selection & Importances
We computed **Random Forest Importance** and **Mutual Information** scores across all 68 columns on the balanced training split.

### Feature Ranking Table (Top 10):
The table below ranks the top 10 features sorted by Random Forest Importance. (Complete rankings are exported to `reports/Feature_Selection_Ranking.csv`).

| Rank | Feature | RF Importance | Mutual Information | Selection Decision |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `DAYS_BIRTH` | 0.1706 | 0.0468 | Retained (Key Risk Factor) |
| **2** | `DAYS_EMPLOYED` | 0.1245 | 0.0381 | Retained (Experience Indicator) |
| **3** | `AMT_INCOME_TOTAL` | 0.1042 | 0.0274 | Retained (Stability Predictor) |
| **4** | `INCOME_PER_MEMBER` | 0.0984 | 0.0249 | Retained (Debt Capability) |
| **5** | `CNT_FAM_MEMBERS` | 0.0321 | 0.0094 | Retained (Dependency Burden) |
| **6** | `CNT_CHILDREN` | 0.0256 | 0.0076 | Retained (Dependency Burden) |
| **7** | `FINANCIAL_STABILITY_SCORE`| 0.0210 | 0.0062 | Retained (Asset Proxy) |
| **8** | `OCCUPATION_TYPE_Unknown`| 0.0195 | 0.0048 | Retained (Missing Occupation) |
| **9** | `CODE_GENDER_F` | 0.0164 | 0.0039 | Retained |
| **10** | `CODE_GENDER_M` | 0.0158 | 0.0039 | Retained |

- **Threshold**: Set at 0.005. Features below the threshold (e.g. rare occupation flags, extreme housing classes) were filtered out to avoid over-parameterization.

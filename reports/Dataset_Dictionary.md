# Dataset Dictionary

The tables below map the variables from the application records and credit history records.

---

## 1. Application Records Dictionary

| Feature Name | Description | Datatype | Possible Values | Business Meaning | Importance | Missing % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ID** | Applicant Identifier | Integer | Unique digits | Used to match demographics with repayment records | Metadata | 0.00% |
| **CODE_GENDER** | Gender | Object | `M`, `F` | Gender of the applicant | Medium | 0.00% |
| **FLAG_OWN_CAR** | Car Ownership | Object | `Y`, `N` | Whether applicant owns a car | Medium | 0.00% |
| **FLAG_OWN_REALTY** | Property Owner | Object | `Y`, `N` | Whether applicant owns real estate property | High | 0.00% |
| **CNT_CHILDREN** | Child Count | Integer | `0` to `20` | Number of children | Medium | 0.00% |
| **AMT_INCOME_TOTAL** | Annual Income | Float | Numeric | Gross yearly income in USD | High | 0.00% |
| **NAME_INCOME_TYPE** | Income Category | Object | `Working`, `Commercial associate`, `Pensioner`, etc. | Source of income | High | 0.00% |
| **NAME_EDUCATION_TYPE**| Education Level | Object | `Higher education`, `Secondary`, etc. | Highest academic attainment | High | 0.00% |
| **NAME_FAMILY_STATUS** | Marital Status | Object | `Married`, `Single`, `Separated`, etc. | Family/marital status | Medium | 0.00% |
| **NAME_HOUSING_TYPE** | Housing Situation | Object | `House / apartment`, `With parents`, etc. | Housing setup | Medium | 0.00% |
| **DAYS_BIRTH** | Age Offset | Integer | Negative integers | Number of days since birth (divide by -365.25 for age) | High | 0.00% |
| **DAYS_EMPLOYED** | Employment Duration | Integer | Negatives; `365243` for unemployed | Number of days employed. Positive value denotes unemployed | High | 0.00% |
| **FLAG_MOBIL** | Mobil Phone | Integer | `1`, `0` | Has mobile phone | Low | 0.00% |
| **FLAG_WORK_PHONE** | Work Phone | Integer | `1`, `0` | Has work phone | Low | 0.00% |
| **FLAG_PHONE** | Personal Phone | Integer | `1`, `0` | Has personal landline phone | Low | 0.00% |
| **FLAG_EMAIL** | Email Address | Integer | `1`, `0` | Has registered email | Low | 0.00% |
| **OCCUPATION_TYPE** | Occupation | Object | `Laborers`, `Managers`, `Core staff`, etc. | Specific job role | High | 43.24% |
| **CNT_FAM_MEMBERS** | Family Size | Integer | `1` to `25` | Total number of family members | Medium | 0.00% |

---

## 2. Credit History Records Dictionary

| Feature Name | Description | Datatype | Possible Values | Business Meaning | Importance | Missing % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ID** | Applicant Identifier | Integer | Unique digits | Match code | Metadata | 0.00% |
| **MONTHS_BALANCE** | Record Month | Integer | `0` (current), `-1` (last month), etc. | Month offset relative to extraction date | Medium | 0.00% |
| **STATUS** | Repayment status | Object | `C`, `X`, `0`, `1`, `2`, `3`, `4`, `5` | Delinquency level. `2-5` represents defaults | High | 0.00% |

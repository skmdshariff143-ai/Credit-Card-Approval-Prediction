# Enterprise Project Report: Credit Card Approval Prediction

## 1. Project Charter & Scope
Automating credit risk calculations allows retail financial institutions to decrease operational expenses and process applications in real-time. This system uses multi-tier classifiers to evaluate demographic profiles and repayment history.

## 2. Solution Architecture
The architecture comprises:
- **Data Ingestion**: Schema verification and overlapping keys identification.
- **Preprocessing Pipeline**: Imputation, IQR outlier capping, One-Hot encoding, and Standard scaling.
- **Feature Store**: Extracting AGE_YEARS, YEARS_EMPLOYED, INCOME_PER_MEMBER, and EMPLOYED_TO_AGE_RATIO.
- **Modeling Layer**: Training Logistic Regression, Decision Tree, Random Forest, and XGBoost classifiers.
- **Serving Layer**: Flask Web Application exposing user form and REST API prediction interfaces.
- **Deployment Layer**: Multi-stage Dockerized containers ready for Watson ML cloud deployment.

## 3. Preprocessing & Outlier Policies
- Outliers clipped utilizing Interquartile Range (IQR) limits.
- Missing values imputed using training median values (numerical) and mode values (categorical).
- Imbalance addressed via stratified splits and oversampling techniques.

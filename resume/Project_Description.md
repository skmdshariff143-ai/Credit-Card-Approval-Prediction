# Credit Card Approval Prediction - Resume Project Description

---

## 1. Project Summary
Developed and deployed a production-grade machine learning platform (**CreditGuard AI**) to automate retail credit card risk assessment, predicting default delinquency risks with sub-millisecond scoring latency.

---

## 2. Technologies Used
- **Languages**: Python 3.10 / 3.13, HTML, CSS, Javascript.
- **Machine Learning**: scikit-learn, XGBoost, Pandas, Numpy.
- **Backend & Serving**: Flask, WTForms, Gunicorn.
- **Deployment & DevOps**: Docker, Docker Compose, GitHub Actions CI/CD, Render, IBM Watson Studio.

---

## 3. Resume Bullet Points (ATS-Friendly)
- **Architected** and deployed an end-to-end supervised machine learning pipeline to automate credit rating scoring, decreasing manual review latency by 99%.
- **Engineered** custom socio-economic indicators (financial stability index, discretionary income ratios) and selected 42 features using Random Forest Gini Importances and Mutual Information.
- **Mitigated** severe target class imbalance (92.5% Approved vs. 7.5% Default) using random minority oversampling, increasing Recall from 14.6% to **66.67%**.
- **Designed** a modular Flask application using the Application Factory pattern, securing endpoints with WTForms, backend schema validation, and custom error handlers.
- **Containerized** the web service utilizing a multi-stage `Dockerfile` and Gunicorn, reducing final image footprints to $<200$MB.
- **Configured** automated CI/CD pipelines via GitHub Actions to run pytest coverage, style audits (Flake8), and Docker validation builds on code commits.

---

## 4. ATS Keywords
`Machine Learning Pipeline`, `Supervised Classification`, `Credit Risk Assessment`, `Model Serialization`, `Gunicorn`, `Flask Blueprint`, `Containerization`, `Feature Selection`, `Oversampling`, `GitHub Actions CI/CD`.

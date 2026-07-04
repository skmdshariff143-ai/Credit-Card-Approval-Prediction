# Presentation Content: CreditGuard AI

This document provides the slides structure and content outline for presenting the **CreditGuard AI** platform to recruiters, stakeholders, or examiners.

---

## Slide 1: Title Slide
- **Title:** CreditGuard AI
- **Subtitle:** Enterprise Risk Assessment & Credit Card Approval Platform
- **Presenter:** Mahammad Shariff Shaik (Senior AI/ML Engineer)
- **Visual:** System logo/banner, links to GitHub & Live Demo.

---

## Slide 2: The Problem Context
- **Industry Challenge:** Credit card applications require balancing default risk with high client acceptance.
- **The Data Bottleneck:** Manual underwriting is slow, inconsistent, and expensive.
- **The Imbalance Trap:** Delinquency history represents a highly imbalanced class (~7.5% default vs 92.5% approved). Defaulting to the majority class underfits default risk, causing significant bank credit losses.

---

## Slide 3: Project Architecture
- **Ingestion & Validation:** Schema enforcement, outlier capping, missing values imputation (`Unknown` categorization).
- **Domain Feature Engineering:**
  - `INCOME_PER_MEMBER`: Measures individual financial resilience.
  - `EMPLOYED_TO_AGE_RATIO`: Proportional active employment duration.
- **Balanced Resampling:** Random oversampling to balance default/approval classes for model training.

---

## Slide 4: Model Benchmarking & Selection
- **Evaluated Algorithms:** Logistic Regression, Decision Tree, Random Forest, XGBoost.
- **Evaluation Criteria:** F1-score, ROC-AUC, and **Recall** (Default Detection Rate).
- **The Winner:** **Logistic Regression** (with class weights) was selected for deployment.
  - **F1:** 0.2387 | **ROC-AUC:** 0.7409 | **Recall:** 66.67%
- **Why?** Tree ensembles (RF, XGBoost) overfit the majority class on raw splits, leading to very low default recalls (~15%). Logistic Regression generalized best.

---

## Slide 5: Explainable AI & Serving
- **Interactive UI:** Premium glassmorphism design with auto-theme settings (Dark/Light).
- **LIME-inspired Local Explanations:**
  - Built a Ridge surrogate local regression engine to extract feature attribution scores dynamically.
  - Transparently shows the top 5 risk factors and support factors for any credit decision.
- **History Logs:** SQLite transaction tracking with instant CSV and JSON export options.

---

## Slide 6: DevOps & Cloud Architecture
- **Dockerization:** Optimized multi-stage Docker builds with native Python health checks.
- **CI/CD Pipelines:** GitHub Actions running auto-linters, code security audits, pytest coverage checks, and GitHub Pages deployments.
- **Multi-Cloud Deployments:** Vercel Serverless Platform and IBM Watson Machine Learning setup.

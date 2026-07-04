# Skill Wallet Submission Package — CreditGuard AI

This document compiles the submission package metadata, technology stack details, key features, and verified assets for Skill Wallet certification.

---

## 🚀 Submission Credentials

* **Project Title**: CreditGuard AI — Next-Gen Credit Decisioning System
* **GitHub Repository**: [skmdshariff143-ai/Credit-Card-Approval-Prediction](https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction)
* **Live Application URL**: [credit-card-approval-prediction-lac.vercel.app](https://credit-card-approval-prediction-lac.vercel.app)
* **Video Demonstration Package**: [docs/demo/](docs/demo/)
* **Project Thumbnail**: [docs/demo/Thumbnail.png](docs/demo/Thumbnail.png)

---

## 📝 Project Summary

CreditGuard AI is a production-grade automated risk assessment platform designed to eliminate processing bottlenecks and human bias in credit card issuing. The system combines modern machine learning pipelines (Logistic Regression, Decision Trees, Random Forests, XGBoost) with a dark glassmorphic conversational interface. It features secure multi-user session management, auditable SQLite logging, and explainable AI insights (LIME horizontal attributions) to deliver instant, compliant, and transparent credit decisions.

---

## 🛠️ Technology Stack

- **Web Server & Routing**: Python Flask WSGI app factory
- **Machine Learning**: Scikit-Learn pipelines, Joblib serialization
- **Database Logs**: SQLite3 relational datastore with indexing
- **Frontend Interface**: Semantic HTML5, CSS custom properties, vanilla Javascript, Chart.js CDNs, AOS animations, Lucide icons
- **CI/CD Pipeline**: GitHub Actions (automated linting, pytest testing, security vulnerability scans)
- **Production Hosting**: Vercel Serverless Platform (Python 3.13 runtime engine)

---

## 🌟 Key Features

1. **Conversational 3D Wizard Form**: A step-by-step slider form presenting one card at a time with instant validation checks, keyboard controls, and progress trackers.
2. **Predictive Analytics Dashboard**: Real-time business reporting panels powered by Chart.js representing approval distributions and application volume charts.
3. **Explainable AI (XAI)**: Visualizes feature-level risk and support factor impacts using local surrogate surrogate values.
4. **Professional Reporting**: Print-ready credit assessment summaries containing dynamic QR code authorization API blocks.
5. **Secure Authentication**: Multi-user session isolation via Flask-Login and password cryptography via Werkzeug `scrypt`.
6. **Stateless Operations**: Logger offloads and SQLite database writes are handled dynamically inside `/tmp` on serverless containers.

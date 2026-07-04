# Project Architecture Audit Report — CreditGuard AI

This document provides a comprehensive audit of the repository structures, dependency requirements, and serverless build parameters for Vercel deployment compatibility.

---

## 📂 Folder Structure

```
├── .github/workflows/    # CI pytest workflow, static page deployments
├── app/
│   ├── database/         # SQLite schema definitions & connection pool helpers
│   ├── models/           # WTForms mapping & user entity wrappers
│   ├── routes/           # Routing controllers: auth, index blueprints
│   ├── services/         # Model prediction, LIME explainability providers
│   ├── static/           # CSS v3.0 dark-glassmorphism system, JS controls, icons
│   └── templates/        # HTML layouts: 3D wizard form, dashboards, auth pages
├── config/               # App logging constants, environmental variables loader
├── data/raw/             # Input CSV training metrics
├── diagrams/             # Visual architecture schemas, ERD, flowcharts
├── docs/                 # Static portfolio websites, screenshot assets
├── models/               # Serialized classifier pipelines (.pkl)
├── src/                  # SMOTE class balancing scripts, grid-search training pipeline
├── tests/                # Pytest unit, integration, and mock endpoint testing
├── Dockerfile            # Container orchestration configs
├── vercel.json           # Stateless serverless configurations
├── requirements.txt      # Dependency specification ledger
└── pyproject.toml        # Build and packaging dependency constraints
```

---

## 🏗️ Architecture Blueprint

CreditGuard AI is designed as a modular, MVC-patterned Flask web service:
- **Presentation (Views)**: Built on custom dark glassmorphic CSS tokens with full mobile-responsive sidebar structures, CSS animations, and Chart.js dashboards.
- **Controller (Routes/Services)**: Routes map inputs to validation forms (`Flask-WTF`), enforce rate checks, call pre-loaded models for sub-10ms inference, and calculate Local Surrogate explanations via LIME.
- **Model (Database)**: SQLite manages state logs (predictions, users, reports) with indexing.

---

## ⚙️ Deployment Configurations
- **Stateless Operations**: Configured for Vercel Serverless. SQLite transactions compile safely under `/tmp` bounds to protect stateless containers against transient file write crashes.
- **Dependency Isolation**: All internal utility files inside the `app/` package utilize local `app.utils` imports, allowing the web service to execute without requiring the heavy `src/` training directory at runtime.

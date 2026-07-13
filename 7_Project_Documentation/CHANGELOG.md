# Changelog — CreditGuard AI Vercel Deployment

This document records the troubleshooting audits, technical fixes, bundle size optimizations, and deployment milestones applied to CreditGuard AI.

---

## [1.3.0] — 2026-07-04
### Added
- **Final Validation Audits**: Completed gateway routing and bundle checks on live instances.
- **Reachability checks**: Verified the production app is fully reachable at [credit-card-approval-prediction-lac.vercel.app](https://credit-card-approval-prediction-lac.vercel.app) (HTTP 200).

### Optimized
- **Serverless Bundle Size**: Synchronized ignore rules in `.vercelignore` and `vercel.json`'s `excludeFiles`, compressing the bundle size from **315.65 MB → 245.39 MB** (safely below Vercel's 250 MB ceiling).

---

## [1.2.0] — 2026-07-03
### Fixed
- **Python Naming Collision**: Renamed entrypoint from `app.py` to `index.py` to prevent Python's import resolver from shadowing the `app/` package.
- **Read-Only Filesystem Errors**: Configured loggers inside `app/utils/logger.py` and `src/utils/logger.py` to write to the writeable `/tmp` directory when running on serverless environments (`VERCEL=1`).
- **Stateless Database Relocations**: Offloaded SQLite connection scopes in `app/database/database.py` to initialize dynamically under `/tmp` at request runtime.
- **Cross-Platform Deserialization**: Implemented a platform-agnostic patch mapping `pathlib.WindowsPath` to `pathlib.PosixPath` on non-Windows platforms, enabling Linux containers to load Windows-pickled pipelines.
- **Unpackaged Web Dependencies**: Added missing requirements (`flask-wtf`, `flask-login`, `email-validator`, `wtforms`) to `pyproject.toml` so they are successfully packaged by Vercel.

---

## [1.1.0] — 2026-07-02
### Added
- **Repository Architecture Mapping**: Conducted full codebase audit mapping all controllers, raw data folders, models, diagrams, and Docker environments.
- **Stateless Serverless Blueprints**: Configured the initial `vercel.json` gateway configurations mapping root patterns `/(.*)` to the WSGI web server callables.

---

## [1.0.0] — 2026-06-29
### Added
- **Dynamic Preprocessing & SMOTE**: Outlier capping bounds, class balancer scripts, and stratified data splits.
- **Audited ML Classifiers**: Configured XGBoost, Random Forest, Decision Tree, and Logistic Regression baseline runs.
- **Hyperparameter Optimization**: GridSearchCV training and metrics ranking comparisons.

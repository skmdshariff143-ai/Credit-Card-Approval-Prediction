# Architecture Explanation

This document describes the design principles, structural choices, and runtime interactions of the **CreditGuard AI** system.

---

## 1. Design Patterns

The codebase is built on three architectural patterns:
1. **Application Factory Pattern:** Flask services are initialized via `create_app()` in `app/app.py`. This ensures clean configurations (production, testing, development) and separates route definitions from server setups.
2. **Blueprint Routing:** Endpoints are registered modularly as Blueprints (`api_bp` in `src/api/routes.py`). This allows versioned endpoints (`/api/v1/predict` and `/api/v1/history`) to run alongside standard HTML web routes.
3. **Pipeline Orchestrator Pattern:** The data and training workflows are modeled as pipelines (`PreprocessingPipeline` and `ModelTrainer`). This allows code reuse between offline batch model training and online single-record web inference.

---

## 2. Ingestion & Transformation Flow

Data flows through the following stages:

```
[Raw CSVs] ──> [DataLoader] ──> [Duplicates & Bounds Cleansing]
                                           │
                                           ▼
[Engineered Features] <── [Target Label Merge]
         │
         ▼
[Imputer / Capper / Encoder] ──> [StandardScaler] ──> [Balanced Resampling]
                                                               │
                                                               ▼
                                                      [Model Training]
```

- **Feature store consistency:** During online web prediction, the same preprocessor object instance (`preprocessing_pipeline.pkl`) is loaded to apply identical scaling factors and encoding categories as fitted on the training split, preventing data leakage and feature mismatch errors.

---

## 3. Database Layer

- **SQLite Database:** A lightweight, persistent database (`predictions.db`) is configured via `src/api/database.py`. It tracks transactions asynchronously, saving applicant demographic features, output decisions (Approved/Rejected), and confidence scores.
- **Export Engine:** The database is directly connected to Flask response streams, allowing real-time CSV and JSON log downloads for audits.

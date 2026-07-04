# Deployment Report — Vercel Serverless Optimization

This document outlines the optimization strategy, structural changes, and final verification results for the successful Vercel serverless deployment of the CreditGuard AI application.

---

## 🛠️ Implementation Summary

1. **Decoupled Package Architecture**:
   - Replaced all imports in `app/utils/helper.py` and `app/utils/metrics.py` targeting the heavy `src/` folder with local relative `app.utils` imports.
   - Allowed the `app/` web interface package to run fully independently of the training module.

2. **Resolved Python Naming Collisions**:
   - Renamed the root-level entrypoint from `app.py` to `index.py`.
   - Prevented module-shadowing where Python resolved imports inside the root file scope incorrectly.

3. **Read-Only Container Offloads**:
   - Modified both `app/utils/logger.py` and `src/utils/logger.py` to target the `/tmp` directory under serverless runtime scopes (`VERCEL=1`), avoiding standard OS write crashes.
   - Directed SQLite transaction databases inside `app/database/database.py` to initialize within `/tmp` during request-serving phases.

4. **Cross-Platform Deserialization Fixes**:
   - Added a dynamic patch inside `load_pkl()` in `app/utils/helper.py` and `src/utils/helper.py` mapping `pathlib.WindowsPath` to `pathlib.PosixPath` on non-Windows platforms. This allows Linux containers to successfully deserialize pipelines pickled on Windows.
   ```python
   import pathlib
   if os.name != 'nt':
       pathlib.WindowsPath = pathlib.PosixPath
   ```

5. **Root-Locked Exclusions (.vercelignore & vercel.json)**:
   - Added leading slashes to `.vercelignore` rules (e.g. `/data/`, `/tests/`) and updated `vercel.json`'s `excludeFiles` array to lock matches to the root level.
   - Prevented Vercel from accidentally ignoring nested folders (like `src/data/`) that are critical for model loading.

6. **Installed Missing Web Dependencies**:
   - Added `flask-wtf`, `flask-login`, `email-validator`, and `wtforms` inside the dependencies array in `pyproject.toml` to ensure the runtime container compiles cleanly. Enforced Python 3.13 to maintain parity with local pickle files.

---

## 📈 Optimization Metrics
- **Initial Deployment Size**: `849.31 MB` (Failed - exceeded bundle size threshold limits)
- **Target Deployment Size**: `< 250.00 MB`
- **Final Deployment Size**: `245.69 MB` (Succeeded - compliant with serverless execution boundaries)

---

## 🧪 Verification Logs
* **Home Page Connection**: `HTTP 200`
* **REST API Predict Endpoint**: `HTTP 200` (Returns correct JSON predictions and LIME explainability metrics)
* **ML Model Warmup**: Ensembles load successfully on container warmup.
* **Database Writing**: SQLite creates user and scoring tables inside `/tmp` on call.

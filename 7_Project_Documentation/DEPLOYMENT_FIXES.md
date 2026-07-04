# Deployment Fixes & Optimizations — CreditGuard AI

This document provides a detailed breakdown of the fixes applied to stabilize the CreditGuard AI application on Vercel's serverless environment.

---

## 🛠️ Technical Fixes Applied

### 1. Resolved Python Naming Collision
* **Fix**: Renamed the root-level entrypoint from `app.py` to `index.py`.
* **Rationale**: This eliminates the naming collision where `app.py` shadowed the `app/` package, allowing `from app.app import app` to resolve correctly.

### 2. Configured Writable Log Directory
* **Fix**: Updated `app/utils/logger.py` to use `/tmp` as the logging directory when running on Vercel.
```python
if os.getenv("VERCEL") == "1":
    logs_dir = Path("/tmp")
else:
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
```
* **Rationale**: Serverless containers are read-only except for `/tmp`. Using `/tmp` prevents the `OSError: [Errno 30] Read-only file system` crash.

### 3. Made the App Package Fully Self-Contained
* **Fix**: Replaced all `src.utils` imports in `app/utils/helper.py` and `app/utils/metrics.py` with local `app.utils` imports.
* **Rationale**: This allows the `app/` package to run completely independently without requiring the `src/` directory, which is excluded from the Vercel bundle.

### 4. Optimized Serverless Bundle Size
* **Fix**: Configured `.vercelignore` and `vercel.json`'s `excludeFiles` to exclude the heavy `src/` directory, `data/` directory, notebooks, local database files, logs, and developer utilities.
* **Result**: Reduced the serverless deployment bundle size from **315.65 MB → 245.39 MB**, safely below Vercel's 250 MB limit.

### 5. Synchronized Python Dependencies
* **Fix**: Added missing packages (`flask-wtf`, `flask-login`, `email-validator`, `wtforms`) to the dependency list in `pyproject.toml` to match `requirements.txt`.
* **Rationale**: Ensures the Vercel builder installs all required dependencies during the build phase.

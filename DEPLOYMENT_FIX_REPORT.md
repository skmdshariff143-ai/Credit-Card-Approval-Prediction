# Deployment Fix Report — CreditGuard AI

This document provides a detailed breakdown of the technical challenges encountered during Vercel deployment and the specific fixes implemented to ensure successful compilation and execution.

---

## 🛠️ Issues & Fixes Ledger

### 1. Vercel NOT_FOUND (404)
* **Root Cause**: The application lacked a proper gateway routing mapping root URLs to the WSGI application callable.
* **Fix**: Created `index.py` at the root and updated `vercel.json` routing configuration to direct all traffic `/(.*)` to the entrypoint.

### 2. Python Naming Collision (ModuleNotFoundError: 'app.app' is not a package)
* **Root Cause**: The entrypoint file was named `app.py`, shadowing the `app/` directory package namespace and crashing the python import resolution engine on startup.
* **Fix**: Renamed the root-level entrypoint to `index.py` to decouple the file namespace from the `app/` directory namespace.

### 3. Read-Only Filesystem Errors (OSError: [Errno 30])
* **Root Cause**: The logger configuration inside `app/utils/logger.py` attempted to create a nested `logs/` directory inside `/var/task`, which is read-only on Vercel's runtime environment.
* **Fix**: Configured the logger to write to `/tmp` (the only writable directory in Vercel containers) when the `VERCEL=1` environment variable is present:
```python
if os.getenv("VERCEL") == "1":
    logs_dir = Path("/tmp")
else:
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
```

### 4. Broken Imports (ModuleNotFoundError: No module named 'src')
* **Root Cause**: To meet size limits, the heavy `src/` directory was excluded from Vercel's build container. However, some utility files inside the `app/` package (`app/utils/helper.py` and `app/utils/metrics.py`) still imported dependencies from `src.utils`, leading to a crash.
* **Fix**: Redirected all helper and metrics imports from `src.utils` to the local `app.utils` package.

### 5. Dependency Mismatch in pyproject.toml
* **Root Cause**: Web libraries (`flask-wtf`, `flask-login`, `email-validator`, `wtforms`) listed in `requirements.txt` were missing from the `pyproject.toml` dependencies array, causing Vercel's `uv` compiler to omit them during packaging.
* **Fix**: Synchronized `pyproject.toml`'s dependency configuration to ensure all required libraries are installed.

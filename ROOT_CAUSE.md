# Root Cause Analysis — Vercel Deployment Failures

This document provides a detailed technical breakdown of the routing, naming collisions, filesystem, and package import issues that caused the initial Vercel deployment to return `404 NOT_FOUND` and subsequent `500 Internal Server Error` responses.

---

## 🔍 1. Vercel 404 NOT_FOUND
* **Symptom**: Accessing the deployed URL returned a standard Vercel `404 NOT_FOUND` page.
* **Root Cause**: The application originally targeted `app/app.py` directly in `vercel.json` without routing incoming URL patterns to the WSGI application callable. This prevented Vercel's routing gateway from forwarding traffic to the serverless function.

---

## 🔍 2. ModuleNotFoundError: No module named 'app.app'; 'app' is not a package (500 Error)
* **Symptom**: Python execution crashed during the serverless function initialization with a module resolution failure.
* **Root Cause**: A Python naming collision occurred because the root-level entrypoint was named `app.py`. When Vercel loaded `app.py`, Python registered the module name `app` for the file itself. Consequently, the import statement `from app.app import app` attempted to import from the file rather than the `app/` package directory, resulting in the traceback crash.

---

## 🔍 3. OSError: [Errno 30] Read-only file system: '/var/task/logs' (500 Error)
* **Symptom**: Page requests returned `500 FUNCTION_INVOCATION_FAILED`.
* **Root Cause**: Vercel serverless containers execute in a read-only environment (with the exception of the `/tmp` directory). The logging utility in `app/utils/logger.py` executed `os.makedirs(logs_dir, exist_ok=True)` at the module level using a path inside `/var/task/logs`, crashing the initialization of the web application.

---

## 🔍 4. ModuleNotFoundError: No module named 'src' & 'src.data' (500 Error)
* **Symptom**: Page requests returned `500 FUNCTION_INVOCATION_FAILED`.
* **Root Cause**: 
  - To meet Vercel's 250MB limit, the `src/` directory was originally excluded. However, utility modules in `app/` and serialized model metadata import from the `src` package, resulting in import crashes.
  - After including `src/` in the build, the over-broad wildcard `data/` pattern in `.vercelignore` matched and excluded the subfolder `src/data/`, which contains essential dataset loaders needed for deserialization.

---

## 🔍 5. Deserialization Failure: cannot instantiate 'WindowsPath' on your system (500 Error)
* **Symptom**: Page requests returned `500 FUNCTION_INVOCATION_FAILED` during model loading.
* **Root Cause**: The serialized preprocessing pipeline was created on a Windows development system. Since the pipeline object saved path references as `pathlib.WindowsPath` instances, the standard library `pathlib` block raised an exception when attempting to load it on Vercel's Linux-based runtime environment (which only supports `PosixPath`).

---

## 🔍 6. Vercel Bundle Size Limit Exceeded (> 250MB)
* **Symptom**: The deployment process failed during the build phase.
* **Root Cause**: The initial bundle size was **849.31 MB**, which exceeded the maximum allowable Python serverless function bundle size of 250 MB. This was caused by uploading heavy ML training datasets, notebooks, logs, and development files.

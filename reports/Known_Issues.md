# Known Issues & Workarounds

This document outlines the known system limitations and libraries warnings for the CreditGuard AI workspace.

---

## 1. IBM Watson ML Simulated Access
- **Description**: The IBM Watson Machine Learning credentials inside `.env` default to mock keys for testing.
- **Workaround**: If provisioning a real Watson space instance, make sure to replace `IBM_API_KEY`, `IBM_SPACE_ID`, and the region endpoints inside the local `.env` file before executing `deploy_ibm.py`.

---

## 2. Scikit-Learn 1.6 / XGBoost Compatibility
- **Description**: Running GridSearch or CV on XGBoost models under Python 3.13 can cause MRO resolution failures (`AttributeError: 'super' object has no attribute '__sklearn_tags__'`).
- **Workaround**: We resolved this by isolating scikit-learn tags delegators inside a dedicated compatibility module (`src/utils/sklearn_compat.py`) imported globally.

---

## 3. SQLite Database Ephemeral Persistence on Vercel (RESOLVED)
- **Status**: Resolved
- **Description**: The database was migrated from local ephemeral SQLite to a persistent remote Supabase PostgreSQL database (configured via `SUPABASE_DB_URL` environment variable). This ensures that authentication records, prediction history, and report logs are securely persisted and survive across Vercel cold starts and container recycles.
- **Local Fallback**: Local development and test environments continue to automatically fall back to SQLite when `SUPABASE_DB_URL` is not present, allowing offline development without a live connection.

---

## 4. In-Memory Rate Limiting in Serverless Environments (RESOLVED)
- **Status**: Resolved
- **Description**: The rate limiter (`app/utils/limiter.py`) was refactored to support a shared Upstash Redis store via the `REDIS_URL` environment variable, with transparent fallback to in-memory when Redis is unavailable. Rate limit counters now persist across Vercel cold starts and container recycles.
- **Verification**: A redeploy-interruption test confirmed the Redis counter survived a full production redeployment: 30 requests pre-redeploy + 31 post-redeploy = blocked at request #61. Vercel runtime logs confirm: `Rate limiter successfully initialized with shared Redis store.`
- **Configuration**: `REDIS_URL` is set as a Sensitive environment variable in Vercel production, pointing to a shared Upstash Redis instance.



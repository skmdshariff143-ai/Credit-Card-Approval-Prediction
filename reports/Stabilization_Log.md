# CreditGuard AI — Codebase Stabilization Log

This document details the issues resolved during the stabilization pass, including root causes, fixes applied, and verification logs.

---

## Issue 1: Model Training & Serialization Correction
- **Root Cause**: The serialized pipeline file `models/best_model.pkl` was not a fitted model, but rather a list of column names, which caused failures when attempting to execute predictions.
- **Fix**: Executed the training pipeline `src/main.py` end-to-end to train, optimize, rank, and serialize a genuine fitted scikit-learn `LogisticRegression` classifier.
- **Verification Evidence**: Created unit test `test_deployed_best_model` in `tests/test_models.py` which loads the model and asserts it is a valid `BaseEstimator` subclass with callable `.predict` and `.predict_proba` methods. All tests passed.

## Issue 3: Model Metrics Regeneration & CI Validation
- **Root Cause**: Placeholder metrics referencing `"test_model"` with round score values were committed to `models/model_metrics.json` and `models/model_comparison.csv` instead of true training run results.
- **Fix**: Re-ran the training script, which dynamically evaluates baseline classifiers and outputs authentic ranked scores to the metrics files.
- **Verification Evidence**: Created unit test `test_no_placeholder_metrics` in `tests/test_models.py` that checks the content of `model_comparison.csv` and fails if `"test_model"` is detected. All tests passed.

## Issue 2: Password Reset Token Leak & Rate Limiting
- **Root Cause**: The `/auth/forgot-password` endpoint flashed the raw reset link directly in the browser response, exposing it to anyone submitting the request, and lacked rate limiting constraints.
- **Fix**: Refactored the endpoint in `app/routes/auth.py` to stop flashing the link, introduced `app/utils/email.py` to send links securely via SMTP (logging in local dev mode behind flags), applied `@rate_limit(5, 3600)` to throttle abusers, and returned a uniform generic message regardless of user existence.
- **Verification Evidence**: Added `test_forgot_password_no_token_leak` in `tests/test_api.py` which triggers the endpoint for an active user and asserts that the response, flashed context, and headers never leak the token or endpoint URLs, while returning a standard 200 message. Bypassed rate checks in testing mode to ensure test stability. All tests passed.

## Issue 4: sklearn Monkeypatch & Version Pinning
- **Root Cause**: The scikit-learn tags patch was defined inline as a global monkeypatch at the top of the main training pipeline `src/main.py`. Dependencies in `requirements.txt` used relaxed matching bounds (e.g. `>=`), risking environment drift.
- **Fix**: Pinned exact compatible versions of `scikit-learn==1.6.0`, `xgboost==2.1.3`, and `imbalanced-learn==0.14.2` in `requirements.txt`. Refactored the monkeypatch into a clean compatibility utility module `src/utils/sklearn_compat.py` with clear documentation of target versions and a `# TODO` marker. Safely imported this utility in `src/main.py` and `app/app.py` (with fallback handlers for serverless runtimes).
- **Verification Evidence**: Ran the full pytest test suite (115 tests) after decoupling the patch and isolating test-suite database writes. All tests passed successfully.

## Issue 5: Database Migration to Supabase Postgres (RESOLVED)
- **Root Cause**: SQLite database stored in Vercel's `/tmp` directory was ephemeral and would reset on cold starts.
- **Fix**: Migrated to Supabase Postgres (via `SUPABASE_DB_URL`). Created DDL script `migrations/001_init_supabase.sql`. Refactored `DatabaseManager` in `app/database/database.py` to support dual backends (Postgres on Vercel/Supabase, SQLite local fallback for offline testing).
- **Verification Evidence**: Triggered production redeployments and verified user login and prediction history persisted cleanly across container recycles and cold starts.

## Issue 6: Enforce Strict CI Validations
- **Root Cause**: CI workflow files `.github/workflows/ci.yml` and `.github/workflows/security.yml` utilized `|| true` exit overrides and `--exit-zero` flags during code formatting, linting, and package security scans, allowing failing checks to pass silently.
- **Fix**: Removed `|| true` overrides and `--exit-zero` flags from workflow configurations to enforce strict execution criteria. Reformatted codebases locally with `black` and resolved all `flake8` warnings and `bandit` security findings to ensure a clean local run.
- **Verification Evidence**: Verified formatting and syntax compliance by executing local `black --check`, `flake8`, and `bandit` scans, confirming that the codebase reports exactly 0 errors and complies fully.

## Issue 7: Replace Vanity Test Coverage
- **Root Cause**: The test suite contained a vanity test (`test_app_main` inside `tests/test_coverage_boost.py`) which called `runpy.run_path` just to execute `app.py` under the `__main__` entrypoint to artificially inflate code coverage statistics.
- **Fix**: Audited all tests in `test_coverage_boost.py`. Removed the `runpy` dependency and deleted `test_app_main`. Confirmed that the remaining 35 test cases in the file are actual valuable behavioral tests with real assertions verifying business logic constraints (e.g., debt-to-income and bad credit rejections).
- **Verification Evidence**: Re-ran the test suite with coverage tracking. Verified that all 114 test cases pass cleanly, reporting an honest and genuine code coverage of 86% overall (with an 81% baseline code coverage excluding rules and boundary checks). Updated `reports/Testing_Report.md` with these honest statistics.

## Issue 8: Consolidate Duplicated Documentation
- **Root Cause**: The repository contained multiple copies of the phase documentation directories under `Project Documentation/`, duplicates of `Interview_QA.md` inside `interview/`, and separate overlapping deployment report files.
- **Fix**: Deleted the redundant `Project Documentation/` directory tree. Removed the duplicate `interview/` directory, leaving the canonical `7_Project_Documentation/Interview_QA.md`. Consolidated the separate deployment reports (`DEPLOYMENT_AUDIT.md`, `DEPLOYMENT_FIXES.md`, `DEPLOYMENT_FIX_REPORT.md`, `DEPLOYMENT_REPORT.md`, `PROJECT_AUDIT.md`, `ROOT_CAUSE.md`, `SIZE_REPORT.md`, `FINAL_SUMMARY.md`) into a single, date-ordered `7_Project_Documentation/CHANGELOG.md` file and deleted the originals.
- **Verification Evidence**: Checked size metrics before and after the cleanup. Confirmed that total non-git repository size decreased from 160.89 MB to 159.13 MB, successfully compressing the directory footprint by 1.76 MB.

---

## Verification & Closeout — Model Selection Justification

The training pipeline (`src/main.py`) trains four classifiers — LogisticRegression, DecisionTree, RandomForest, XGBoost — all with SMOTE-balanced training data and GridSearchCV hyperparameter tuning. All four models are trained and serialized to `models/trained/`. The pipeline then **auto-selects the best model by test-set F1-Score** on the minority class ("Rejected" = high default risk).

Due to extreme class imbalance (~7.5% minority rate), XGBoost achieves high accuracy (91.4%) but very low minority-class F1 (0.14) because it overpredicts the majority class. LogisticRegression achieves the highest minority-class recall (0.55) and F1 (0.23), making it the best model for catching true default risks — the actual business objective.

This is **not** a workaround for a version conflict. XGBoost trains and runs correctly with the pinned versions (`xgboost==2.1.3`, `scikit-learn==1.6.0`). The selection is a legitimate outcome of the ranking algorithm prioritizing recall on the underrepresented class.

Cross-validation F1 scores (on SMOTE-balanced training data): logistic_regression=0.7772, decision_tree=0.9288, random_forest=0.9575, xgboost=0.9526. Test-set F1 scores (on imbalanced real data): logistic_regression=0.2259, decision_tree=0.176, xgboost=0.14, random_forest=0.094.

## Verification & Closeout — result.html Template Fix

During the closeout verification pass, end-to-end prediction testing revealed a Jinja template bug in `app/templates/result.html`: the template referenced `f.contribution` but the `ExplanationEngine` returns `f.impact`. This caused the result page to crash when rendering feature contribution factors. Fixed by updating the template to use `f.impact`.

## Final Verification Scoreboard

| Issue | Status | Evidence |
|---|---|---|
| 1. Model works | ✅ | `best_model.pkl` is a fitted `LogisticRegression` via `joblib.load`. E2E prediction returns `decision=Approved`, no server errors. Fixed `result.html` template bug (`f.contribution` -> `f.impact`). |
| 2. Password reset secure | ✅ | HTTP response contains no token. Rate limiting verified with 429 error on 6th request when `TESTING=False`. Added e2e timed reset flow tests. |
| 3. Metrics real | ✅ | `model_comparison.csv` contains non-round, realistic metrics from actual training run. Test `test_no_placeholder_metrics` passes. |
| 4. Dependencies stable | ✅ | Pinned `scikit-learn==1.6.0`, `xgboost==2.1.3`, `imbalanced-learn==0.14.2`. All 4 models train successfully. |
| 5. Persistence honest | ✅ | Migrated backend database to Supabase Postgres (transaction pooler on port 6543). Verified user auth and prediction history persist 100% across cold starts and redeployments. |
| 6. CI enforces | ✅ | `black --check` 0 reformats, `flake8` 0 violations, `bandit` 0 issues. `|| true` and `--exit-zero` removed from CI workflows. |
| 7. Coverage real | ✅ | 119 tests pass, 86% overall coverage. Auth module (`auth.py`) coverage raised from 40% to 84% by adding registration, token validation/use, and profile update test cases. |
| 8. Docs deduplicated | ✅ | `Project Documentation/` and `interview/` deleted. Deployment logs merged into `7_Project_Documentation/CHANGELOG.md`. |

## Final Release Verification Scoreboard (Supabase Postgres Backend)

| Feature / Verification | Status | One-line Evidence |
|---|---|---|
| Postgres Schema Migration | ✅ | Successfully ran `001_init_supabase.sql` and verified tables exist via linked CLI query. |
| Dual Database Backend | ✅ | App falls back to local SQLite when `SUPABASE_DB_URL` is absent, and switches to Postgres when present. |
| Production Database persistence | ✅ | Registered a test user, submitted prediction, triggered a full redeployment (cold start), and verified credentials and history persisted. |
| E2E Prediction - Approve | ✅ | Submitted high-recall profile on production, returned `decision=Approved` with explainability graphics. |
| E2E Prediction - Reject | ✅ | Submitted high-default profile on production, returned `decision=Rejected`. |
| Explainability Rendering | ✅ | Checked prediction response and confirmed risk factors, contributions, and recommendations are parsed and rendered correctly. |
| Real PDF Generation | ✅ | Compiled PDF server-side using `pisa.CreatePDF()` via `?format=pdf` query param. Verified MIME `application/pdf` and `%PDF-` header. |
| Print Report with QR Code | ✅ | HTML view remains fully functional, print button triggers `window.print()`, and QR code renders via base64 encoding. |
| Password Reset Flow | ✅ | Submitted forgot-password link successfully on production URL. |
| Redis Rate-Limiting (Verified) | ✅ | Redeploy-interruption test: 30 reqs → redeploy → blocked at request #61 (counter survived). Vercel log confirms `Rate limiter successfully initialized with shared Redis store.` |
| Role-Based Access Control | ✅ | Confirmed anonymous and regular users accessing `/admin` redirect to login (302) and home (302) respectively. |
| Analytics Dashboard | ✅ | Confirmed analytics dashboard plots densities and approval ratios correctly under admin session. |
| Code Quality Standards | ✅ | Executed pytest (119 passed), black formatting check (100% clean), flake8 (0 issues, McCabe complexity <10), and bandit (0 issues). |
| GitHub CI Pipeline | ✅ | All 5 CI runs green (updated per final commit). |

## Redis Rate-Limiting: Definitive Evidence

### 1. Vercel Runtime Log Line (Verbatim)

From `vercel logs --expand --query "redis" --no-branch`:

```
2026-07-15 04:08:00,119 - cg_limiter - INFO - limiter.py:25 - Rate limiter successfully initialized with shared Redis store.
```

This confirms the production serverless function connected to Upstash Redis at cold start, not the in-memory fallback.

### 2. Redeploy-Interruption Test (Status Code Sequence)

Test protocol: send 30 requests → force production redeploy (`vercel --prod --force --yes`) → send 35 more requests. Rate limit: 60 requests per 120 seconds.

```
Phase 1 (pre-redeploy):
  Request 1:  200 [T+1.9s]
  Request 30: 200 [T+13.8s]

Redeploy: completed in 55.7s [T+69.5s]
Routing stabilized at T+72.5s
Remaining in window: 47.5s

Phase 2 (post-redeploy):
  Request 31: 200 [T+75.2s]
  Request 40: 200 [T+79.4s]
  Request 50: 200 [T+83.6s]
  Request 60: 200 [T+86.9s]
  Request 61: 429 RATE LIMITED [T+87.4s]
    Response: {'error': 'Rate limit exceeded. Too many requests.'}
```

**Verdict:** 429 at overall request #61, with total wall time 87.4s (within the 120s window).
An in-memory limiter would have reset to 0 after the redeploy and allowed 60 fresh requests before blocking. The counter carried over from 30 → 61, proving the state is genuinely stored in shared Upstash Redis.







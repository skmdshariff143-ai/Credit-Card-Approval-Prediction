# Error Audit Report — CreditGuard AI Stabilization

**Date:** July 3, 2026  
**Scope:** Full project audit — Python, Flask, HTML, CSS, JS, database, static assets, CI, dependencies  
**Objective:** Stabilize application without UI redesign  

---

## Executive Summary

| Metric | Before Audit | After Fixes |
|--------|-------------|-------------|
| Pytest suite | 108 passed | **108 passed** |
| Flask startup | OK | **OK** |
| `/api/predict` REST | OK | **OK** |
| Form prediction → result page | **Broken** (500/template crash) | **Fixed** |
| Profile update | **Broken** (405 Method Not Allowed) | **Fixed** |
| Password reset form | **Broken** (missing token in action URL) | **Fixed** |
| Static assets (`/static/css`, `/static/js`) | OK | **OK** |

---

## Critical Issues Fixed

### 1. Prediction Result Page Crash (CRITICAL)

**Severity:** Critical — blocked end-to-end prediction workflow  
**Location:** `app/templates/result.html` lines 118, 137  

**Symptom:** After submitting the credit application wizard, inference succeeded but the result page failed with:
```
Inference pipeline failure: type Undefined doesn't define __round__ method
```

**Root cause:** The LIME explainability engine returns feature attributions with key `impact`, but the template referenced `factor.weight`. Jinja2's `| round(3)` filter was applied to an `Undefined` value, raising an exception caught by the route handler and redirecting back to the form.

**Fix:** Changed `factor.weight` → `factor.impact` in both supporting-factors and risk-factors sections.

**Verification:** Unmocked POST to `/predict` now renders the result page with decision score and LIME attributions.

---

### 2. Profile Settings Form — Wrong POST Target (HIGH)

**Severity:** High — profile and password updates non-functional  
**Location:** `app/templates/auth/profile.html`, `app/routes/auth.py`  

**Symptom:** POST to `/auth/profile` returned **405 Method Not Allowed** because the route only accepts GET.

**Root cause:** Both profile and password forms posted to `url_for('auth.profile')` instead of `url_for('auth.profile_edit')`.

**Fix:**
- Updated both form `action` attributes to `auth.profile_edit`
- Extended `profile_edit()` to handle `form_type=password` with current-password verification and scrypt hash update
- Aligned password `minlength` to 8 characters (matching server validation)

**Verification:** Profile name/email update and password change both succeed with flash confirmation.

---

### 3. Password Reset Form — Missing Token in Action URL (HIGH)

**Severity:** High — password reset submissions would fail  
**Location:** `app/routes/auth.py` → `reset_password()`  

**Symptom:** Reset password form rendered with `action="/auth/reset-password/"` (empty token segment).

**Root cause:** `render_template("auth/reset_password.html", form=form)` did not pass `token=token` to the template, so `url_for('auth.reset_password', token=token)` produced an invalid URL.

**Fix:** Added `token=token` to the render_template call.

**Verification:** Form action now includes the full signed token path.

---

## Medium Issues Fixed

### 4. Health Endpoint — Duplicate Predictor Singleton (MEDIUM)

**Severity:** Medium — inconsistent model status reporting  
**Location:** `app/routes/routes.py` → `health()`  

**Root cause:** Health check imported `_predictor` from `src.models.predict` while the application loads models via `app.services.predict._predictor`. Two separate singletons could report different load states.

**Fix:** Unified health endpoint to use `app.services.predict._predictor`. Added missing `get_model_name()` to `src/models/predict.py` for backward compatibility with ML pipeline tests.

---

### 5. History Table Sort — `application_id` Silently Ignored (MEDIUM)

**Severity:** Medium — broken sort UX on history page  
**Location:** `app/database/database.py`  

**Root cause:** History UI offers sort-by Application ID, but `allowed_sorts` did not include `application_id`, causing fallback to default `id` sort.

**Fix:** Added `application_id` to `allowed_sorts` in both query methods.

---

### 6. Error Page — Missing Icon Library (LOW)

**Severity:** Low — broken icons on generic error page  
**Location:** `app/templates/error.html`  

**Root cause:** Template used Bootstrap Icons (`bi bi-*`) but the app only loads Font Awesome 6.

**Fix:** Replaced with equivalent Font Awesome icons (`fa-solid fa-triangle-exclamation`, `fa-solid fa-house`).

---

### 7. Seaborn Deprecation Warning (LOW)

**Severity:** Low — test/log noise, future breakage in Seaborn v0.14  
**Location:** `src/models/evaluate.py` line 123  

**Root cause:** `sns.barplot(..., palette="viridis")` without assigning `hue`.

**Fix:** Added `hue` parameter and `legend=False` per Seaborn v0.14 migration guidance.

---

## Issues Audited — No Change Required

| Area | Status | Notes |
|------|--------|-------|
| Flask routing | OK | All 16 templates present; blueprints registered correctly |
| Model artifacts | OK | `best_model.pkl`, `preprocessing_pipeline.pkl`, `encoder.pkl`, `scaler.pkl` present |
| SQLite database | OK | Schema migrations, indexes, user/prediction/report tables functional |
| Static CSS/JS | OK | `style.css` (28 KB), `main.js` (10 KB) serve with HTTP 200 |
| CDN assets | OK | Bootstrap 5.3.3, Font Awesome 6.5.1, Chart.js, AOS, GSAP load from CDN |
| Import graph | OK | No E9/F63/F7/F82 flake8 errors |
| REST API `/api/predict` | OK | Returns decision, probability, LIME explanation JSON |
| GitHub Actions CI | OK | Workflows for lint, test (3.10–3.13), Docker build, security, pages |
| Dependencies | OK | `requirements.txt` and `pip install -e .` compatible; no version conflicts detected |
| Auth (login/register) | OK | CSRF-protected forms; scrypt password hashing |
| Rate limiting | OK | Applied to health, admin stats, export endpoints |

---

## Code Smells Documented (Not Fixed — Out of Stabilization Scope)

1. **Duplicate `RiskPredictor` classes** in `app/services/predict.py` and `src/models/predict.py` — identical logic, two singletons. Recommend consolidating in a future refactor.
2. **Duplicate helper modules** — `app/utils/helper.py` and `src/utils/helper.py` are identical copies.
3. **SQLite ResourceWarning** — unclosed connection warning during test teardown; cosmetic, no functional impact.
4. **Test coverage gap** — `test_predict_page_post_success` mocks the predictor, so the `factor.weight` bug was not caught by CI. Recommend adding one integration test without mocks.
5. **setup.py vs requirements.txt drift** — `setup.py` omits `flask-wtf`, `flask-login`, etc.; CI installs both so no failure today.
6. **docs/ static site** — GitHub Pages HTML uses Bootstrap Icons without loading the BI stylesheet (separate from Flask app).

---

## Local Verification Checklist

| Check | Result |
|-------|--------|
| Flask starts on `http://127.0.0.1:5000` | ✓ |
| ML model pre-loaded at startup | ✓ |
| GET `/`, `/about`, `/health`, `/api/v1/health` | ✓ 200 |
| POST `/api/predict` (JSON) | ✓ Approved/Rejected + explanation |
| POST `/predict` (authenticated form) | ✓ Result page renders |
| `/static/css/style.css`, `/static/js/main.js` | ✓ 200 |
| Profile update via `/auth/profile/edit` | ✓ |
| Password change via profile form | ✓ |
| Reset password form action includes token | ✓ |
| Pytest 108/108 | ✓ |
| Seaborn deprecation warning | ✓ Resolved (38 warnings remain — sklearn/numpy only) |

---

## Files Modified

| File | Change |
|------|--------|
| `app/templates/result.html` | `factor.weight` → `factor.impact` (critical prediction fix) |
| `app/templates/auth/profile.html` | Form actions → `auth.profile_edit`; minlength 8 |
| `app/templates/auth/reset_password.html` | minlength 8 |
| `app/routes/auth.py` | Pass token to template; password change handler |
| `app/routes/routes.py` | Health endpoint uses app predictor singleton |
| `app/database/database.py` | Allow sort by `application_id` |
| `app/templates/error.html` | Font Awesome icons instead of Bootstrap Icons |
| `src/models/evaluate.py` | Seaborn hue/palette fix |
| `src/models/predict.py` | Added `get_model_name()` for API parity |

---

## Recommended Next Steps (Post-Stabilization)

1. Add an unmocked integration test for the full predict → result page flow.
2. Consolidate duplicate predictor and helper modules.
3. Add `flask-wtf`, `flask-login`, `email-validator` to `setup.py` install_requires.
4. Commit model `.pkl` artifacts or add a CI step to run `python src/main.py` when artifacts are absent.

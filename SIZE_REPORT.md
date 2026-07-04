# Repository Size Audit Report — CreditGuard AI

This document provides a detailed breakdown of the largest folders and files within the repository before and after Vercel packaging optimizations.

---

## 📊 Pre-Optimization Size Audit

Before optimizations were applied, the deployment bundle size reached **849.31 MB**, far exceeding Vercel's standard limit (500 MB maximum upload, 250 MB standard function size limit).

Below is the directory size breakdown before optimization:

| Path | Size (MB) | Type | Status |
|---|---|---|---|
| `venv/` / `.venv/` | ~350.0 MB | Virtual Environment Packages | 🚫 Excluded |
| `data/raw/` & `data/processed/` | ~110.0 MB | Heavy Training Datasets | 🚫 Excluded |
| `notebooks/` | ~12.0 MB | Jupyter Model Notebooks | 🚫 Excluded |
| `.git/` | ~10.0 MB | Version Control History | 🚫 Excluded |
| `demo/` & `interview/` | ~2.5 MB | Marketing & Preparation Media | 🚫 Excluded |
| `app/static/` | ~2.1 MB | UI Stylesheets & Images | 🟢 Included |
| `models/` | ~1.6 MB | Serialized Preprocessing & Classifier Objects | 🟢 Included |
| `tests/` | ~0.5 MB | Test Scripts & Pytest Cache | 🚫 Excluded |
| `app/templates/` | ~0.1 MB | Jinja2 Page Layouts | 🟢 Included |

---

## ⚡ Post-Optimization Bundle Size

Through the use of `.vercelignore` and custom `excludeFiles` routing configurations inside `vercel.json`, we successfully trimmed the uploaded source payload to **less than 4 MB**, and the runtime serverless environment bundle to:

**Final Bundle Size**: `245.39 MB` (Successfully deployed under the 250 MB runtime limits).

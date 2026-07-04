# Vercel Serverless Deployment Guide

This guide details the prerequisites, local verification steps, and deployment workflow for serving the CreditGuard AI Flask application on Vercel's serverless platform.

---

## ⚡ Deployment Prerequisites

- **Vercel CLI** installed (`npm install -g vercel`)
- **Python 3.10+** environment installed locally
- Git tracking main branch

---

## ⚙️ Configuration Files

### 1. Vercel Configuration (`vercel.json`)
The application is configured to build using Vercel's Python builder.
```json
{
  "version": 2,
  "builds": [
    {
      "src": "index.py",
      "use": "@vercel/python",
      "config": {
        "excludeFiles": "{data,notebooks,logs,diagrams,tests,docs,demo,interview,reports,resume,screenshots,src,credit_card_approval_prediction.egg-info,.pytest_cache,__pycache__,.github,.git,models/artifacts,models/trained}/**"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "index.py"
    },
    {
      "src": "/(.*)",
      "dest": "index.py"
    }
  ]
}
```

### 2. Ignore Configurations (`.vercelignore`)
To bypass Vercel's standard 250 MB size limit, non-essential files are excluded during upload:
```text
data/
notebooks/
logs/
diagrams/
tests/
docs/
/app.py
```

---

## 🧪 Local Verification Workflow

Before deploying, always test the serverless configuration locally:

1. **Verify relative imports**:
   ```bash
   python -c "import sys; sys.path.insert(0, '.'); from app.app import app; print('Imports pass')"
   ```
2. **Launch the server locally**:
   ```bash
   python index.py
   ```
3. Check that the console prints model pre-loading success statements and serves on `http://127.0.0.1:5000`.

---

## 🚀 Deployment Commands

Deploy the optimized application using Vercel CLI:

```bash
# Deploy preview build
vercel

# Promote to production
vercel --prod
```
Once complete, the CLI will output the URL and verify that the page returns `HTTP 200`.

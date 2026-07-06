# 7. Project Documentation

This document contains the complete SmartBridge internship documentation for this phase.

---

## 📚 REST API Reference

### 1. Get Health Check
*   **Endpoint**: `GET /health`
*   **Response**:
    ```json
    {
      "status": "healthy",
      "model_loaded": true,
      "pipeline_loaded": true,
      "timestamp": "2026-07-06T09:20:22Z"
    }
    ```

### 2. Post Scoring Prediction
*   **Endpoint**: `POST /api/predict`
*   **Payload**:
    ```json
    {
      "gender": "M",
      "car": "Y",
      "realty": "N",
      "children": 0,
      "income": 220000,
      "income_type": "Working",
      "education": "Higher education",
      "family_status": "Married",
      "housing": "House / apartment",
      "age": 42,
      "experience": 12.0,
      "phone": 1,
      "email": 1,
      "family_members": 2,
      "debt": 0.0
    }
    ```

---

## 🛠️ Deploy Configurations (`vercel.json`)
The routing setup for Vercel serverless execution:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ]
}
```

---

## 🔗 Documentation Links
* 📄 [DOCX Document](Project%20Documentation.docx)
* 📕 [PDF Document](Project%20Documentation.pdf)

---

### Navigation
* ⬅️ **Previous Section**: [6. Project Testing](../6.%20Project%20Testing/README.md)
* ➡️ **Next Section**: [8. Project Demonstration](../8.%20Project%20Demonstration/README.md)

# REST API Documentation

This document describes the versioned REST API endpoints provided by the **CreditGuard AI** portal.

---

## 1. Authentication & Rate Limits

- **Authentication:** Currently, endpoints do not require token authorization for public sandbox access.
- **Rate Limiting:** To ensure system stability, public endpoints are rate-limited using a sliding window:
  - Health check: Max 60 requests per minute.
  - History / Prediction: Max 30 requests per minute.
  - Exports: Max 10 requests per minute.

---

## 2. API Endpoints Reference

### Endpoint 2.1: System Health Check
Returns the current API system version, operational status, and loaded model details.

* **URL:** `/api/v1/health`
* **Method:** `GET`
* **Headers:** `Content-Type: application/json`
* **Response (Success - 200 OK):**
  ```json
  {
    "status": "healthy",
    "version": "1.0.0",
    "model_loaded": "logistic_regression",
    "timestamp": "2026-07-01 08:30:20"
  }
  ```

---

### Endpoint 2.2: Fetch Prediction Log History
Retrieves past customer credit assessment records stored in the SQLite database.

* **URL:** `/api/v1/history`
* **Method:** `GET`
* **Headers:** `Content-Type: application/json`
* **Response (Success - 200 OK):**
  ```json
  [
    {
      "id": 1,
      "timestamp": "2026-07-01 08:35:10",
      "decision": "Approved",
      "probability_percent": 84.50,
      "input": {
        "code_gender": "F",
        "cnt_children": 0,
        "cnt_fam_members": 2,
        "age_years": 35.0,
        "amt_income_total": 120000.0,
        "flag_own_car": "N",
        "flag_own_realty": "Y",
        "name_income_type": "Working",
        "name_education_type": "Higher education",
        "name_family_status": "Married",
        "name_housing_type": "House / apartment",
        "years_employed": 8.5,
        "flag_unemployed": 0,
        "occupation_type": "Managers",
        "flag_work_phone": 0,
        "flag_phone": 1,
        "flag_email": 0
      }
    }
  ]
  ```

---

### Endpoint 2.3: Run Credit scoring
Evaluates applicant details and computes approval probability and explainability attributions.

* **URL:** `/api/v1/predict`
* **Method:** `POST`
* **Headers:**
  - `Content-Type: application/json`
* **Request Payload Example:**
  ```json
  {
    "code_gender": "M",
    "cnt_children": 0,
    "cnt_fam_members": 2,
    "age_years": 42.0,
    "amt_income_total": 95000.0,
    "flag_own_car": "Y",
    "flag_own_realty": "Y",
    "name_income_type": "Commercial associate",
    "name_education_type": "Secondary / secondary special",
    "name_family_status": "Married",
    "name_housing_type": "House / apartment",
    "years_employed": 12.0,
    "flag_unemployed": 0,
    "occupation_type": "Drivers",
    "flag_work_phone": 1,
    "flag_phone": 0,
    "flag_email": 1
  }
  ```
* **Response (Success - 200 OK):**
  ```json
  {
    "decision": "Approved",
    "approval_probability_percent": 91.24,
    "explanation": {
      "intercept": 0.125,
      "risk_factors": [
        { "feature": "Years Employed", "impact": 0.12 }
      ],
      "support_factors": [
        { "feature": "Annual Income", "impact": -0.85 }
      ]
    }
  }
  ```
* **Response (Client Error - 400 Bad Request):**
  ```json
  {
    "error": "Input verification failed. Missing fields: {'code_gender'}"
  }
  ```

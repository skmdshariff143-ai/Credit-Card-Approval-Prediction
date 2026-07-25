# REST API Documentation

This document describes the routing endpoints, request parameters, JSON payloads, and response structures for the CreditGuard AI scoring server.

---

## 1. Web Views Routing

| Route | Method | Description |
| :--- | :--- | :--- |
| **`/`** | `GET` | Landing home page of the Credit Card platform. |
| **`/about`** | `GET` | General project overview, business definition, and model scores. |
| **`/predict`** | `GET` | Application form interface (WTForms fields). |
| **`/predict`** | `POST` | Processes form inputs, runs model scoring, and renders results. |
| **`/history`** | `GET` | Dashboard displaying the log of last 50 decisions. |

---

## 2. Health Monitoring API

### `GET /health`
Returns the status, version, loaded model, and timestamp.

#### Response Example (JSON - 200 OK):
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": "logistic_regression",
  "timestamp": "2026-06-29 17:45:00"
}
```

---

## 3. Scoring REST API

### `POST /api/predict`
Calculates credit delinquency risk for a single applicant record.

#### Request Headers:
- `Content-Type: application/json`

#### Request Payload Example:
```json
{
  "code_gender": "M",
  "cnt_children": 0,
  "cnt_fam_members": 2,
  "age_years": 35.0,
  "amt_income_total": 150000.0,
  "flag_own_car": "Y",
  "flag_own_realty": "Y",
  "name_income_type": "Working",
  "name_education_type": "Higher education",
  "name_family_status": "Married",
  "name_housing_type": "House / apartment",
  "years_employed": 5.5,
  "flag_unemployed": 0
}
```

#### Response Example (JSON - 200 OK):
```json
{
  "decision": "Approved",
  "approval_probability_percent": 98.54
}
```

#### Error Response Example (JSON - 400 Bad Request):
```json
{
  "error": "Age must be between 18 and 120 years."
}
```

# IBM Cloud & Watson Machine Learning Deployment Guide

This guide details the step-by-step instructions to deploy the credit classification model to IBM Watson Machine Learning.

---

## Step 1: Create IBM Cloud Account & Watson Studio Instance
1. Sign up for an account at [IBM Cloud](https://cloud.ibm.com).
2. Provision a **Watson Machine Learning** (WML) service instance from the Catalog.
3. Access Watson Studio and create a new **Deployment Space** (e.g. `CreditGuard-Space`).

---

## Step 2: Configure Local Credentials
Set the following variables inside your local `.env` file:
- `IBM_API_KEY`: Generate an IBM API Key from **Manage > Access (IAM) > API keys**.
- `IBM_REGION`: Cloud WML endpoint location (e.g., `us-south` or `eu-de`).
- `IBM_SPACE_ID`: Under your deployment space settings tab, copy the Space GUID.

---

## Step 3: Run Model Upload Script
Execute the deployment runner script from the project root:
```bash
python deploy_ibm.py
```
This script initializes WML client credentials, formats model details, and uploads `best_model.pkl` to the space.

---

## Step 4: Verify Scoring Endpoint
Once uploaded, retrieve the REST Scoring endpoint from the IBM Cloud Space dashboard.
Use the scoring URL to post JSON scoring payloads directly to Watson ML for sub-millisecond credit rating queries!

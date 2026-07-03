# Deployment Guide: Credit Card Approval Prediction

This guide provides step-by-step instructions for running and deploying the **CreditGuard AI** application locally, in Docker containers, and on the IBM Cloud.

---

## 1. Local Development Setup

### Prerequisites
- Python 3.10+
- Anaconda / Jupyter (optional)

### Steps
1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd e:\Credit-Card-Approval-Prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Generate synthetic datasets (if raw files are not present):**
   ```bash
   python generate_mock_data.py
   ```

4. **Run the training and tuning pipeline:**
   ```bash
   python src/main.py
   ```
   This will train all four classifiers (Logistic Regression, Decision Tree, Random Forest, XGBoost), tune their parameters, run cross-validation, save metric comparison plots under `screenshots/models/`, and serialize the best model as `models/best_model.pkl`.

5. **Start the Flask web application:**
   ```bash
   python app/app.py
   ```
   Access the web interface at: `http://localhost:5000`

---

## 2. Containerization with Docker

### Prerequisites
- Docker Desktop installed and running.

### Steps
1. **Build the production Docker image:**
   ```bash
   docker build -t creditguard-ai:latest .
   ```

2. **Run the container locally:**
   ```bash
   docker run -p 5000:5000 --env-file .env creditguard-ai:latest
   ```

3. **Verify the container:**
   Access the web app at `http://localhost:5000`. You can check the container status and logs:
   ```bash
   docker ps
   docker logs <container_id>
   ```

---

## 3. IBM Cloud Watson Machine Learning Deployment

### Prerequisites
- Active IBM Cloud Account.
- Provisioned instance of **Watson Machine Learning**.
- A created **Deployment Space** in Watson ML.

### Steps
1. **Retrieve credentials:**
   - **IBM Cloud API Key:** Generate an API Key under IAM settings in IBM Cloud console.
   - **Watson ML Instance URL:** Check your Watson ML service instance details (e.g., `https://us-south.ml.cloud.ibm.com`).
   - **Space ID:** Copy the UID of your Watson ML deployment space from the space settings dashboard.

2. **Configure the Environment:**
   Update your local `.env` file with your IBM credentials:
   ```env
   IBM_API_KEY=your_actual_ibm_cloud_api_key
   IBM_URL=https://us-south.ml.cloud.ibm.com
   IBM_SPACE_ID=your_watson_ml_space_id
   ```

3. **Deploy the best model to the cloud:**
   Run the deployment script:
   ```bash
   python deploy_ibm.py
   ```
   This script registers the best model from `models/` with Watson ML and provisions an online scoring service. It will output the `Scoring Endpoint URL` (e.g. `https://us-south.ml.cloud.ibm.com/ml/v4/deployments/.../predictions`).

---

## 4. Vercel Serverless Deployment

### Prerequisites
- Active [Vercel](https://vercel.com) account.
- Vercel CLI installed (`npm install -g vercel`) or GitHub repository connected.

### Configuration
The project is fully pre-configured for Vercel deployment using the root [vercel.json](file:///e:/Credit-Card-Approval-Prediction/vercel.json) file:
- **Runtime**: `@vercel/python` serverless engine
- **WSGI Entrypoint**: [app/app.py](file:///e:/Credit-Card-Approval-Prediction/app/app.py)

### Steps
1. **Deploy using Vercel CLI**:
   From the repository root, run:
   ```bash
   vercel
   ```
   Follow the prompts to link the project.
2. **Configure Environment Variables**:
   In your Vercel Dashboard under **Settings > Environment Variables**, add:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `<your-secure-random-key>`
   - `VERCEL`: `1` (Automatically set by Vercel, but good to configure for local Vercel emulators)
3. **Promote to Production**:
   Run:
   ```bash
   vercel --prod
   ```
   Alternatively, connect your GitHub repository directly to Vercel for automated deployments on every `push` to the `main` branch.


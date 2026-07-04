# Installation Guide

This document describes how to install the required environment, configure settings, and prepare the database and model binaries for **CreditGuard AI**.

---

## 1. Prerequisites

Before installing, ensure your machine has the following tools:
- **Python 3.10 or 3.11** (recommended version is 3.10).
- **Git** (for version control).
- **Docker Desktop** (optional, for containerized execution).
- **Pip** (Python package installer).

---

## 2. Step-by-Step Installation

### Step 2.1: Clone the Repository
Clone this repository to your local system and navigate to the root directory:
```bash
git clone https://github.com/skmdshariff143-ai/Credit-Card-Approval-Prediction.git
cd Credit-Card-Approval-Prediction
```

### Step 2.2: Setup Virtual Environment
It is highly recommended to use a virtual environment to prevent package version conflicts:
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 2.3: Install Package Dependencies
Install the required packages listed in `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### Step 2.4: Configure Environment Settings
Create a `.env` file in the root directory by copying the sample config:
```bash
copy .env.example .env
```
Open `.env` and verify the settings:
```env
FLASK_ENV=development
SECRET_KEY=dev_secret_key_12345
LOG_LEVEL=INFO
```

### Step 2.5: Train Model Binaries
Run the pipeline script to ingest raw data, preprocess variables, train models, and serialize the best candidate model:
```bash
python src/main.py
```
Verify that the output binaries are created:
- `models/best_model.pkl`
- `models/scaler.pkl`
- `models/encoder.pkl`
- `models/preprocessing_pipeline.pkl`

---

## 3. Running the Server

Start the local Flask development server:
```bash
python app/app.py
```
Open your browser and navigate to `http://localhost:5000` to access the portal!

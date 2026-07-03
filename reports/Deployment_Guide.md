# Deployment Guide

Detailed step-by-step setup guides are provided below.

## 1. Local Serving
1. Clone the repository and navigate to workspace:
   ```bash
   cd e:\Credit-Card-Approval-Prediction
   ```
2. Setup environment and install packages:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
3. Run complete ML pipeline:
   ```bash
   python src/main.py --tune
   ```
4. Start Flask server:
   ```bash
   python app/app.py
   ```

## 2. Docker container serving
1. Build local image:
   ```bash
   docker build -t creditguard-ai:latest .
   ```
2. Start container:
   ```bash
   docker run -p 5000:5000 --env-file .env creditguard-ai:latest
   ```

## 3. IBM Watson ML deployment
1. Configure credentials inside `.env` file:
   ```env
   IBM_API_KEY=your_key
   IBM_URL=https://us-south.ml.cloud.ibm.com
   IBM_SPACE_ID=your_space_id
   ```
2. Execute deployment runner:
   ```bash
   python src/deployment/deploy.py
   ```

## 4. Vercel Serverless Deployment
1. Install Vercel CLI (`npm install -g vercel`) and log in.
2. Link repository:
   ```bash
   vercel
   ```
3. Set environment variable configurations in Vercel settings panel:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `<production_secret>`
4. Deploy to production:
   ```bash
   vercel --prod
   ```


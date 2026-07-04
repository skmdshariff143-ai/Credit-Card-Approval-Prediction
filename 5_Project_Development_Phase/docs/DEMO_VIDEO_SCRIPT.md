# Demo Video Script: CreditCard Approval Prediction

**Duration:** ~3 Minutes
**Presenter:** Mahammad Shariff Shaik

---

## Scene 1: Introduction & Problem Statement (~45 Seconds)
- **Visual:** Screen sharing the repository homepage (`README.md` and file tree). Presenter's camera in the corner.
- **Audio (Script):**
  > "Hello everyone! My name is Mahammad Shariff Shaik, and today I'm presenting my end-to-end Machine Learning project: Credit Card Approval Prediction.
  > In the banking sector, automated risk evaluation is critical. Manual reviews are slow and error-prone. This project delivers a production-grade machine learning system that automates credit application approvals. 
  > We utilize the Kaggle Credit Card Approval dataset, joining demographic application profiles with monthly repayment records, defining credit risk based on historical delinquencies of 60 days or more."

---

## Scene 2: Pipeline Architecture & Code Walkthrough (~60 Seconds)
- **Visual:** Showing VS Code. Opening `config/config.yaml`, `src/pipeline/ml_pipeline.py`, and training logs or a Jupyter notebook.
- **Audio (Script):**
  > "Here is our codebase, designed with clean modular architecture. We manage parameters centrally in `config.yaml`.
  > Our end-to-end machine learning pipeline covers: Ingestion, schema validation, cleaning, and custom feature engineering. Since credit datasets are heavily imbalanced, we apply SMOTE to balance the training split.
  > We train and compare four algorithms: Logistic Regression, Decision Tree, Random Forest, and XGBoost. The pipeline uses cross-validated grid search to optimize F1-score, and automatically registers the best model in our model registry with full metadata."

---

## Scene 3: Flask Application & Predictions (~45 Seconds)
- **Visual:** Transition to browser. Renders the local Flask app page `http://localhost:5000`. Fill in sample low-risk applicant inputs, hit submit, show approval page. Then go back, fill in high-risk applicant inputs, show rejection page.
- **Audio (Script):**
  > "Let's see the application in action. This is our Flask web application, styled with a premium dark theme and responsive layout. 
  > Let's enter a low-risk profile: high annual income, higher education, and 8 years of active employment. When we submit, client-side validation triggers, followed by backend inference. 
  > The application is Approved with a 94% confidence level. 
  > Now, if we submit an applicant with low income and a prior history of job instability, the model evaluates this as high-risk and recommends rejection."

---

## Scene 4: Conclusion & Cloud Deployment (~30 Seconds)
- **Visual:** VS Code. Showing `Dockerfile` and `deployment/ibm_cloud/deploy.py`.
- **Audio (Script):**
  > "The codebase is fully containerized using Docker and utilizes GitHub Actions for CI/CD linting and tests. We also provide integration scripts to register and deploy this model to the IBM Cloud using Watson Machine Learning.
  > Thank you for watching my demonstration! The complete codebase, along with detailed documentation and deployment guides, is available on my GitHub repository. I look forward to your questions."

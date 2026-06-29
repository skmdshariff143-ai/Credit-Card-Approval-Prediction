# Demo Video Script

**Duration**: ~3 Minutes  
**Presenter**: Mahammad Shariff Shaik  

---

## Scene 1: Introduction & Problem Statement (~45 Seconds)
- **Visual**: Show repo landing page in browser.
- **Presenter Script**:
  > "Hello! Today I'm demonstrating CreditGuard AI, an end-to-end Machine Learning system that predicts credit card approval status. 
  > We evaluate credit risk based on demographic data and monthly payment history. 
  > Rejections are defined as having late payments of 60 days or more."

---

## Scene 2: Code Walkthrough (~60 Seconds)
- **Visual**: Show VS Code editor configurations and ML pipelines.
- **Presenter Script**:
  > "Our system follows enterprise-grade modular coding standards. 
  > We centrally manage configuration settings in `configs/config.py` and constants in `configs/constants.py`.
  > Our preprocessing pipeline wraps missing value imputation, IQR outlier capping, categorical encoding, and standardization.
  > We train and compare Logistic Regression, Decision Trees, Random Forests, and XGBoost, registering the best model in the model registry."

---

## Scene 3: Live Application Demo (~45 Seconds)
- **Visual**: Show Flask web application form. Submit low-risk and high-risk applications.
- **Presenter Script**:
  > "Let's test the web app. We fill in a low-risk applicant profile. 
  > Upon submission, client-side validation triggers, followed by ML prediction. 
  > The system recommends Approval with high confidence. 
  > For a high-risk profile, the system flags the applicant and recommends Rejection."

---

## Scene 4: Docker & Cloud Integration (~30 Seconds)
- **Visual**: Show Dockerfile and deploy.py.
- **Presenter Script**:
  > "The app is containerized using Docker and uses GitHub Actions for continuous integration. 
  > We also include python deployment scripts to register and host this model on IBM Watson Machine Learning."

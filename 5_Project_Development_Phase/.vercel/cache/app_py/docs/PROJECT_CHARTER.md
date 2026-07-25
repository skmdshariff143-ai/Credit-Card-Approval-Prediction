# Project Charter: Credit Card Approval Prediction

## 1. Project Overview
- **Name:** Credit Card Approval Prediction
- **Objective:** Build an end-to-end machine learning system to automate the credit card application approval process. The model predicts whether an applicant will be a "good" or "bad" client based on their demographics, financial background, and credit history.
- **Audience:** Skill Wallet Submission, GitHub Portfolio, Resume Project, IBM Cloud deployment.

## 2. Business Requirements
- **High Accuracy & Interpretability:** The system must predict creditworthiness accurately while maintaining interpretability (via Logistic Regression and Decision Trees) alongside high-performance ensemble models (Random Forest, XGBoost).
- **Automation:** Reduce the manual screening overhead for credit applications by auto-approving low-risk applicants and flagging high-risk applicants for review.
- **Auditable System:** All steps—from data collection, cleaning, and model evaluation to deployment—must be documented, versioned, and auditable.

## 3. Technology Stack
- **Languages:** Python 3.10+
- **Data Engineering:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn, XGBoost, Imbalanced-learn (for SMOTE)
- **Deployment:** Flask (Web App), Docker (Containerization), IBM Cloud & Watson Machine Learning
- **CI/CD:** GitHub Actions
- **Testing:** Pytest

## 4. Key Milestones & Workflow
1. **Phase 1: Project Planning:** Define objectives, scope, architecture, and timeline. (Current)
2. **Phase 2: Repository Structure:** Establish a production-grade folder layout.
3. **Phase 3: Environment Setup:** Package requirements, settings, custom logging, and exception handling.
4. **Phase 4: Dataset Collection:** Build the data ingestion pipeline for application and credit history records.
5. **Phase 5: EDA:** Perform descriptive statistics, distribution plotting, and correlation analysis.
6. **Phase 6: Data Cleaning:** Handle duplicates, anomalous fields (e.g., negative employment days), and missing values. Merge records and define labels.
7. **Phase 7: Feature Engineering:** Feature scaling, categorical encoding, class imbalance handling (SMOTE), and selection.
8. **Phase 8: Model Training:** Train Logistic Regression, Decision Tree, Random Forest, and XGBoost.
9. **Phase 9: Model Evaluation:** Compare models using F1, ROC-AUC, Recall, and Precision. Export results.
10. **Phase 10: Flask Application:** Develop user-friendly interface with input forms and REST API endpoint.
11. **Phase 11: Unit Testing:** Validate each module using Pytest.
12. **Phase 12: Documentation:** Write the final Project Report, README, Diagrams, and Deployment Guides.
13. **Phase 13: GitHub CI/CD:** Establish workflows to lint and run tests automatically.
14. **Phase 14: IBM Cloud Deployment:** Package with Docker and write Watson Machine Learning integration code.
15. **Phase 15: Final Audit:** Complete validation checklist and review the codebase.

## 5. Risks and Mitigations
- **Data Imbalance:** Credit approval datasets typically contain highly imbalanced classes (few defaults). *Mitigation:* Apply SMOTE (Synthetic Minority Over-sampling Technique) or class weighting, and use F1/ROC-AUC as evaluation metrics instead of accuracy.
- **Feature Anonymization / Integrity:** Data might contain weird formats (like negative values for age/employment in days). *Mitigation:* Explicit cleanup and validation layer during data loading.
- **Deployment Failures:** Differences between local testing and cloud environment. *Mitigation:* Dockerize the application to ensure environmental parity.

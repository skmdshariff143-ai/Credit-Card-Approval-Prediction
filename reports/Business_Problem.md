# Business Problem Statement & Understanding

## 1. Domain Background
In retail banking, credit card issuance represents a key revenue generator but also exposes financial institutions to credit default risks. Manually reviewing every application is slow, expensive, and subject to human bias.

## 2. Objective
To construct an automated, high-confidence risk screening tool (**CreditGuard AI**) that determines whether to approve or reject card applications in real-time.

## 3. Delinquency & The Cost of Errors
The system classifies applicants into binary target classes based on their monthly repayment status. Grouping history profiles identifies:
- **Class 0 (Approved)**: Low credit risk profiles.
- **Class 1 (Rejected)**: High risk of default (late payment of 60+ days).

### Cost of Machine Learning Errors:
1. **False Positives (Bad Approval)**:
   - *Scenario*: Model approves a high-risk applicant (Class 1 predicted as Class 0).
   - *Business Cost*: Extremely high. Leads to credit write-offs, default collections expenses, and direct loss of principal capital.
2. **False Negatives (Bad Rejection)**:
   - *Scenario*: Model rejects a low-risk applicant (Class 0 predicted as Class 1).
   - *Business Cost*: Medium. Represents opportunity cost from lost interest revenues, annual card fees, and transaction commissions, alongside potential customer frustration.

Thus, the evaluation objective is to maximize **Recall/F1-Score** for Class 1 (rejections) to capture defaults, while preserving high overall efficiency.

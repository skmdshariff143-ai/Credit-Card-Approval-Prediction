# Future Product Roadmap

This document outlines the planned extensions and next-step enhancements to scale the CreditGuard AI credit rating engine.

---

## 1. Credit History Sequence Windowing
- **Goal**: Incorporate billing patterns and sequence time-series variables to predict change in defaults risk over time.
- **Approach**: Train LSTMs or TabNet models on monthly repayment logs directly rather than relying on aggregated target codes.

---

## 2. LLM Risk Explanations (Explainable AI)
- **Goal**: Provide user-friendly natural language justifications for approvals/rejections.
- **Approach**: Feed model feature coefficients and stability indices into a local Llama/Gemini model to output descriptive recommendation letters for the applicant.

---

## 3. Data Drift Monitoring
- **Goal**: Detect changes in incoming applicant profiles compared to the training set distribution.
- **Approach**: Set up an automated monitoring suite using Evidently AI to calculate population stability indices (PSI).

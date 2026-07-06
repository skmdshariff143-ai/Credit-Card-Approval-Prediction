# 3. Project Design Phase

This document contains the complete SmartBridge internship documentation for this phase.

---

## 📐 Problem Solution Fit

CreditGuard AI maps retail banking problems directly to machine learning solutions:

| Identified Problem | Proposed System Solution | Core Engineering Method |
| :--- | :--- | :--- |
| High Default Rates | Maximize prediction Recall | SMOTE balancing and XGBoost training |
| Black-Box Scores | Explainable AI (XAI) dashboard | Ridge Local Surrogate Coefficients |
| Database Lockouts | Temp path configuration | Dynamic TempDir routing for serverless |

---

## ⚙️ Proposed Solution Architecture

The system utilizes an MVC layout preloading preprocessors and pipelines at start:

<p align="center">
  <img src="../../docs/assets/images/system_architecture.png" width="700" alt="System Architecture">
</p>

### ER Diagram Layout
Database schemas managing user logins and prediction histories:

<p align="center">
  <img src="../../docs/assets/images/er_diagram.png" width="700" alt="ER Diagram">
</p>

---

## 🔗 Documentation Links
* 📄 [DOCX Document](Proposed%20Solution.docx)
* 📕 [PDF Document](Proposed%20Solution.pdf)

---

### Navigation
* ⬅️ **Previous Section**: [2. Requirement Analysis](../2.%20Requirement%20Analysis/README.md)
* ➡️ **Next Section**: [4. Project Planning Phase](../4.%20Project%20Planning%20Phase/README.md)

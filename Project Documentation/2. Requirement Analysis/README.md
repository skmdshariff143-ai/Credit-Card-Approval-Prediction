# 2. Requirement Analysis

This document contains the complete SmartBridge internship documentation for this phase.

---

## 🚶 Customer Journey Map

The journey of an applicant and risk officer maps the process from scoring onboarding to assessment validation:

| Phase | Touchpoint | User Action | User Feeling | Operational Pain Point |
| :--- | :--- | :--- | :---: | :--- |
| **Onboarding** | Web Browser | Registers secure account | Hopeful | Password security risks |
| **Application** | 4-step wizard form | Enters demographic facts | Anxious | Form length validation lags |
| **Processing** | Inference service | Preprocesses parameters | Eager | Opaque black-box outputs |
| **Result** | Gauges dashboard | Reviews LIME attributions | Reassured | Lack of printable backups |

---

## 📐 Data Flow Diagram (DFD)

The data flows from user forms through validation layers to inference services and logs persistence:

<p align="center">
  <img src="../../docs/assets/images/data_flow_diagram.png" width="700" alt="Data Flow Diagram">
</p>

---

## 🛡️ Functional & Non-Functional Requirements

### Functional Requirements
1. **User Authentication**: Secure scrypt registry with boundaries controls (Admin, Officer, User).
2. **Dynamic Wizard**: Interactive 4-step application wizard with validation checks.
3. **Telemetry Console**: Operations charts mapping database metrics.
4. **Log Ledgers**: Database logs query table with sort and search options.

### Non-Functional Requirements
- **Latency**: Scoring results returned under 15ms.
- **Security**: Zero medium/high Bandit compile alerts.
- **Portability**: Complete stateless Vercel Serverless configuration with `/tmp` writes.

---

## 🔗 Documentation Links
* 📄 [DOCX Document](Customer%20Journey%20Map.docx)
* 📕 [PDF Document](Customer%20Journey%20Map.pdf)

---

### Navigation
* ⬅️ **Previous Section**: [1. Brainstorming & Ideation](../1.%20Brainstorming%20&%20Ideation/README.md)
* ➡️ **Next Section**: [3. Project Design Phase](../3.%20Project%20Design%20Phase/README.md)

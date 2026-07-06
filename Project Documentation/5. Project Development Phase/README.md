# 5. Project Development Phase

This document contains the complete SmartBridge internship documentation for this phase.

---

## 📁 Code Layout & Reusability

The backend codebase is structured modularly:
*   `app/database/`: SQLite schema initialization and users table creation.
*   `app/routes/`: Route controllers (`auth.py`, `api.py`, `dashboard.py`).
*   `app/services/`: Preloaded model singletons and LIME mathematical explainers.
*   `app/static/`: Design tokens, wizard controller engines, and Chart.js metrics.

---

## ⚙️ Coding & Preprocessing Solutions

Below is the dynamic preprocessor configuration in `src/preprocessing/pipeline.py`:

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

class PreprocessingPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.medians = {}
        
    def fit(self, X, y=None):
        # Compute column medians and scale
        for col in X.select_dtypes(include=[np.number]):
            self.medians[col] = X[col].median()
        return self
```

---

## 🔮 Functional Features & Screenshots

### 1. Operations Dashboard
Telemetry console widgets track total requests:

<p align="center">
  <img src="../../docs/assets/images/dashboard.png" width="600" alt="Telemetry Dashboard">
</p>

### 2. Onboarding Wizard
The 4-step credit application form validation:

<p align="center">
  <img src="../../docs/assets/images/prediction_form.png" width="600" alt="Onboarding Wizard">
</p>

---

## 🔗 Documentation Links
* 📄 [DOCX Document](Coding%20&%20Solution.docx)
* 📕 [PDF Document](Coding%20&%20Solution.pdf)

---

### Navigation
* ⬅️ **Previous Section**: [4. Project Planning Phase](../4.%20Project%20Planning%20Phase/README.md)
* ➡️ **Next Section**: [6. Project Testing](../6.%20Project%20Testing/README.md)

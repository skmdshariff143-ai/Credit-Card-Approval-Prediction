# Known Issues & Workarounds

This document outlines the known system limitations and libraries warnings for the CreditGuard AI workspace.

---

## 1. IBM Watson ML Simulated Access
- **Description**: The IBM Watson Machine Learning credentials inside `.env` default to mock keys for testing.
- **Workaround**: If provisioning a real Watson space instance, make sure to replace `IBM_API_KEY`, `IBM_SPACE_ID`, and the region endpoints inside the local `.env` file before executing `deploy_ibm.py`.

---

## 2. Scikit-Learn 1.6 / XGBoost Compatibility
- **Description**: Running GridSearch or CV on XGBoost models under Python 3.13 can cause MRO resolution failures (`AttributeError: 'super' object has no attribute '__sklearn_tags__'`).
- **Workaround**: We resolved this by isolating scikit-learn tags delegators inside a dedicated compatibility module (`src/utils/sklearn_compat.py`) imported globally.

---

## 3. SQLite Database Ephemeral Persistence on Vercel
- **Description**: Vercel executes application instances in stateless, serverless environments. The SQLite database stored inside `/tmp` is ephemeral and resets during cold starts.
- **Workaround**: The application includes a UI banner when running on Vercel informing the user of the periodic session resets. For persistent production use, migrate to a hosted database (such as PostgreSQL or Turso) by configuring a `DATABASE_URL` connection.


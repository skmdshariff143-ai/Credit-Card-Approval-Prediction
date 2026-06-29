# CreditGuard AI - Comprehensive Interview Q&A

This guide contains key technical interview questions and answers mapping Machine Learning, Flask backend, Python coding, and project-specific architectures.

---

## 1. Machine Learning Engineering Questions (Top 5)

### Q1: Why did you prioritize Recall over Accuracy or Precision for this banking project?
*Answer*: In credit risk management, a False Negative (approving an applicant who eventually defaults) is significantly more expensive than a False Positive (subjecting a low-risk applicant to manual review). Accuracy is misleading under a 92.5% skewed class balance. Thus, Recall is our primary target metric.

### Q2: How did you handle the severe class imbalance in the training data?
*Answer*: We applied random oversampling of the default class (Class 1) exclusively on the training split. Applying oversampling before splitting would cause data leakage from the test set.

### Q3: Explain why Logistic Regression outperformed tree ensembles on the test set.
*Answer*: Tree models (Random Forest, XGBoost) partitioned the feature space tightly, overfitting the majority class. Logistic Regression with balanced weights adjusted the linear decision boundary threshold globally, achieving a test Recall of 66.67%.

### Q4: What is the purpose of Gini Importance in Random Forest?
*Answer*: It measures the total reduction in node impurity (Gini index) contributed by a feature across all trees in the ensemble. It ranks features by predictive strength.

### Q5: Why did you cap income at 1.5 IQR limits?
*Answer*: Income has a skewed log-normal tail. Extreme values skew standard scaling, distorting linear decision boundaries. Capping limits this distortion.

---

## 2. Flask & Web Development Questions (Top 5)

### Q1: Explain the Application Factory pattern in Flask.
*Answer*: It defines application initialization inside a function (e.g. `create_app()`) returning the `app` instance. This prevents global app imports and enables config switching for testing.

### Q2: Why did you use Flask Blueprints?
*Answer*: Blueprints organize routes, templates, and static folders into modular sub-modules, preventing route pollution in `app.py`.

### Q3: How does WTForms CSRF protection work?
*Answer*: It injects a hidden token into HTML forms matched against a session key, preventing Cross-Site Request Forgery attacks.

### Q4: Explain the difference between Gunicorn and Flask's development server.
*Answer*: Flask's default server is single-threaded and not designed for concurrent traffic. Gunicorn is a WSGI server that spins up multiple worker processes.

### Q5: How do you handle custom 404 and 500 errors in Flask?
*Answer*: We register handlers using `@app.errorhandler(code)` returning custom template views.

---

## 3. Python Coding & Architecture Questions (Top 5)

### Q1: How did you resolve the XGBoost MRO scikit-learn 1.6 bug?
*Answer*: We dynamically patched `ClassifierMixin.__sklearn_tags__` at startup to safely delegate tags to `BaseEstimator` and avoid MRO lookup failures on python 3.13.

### Q2: What is the difference between joblib and pickle for model serialization?
*Answer*: Joblib is optimized for storing large numpy arrays (such as model weights) efficiently, making it faster than standard pickle.

### Q3: How do you prevent data leakage during scaling?
*Answer*: We call `.fit()` only on the training split, and apply `.transform()` on test/inference data.

### Q4: Explain Python's type hints and their benefits.
*Answer*: Type hints specify expected argument types (e.g. `df: pd.DataFrame`), assisting static code analyzers (like MyPy) and improving readability.

### Q5: What is the benefit of using `sys.path.append` at script startup?
*Answer*: It guarantees python finds import statements relative to the project root, regardless of the script's execution folder.

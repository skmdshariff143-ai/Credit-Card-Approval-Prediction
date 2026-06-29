# CreditGuard AI - Comprehensive Interview Q&A

This guide contains key technical interview questions and answers mapping Machine Learning, Flask backend, Python coding, and project-specific architectures.

---

## 1. Machine Learning Engineering Questions (100 Q&As)

### Q1: Why did you prioritize Recall over Accuracy or Precision for this credit risk project?
*Category*: Imbalance & Splitting

*Answer*: In credit risk modeling, approving a defaulter (False Negative) costs the bank significantly more than rejecting a creditworthy applicant (False Positive). Since the dataset is highly imbalanced (e.g., 92.5% approved vs. 7.5% defaulted), Accuracy is highly misleading. Recall directly measures the proportion of actual defaults caught, making it the primary optimization target.

### Q2: How did you handle the severe class imbalance in your dataset?
*Category*: Imbalance & Splitting

*Answer*: We utilized random oversampling of the minority (default) class on the training dataset. We avoided applying it on the test set or before cross-validation to prevent data leakage and ensure realistic model evaluation.

### Q3: What is data leakage and how did your pipeline prevent it?
*Category*: Imbalance & Splitting

*Answer*: Data leakage occurs when information from the target or test set is inadvertently used during training. We prevented leakage by fitting all preprocessing transformations (imputers, scalers, encoders) solely on the training fold, and then applying the fitted transformations to the validation and test splits.

### Q4: Explain the difference between K-Fold and Stratified K-Fold cross-validation.
*Category*: Imbalance & Splitting

*Answer*: K-Fold splits the dataset randomly into K folds. Stratified K-Fold ensures that each fold contains approximately the same percentage of samples of each target class as the complete set. Stratified K-Fold is essential for imbalanced classification to prevent folds with zero minority class representatives.

### Q5: What are the drawbacks of using SMOTE (Synthetic Minority Over-sampling Technique) compared to random oversampling?
*Category*: Imbalance & Splitting

*Answer*: SMOTE generates synthetic samples along the line segments joining k-nearest neighbors of the minority class. Its drawback is that it can exacerbate noise and create unrealistic data points if minority samples are interspersed with majority class noise, leading to class overlaps.

### Q6: Why is it incorrect to evaluate a model on an oversampled test dataset?
*Category*: Imbalance & Splitting

*Answer*: Oversampling the test set artificially alters the class distribution, violating the assumption that the test set reflects the real-world data distribution. This leads to overly optimistic performance metrics that fail to generalize to production.

### Q7: How does under-sampling compare to over-sampling for class imbalance?
*Category*: Imbalance & Splitting

*Answer*: Under-sampling discards majority class samples to balance the dataset, which saves training time but throws away valuable information. Over-sampling duplicates or synthesizes minority class samples, preserving all data but increasing computational complexity and risk of overfitting.

### Q8: What is class-weight balancing and how is it implemented in Scikit-Learn?
*Category*: Imbalance & Splitting

*Answer*: Class-weight balancing adjusts the loss function's cost associated with misclassifying different classes. In Scikit-Learn, setting `class_weight='balanced'` automatically assigns weights inversely proportional to class frequencies, forcing the optimizer to penalize minority class errors more heavily.

### Q9: How does the choice of class balancing affect the decision threshold of a classifier?
*Category*: Imbalance & Splitting

*Answer*: Balancing shifts the model's internal probability outputs. Without balancing, a model might require a probability > 0.5 to predict default. With balancing or threshold tuning, the decision boundary is calibrated to optimize Recall, often lowering the threshold to capture more true defaults.

### Q10: What is the relation between default rate and class balance in banking?
*Category*: Imbalance & Splitting

*Answer*: In prime banking portfolios, default rates are typically very low (1% to 5%). This natural class imbalance represents the low-risk nature of the bank's clients but creates a challenging classification landscape for ML algorithms.

### Q11: Explain how you aggregated credit payment history to define the binary target variable.
*Category*: Imbalance & Splitting

*Answer*: We grouped the payment history table (`credit_record.csv`) by application ID, determined the maximum delinquency level (STATUS), and classified applicants as 'Rejected' (Class 1) if they had payments overdue by 60+ days, and 'Approved' (Class 0) otherwise.

### Q12: Why did you choose 60 days past due (DPD) as the cutoff for rejection?
*Category*: Imbalance & Splitting

*Answer*: In banking Basel accords, 90 DPD is typically classified as non-performing loan status (NPL). However, for credit card approvals, a tighter threshold of 60 DPD is standard to catch early-stage default risk before severe losses accumulate.

### Q13: What is target leakage in feature engineering?
*Category*: Imbalance & Splitting

*Answer*: Target leakage occurs when a feature contains information about the target variable that would not be available at the time of prediction. For example, using credit card utilization *after* approval to predict if an applicant *should be* approved is target leakage.

### Q14: How did you ensure that test features are processed identically to train features?
*Category*: Imbalance & Splitting

*Answer*: By encapsulating the entire preprocessing logic in a Scikit-Learn `Pipeline` object, which fits parameters on the training set and uses the exact same parameters to transform the test set.

### Q15: What is the risk of using a validation split that does not match the time period of the training data?
*Category*: Imbalance & Splitting

*Answer*: Temporal validation is critical when data drifts over time. If a model is trained on future data and validated on past data, it may leak future trends, leading to poor generalization. In our case, the data was cross-sectional, so stratified splitting was appropriate.

### Q16: What are the common strategies to treat missing values in tabular datasets?
*Category*: Feature Engineering & Preprocessing

*Answer*: Common strategies include dropping rows (leads to data loss), constant value imputation, mean/median imputation for numerical variables, mode imputation for categorical features, and model-based imputations like KNN Imputer.

### Q17: Why did you choose Median Imputation over Mean Imputation for the 'OCCUPATION_TYPE' or other features?
*Category*: Feature Engineering & Preprocessing

*Answer*: Median imputation is robust to outliers and skewed distributions. For categorical missing features (like occupation type), we used Mode Imputation (most frequent category) or created a separate category named 'Unknown'.

### Q18: How do extreme outliers affect linear models versus tree-based models?
*Category*: Feature Engineering & Preprocessing

*Answer*: Linear models (like Logistic Regression) are highly sensitive to outliers because they try to fit a global decision boundary, which can be heavily skewed by extreme points. Tree-based models are split-based and relatively immune to outliers since they partition the feature space.

### Q19: What is the Interquartile Range (IQR) method for outlier detection?
*Category*: Feature Engineering & Preprocessing

*Answer*: IQR is the difference between the 75th percentile (Q3) and the 25th percentile (Q1). Outliers are defined as values falling below Q1 - 1.5*IQR or above Q3 + 1.5*IQR.

### Q20: Explain the difference between outlier trimming and outlier capping (winsorization).
*Category*: Feature Engineering & Preprocessing

*Answer*: Outlier trimming removes rows containing outliers, which reduces sample size. Outlier capping (winsorization) replaces extreme values with threshold limits (like 1.5*IQR limits), preserving all observations while neutralizing extreme effects.

### Q21: Why is it important to convert 'DAYS_BIRTH' and 'DAYS_EMPLOYED' to positive values?
*Category*: Feature Engineering & Preprocessing

*Answer*: Raw Kaggle datasets often record age and employment length as negative counts of days relative to the current date. Converting these to positive years makes the features intuitive for business stakeholders and standardizes values for scaling.

### Q22: How did you handle the anomaly where 'DAYS_EMPLOYED' was 365,243?
*Category*: Feature Engineering & Preprocessing

*Answer*: A value of 365,243 days equals 1,000 years, which represents retired or unemployed applicants. We replaced this anomaly with 0 years employed and created a binary indicator variable `FLAG_UNEMPLOYED` to capture this specific state.

### Q23: What is the difference between One-Hot Encoding and Label Encoding?
*Category*: Feature Engineering & Preprocessing

*Answer*: One-Hot Encoding creates a binary column for each category, which is suitable for nominal data but increases dimensionality. Label Encoding assigns a unique integer to each category, which is suitable for ordinal data but can imply artificial order if used in linear models.

### Q24: When is Target Encoding preferred over One-Hot Encoding?
*Category*: Feature Engineering & Preprocessing

*Answer*: Target Encoding replaces categories with the mean target value for that category. It is preferred for high-cardinality features where One-Hot Encoding would create too many columns, but it carries a high risk of target leakage if not regularized.

### Q25: Why is feature scaling (Standardization) necessary for Logistic Regression but not for Random Forest?
*Category*: Feature Engineering & Preprocessing

*Answer*: Logistic Regression calculates coefficients using gradient descent or coordinate descent, which converges faster and works correctly only when features are on the same scale. Trees split features individually, meaning their mathematical splits are invariant to scaling.

### Q26: What is the mathematical difference between StandardScaler and MinMaxScaler?
*Category*: Feature Engineering & Preprocessing

*Answer*: StandardScaler shifts values to have a mean of 0 and standard deviation of 1. MinMaxScaler scales values into a range of [0, 1]. StandardScaler is preferred when features are normally distributed and contains moderate outliers.

### Q27: How does multicollinearity affect Logistic Regression?
*Category*: Feature Engineering & Preprocessing

*Answer*: Multicollinearity (high correlation between features) makes the model coefficients unstable and highly sensitive to small changes in training data, complicating feature importance interpretation.

### Q28: What is Variance Inflation Factor (VIF)?
*Category*: Feature Engineering & Preprocessing

*Answer*: VIF measures the severity of multicollinearity in an OLS regression analysis. A VIF value greater than 5 or 10 indicates high multicollinearity, suggesting that one feature is highly predictable from other features.

### Q29: What new features did you engineer, and what was their business rationale?
*Category*: Feature Engineering & Preprocessing

*Answer*: We engineered `income_per_family_member` (measures disposable household income), `employment_length_ratio` (employment duration relative to age), and `age_group` bins (captures generational spending/repayment behaviors).

### Q30: What is Mutual Information (MI) score in feature selection?
*Category*: Feature Engineering & Preprocessing

*Answer*: Mutual Information measures the amount of information obtained about one random variable through observing the other. Unlike linear correlation, it captures non-linear relationships between features and the target.

### Q31: Explain the mathematical formulation of Logistic Regression.
*Category*: Supervised Classifiers

*Answer*: Logistic Regression models the probability of class 1 using the logistic sigmoid function: P(Y=1|X) = 1 / (1 + e^-z), where z is the linear combination of inputs: z = beta_0 + beta_1*x_1 + ... + beta_n*x_n.

### Q32: How does L1 regularization (Lasso) differ from L2 regularization (Ridge)?
*Category*: Supervised Classifiers

*Answer*: L1 regularization adds the absolute values of coefficients to the loss function, forcing some coefficients to exactly zero (performing feature selection). L2 regularization adds the squared values of coefficients, shrinking them towards zero but keeping all features.

### Q33: What is ElasticNet regularization?
*Category*: Supervised Classifiers

*Answer*: ElasticNet is a regularization method that combines both L1 and L2 penalties. It is useful when there are multiple correlated features, allowing it to select groups of correlated features together.

### Q34: Explain how a Decision Tree determines where to split a node.
*Category*: Supervised Classifiers

*Answer*: Decision Trees search for the split that maximizes the reduction in impurity, measured either by Gini Impurity (for classification) or Entropy (information gain).

### Q35: What is the formula for Gini Impurity?
*Category*: Supervised Classifiers

*Answer*: Gini Impurity = 1 - sum(p_i^2), where p_i is the probability of a sample belonging to class i in that node.

### Q36: How does Random Forest reduce the variance of individual Decision Trees?
*Category*: Supervised Classifiers

*Answer*: Random Forest uses bagging (Bootstrap Aggregating) and feature randomness. By training multiple trees on random subsets of data and features, it averages their predictions, reducing variance without increasing bias.

### Q37: What is Out-Of-Bag (OOB) error in Random Forest?
*Category*: Supervised Classifiers

*Answer*: OOB error is a method of measuring the prediction error of a Random Forest. Each tree is trained on a bootstrap sample; the remaining ~36.8% 'out-of-bag' samples are used to evaluate the model's generalization score without needing a separate validation split.

### Q38: Explain how Gradient Boosting differs from Bagging.
*Category*: Supervised Classifiers

*Answer*: Bagging builds independent models in parallel and averages their results. Boosting builds models sequentially, where each new model is trained to correct the residual errors made by the previous models.

### Q39: What is XGBoost and why is it so popular in machine learning competitions?
*Category*: Supervised Classifiers

*Answer*: XGBoost (Extreme Gradient Boosting) is an optimized, highly scalable implementation of gradient boosted decision trees. It includes built-in regularization (L1/L2), tree pruning, parallel execution, and missing value handling.

### Q40: What is the role of learning rate (eta) in XGBoost?
*Category*: Supervised Classifiers

*Answer*: The learning rate scales the contribution of each new tree. A smaller learning rate makes the model more robust to overfitting but requires more trees (estimators) to converge.

### Q41: Explain why tree ensembles can struggle with extrapolation.
*Category*: Supervised Classifiers

*Answer*: Decision trees predict based on the average values of training samples in the leaf nodes. They cannot extrapolate beyond the minimum and maximum feature values seen in the training data, unlike linear models.

### Q42: How does XGBoost handle missing values natively?
*Category*: Supervised Classifiers

*Answer*: XGBoost automatically learns a default direction (left or right split) for missing values at each node, optimizing the split direction to maximize training objective gains.

### Q43: What is the difference between hard voting and soft voting in ensemble classifiers?
*Category*: Supervised Classifiers

*Answer*: Hard voting predicts the class that receives the majority of votes from individual classifiers. Soft voting averages the predicted class probabilities of each classifier and predicts the class with the highest average probability.

### Q44: What are the key hyperparameters of a Random Forest model?
*Category*: Supervised Classifiers

*Answer*: `n_estimators` (number of trees), `max_depth` (max depth of trees), `min_samples_split` (minimum samples required to split a node), `min_samples_leaf` (minimum samples required in a leaf node), and `max_features` (size of feature subset).

### Q45: What are the key hyperparameters of XGBoost?
*Category*: Supervised Classifiers

*Answer*: `learning_rate`, `max_depth`, `n_estimators`, `subsample` (fraction of training instances to sample), `colsample_bytree` (fraction of features to sample), and regularization parameters `alpha` (L1) and `lambda` (L2).

### Q46: Why did Logistic Regression outperform XGBoost on the test set in your case?
*Category*: Supervised Classifiers

*Answer*: XGBoost and Random Forest overfit the majority class due to high model capacity and the skewed imbalance. Logistic Regression with class weight adjustments established a smooth global decision boundary, generalization better to the unseen test set.

### Q47: What is the curse of dimensionality?
*Category*: Supervised Classifiers

*Answer*: As the number of features increases, the volume of space grows exponentially, making the available data sparse. This sparsity degrades distance-based algorithms and increases the risk of overfitting.

### Q48: Explain the difference between generative and discriminative classifiers.
*Category*: Supervised Classifiers

*Answer*: Generative models (like Naive Bayes) learn the joint probability distribution P(X, Y) and predict using Bayes' rule. Discriminative models (like Logistic Regression) learn the conditional probability distribution P(Y|X) directly.

### Q49: What is the purpose of pruning in Decision Trees?
*Category*: Supervised Classifiers

*Answer*: Pruning removes parts of the tree that provide little power to classify instances, reducing size and preventing overfitting. It can be pre-pruning (limiting depth) or post-pruning (collapsing nodes after training).

### Q50: How do you evaluate if a model is overfitting?
*Category*: Supervised Classifiers

*Answer*: By comparing training set performance against validation/testing performance. High training accuracy coupled with low validation accuracy is a signature of overfitting.

### Q51: Define the elements of a Confusion Matrix.
*Category*: Model Metrics & Evaluation

*Answer*: True Positive (TP): correctly predicted default. False Positive (FP): approved client predicted as default. True Negative (TN): correctly predicted approval. False Negative (FN): defaulted client predicted as approved.

### Q52: Why is Precision-Recall curve preferred over ROC curve for highly imbalanced datasets?
*Category*: Model Metrics & Evaluation

*Answer*: The ROC curve uses False Positive Rate (FPR = FP/(FP+TN)), which can remain small even with high FP counts if TN (majority class) is huge. The PR curve plots Precision (TP/(TP+FP)) against Recall (TP/(TP+FN)), exposing false positives directly.

### Q53: What is the F1-Score and when should you use it?
*Category*: Model Metrics & Evaluation

*Answer*: F1-Score is the harmonic mean of Precision and Recall. It is used when a balance between Precision and Recall is desired, especially on imbalanced datasets.

### Q54: What is the F-beta score?
*Category*: Model Metrics & Evaluation

*Answer*: F-beta is a generalization of the F1-score that allows weighting Precision or Recall higher using a beta coefficient. An F-2 score (beta=2) weights Recall twice as heavily as Precision, making it useful in credit default modeling.

### Q55: Explain the ROC-AUC score.
*Category*: Model Metrics & Evaluation

*Answer*: ROC-AUC (Area Under the Receiver Operating Characteristic curve) measures the model's ability to distinguish between classes. It represents the probability that a randomly chosen positive instance will be ranked higher than a randomly chosen negative one.

### Q56: What is Log Loss (Cross-Entropy Loss)?
*Category*: Model Metrics & Evaluation

*Answer*: Log Loss measures the performance of a classification model whose output is a probability value between 0 and 1. It heavily penalizes predictions that are confident but wrong.

### Q57: What is Cohen's Kappa?
*Category*: Model Metrics & Evaluation

*Answer*: Cohen's Kappa measures inter-rater agreement for categorical items, adjusting for the agreement occurring by chance. It is a robust metric for imbalanced classification.

### Q58: Why is F1-score better than Accuracy in our business scenario?
*Category*: Model Metrics & Evaluation

*Answer*: If 92.5% of applicants are approved, a dummy model predicting 'Approved' for everyone has 92.5% Accuracy but 0% Recall and undefined Precision. F1-Score for the default class exposes this failure instantly.

### Q59: How does changing the classification probability threshold affect Precision and Recall?
*Category*: Model Metrics & Evaluation

*Answer*: Lowering the threshold classifies more instances as positive, increasing Recall but potentially increasing False Positives (lowering Precision). Raising it increases Precision but lowers Recall.

### Q60: What is Calibration of probabilities?
*Category*: Model Metrics & Evaluation

*Answer*: Calibration ensures that the predicted probability matches the empirical frequency of the event. For example, out of all instances predicted to default with 80% probability, approximately 80% should actually default.

### Q61: Explain Platt Scaling.
*Category*: Model Metrics & Evaluation

*Answer*: Platt Scaling is a method for transforming the outputs of a classification model (like SVM decision values) into a probability distribution by fitting a logistic regression model to the outputs.

### Q62: What is Isotonic Regression for calibration?
*Category*: Model Metrics & Evaluation

*Answer*: Isotonic Regression fits a non-decreasing piecewise linear function to map model scores to probabilities. It is more powerful than Platt Scaling but requires more data to avoid overfitting.

### Q63: How do you calculate inference latency?
*Category*: Model Metrics & Evaluation

*Answer*: Inference latency is the time taken to process a single prediction request. It is measured by recording timestamps immediately before and after invoking the model's predict/predict_proba method.

### Q64: What is the business meaning of a False Negative in credit approval?
*Category*: Model Metrics & Evaluation

*Answer*: A False Negative means the bank approves an applicant who is high-risk and will default. This causes direct financial loss (loss of principal and recovery costs).

### Q65: What is the business meaning of a False Positive in credit approval?
*Category*: Model Metrics & Evaluation

*Answer*: A False Positive means a low-risk applicant is classified as high-risk and rejected. This leads to lost business opportunity and potential customer frustration.

### Q66: What is Grid Search CV?
*Category*: Hyperparameter Tuning & CV

*Answer*: GridSearchCV performs exhaustive search over a specified parameter grid, evaluating all parameter combinations using cross-validation to select the configuration that maximizes validation metrics.

### Q67: What is Randomized Search CV?
*Category*: Hyperparameter Tuning & CV

*Answer*: RandomizedSearchCV samples a fixed number of parameter combinations from specified probability distributions. It is faster and more efficient than GridSearchCV for large parameter spaces.

### Q68: Explain Bayesian Optimization for hyperparameter tuning.
*Category*: Hyperparameter Tuning & CV

*Answer*: Bayesian Optimization builds a probabilistic model of the objective function (surrogate model) and uses it to select the next parameters to evaluate, balancing exploration and exploitation.

### Q69: What is the risk of tuning hyperparameters on the test set?
*Category*: Hyperparameter Tuning & CV

*Answer*: Tuning on the test set causes information leakage. The model's parameters adapt to the test set, leading to optimistic performance estimates that fail to generalize to production.

### Q70: How do you choose the number of splits (K) in cross-validation?
*Category*: Hyperparameter Tuning & CV

*Answer*: Typically K=5 or K=10. Smaller K is faster but has higher bias; larger K is computationally expensive and has higher variance.

### Q71: What is nested cross-validation?
*Category*: Hyperparameter Tuning & CV

*Answer*: Nested CV has an inner loop for hyperparameter tuning and an outer loop for estimating generalization error. It prevents optimistic bias in performance estimation.

### Q72: Why is random state configuration critical in train-test splitting?
*Category*: Hyperparameter Tuning & CV

*Answer*: Setting a seed (random state) ensures that data splits are reproducible, allowing developers to compare model changes fairly on identical datasets.

### Q73: What is Out-Of-Sample (OOS) validation?
*Category*: Hyperparameter Tuning & CV

*Answer*: OOS validation evaluates the model on a completely separate dataset that was not used during training or hyperparameter tuning, serving as a final test of generalization.

### Q74: What is Out-Of-Time (OOT) validation?
*Category*: Hyperparameter Tuning & CV

*Answer*: OOT validation uses data from a later time period than the training data. This is crucial in banking to ensure that the model remains robust to economic cycles and seasonal shifts.

### Q75: How do you evaluate cross-validation stability?
*Category*: Hyperparameter Tuning & CV

*Answer*: By checking the standard deviation of cross-validation scores. A high standard deviation indicates that the model is sensitive to training set variations (high variance).

### Q76: What is SHAP (SHapley Additive exPlanations)?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: SHAP is a game theoretic approach to explain the output of any machine learning model. It connects optimal credit allocation with local explanations using classical Shapley values.

### Q77: What are Shapley values?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Shapley values calculate the average marginal contribution of a feature value across all possible feature coalitions, guaranteeing fair contribution distribution.

### Q78: Explain the difference between local and global model explainability.
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Global explainability describes which features are most important *overall* across the entire dataset. Local explainability explains *why* a specific individual prediction was made.

### Q79: How does LIME (Local Interpretable Model-agnostic Explanations) work?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: LIME perturbs the input features of a specific instance, collects the predictions, and trains an interpretable local surrogate model (like a simple linear regression) to approximate the decision boundary locally.

### Q80: Why is model interpretability critical in banking?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Regulations (like ECOA in the US) require banks to provide 'adverse action notices' explaining why an applicant was denied credit. Black-box models must be coupled with explainability tools to meet this legal requirement.

### Q81: What is the difference between permutation feature importance and Gini importance?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Gini importance calculates importance based on training impurity reduction. Permutation importance evaluates importance on test data by shuffling a feature's values and measuring the drop in performance.

### Q82: Explain how you calculated SHAP-style contributions for your Logistic Regression model.
*Category*: Model Explainability (SHAP/LIME)

*Answer*: We multiplied the scaled input feature values by their corresponding model coefficients, yielding log-odds contributions. This represents the local linear impact of each feature.

### Q83: What are the limitations of local linear model explanations?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Linear explanations assume features act independently. In reality, features interact (e.g., age and income interact), which linear coefficients fail to capture.

### Q84: What is a SHAP summary plot?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: A SHAP summary plot combines feature importance with feature effects. It displays the SHAP values of all features for all instances, showing how high/low feature values drive predictions.

### Q85: What is a partial dependence plot (PDP)?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: A PDP shows the marginal effect of one or two features on the predicted outcome of a machine learning model, keeping all other features constant.

### Q86: How does feature interaction manifest in SHAP values?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Through SHAP interaction values, which separate the joint impact of two features from their individual marginal effects.

### Q87: Explain the concept of adversarial attacks on explainability methods.
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Adversarial attacks can manipulate model training or inputs to hide biased features from SHAP/LIME while maintaining the model's underlying bias, highlighting the need for robust audits.

### Q88: What is the difference between model-agnostic and model-specific explainability?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: Model-agnostic tools (like LIME) work on any machine learning model. Model-specific tools (like TreeSHAP) leverage model-internal structures (like trees) for faster and exact computations.

### Q89: How do you present ML explanations to a non-technical business stakeholder?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: By translating numbers into intuitive natural language (e.g., 'Your application was rejected due to short employment history' rather than 'YEARS_EMPLOYED log-odds contribution is +1.2').

### Q90: What is a waterfall plot in SHAP?
*Category*: Model Explainability (SHAP/LIME)

*Answer*: A waterfall plot illustrates how a model prediction starts at the base rate (average prediction) and accumulates feature contributions sequentially to arrive at the final predicted probability.

### Q91: What is data drift (covariate shift)?
*Category*: Data Validation & Drift

*Answer*: Data drift occurs when the input feature distribution changes over time, while the relationship between features and target remains constant. For example, average applicant income increases due to inflation.

### Q92: What is concept drift?
*Category*: Data Validation & Drift

*Answer*: Concept drift occurs when the relationship between features and the target variable changes over time. For example, during a recession, applicants who previously would not default begin to default.

### Q93: Explain how you would detect data drift in production.
*Category*: Data Validation & Drift

*Answer*: By setting up periodic statistical tests (like Kolmogorov-Smirnov test for continuous variables or Chi-Square test for categoricals) to compare incoming production features against the baseline training distribution.

### Q94: What is the Population Stability Index (PSI)?
*Category*: Data Validation & Drift

*Answer*: PSI measures how much a variable's distribution has shifted between two points in time. A PSI > 0.25 indicates significant shift, requiring model retraining.

### Q95: What is schema validation and why is it used?
*Category*: Data Validation & Drift

*Answer*: Schema validation checks if incoming API inputs match expected formats, types, and ranges, preventing invalid data from causing model inference crashes.

### Q96: Explain Great Expectations.
*Category*: Data Validation & Drift

*Answer*: Great Expectations is an open-source tool for validating, documenting, and profiling data. It allows developers to assert expectations about dataset schemas, null ratios, and distributions.

### Q97: How do you handle a drift alert in production?
*Category*: Data Validation & Drift

*Answer*: Trigger alerts, collect new data, perform root-cause analysis, and retrain/re-calibrate the model on the latest data.

### Q98: What is shadow deployment?
*Category*: Data Validation & Drift

*Answer*: Shadow deployment deploys the new model alongside the active model. The shadow model receives production requests and generates predictions for evaluation, but its outputs are not returned to users.

### Q99: What is canary deployment?
*Category*: Data Validation & Drift

*Answer*: Canary deployment routes a small percentage of production traffic (e.g., 5%) to the new model, expanding traffic gradually as the model proves stable.

### Q100: What is the purpose of model registry?
*Category*: Data Validation & Drift

*Answer*: A model registry is a centralized store for managing models, tracking versions, storage locations, training runs, and deployment states.

---

## 2. Flask & Web Development Questions (50 Q&As)

### Q1: What is the Application Factory pattern in Flask?
*Category*: Core Architecture

*Answer*: It is a pattern where the Flask application instance is created inside a function (e.g. `create_app()`) rather than globally. This avoids circular imports and allows creating multiple app instances with different configurations for testing.

### Q2: Why are Flask Blueprints useful?
*Category*: Core Architecture

*Answer*: Blueprints allow developers to organize a Flask application into modular sub-modules, grouping related routes, templates, and static files. This makes large applications maintainable.

### Q3: How do you manage application configurations in Flask?
*Category*: Core Architecture

*Answer*: By loading configurations from objects (e.g., `app.config.from_object(Config)`), environment variables (`os.getenv`), or configuration files (YAML, JSON) using Flask's built-in `config` dictionary.

### Q4: What is the purpose of the application context in Flask?
*Category*: Core Architecture

*Answer*: The application context keeps track of application-level data (such as database connections or configurations) during a request. It is represented by the `current_app` and `g` proxies.

### Q5: Explain the difference between `current_app` and `g` in Flask.
*Category*: Core Architecture

*Answer*: `current_app` is a proxy pointing to the active Flask application instance. `g` is a global namespace object used to store request-specific temporary data (such as DB connection).

### Q6: What is the request context in Flask?
*Category*: Core Architecture

*Answer*: The request context tracks request-level data (such as headers, args, and form data). It is represented by the `request` and `session` proxies.

### Q7: How does Flask handle circular imports?
*Category*: Core Architecture

*Answer*: By using the Application Factory pattern and importing blueprints or routes inside functions (lazy imports) rather than at the top of module files.

### Q8: Explain how Flask's template rendering works with Jinja2.
*Category*: Core Architecture

*Answer*: Flask uses Jinja2 as its template engine. `render_template` compiles HTML files containing template tags, executing statements (like loops, conditionals) and inserting variables passed from routes.

### Q9: What is Flask-WTF and why did you use it?
*Category*: Core Architecture

*Answer*: Flask-WTF integrates WTForms with Flask, providing form rendering, server-side validation, and built-in CSRF protection.

### Q10: What is WSGI?
*Category*: Core Architecture

*Answer*: WSGI (Web Server Gateway Interface) is a standard specification for web servers to communicate with Python web applications, ensuring compatibility between servers (like Gunicorn) and frameworks (like Flask).

### Q11: How do you handle custom 404 and 500 errors in Flask?
*Category*: Core Architecture

*Answer*: By registering error handlers using `@app.errorhandler(404)` or `@app.errorhandler(500)`, returning custom error templates and appropriate HTTP status codes.

### Q12: What is Flask's development server and why shouldn't it be used in production?
*Category*: Core Architecture

*Answer*: Flask's development server is single-threaded and not optimized for security or performance. It lacks concurrent request handling and can crash under load.

### Q13: What is Gunicorn and how does it serve Flask apps?
*Category*: Core Architecture

*Answer*: Gunicorn is a Python WSGI HTTP server that uses a pre-fork worker model, running multiple worker processes in parallel to handle concurrent traffic.

### Q14: How does `sys.path.append` help in modular Flask layouts?
*Category*: Core Architecture

*Answer*: It adds the project root directory to Python's search path, enabling absolute imports across different sub-directories (like `src/`, `app/`, `tests/`).

### Q15: What is the purpose of the `static` folder in Flask?
*Category*: Core Architecture

*Answer*: It stores static assets such as CSS files, JavaScript code, and images, which Flask serves directly to clients.

### Q16: How do you handle HTTP GET and POST requests on the same route?
*Category*: Routing & Request Handling

*Answer*: By specifying `methods=['GET', 'POST']` in the route decorator, and checking `request.method == 'POST'` inside the view function.

### Q17: How do you extract JSON payload data from an incoming POST request?
*Category*: Routing & Request Handling

*Answer*: By calling `request.get_json()` which parses the raw request body as JSON and returns a Python dictionary.

### Q18: What is the difference between `request.form` and `request.args`?
*Category*: Routing & Request Handling

*Answer*: `request.form` contains parameters parsed from an HTML form POST request. `request.args` contains URL query string parameters parsed from a GET request.

### Q19: How do you perform redirection in Flask?
*Category*: Routing & Request Handling

*Answer*: By returning `redirect(url_for('route_name'))` which sends an HTTP redirect header back to the client.

### Q20: What does `url_for` do?
*Category*: Routing & Request Handling

*Answer*: `url_for` dynamically generates a URL for a given view function name, preventing hardcoded URL path failures.

### Q21: Explain flash messaging in Flask.
*Category*: Routing & Request Handling

*Answer*: Flash messaging allows passing messages from one request to the next request (stored in session) using `flash(message, category)`.

### Q22: How do you return custom headers or status codes from a Flask route?
*Category*: Routing & Request Handling

*Answer*: By returning a tuple: `return response_data, status_code, headers_dict`.

### Q23: Explain Flask's `jsonify` function.
*Category*: Routing & Request Handling

*Answer*: `jsonify` serializes python data structures into JSON strings and returns a Flask Response object with the `application/json` MIME type.

### Q24: What are path converters in Flask routes?
*Category*: Routing & Request Handling

*Answer*: They parse variables from paths (e.g. `<int:id>`), automatically converting them to the specified type (integer, string, path).

### Q25: How do you access request headers in a Flask view?
*Category*: Routing & Request Handling

*Answer*: Through the `request.headers` dictionary (e.g., `request.headers.get('Authorization')`).

### Q26: What is `request.values`?
*Category*: Routing & Request Handling

*Answer*: A combined MultiDict containing both query parameters (`request.args`) and form data (`request.form`).

### Q27: How do you handle file uploads in Flask?
*Category*: Routing & Request Handling

*Answer*: By accessing files in `request.files`, validating file extensions, and calling `.save(path)` on the file object.

### Q28: Why is it important to use `secure_filename` from Werkzeug during uploads?
*Category*: Routing & Request Handling

*Answer*: `secure_filename` sanitizes upload names, preventing directory traversal attacks (e.g., uploading to `../../etc/passwd`).

### Q29: What is a Flask blueprint prefix?
*Category*: Routing & Request Handling

*Answer*: An optional URL prefix registered with a blueprint (e.g. `/api/v1`) that prepends to all routes inside that blueprint.

### Q30: How does Flask handle asynchronous request handlers?
*Category*: Routing & Request Handling

*Answer*: Flask 2.0+ supports native `async def` views, executing them inside a separate event loop thread or worker process.

### Q31: How does WTForms CSRF protection work?
*Category*: Security & Middleware

*Answer*: It embeds a hidden token containing a cryptographic signature in HTML forms. The server validates this token against the user's session key on submission.

### Q32: What is Flask Session and how is it secured?
*Category*: Security & Middleware

*Answer*: Flask session stores client state. By default, it uses signed cookies stored in the client browser, secured cryptographically using `SECRET_KEY`.

### Q33: What happens if you leak the Flask `SECRET_KEY`?
*Category*: Security & Middleware

*Answer*: An attacker can decrypt and tamper with session cookies, potentially escalating privileges or hijacking user sessions.

### Q34: What is CORS and how do you enable it in Flask?
*Category*: Security & Middleware

*Answer*: CORS (Cross-Origin Resource Sharing) restricts resource sharing across domains. It is enabled using the `flask-cors` extension.

### Q35: Explain how you implemented Rate Limiting in your Flask API.
*Category*: Security & Middleware

*Answer*: We implemented a custom `@rate_limit` decorator in `src/utils/limiter.py` tracking client IP addresses in an in-memory dictionary.

### Q36: What is the purpose of `@app.before_request`?
*Category*: Security & Middleware

*Answer*: It registers a function to run before every request, useful for authorization, logging, or setting up database sessions.

### Q37: What is `@app.after_request`?
*Category*: Security & Middleware

*Answer*: It registers a function to run after every request, allowing developers to modify response headers or close connections.

### Q38: Explain SQL injection and how to prevent it in Flask.
*Category*: Security & Middleware

*Answer*: SQL injection occurs when raw user inputs are executed directly in SQL statements. It is prevented by using parameterized queries or ORMs like SQLAlchemy.

### Q39: What is XSS (Cross-Site Scripting) and how does Jinja2 prevent it?
*Category*: Security & Middleware

*Answer*: XSS injects malicious scripts into web pages. Jinja2 automatically escapes HTML tags (converting `<` to `&lt;`) unless explicitly disabled.

### Q40: What is CSRF and how is it different from XSS?
*Category*: Security & Middleware

*Answer*: CSRF tricks a logged-in user into executing unwanted actions. XSS runs scripts within the user's browser, stealing credentials or data.

### Q41: Why is it important to set HTTPOnly and Secure flags on session cookies?
*Category*: Security & Middleware

*Answer*: `HTTPOnly` prevents JavaScript access (mitigating XSS session theft); `Secure` ensures cookies are sent only over HTTPS.

### Q42: How do you configure logging in a production Flask application?
*Category*: Security & Middleware

*Answer*: By using Python's standard `logging.config.dictConfig`, setting file rotation, formatters, and routing logs to stdout/stderr.

### Q43: What is Flask-SQLAlchemy?
*Category*: Security & Middleware

*Answer*: An extension that adds SQLAlchemy support to Flask, simplifying database connections and model management.

### Q44: What is Flask-Migrate?
*Category*: Security & Middleware

*Answer*: An extension that handles SQLAlchemy database migrations using Alembic, tracking schema changes in versioned scripts.

### Q45: Explain the difference between `g` and session.
*Category*: Security & Middleware

*Answer*: `g` stores data for the duration of a *single* request. `session` stores data across *multiple* requests for a specific client.

### Q46: How do you run a Flask app in production using Docker?
*Category*: Production Deployment

*Answer*: By using a multi-stage Dockerfile copy-pasting code, installing requirements, and running Gunicorn via CMD (e.g. `gunicorn -w 4 -b 0.0.0.0:5000 app.app:app`).

### Q47: How do you handle database connections efficiently in a multi-worker Gunicorn setup?
*Category*: Production Deployment

*Answer*: By initializing database connections per worker process (on request or using connection pools) rather than sharing a global connection.

### Q48: What is the purpose of a health check endpoint `/health`?
*Category*: Production Deployment

*Answer*: It provides a simple API to return application status, allowing orchestrators (Kubernetes, Render) to verify app availability.

### Q49: Explain how you deploy a Flask application to Render.
*Category*: Production Deployment

*Answer*: We define a `render.yaml` blueprint mapping build commands (`pip install`) and start commands (`gunicorn app.app:app`), binding it to GitHub.

### Q50: What is the difference between Gunicorn sync and async workers?
*Category*: Production Deployment

*Answer*: Sync workers process requests sequentially (one worker per connection). Async workers (like eventlet/gevent) handle concurrent connections using cooperative greenlets.

---

## 3. Python Coding & Architecture Questions (50 Q&As)

### Q1: What is a Python decorator and how does it work?
*Category*: Language Fundamentals

*Answer*: A decorator is a function that takes another function as an argument, extends its behavior without modifying it, and returns a new function. It leverages Python's first-class functions and closures.

### Q2: Explain the difference between `__init__` and `__new__` in Python.
*Category*: Language Fundamentals

*Answer*: `__new__` is the constructor method that actually creates the instance of a class and returns it. `__init__` is the initializer method that initializes the attributes of the created object.

### Q3: What is the Global Interpreter Lock (GIL)?
*Category*: Language Fundamentals

*Answer*: The GIL is a mutex in CPython that prevents multiple native threads from executing Python bytecodes at once, ensuring thread safety but limiting multi-threaded CPU performance.

### Q4: What is a generator and how does it save memory?
*Category*: Language Fundamentals

*Answer*: A generator is a function containing `yield` statements that returns an iterator. It yields values lazily one by one, avoiding loading the entire list into memory.

### Q5: Explain the difference between `list.append()` and `list.extend()`.
*Category*: Language Fundamentals

*Answer*: `append()` adds its argument as a single element to the end of the list. `extend()` iterates over its argument, adding each item individually.

### Q6: What is a closure in Python?
*Category*: Language Fundamentals

*Answer*: A closure is a nested function that retains access to variables from its enclosing scope even after the outer function has finished executing.

### Q7: How is memory managed in Python?
*Category*: Language Fundamentals

*Answer*: Python manages memory automatically using a private heap space, monitored by a reference counting garbage collector and a cyclic garbage collector.

### Q8: What is the difference between deepcopy and shallow copy?
*Category*: Language Fundamentals

*Answer*: A shallow copy constructs a new object but references the child objects. A deepcopy recursively copies everything, constructing a completely independent object.

### Q9: What are Python magic (dunder) methods?
*Category*: Language Fundamentals

*Answer*: Magic methods (like `__str__`, `__len__`, `__repr__`) begin and end with double underscores, allowing custom classes to define behaviors for operator overloading.

### Q10: What is the difference between `__str__` and `__repr__`?
*Category*: Language Fundamentals

*Answer*: `__str__` returns an informal, user-friendly string representation of an object. `__repr__` returns an official, unambiguous representation for debugging.

### Q11: Explain duck typing in Python.
*Category*: Language Fundamentals

*Answer*: Duck typing determines object suitability based on the presence of specific methods or properties rather than its explicit inheritance ('If it walks like a duck...').

### Q12: What are Python list comprehensions and their benefits?
*Category*: Language Fundamentals

*Answer*: List comprehensions offer a concise syntax to create lists from iterables. They are readable and run faster than equivalent for-loops because they are optimized in C.

### Q13: How do you handle exceptions in Python?
*Category*: Language Fundamentals

*Answer*: Using `try-except-else-finally` blocks. `else` runs if no exception occurred; `finally` always runs, ensuring cleanup.

### Q14: Explain Python's type hinting and static analysis tools.
*Category*: Language Fundamentals

*Answer*: Type hints specify expected types of variables and arguments, helping IDEs and static analyzers (like MyPy) identify bugs before runtime.

### Q15: What is the difference between a list and a tuple?
*Category*: Language Fundamentals

*Answer*: Lists are mutable (can be changed in-place) and use more memory. Tuples are immutable (cannot be changed) and use less memory.

### Q16: What is Method Resolution Order (MRO) in Python?
*Category*: Advanced Concepts & OOP

*Answer*: MRO is the order in which Python searches for inherited methods, resolved using the C3 Linearization algorithm.

### Q17: How did you resolve the XGBoost MRO bug on Python 3.13?
*Category*: Advanced Concepts & OOP

*Answer*: We dynamically patched `ClassifierMixin.__sklearn_tags__` at startup to bypass MRO lookup failures on Python 3.13, delegating tags safely.

### Q18: Explain the `with` statement and context managers.
*Category*: Advanced Concepts & OOP

*Answer*: The `with` statement simplifies resource management using context managers, automatically calling `__enter__` at setup and `__exit__` at teardown.

### Q19: What is the difference between class methods and static methods?
*Category*: Advanced Concepts & OOP

*Answer*: `classmethod` receives the class (`cls`) as its first argument and can modify class state. `staticmethod` receives no implicit arguments.

### Q20: What is abstract base class (ABC) in Python?
*Category*: Advanced Concepts & OOP

*Answer*: ABCs define common APIs for a set of subclasses, preventing instantiation of base classes and enforcing implementation of abstract methods.

### Q21: Explain *args and **kwargs.
*Category*: Advanced Concepts & OOP

*Answer*: `*args` allows passing a variable number of positional arguments as a tuple. `**kwargs` allows passing keyword arguments as a dictionary.

### Q22: How do you check if an object is an instance of a specific class?
*Category*: Advanced Concepts & OOP

*Answer*: Using the built-in `isinstance(object, class)` function, which is preferred over direct type comparison because it respects inheritance.

### Q23: What is a dictionary view object?
*Category*: Advanced Concepts & OOP

*Answer*: Objects returned by `dict.keys()`, `dict.values()`, and `dict.items()`. They provide dynamic, read-only views of the dictionary's entries.

### Q24: What is the difference between `is` and `==`?
*Category*: Advanced Concepts & OOP

*Answer*: `is` checks object identity (if they reference the same memory address). `==` checks value equality (if values are equivalent).

### Q25: Explain Python's scope resolution (LEGB rule).
*Category*: Advanced Concepts & OOP

*Answer*: Python resolves names in order: Local, Enclosing (non-local), Global, and Built-in scopes.

### Q26: What are lambda functions?
*Category*: Advanced Concepts & OOP

*Answer*: Lambda functions are small, anonymous, single-expression functions defined using the `lambda` keyword.

### Q27: What is the difference between `__getattr__` and `__getattribute__`?
*Category*: Advanced Concepts & OOP

*Answer*: `__getattribute__` is called unconditionally for every attribute access. `__getattr__` is called only if the attribute is not found.

### Q28: What are descriptors in Python?
*Category*: Advanced Concepts & OOP

*Answer*: Descriptors are objects that define binding behaviors for attributes, overriding `__get__`, `__set__`, and `__delete__` (used to implement properties).

### Q29: How does multiple inheritance work in Python?
*Category*: Advanced Concepts & OOP

*Answer*: Python allows a class to inherit from multiple parent classes, resolving method conflicts using the Method Resolution Order (MRO).

### Q30: What is metaclass in Python?
*Category*: Advanced Concepts & OOP

*Answer*: A metaclass is the class of a class, defining how classes are constructed. In Python, the default metaclass is `type`.

### Q31: How do you achieve parallelism in Python despite the GIL?
*Category*: Memory & Concurrency

*Answer*: By using the `multiprocessing` module (runs code in separate OS processes with independent GILs) or offloading work to C-extensions (like NumPy).

### Q32: What is the difference between multi-threading and multi-processing?
*Category*: Memory & Concurrency

*Answer*: Multi-threading runs threads in the same memory space (bounded by GIL). Multi-processing spawns independent processes with independent memory.

### Q33: Explain asyncio in Python.
*Category*: Memory & Concurrency

*Answer*: `asyncio` is a library to write concurrent code using the async/await syntax, executing tasks cooperatively on a single-thread event loop.

### Q34: What is a thread safety issue?
*Category*: Memory & Concurrency

*Answer*: Thread safety issues occur when multiple threads access shared resources concurrently without synchronization, leading to race conditions.

### Q35: What is the purpose of `threading.Lock`?
*Category*: Memory & Concurrency

*Answer*: A lock (mutex) ensures that only one thread can access a shared resource or execute a critical section of code at a time.

### Q36: How do you share data between processes in Python?
*Category*: Memory & Concurrency

*Answer*: Using IPC (Inter-Process Communication) mechanisms like `multiprocessing.Queue`, `Value`, `Array`, or managers.

### Q37: What is a daemon thread?
*Category*: Memory & Concurrency

*Answer*: A daemon thread runs in the background and does not prevent the Python program from exiting when only daemon threads are left.

### Q38: Explain reference counting in Python.
*Category*: Memory & Concurrency

*Answer*: Each object tracks how many references point to it. When an object's reference count drops to 0, its memory is immediately deallocated.

### Q39: What is cyclic garbage collection?
*Category*: Memory & Concurrency

*Answer*: A mechanism that detects reference cycles (e.g. A references B, and B references A) that reference counting alone cannot clean up.

### Q40: How does Python handle memory fragmentation?
*Category*: Memory & Concurrency

*Answer*: Python uses a custom memory allocator called PyMalloc for small objects (<= 512 bytes), allocating objects in arenas to reduce fragmentation.

### Q41: What is the difference between `os.path` and `pathlib`?
*Category*: Memory & Concurrency

*Answer*: `os.path` represents paths as strings. `pathlib` represents paths as robust, cross-platform object-oriented Path objects.

### Q42: What is the `__slots__` attribute?
*Category*: Memory & Concurrency

*Answer*: `__slots__` tells Python to allocate a fixed set of attributes on instances rather than using a dynamic `__dict__`, reducing memory usage.

### Q43: How do you create a package in Python?
*Category*: Memory & Concurrency

*Answer*: By organizing code in a directory containing module files and an `__init__.py` file (which can be empty).

### Q44: What is the purpose of `setup.py`?
*Category*: Memory & Concurrency

*Answer*: `setup.py` is the build script for setuptools, defining package metadata, dependencies, and entrypoints for distribution.

### Q45: What is a wheel package format?
*Category*: Memory & Concurrency

*Answer*: A wheel is the standard built package format for Python, allowing faster installation since it avoids building from source.

### Q46: What is virtualenv?
*Category*: Standard Library & Packaging

*Answer*: An isolated environment tool that creates independent Python environments, preventing library version conflicts across projects.

### Q47: How does PIP resolve package dependencies?
*Category*: Standard Library & Packaging

*Answer*: PIP uses a backtracking dependency resolver to find a set of package versions that satisfy all requirements.

### Q48: What is the difference between `requirements.txt` and `setup.py` dependencies?
*Category*: Standard Library & Packaging

*Answer*: `setup.py` defines abstract dependencies for library distribution. `requirements.txt` defines concrete, pinned versions for environment replication.

### Q49: Explain PEP 8.
*Category*: Standard Library & Packaging

*Answer*: PEP 8 is the official style guide for Python code, outlining formatting standards (indentation, naming conventions, line limits).

### Q50: What is the difference between `unittest` and `pytest`?
*Category*: Standard Library & Packaging

*Answer*: `unittest` is standard library-based and requires class structures. `pytest` supports simple functions, assertion syntax, and powerful fixtures.

---

## 4. System Design & MLOps Questions (20 Q&As)

### Q1: Design a system architecture for real-time credit card risk scoring.
*Category*: Production Architectures

*Answer*: The system consists of an API Gateway routing requests to a Flask or FastAPI microservice cluster deployed on Kubernetes. A load balancer distributes traffic. Inputs are validated, and the model (loaded in memory) performs inference. Inference results and inputs are saved to a write-heavy database (like PostgreSQL/SQLite) and logged asynchronously to Kafka for monitoring and audit logging.

### Q2: How would you handle high concurrency (>10,000 requests/sec) in your scoring service?
*Category*: Production Architectures

*Answer*: We would deploy multiple replicas of the prediction service in a Kubernetes cluster with autoscaling. We would use an asynchronous web server framework (like FastAPI or Sanic) or run Gunicorn with gevent/uvicorn workers. A Redis cache can cache predictions for duplicate applications within a short time window.

### Q3: Explain the advantages of microservices over monoliths for machine learning deployments.
*Category*: Production Architectures

*Answer*: Microservices decouple ML inference from main application backends. This allows scaling inference hardware independently, updating models without redeploying the core application, and using optimal technology stacks.

### Q4: Where should the machine learning model be loaded in a production web application?
*Category*: Production Architectures

*Answer*: The model should be loaded in memory during application startup (in the app factory or global namespace), not inside route functions, ensuring that each prediction request has zero model-loading overhead.

### Q5: How do you handle model updates without causing downtime?
*Category*: Production Architectures

*Answer*: Using rolling updates or blue-green deployments. The orchestrator spawns new pods containing the updated model, verifies their health, and transitions traffic away from old pods.

### Q6: What is a Feature Store and how does it fit into ML system design?
*Category*: Production Architectures

*Answer*: A feature store (like Feast) is a centralized repository that stores and serves pre-computed feature vectors for both offline training and online real-time inference, preventing training-serving skew.

### Q7: How do you handle API security and rate limiting in production?
*Category*: Production Architectures

*Answer*: By deploying an API Gateway (like Kong or AWS API Gateway) to manage client authentication (API keys, JWTs), request rate limiting, SSL termination, and IP white-listing.

### Q8: Design a batch prediction pipeline for credit card scoring.
*Category*: Production Architectures

*Answer*: A cron schedule (or Airflow dag) triggers a batch job (e.g. Spark or Pandas in ECS) that reads new applications from a data warehouse (Snowflake), loads the model, computes predictions in batches, and writes scores back to the warehouse.

### Q9: How do you handle model fallback if the primary ML service fails?
*Category*: Production Architectures

*Answer*: By implementing a fallback layer. If the ML model fails, the client or gateway falls back to a lightweight heuristic rule engine (e.g., if income < threshold, reject) to ensure high availability.

### Q10: Explain training-serving skew and how to mitigate it.
*Category*: Production Architectures

*Answer*: Training-serving skew is the difference in model performance between training and production. It is mitigated by using identical preprocessing libraries, feature stores, and automated schema validation.

### Q11: How do you monitor a machine learning model's performance in real time?
*Category*: Scaling & Monitoring

*Answer*: By logging all inputs, predicted probabilities, and final decisions to a log collector (Prometheus/ElasticSearch), visualizing metrics (prediction distributions, average risk scores) on a Grafana dashboard.

### Q12: Explain how you would log and track model predictions for audit compliance.
*Category*: Scaling & Monitoring

*Answer*: We would write predictions to a persistent database containing: application ID, request payload, model version, prediction, probability, timestamp, and explanation ID, ensuring traceability.

### Q13: How do you design a database schema for storing prediction history?
*Category*: Scaling & Monitoring

*Answer*: A normalized schema: `applications` table (demographics), `predictions` table (foreign key to applications, stores decision, probability, model version, timestamp), and `explanations` table (stores SHAP/local contribution coefficients).

### Q14: Design an alert system for data drift in production.
*Category*: Scaling & Monitoring

*Answer*: A daily cron job calculates the Population Stability Index (PSI) on yesterday's production inputs against the training baseline. If PSI exceeds 0.25, the system sends an automated alert via Slack/PagerDuty to trigger retrain routines.

### Q15: How would you handle feature versioning?
*Category*: Scaling & Monitoring

*Answer*: By managing features in a Git repository using declarative files, versioning code pipelines, and utilizing a feature store to track schema modifications.

### Q16: What is the role of an API Gateway in machine learning deployments?
*Category*: Scaling & Monitoring

*Answer*: It serves as the single entrypoint for clients, managing authentication, SSL decryption, traffic routing, request logging, and rate limiting.

### Q17: How do you scale model inference for huge datasets?
*Category*: Scaling & Monitoring

*Answer*: By using distributed inference engines (like Apache Spark), running inference on GPU clusters for deep learning, or batching requests using Triton Inference Server.

### Q18: What is the difference between online inference and offline inference?
*Category*: Scaling & Monitoring

*Answer*: Online inference computes predictions immediately upon receiving requests (low latency). Offline inference computes predictions in advance on batches of data and stores them for fast retrieval.

### Q19: Design a system for continuous retraining of models.
*Category*: Scaling & Monitoring

*Answer*: An orchestrator monitors target labels (e.g. defaults). When new label feedback accumulates, it triggers a training pipeline, registers the new model version, runs validation tests, and promotes it to staging.

### Q20: How do you choose between CPU and GPU for model serving?
*Category*: Scaling & Monitoring

*Answer*: CPUs are sufficient for tabular ML models (Scikit-Learn, XGBoost) and have lower cost. GPUs are preferred for deep learning models (NLP, Computer Vision) where parallel execution speed offsets hardware cost.


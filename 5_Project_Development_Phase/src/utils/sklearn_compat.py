# sklearn_compat.py
# Resolves scikit-learn 1.6 / Python 3.13 / XGBoost MRO compatibility bug.
# In scikit-learn 1.6, the tag resolution mechanism triggers MRO issues when
# executing classifiers like XGBoost which do not natively support the updated
# __sklearn_tags__ interface. This patch catches Tag errors and delegates
# cleanly back to BaseEstimator tags.
# TODO: remove when upgrading to sklearn 1.7+ or xgboost 2.2+ which resolves this natively.

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils._tags import ClassifierTags


def safe_sklearn_tags(self):
    try:
        # BaseEstimator is parent class, resolve its tags
        tags = BaseEstimator.__sklearn_tags__(self)
        tags.estimator_type = "classifier"
        tags.classifier_tags = ClassifierTags()
        tags.target_tags.required = True
        return tags
    except Exception:
        # Fallback to default empty tags if resolution fails
        return BaseEstimator.__sklearn_tags__(self)


# Apply the monkeypatch globally
ClassifierMixin.__sklearn_tags__ = safe_sklearn_tags

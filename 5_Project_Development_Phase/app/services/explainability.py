import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExplanationEngine:
    """
    Computes local feature contributions for predictions using SHAP-inspired linear coefficients.
    Supports linear models directly and tree-based models via local linear surrogates (LIME-inspired).
    """

    def __init__(self, model, preprocessing_pipeline):
        self.model = model
        self.pipeline = preprocessing_pipeline

    def explain_instance(self, input_df: pd.DataFrame) -> dict:
        """
        Calculates local feature contributions (log-odds impact) for a single record.
        """
        try:
            feature_names, instance_vals = self._get_instance_values(input_df)
            coefs, intercept = self._get_coefficients_and_intercept(feature_names, instance_vals)
            return self._build_explanation_factors(feature_names, instance_vals, coefs, intercept)
        except Exception as e:
            logger.error(f"Explainability computation failed: {str(e)}")
            return {"error": str(e)}

    def _get_instance_values(self, input_df: pd.DataFrame):
        transformed_arr = self.pipeline.transform(input_df)
        feature_names = self.pipeline.get_feature_names_out()
        if isinstance(transformed_arr, pd.DataFrame):
            instance_vals = transformed_arr.values[0]
        else:
            instance_vals = transformed_arr[0]
        return feature_names, instance_vals

    def _get_coefficients_and_intercept(self, feature_names, instance_vals):
        if hasattr(self.model, "coef_") and self.model.coef_ is not None:
            coefs = self.model.coef_[0]
            intercept = self.model.intercept_[0]
            return coefs, intercept

        # Tree-based model surrogate explanation (LIME-inspired)
        logger.info("Non-linear model detected. Fitting local Ridge surrogate...")
        n_features = len(feature_names)

        # Generate perturbed samples around the scaled instance
        np.random.seed(42)
        perturbations = np.random.normal(0, 0.05, size=(50, n_features))
        perturbed_samples = instance_vals + perturbations

        # Predict probabilities/scores for perturbed samples
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(perturbed_samples)[:, 1]
        elif hasattr(self.model, "decision_function"):
            probs = self.model.decision_function(perturbed_samples)
        else:
            probs = self.model.predict(perturbed_samples)

        # Fit weighted local surrogate model: y = w * x_diff + intercept
        distances = np.sqrt(np.sum(perturbations**2, axis=1))
        weights = np.exp(-(distances**2) / (2 * (0.25**2)))

        surrogate = Ridge(alpha=1.0)
        surrogate.fit(perturbations, probs, sample_weight=weights)

        return surrogate.coef_, float(surrogate.intercept_)

    def _clean_feature_name(self, name: str) -> str:
        clean_name = name.split("__")[-1].replace("_", " ").title()
        clean_name = clean_name.replace("Flag ", "").replace("Amt ", "").replace("Cnt ", "")
        mapping = {
            "Code Gender": "Gender",
            "Own Realty": "Owns Property",
            "Own Car": "Owns Car",
            "Income Total": "Annual Income",
        }
        return mapping.get(clean_name, clean_name)

    def _build_explanation_factors(self, feature_names, instance_vals, coefs, intercept):
        contributions = {}
        for name, val, coef in zip(feature_names, instance_vals, coefs):
            contributions[name] = float(val * coef)

        # Sort contributions by absolute impact
        sorted_contrib = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)

        risk_factors = []
        support_factors = []

        for name, val in sorted_contrib:
            clean_name = self._clean_feature_name(name)
            factor_data = {"feature": clean_name, "impact": round(val, 4)}
            if val > 0:
                risk_factors.append(factor_data)
            else:
                support_factors.append(factor_data)

        return {
            "intercept": float(intercept),
            "risk_factors": risk_factors[:5],
            "support_factors": support_factors[:5],
        }

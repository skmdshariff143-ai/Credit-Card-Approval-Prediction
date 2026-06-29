import numpy as np
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ExplanationEngine:
    """
    Computes local feature contributions for predictions using SHAP-inspired linear coefficients.
    """
    def __init__(self, model, preprocessing_pipeline):
        self.model = model
        self.pipeline = preprocessing_pipeline

    def explain_instance(self, input_df: pd.DataFrame) -> dict:
        """
        Calculates local feature contributions (log-odds impact) for a single record.
        """
        try:
            # Transform raw input
            transformed_arr = self.pipeline.transform(input_df)
            feature_names = self.pipeline.get_feature_names_out()
            
            # Retrieve model coefficients (assuming Logistic Regression)
            if hasattr(self.model, "coef_"):
                coefs = self.model.coef_[0]
                intercept = self.model.intercept_[0]
            else:
                # Fallback for tree-based models
                coefs = np.zeros(len(feature_names))
                intercept = 0.0

            # Calculate individual contributions (scaled relative to averages/standard deviations)
            contributions = {}
            for name, val, coef in zip(feature_names, transformed_arr[0], coefs):
                impact = float(val * coef)
                contributions[name] = impact

            # Sort contributions
            sorted_contrib = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Extract top positive (rejection risk) and top negative (approval support) features
            risk_factors = []
            support_factors = []
            
            for name, val in sorted_contrib:
                # Clean up names for presentation
                clean_name = name.split("__")[-1].replace("_", " ").title()
                if val > 0:
                    risk_factors.append({"feature": clean_name, "impact": round(val, 4)})
                else:
                    support_factors.append({"feature": clean_name, "impact": round(val, 4)})

            return {
                "intercept": float(intercept),
                "risk_factors": risk_factors[:5],
                "support_factors": support_factors[:5]
            }
        except Exception as e:
            logger.error(f"Explainability computation failed: {str(e)}")
            return {"error": str(e)}

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from src.utils.logger import get_logger

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
            # Transform raw input
            transformed_arr = self.pipeline.transform(input_df)
            feature_names = self.pipeline.get_feature_names_out()
            
            # Handle both pandas DataFrame and numpy array output from transform
            if isinstance(transformed_arr, pd.DataFrame):
                instance_vals = transformed_arr.values[0]
            else:
                instance_vals = transformed_arr[0]
            
            # Retrieve model coefficients or fit local linear surrogate
            if hasattr(self.model, "coef_") and self.model.coef_ is not None:
                coefs = self.model.coef_[0]
                intercept = self.model.intercept_[0]
            else:
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
                else:
                    # Fallback to decision function or raw predictions
                    if hasattr(self.model, "decision_function"):
                        probs = self.model.decision_function(perturbed_samples)
                    else:
                        probs = self.model.predict(perturbed_samples)
                
                # Fit weighted local surrogate model: y = w * x_diff + intercept
                # Weight samples higher if they are closer to the original instance (standard normal kernel)
                distances = np.sqrt(np.sum(perturbations ** 2, axis=1))
                weights = np.exp(-(distances ** 2) / (2 * (0.25 ** 2)))
                
                surrogate = Ridge(alpha=1.0)
                surrogate.fit(perturbations, probs, sample_weight=weights)
                
                coefs = surrogate.coef_
                intercept = float(surrogate.intercept_)

            # Calculate individual contributions (scaled relative to averages/standard deviations)
            contributions = {}
            for name, val, coef in zip(feature_names, instance_vals, coefs):
                impact = float(val * coef)
                contributions[name] = impact

            # Sort contributions by absolute impact
            sorted_contrib = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Extract top positive (rejection risk) and top negative (approval support) features
            risk_factors = []
            support_factors = []
            
            for name, val in sorted_contrib:
                # Clean up names for presentation (remove category prefixes)
                clean_name = name.split("__")[-1].replace("_", " ").title()
                
                # Avoid redundant clean names
                clean_name = clean_name.replace("Flag ", "").replace("Amt ", "").replace("Cnt ", "")
                if clean_name == "Code Gender":
                    clean_name = "Gender"
                elif clean_name == "Own Realty":
                    clean_name = "Owns Property"
                elif clean_name == "Own Car":
                    clean_name = "Owns Car"
                elif clean_name == "Income Total":
                    clean_name = "Annual Income"
                
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

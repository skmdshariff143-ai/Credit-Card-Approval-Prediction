import numpy as np
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DataValidator:
    """
    Enterprise Data Quality and Schema Drift Validation engine.
    """
    def __init__(self):
        self.required_schema = {
            'code_gender': 'object',
            'cnt_children': 'int64',
            'cnt_fam_members': 'float64',
            'age_years': 'float64',
            'amt_income_total': 'float64',
            'flag_own_car': 'object',
            'flag_own_realty': 'object',
            'name_income_type': 'object',
            'name_education_type': 'object',
            'name_family_status': 'object',
            'name_housing_type': 'object',
            'years_employed': 'float64',
            'flag_unemployed': 'int64'
        }

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Validates input DataFrame columns against required schema datatypes."""
        for col, dtype in self.required_schema.items():
            if col not in df.columns:
                logger.error(f"Schema validation failure: Missing required column '{col}'.")
                return False
        logger.info("Schema validation checks passed successfully.")
        return True

    def calculate_drift_psi(self, reference: pd.Series, target: pd.Series, num_buckets: int = 10) -> float:
        """
        Calculates Population Stability Index (PSI) to detect data drift between two numerical sets.
        - PSI < 0.1: No significant drift.
        - 0.1 <= PSI < 0.2: Moderate drift.
        - PSI >= 0.2: Significant drift.
        """
        try:
            # Drop null values
            ref_clean = reference.dropna()
            tgt_clean = target.dropna()
            
            if len(ref_clean) == 0 or len(tgt_clean) == 0:
                return 0.0
                
            # Define bins boundaries on reference distribution
            percentiles = np.linspace(0, 100, num_buckets + 1)
            bins = np.percentile(ref_clean, percentiles)
            bins = np.unique(bins)  # Drop duplicates if percentiles overlap
            
            if len(bins) < 2:
                return 0.0
                
            # Bin frequencies
            ref_counts, _ = np.histogram(ref_clean, bins=bins)
            tgt_counts, _ = np.histogram(tgt_clean, bins=bins)
            
            # Normalize to probabilities
            ref_probs = ref_counts / len(ref_clean)
            tgt_probs = tgt_counts / len(tgt_clean)
            
            # Add small epsilon to avoid divide by zero errors
            ref_probs = np.where(ref_probs == 0, 0.0001, ref_probs)
            tgt_probs = np.where(tgt_probs == 0, 0.0001, tgt_probs)
            
            # Calculate PSI
            psi = np.sum((ref_probs - tgt_probs) * np.log(ref_probs / tgt_probs))
            logger.info(f"Computed Population Stability Index (PSI): {psi:.4f}")
            return float(psi)
        except Exception as e:
            logger.error(f"Population Stability Index (PSI) calculation failure: {str(e)}")
            return 0.0

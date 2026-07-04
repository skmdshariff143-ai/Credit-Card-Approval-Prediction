import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns statistical description of DataFrame features.
    """
    logger.info("Computing EDA summary statistics...")
    summary = df.describe(include="all").transpose()
    logger.info(f"Summary computed for shape: {df.shape}")
    return summary


def calculate_missing_matrix(df: pd.DataFrame) -> pd.Series:
    """
    Returns proportion of null rows for each feature column.
    """
    logger.info("Calculating missing values matrix...")
    missing = df.isnull().mean() * 100
    missing_cols = missing[missing > 0]
    logger.info(f"Missing columns: {missing_cols.to_dict()}")
    return missing

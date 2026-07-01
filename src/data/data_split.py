import pandas as pd
from sklearn.model_selection import train_test_split

from configs.constants import RANDOM_STATE, TARGET_COL, TEST_SIZE
from src.utils.exceptions import DataPreprocessingError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def perform_stratified_split(df: pd.DataFrame):
    """
    Splits the cleaned dataset into stratified train and test splits.
    """
    logger.info("Executing stratified train-test split (80/20)...")
    if TARGET_COL not in df.columns:
        logger.error(f"Target column '{TARGET_COL}' not found in dataframe.")
        raise DataPreprocessingError(f"Target column '{TARGET_COL}' missing.")

    try:
        X = df.drop(columns=[TARGET_COL])
        y = df[TARGET_COL]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
        )
        logger.info(f"Split completed. Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(f"Failed to split data: {str(e)}")
        raise DataPreprocessingError(f"Split execution failed: {str(e)}")

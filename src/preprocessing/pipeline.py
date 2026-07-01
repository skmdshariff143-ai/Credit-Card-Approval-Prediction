import os

import pandas as pd

from configs.config import config
from configs.constants import TARGET_COL
from src.data.data_split import perform_stratified_split
from src.data.load_data import DataLoader
from src.preprocessing.duplicates import DuplicateHandler
from src.preprocessing.encoding import CategoricalEncoder
from src.preprocessing.feature_engineering import FeatureEngineer
from src.preprocessing.missing_values import MissingValueImputer
from src.preprocessing.outliers import OutlierCapper
from src.preprocessing.scaling import NumericalScaler
from src.utils.exceptions import DataPreprocessingError
from src.utils.helper import save_pkl
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PreprocessingPipeline:
    """
    Unified pipeline orchestrating data ingestion, duplicates removal, invalid data cleansing,
    feature engineering, split partition, numerical standardizations, and categorical encodings.
    """

    def __init__(self):
        paths = config.get_paths()
        self.processed_dir = paths["processed_dir"]
        self.models_dir = paths["models_dir"]

        self.dup_handler = DuplicateHandler()
        self.engineer = FeatureEngineer()
        self.imputer = MissingValueImputer()
        self.capper = OutlierCapper(factor=1.5)
        self.encoder = CategoricalEncoder()
        self.scaler = NumericalScaler()

        # Keep track of columns
        self.num_cols = []
        self.cat_cols = []
        self.feature_names = []

    def load_and_clean_raw(self):
        """
        Loads raw files, cleans obvious logical range invalidations.
        """
        logger.info("Loading raw data for pipeline...")
        loader = DataLoader()
        app_df, credit_df = loader.load_all()

        # Duplicate removal
        app_clean = self.dup_handler.remove_duplicates(app_df)

        # Invalid data cleansing
        # 1. Negative income -> absolute value
        if "AMT_INCOME_TOTAL" in app_clean.columns:
            app_clean["AMT_INCOME_TOTAL"] = app_clean["AMT_INCOME_TOTAL"].abs()
        # 2. Negative children -> set to 0
        if "CNT_CHILDREN" in app_clean.columns:
            app_clean["CNT_CHILDREN"] = app_clean["CNT_CHILDREN"].clip(lower=0)
        # 3. Family members < 1 -> set to 1
        if "CNT_FAM_MEMBERS" in app_clean.columns:
            app_clean["CNT_FAM_MEMBERS"] = app_clean["CNT_FAM_MEMBERS"].clip(lower=1)

        return app_clean, credit_df

    def process_data(self) -> pd.DataFrame:
        """
        Runs ingestion, cleaning, target derivation, feature engineering, and
        returns the fully engineered and merged dataset (pre-split).
        """
        app_clean, credit_df = self.load_and_clean_raw()

        # Target derivation
        bad_statuses = {"2", "3", "4", "5"}
        credit_df["IS_BAD"] = credit_df["STATUS"].astype(str).apply(lambda x: 1 if x in bad_statuses else 0)
        target_df = credit_df.groupby("ID")["IS_BAD"].max().reset_index()
        target_df.rename(columns={"IS_BAD": TARGET_COL}, inplace=True)

        # Join target
        merged_df = pd.merge(app_clean, target_df, on="ID", how="inner")
        logger.info(f"Target matched successfully. Shape: {merged_df.shape}")

        # Feature engineering
        engineered_df = self.engineer.transform(merged_df)
        return engineered_df

    def execute_full_pipeline(self):
        """
        Executes end-to-end preprocessing, splits datasets, fits transformations,
        oversamples training split, saves files, and serializes pickle files.
        """
        logger.info("Starting complete preprocessing pipeline execution...")
        try:
            # 1. Clean & Feature Engineer
            df_full = self.process_data()

            # Save fully merged processed file
            os.makedirs(self.processed_dir, exist_ok=True)
            full_processed_path = os.path.join(self.processed_dir, "credit_card_processed.csv")
            df_full.to_csv(full_processed_path, index=False)
            logger.info(f"Saved full processed data to: {full_processed_path}")

            # 2. Stratified Split (80/20)
            X_train, X_test, y_train, y_test = perform_stratified_split(df_full)

            # Drop ID metadata column
            X_train = X_train.drop(columns=["ID"], errors="ignore")
            X_test = X_test.drop(columns=["ID"], errors="ignore")

            # Identify columns for transformations
            # Numerical features include new stability score & engineered continuous fields
            self.num_cols = [
                "AMT_INCOME_TOTAL",
                "CNT_CHILDREN",
                "CNT_FAM_MEMBERS",
                "AGE_YEARS",
                "YEARS_EMPLOYED",
                "INCOME_PER_MEMBER",
                "FINANCIAL_STABILITY_SCORE",
            ]
            # Categorical features include original text categories and new binned categories
            self.cat_cols = [
                "CODE_GENDER",
                "FLAG_OWN_CAR",
                "FLAG_OWN_REALTY",
                "NAME_INCOME_TYPE",
                "NAME_EDUCATION_TYPE",
                "NAME_FAMILY_STATUS",
                "NAME_HOUSING_TYPE",
                "OCCUPATION_TYPE",
                "INCOME_GROUP",
                "AGE_GROUP",
                "EXPERIENCE_BUCKET",
            ]

            # 3. Fit Imputer
            self.imputer.fit(X_train, self.num_cols, self.cat_cols)
            X_train_imputed = self.imputer.transform(X_train)
            X_test_imputed = self.imputer.transform(X_test)

            # 4. Fit Capper
            self.capper.fit(X_train_imputed, self.num_cols)
            X_train_capped = self.capper.transform(X_train_imputed)
            X_test_capped = self.capper.transform(X_test_imputed)

            # 5. Fit Encoder
            self.encoder.fit(X_train_capped, self.cat_cols)
            X_train_encoded = self.encoder.transform(X_train_capped)
            X_test_encoded = self.encoder.transform(X_test_capped)

            # 6. Fit Scaler
            self.scaler.fit(X_train_encoded, self.num_cols)
            X_train_scaled = self.scaler.transform(X_train_encoded)
            X_test_scaled = self.scaler.transform(X_test_encoded)

            self.feature_names = list(X_train_scaled.columns)

            # 7. Imbalance Handling - Oversample training class 1 in Pandas
            # Combine X_train_scaled and y_train
            train_full = pd.concat([X_train_scaled, y_train], axis=1)
            class_0 = train_full[train_full[TARGET_COL] == 0]
            class_1 = train_full[train_full[TARGET_COL] == 1]

            # Oversample class 1 to match class 0 count
            class_1_over = class_1.sample(len(class_0), replace=True, random_state=42)
            train_balanced = pd.concat([class_0, class_1_over], axis=0).sample(frac=1.0, random_state=42)

            X_train_final = train_balanced.drop(columns=[TARGET_COL])
            y_train_final = train_balanced[TARGET_COL]

            # 8. Save final datasets
            X_train_final.to_csv(os.path.join(self.processed_dir, "X_train.csv"), index=False)
            y_train_final.to_csv(os.path.join(self.processed_dir, "y_train.csv"), index=False)
            X_test_scaled.to_csv(os.path.join(self.processed_dir, "X_test.csv"), index=False)
            y_test.to_csv(os.path.join(self.processed_dir, "y_test.csv"), index=False)

            logger.info("Saved all train/test splits to processed directory.")

            # 9. Save artifacts to models/
            os.makedirs(self.models_dir, exist_ok=True)
            save_pkl(self.scaler.scaler, os.path.join(self.models_dir, "scaler.pkl"))
            save_pkl(self.encoder.encoder, os.path.join(self.models_dir, "encoder.pkl"))
            save_pkl(self, os.path.join(self.models_dir, "preprocessing_pipeline.pkl"))
            logger.info("Saved scaler.pkl, encoder.pkl, and preprocessing_pipeline.pkl.")

            return X_train_final.shape, X_test_scaled.shape

        except Exception as e:
            logger.exception("Failed end-to-end preprocessing execution:")
            raise DataPreprocessingError(f"Preprocessing pipeline failure: {str(e)}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies imputer, capper, encoder, and scaler transformations.
        Called during inference serving.
        """
        try:
            # Check ID column
            df_cleaned = df.drop(columns=["ID"], errors="ignore")

            # Apply feature engineering transformations first
            df_engineered = self.engineer.transform(df_cleaned)

            # Impute, cap, encode, scale
            df_imputed = self.imputer.transform(df_engineered)
            df_capped = self.capper.transform(df_imputed)
            df_encoded = self.encoder.transform(df_capped)
            df_scaled = self.scaler.transform(df_encoded)

            # Filter and order columns matching the fitted template
            for col in self.feature_names:
                if col not in df_scaled.columns:
                    df_scaled[col] = 0.0
            return df_scaled[self.feature_names]
        except Exception as e:
            logger.error(f"Inference preprocessing failed: {str(e)}")
            raise DataPreprocessingError(f"Inference preprocessing failure: {str(e)}")

    def get_feature_names_out(self) -> list:
        """
        Returns list of processed column names after encoding and scaling.
        """
        return self.feature_names

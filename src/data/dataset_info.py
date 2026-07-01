import json
import os

import pandas as pd

from configs.config import config
from configs.constants import TARGET_COL
from src.data.load_data import DataLoader
from src.utils.helper import save_json
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatasetMetadataGenerator:
    """
    Computes statistical summaries, missing values, duplicates, and
    imbalances across loaded application and credit history datasets.
    """

    def __init__(self):
        self.loader = DataLoader()
        paths = config.get_paths()
        self.reports_dir = paths["reports_dir"]
        self.models_dir = paths["models_dir"]

    def generate_and_save_metadata(self) -> dict:
        """
        Loads datasets, calculates profiling indicators, and writes them to a JSON file.
        """
        logger.info("Initializing metadata profile generator...")
        app_df = self.loader.load_application_records()
        credit_df = self.loader.load_credit_records()

        # Delinquency targeting mapping
        bad_statuses = {"2", "3", "4", "5"}
        credit_df["IS_BAD"] = credit_df["STATUS"].astype(str).apply(lambda x: 1 if x in bad_statuses else 0)
        target_df = credit_df.groupby("ID")["IS_BAD"].max().reset_index()
        target_df.rename(columns={"IS_BAD": TARGET_COL}, inplace=True)

        merged_df = pd.merge(app_df, target_df, on="ID", how="inner")
        logger.info(f"Target variable merged. Records matched: {merged_df.shape[0]}")

        # Compute counts
        app_records = int(app_df.shape[0])
        app_cols = int(app_df.shape[1])
        credit_records = int(credit_df.shape[0])
        credit_cols = int(credit_df.shape[1])

        # Missing values (Application)
        missing_app = app_df.isnull().sum().to_dict()
        missing_app = {k: int(v) for k, v in missing_app.items() if v > 0}

        # Duplicates
        dup_app = int(app_df.duplicated().sum())
        dup_credit = int(credit_df.duplicated().sum())

        # Target Distribution
        target_counts = merged_df[TARGET_COL].value_counts().to_dict()
        total_targets = sum(target_counts.values())

        target_distribution = {}
        for cls, count in target_counts.items():
            label = "Approved (Good)" if cls == 0 else "Rejected (Bad)"
            pct = round((count / total_targets) * 100, 2)
            target_distribution[label] = {"count": int(count), "percentage": float(pct)}

        metadata = {
            "dataset_version": "1.0.0",
            "download_date": "2026-06-29",
            "dataset_source": "Kaggle Credit Card Approval Prediction Dataset",
            "license": "CC0: Public Domain",
            "application_records": app_records,
            "application_columns": app_cols,
            "credit_records": credit_records,
            "credit_columns": credit_cols,
            "merged_records": int(merged_df.shape[0]),
            "application_duplicates": dup_app,
            "credit_duplicates": dup_credit,
            "application_missing_fields": missing_app,
            "target_classes_distribution": target_distribution,
        }

        # Write reports file
        os.makedirs(self.reports_dir, exist_ok=True)
        meta_path = os.path.join(self.reports_dir, "dataset_metadata.json")
        save_json(metadata, meta_path)
        logger.info(f"Dataset metadata successfully written to: {meta_path}")

        return metadata


if __name__ == "__main__":
    generator = DatasetMetadataGenerator()
    generator.generate_and_save_metadata()

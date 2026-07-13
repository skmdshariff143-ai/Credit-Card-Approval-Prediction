import os

import pandas as pd

from config.config import config
from config.constants import BINARY_COLS, CATEGORICAL_COLS, NUMERICAL_COLS
from src.utils.exceptions import DataValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataValidator:
    """
    Executes validation checks on input data schemas, types, ranges, categories,
    and target distributions. Generates validation reports.
    """

    def __init__(self):
        paths = config.get_paths()
        self.reports_dir = paths["reports_dir"]
        self.expected_app_cols = set(NUMERICAL_COLS + CATEGORICAL_COLS + BINARY_COLS)

    def validate_dataset(self, app_df: pd.DataFrame, credit_df: pd.DataFrame) -> bool:
        """
        Runs comprehensive checks and saves a markdown validation report.
        """
        logger.info("Executing comprehensive dataset validation...")

        report_lines = []
        report_lines.append("# Data Validation Report\n")
        report_lines.append("## 1. Schema & Null Checks")

        self._validate_schema_and_nulls(app_df, credit_df, report_lines)
        invalid_types = self._validate_types_and_ranges(app_df, report_lines)
        self._validate_categorical(app_df, report_lines)

        # Save report
        os.makedirs(self.reports_dir, exist_ok=True)
        report_path = os.path.join(self.reports_dir, "Validation_Report.md")
        with open(report_path, "w") as f:
            f.write("\n".join(report_lines))
        logger.info(f"Validation report saved to: {report_path}")

        # Verify schema
        if len(invalid_types) > 0:
            raise DataValidationError("Schema validation failed: Invalid data types found.")

        return True

    def _validate_schema_and_nulls(self, app_df: pd.DataFrame, credit_df: pd.DataFrame, report_lines: list):
        app_rows = app_df.shape[0]
        credit_rows = credit_df.shape[0]
        app_dups = app_df.duplicated().sum()
        credit_dups = credit_df.duplicated().sum()

        report_lines.append(f"- **Application records**: {app_rows} (Duplicates: {app_dups})")
        report_lines.append(f"- **Credit history records**: {credit_rows} (Duplicates: {credit_dups})")

        # Missing values & null percentages
        report_lines.append("\n### Null Percentages (Application):")
        null_counts = app_df.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                pct = (count / app_rows) * 100
                report_lines.append(f"  - **{col}**: {count} nulls ({pct:.2f}%)")
        if not null_counts.any():
            report_lines.append("  - No missing values detected.")

    def _validate_types_and_ranges(self, app_df: pd.DataFrame, report_lines: list) -> list:
        report_lines.append("\n## 2. Type & Range Validation")
        invalid_types = []
        for col in NUMERICAL_COLS:
            if col in app_df.columns and not pd.api.types.is_numeric_dtype(app_df[col]):
                invalid_types.append(col)

        if invalid_types:
            report_lines.append(f"- **[FAILED]** Column types are not numeric: {invalid_types}")
        else:
            report_lines.append("- **[PASSED]** All numerical feature data types are correct.")

        # Invalid numeric ranges (Income > 0, family size >= 1, children >= 0)
        invalid_ranges = []
        if "AMT_INCOME_TOTAL" in app_df.columns and (app_df["AMT_INCOME_TOTAL"] <= 0).any():
            invalid_ranges.append("AMT_INCOME_TOTAL contains negative/zero values.")
        if "CNT_FAM_MEMBERS" in app_df.columns and (app_df["CNT_FAM_MEMBERS"] < 1).any():
            invalid_ranges.append("CNT_FAM_MEMBERS contains values less than 1.")
        if "CNT_CHILDREN" in app_df.columns and (app_df["CNT_CHILDREN"] < 0).any():
            invalid_ranges.append("CNT_CHILDREN contains negative values.")

        if invalid_ranges:
            report_lines.append("- **[WARNING]** Numeric range outliers/anomalies:")
            for item in invalid_ranges:
                report_lines.append(f"  - {item}")
        else:
            report_lines.append("- **[PASSED]** All basic numerical ranges are valid.")

        # Invalid dates (Birth days must be negative offset)
        if "DAYS_BIRTH" in app_df.columns and (app_df["DAYS_BIRTH"] > 0).any():
            report_lines.append("- **[WARNING]** DAYS_BIRTH contains positive values (born in future).")
        else:
            report_lines.append("- **[PASSED]** DAYS_BIRTH values are valid negative offsets.")
        return invalid_types

    def _validate_categorical(self, app_df: pd.DataFrame, report_lines: list):
        report_lines.append("\n## 3. Categorical Distribution checks")
        gender_cats = app_df["CODE_GENDER"].unique() if "CODE_GENDER" in app_df.columns else []
        report_lines.append(f"- **CODE_GENDER categories**: {list(gender_cats)}")
        if not set(gender_cats).issubset({"M", "F"}):
            report_lines.append("  - **[WARNING]** Unexpected values in CODE_GENDER.")

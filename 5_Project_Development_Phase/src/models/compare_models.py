import os

import pandas as pd

from config.config import config
from src.utils.helper import save_json
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelComparator:
    """
    Compares and ranks models on training/inference times and standard classification scores.
    Saves outputs to models/ directory and generates comparison reports.
    """

    def __init__(self):
        paths = config.get_paths()
        self.models_dir = paths["models_dir"]
        self.reports_dir = paths["reports_dir"]
        self.results = []

    def add_model_metrics(self, name: str, metrics: dict, train_time: float, inference_time: float):
        """
        Appends metrics dict and execution speeds of a model to comparison store.
        """
        record = {
            "Model": name,
            "Accuracy": metrics["Accuracy"],
            "Precision": metrics["Precision"],
            "Recall": metrics["Recall"],
            "F1-Score": metrics["F1-Score"],
            "ROC-AUC": metrics["ROC-AUC"],
            "Balanced_Accuracy": metrics.get("Balanced_Accuracy", metrics["Accuracy"]),
            "Log_Loss": metrics.get("Log_Loss", 0.0),
            "Training_Time_Sec": round(train_time, 4),
            "Prediction_Time_Sec": round(inference_time, 4),
        }
        self.results.append(record)

    def compare_and_rank(self) -> pd.DataFrame:
        """
        Creates a comparison table, ranks models by F1-Score / ROC-AUC,
        and serializes artifacts to models/ and reports/ folders.
        """
        logger.info("Executing comparison ranking logic...")
        df = pd.DataFrame(self.results)

        # Sort by F1-Score and ROC-AUC descending
        df = df.sort_values(by=["F1-Score", "ROC-AUC"], ascending=False).reset_index(drop=True)
        df["Rank"] = df.index + 1

        # Reorder columns
        cols = [
            "Rank",
            "Model",
            "F1-Score",
            "ROC-AUC",
            "Accuracy",
            "Precision",
            "Recall",
            "Balanced_Accuracy",
            "Log_Loss",
            "Training_Time_Sec",
            "Prediction_Time_Sec",
        ]
        df = df[cols]

        # Save model_comparison.csv
        csv_path = os.path.join(self.models_dir, "model_comparison.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"Model comparison table saved to: {csv_path}")

        # Save model_metrics.json
        meta_json_path = os.path.join(self.models_dir, "model_metrics.json")
        save_json(self.results, meta_json_path)
        logger.info(f"Model metrics JSON saved to: {meta_json_path}")

        # Write reports file Model_Comparison.md
        self._write_comparison_report(df)

        return df

    def _write_comparison_report(self, df: pd.DataFrame):
        """
        Generates Model_Comparison.md detailing strengths/weaknesses and selections.
        """
        report_path = os.path.join(self.reports_dir, "Model_Comparison.md")

        # Native markdown table formatter
        headers = list(df.columns)
        md_table_lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for _, row in df.iterrows():
            row_vals = []
            for col in headers:
                val = row[col]
                if isinstance(val, float):
                    row_vals.append(f"{val:.4f}")
                else:
                    row_vals.append(str(val))
            md_table_lines.append("| " + " | ".join(row_vals) + " |")
        md_table_str = "\n".join(md_table_lines)

        report_content = [
            "# Model Comparison & Ranking Report\n",
            (
                "This report compares and ranks candidate risk models based on F1-Score, ROC-AUC, "
                "and processing time profiles.\n"
            ),
            "## 1. Metrics Performance Table\n",
            md_table_str,
            "\n## 2. Algorithm Strengths & Weaknesses Assessment\n",
            "### Logistic Regression",
            (
                "- **Strengths**: High business interpretability, linear decision boundary mapping, "
                "and sub-millisecond inference speed."
            ),
            "- **Weaknesses**: Underfits complex feature interactions; lower Recall/F1 values.",
            "\n### Decision Tree Classifier",
            "- **Strengths**: Simple visual tree rules, natively handles mixed data types.",
            "- **Weaknesses**: Prone to overfitting on small data partitions; higher variance.",
            "\n### Random Forest Classifier",
            (
                "- **Strengths**: Exceptional bagging stability, lower variance, reduces overfitting, "
                "and ranks features accurately."
            ),
            "- **Weaknesses**: Larger file sizes; slower training on multiple trees.",
            "\n### XGBoost Classifier",
            (
                "- **Strengths**: State-of-the-art boosting formulation, optimizes F1 target objectives, "
                "robust missing values handling."
            ),
            "- **Weaknesses**: Hyperparameter space requires extensive tuning; complex to interpret visually.",
            "\n## 3. Final Recommendation Summary",
            f"The best model selected by F1-Score objective is **{df.loc[0, 'Model']}** (Rank 1).",
        ]

        try:
            with open(report_path, "w") as f:
                f.write("\n".join(report_content))
            logger.info(f"Comparison report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Failed to write comparison report: {str(e)}")

    def save_classification_report_txt(self, name: str, report_str: str):
        """
        Saves the text classification report to models/classification_report.txt.
        """
        txt_path = os.path.join(self.models_dir, "classification_report.txt")
        try:
            with open(txt_path, "w") as f:
                f.write(f"=== Classification Report - Deployed Model: {name} ===\n\n")
                f.write(report_str)
            logger.info(f"Classification report text saved to: {txt_path}")
        except Exception as e:
            logger.error(f"Failed to save classification report text: {str(e)}")

        # Save to reports folder as well
        eval_report_path = os.path.join(self.reports_dir, "Evaluation_Report.md")
        try:
            with open(eval_report_path, "w") as f:
                f.write("# Model Evaluation Report\n\n")
                f.write(f"The best registered model is **{name}**.\n\n")
                f.write("## 1. Classification Metrics Summary\n")
                f.write("```text\n")
                f.write(report_str)
                f.write("\n```\n")
            logger.info(f"Evaluation report saved to: {eval_report_path}")
        except Exception as e:
            logger.error(f"Failed to write evaluation report: {str(e)}")


ClassModelComparator = ModelComparator

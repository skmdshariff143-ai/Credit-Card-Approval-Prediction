import os
import pandas as pd
from configs.config import config
from src.utils.logger import get_logger
from src.utils.helper import save_json

logger = get_logger(__name__)

class ModelComparator:
    """
    Compares metrics across multiple models and outputs visual markdown comparison tables.
    """
    def __init__(self):
        paths = config.get_paths()
        self.reports_dir = paths["reports_dir"]
        self.models_dir = paths["models_dir"]
        self.results = []
        
    def add_model_metrics(self, name: str, metrics: dict):
        """
        Appends metrics dict of a model to comparison store.
        """
        metrics_copy = metrics.copy()
        metrics_copy["Model"] = name
        self.results.append(metrics_copy)
        
    def compare_and_report(self) -> pd.DataFrame:
        """
        Constructs comparison DataFrame, saves metrics json, and outputs summary report.
        """
        logger.info("Generating model comparison report...")
        df = pd.DataFrame(self.results)
        
        # Ensure 'Model' is the first column
        cols = ["Model"] + [col for col in df.columns if col != "Model"]
        df = df[cols]
        
        # Save comparison JSON metrics
        save_json(self.results, os.path.join(self.models_dir, "model_metrics.json"))
        
        # Print comparison table to logger
        logger.info("\n" + df.to_string(index=False))
        
        # Create reports file Model_Report.md
        report_path = os.path.join(self.reports_dir, "Model_Report.md")
        try:
            with open(report_path, 'w') as f:
                f.write("# Model Performance Report\n\n")
                f.write("Evaluation results across baseline and tuned models:\n\n")
                f.write(df.to_markdown(index=False))
                f.write("\n\n*Evaluation performed using 20% test split stratified by the delinquency target variable.*\n")
            logger.info(f"Model comparison report written to: {report_path}")
        except Exception as e:
            logger.error(f"Failed to write comparison report: {str(e)}")
            
        return df

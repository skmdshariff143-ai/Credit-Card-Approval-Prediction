import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc
from configs.config import config
from src.utils.logger import get_logger
from src.utils.exceptions import ModelEvaluationError

logger = get_logger(__name__)

class ModelEvaluator:
    """
    Orchestrates calculation of classification metrics and saves visual assets (ROC, 
    PR-curves, confusion matrices, feature importances) to screenshots/models/.
    """
    def __init__(self):
        paths = config.get_paths()
        # Direct folder screenshots/models/ as required
        self.models_screenshots_dir = os.path.join(paths["raw_dir"].parent.parent, "screenshots", "models")
        os.makedirs(self.models_screenshots_dir, exist_ok=True)
        
    def plot_confusion_matrix(self, name: str, y_true, y_pred):
        """
        Generates and saves confusion matrix heatmap.
        """
        logger.info(f"Generating confusion matrix plot for '{name}'...")
        try:
            cm = confusion_matrix(y_true, y_pred)
            plt.figure(figsize=(6, 5))
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Approved (0)', 'Rejected (1)'],
                yticklabels=['Approved (0)', 'Rejected (1)']
            )
            plt.title(f"Confusion Matrix - {name}", fontsize=12, fontweight='bold')
            plt.ylabel("Actual Status")
            plt.xlabel("Predicted Status")
            plt.tight_layout()
            
            output_path = os.path.join(self.models_screenshots_dir, f"{name}_confusion_matrix.png")
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved confusion matrix for {name} to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot confusion matrix for {name}: {str(e)}")

    def plot_roc_curve(self, name: str, y_true, y_prob):
        """
        Generates and saves the ROC curve for a model.
        """
        logger.info(f"Generating ROC curve for '{name}'...")
        try:
            fpr, tpr, _ = roc_curve(y_true, y_prob)
            roc_auc = auc(fpr, tpr)
            
            plt.figure(figsize=(6, 5))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f"ROC curve (AUC = {roc_auc:.4f})")
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title(f"ROC Curve - {name}", fontsize=12, fontweight='bold')
            plt.legend(loc="lower right")
            plt.grid(True)
            plt.tight_layout()
            
            output_path = os.path.join(self.models_screenshots_dir, f"{name}_roc_curve.png")
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved ROC curve for {name} to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot ROC curve for {name}: {str(e)}")

    def plot_precision_recall_curve(self, name: str, y_true, y_prob):
        """
        Generates and saves the Precision-Recall curve.
        """
        logger.info(f"Generating PR curve for '{name}'...")
        try:
            precision, recall, _ = precision_recall_curve(y_true, y_prob)
            pr_auc = auc(recall, precision)
            
            plt.figure(figsize=(6, 5))
            plt.plot(recall, precision, color='forestgreen', lw=2, label=f"PR curve (AUC = {pr_auc:.4f})")
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title(f"Precision-Recall Curve - {name}", fontsize=12, fontweight='bold')
            plt.legend(loc="lower left")
            plt.grid(True)
            plt.tight_layout()
            
            output_path = os.path.join(self.models_screenshots_dir, f"{name}_precision_recall_curve.png")
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved PR curve for {name} to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot Precision-Recall curve for {name}: {str(e)}")

    def plot_feature_importance(self, name: str, model, feature_names):
        """
        Generates and saves feature importance bar chart for tree-based models.
        """
        logger.info(f"Generating Feature Importance chart for '{name}'...")
        if not hasattr(model, "feature_importances_"):
            logger.warning(f"Model '{name}' does not support feature_importances_. Skipping plot.")
            return
            
        try:
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1][:15] # Top 15 features
            
            plt.figure(figsize=(10, 6))
            sns.barplot(
                x=importances[indices],
                y=np.array(feature_names)[indices],
                palette="viridis"
            )
            plt.title(f"Top 15 Feature Importances - {name}", fontsize=12, fontweight='bold')
            plt.xlabel("Relative Importance")
            plt.ylabel("Features")
            plt.tight_layout()
            
            output_path = os.path.join(self.models_screenshots_dir, f"{name}_feature_importance.png")
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved feature importance chart for {name} to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot feature importance for {name}: {str(e)}")

    def plot_model_comparison(self, comparison_df: pd.DataFrame):
        """
        Generates a comparison bar chart across models using F1-Score and ROC-AUC.
        """
        logger.info("Generating model comparison bar chart...")
        try:
            df_melt = pd.melt(
                comparison_df, 
                id_vars=["Model"], 
                value_vars=["F1-Score", "ROC-AUC"],
                var_name="Metric", 
                value_name="Score"
            )
            
            plt.figure(figsize=(8, 5))
            sns.barplot(data=df_melt, x="Model", y="Score", hue="Metric", palette="Set1")
            plt.title("Model Comparison - F1-Score vs ROC-AUC", fontsize=14, fontweight='bold')
            plt.ylim([0.0, 1.05])
            plt.ylabel("Metric Score")
            plt.xlabel("Classification Algorithm")
            plt.legend(loc="lower right")
            plt.grid(True, axis='y')
            plt.tight_layout()
            
            output_path = os.path.join(self.models_screenshots_dir, "model_comparison_bar_chart.png")
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved model comparison bar chart to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot model comparison chart: {str(e)}")

    def evaluate_model(self, name: str, model, X_test, y_test) -> dict:
        """
        Runs model predictions, computes metrics, generates plots, and returns metrics dict.
        For backward compatibility with unit tests.
        """
        from src.models.train import ModelTrainer
        from src.models.metrics import calculate_all_metrics
        trainer = ModelTrainer()
        y_pred, y_prob, _ = trainer.measure_inference_speed(model, X_test)
        metrics = calculate_all_metrics(y_test, y_pred, y_prob)
        self.plot_confusion_matrix(name, y_test, y_pred)
        if y_prob is not None:
            self.plot_roc_curve(name, y_test, y_prob)
            self.plot_precision_recall_curve(name, y_test, y_prob)
        return metrics


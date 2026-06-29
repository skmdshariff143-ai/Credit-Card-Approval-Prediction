import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from configs.config import config
from src.utils.logger import get_logger
from src.utils.exceptions import ModelEvaluationError
from src.utils.metrics import calculate_classification_metrics

logger = get_logger(__name__)

class ModelEvaluator:
    """
    Computes performance metrics and generates plots (ROC, confusion matrices) on test splits.
    """
    def __init__(self):
        paths = config.get_paths()
        self.reports_dir = paths["reports_dir"]
        self.figures_dir = paths["reports_dir"] # reports acts as parent for visual checks
        
    def evaluate_model(self, name, model, X_test, y_test) -> dict:
        """
        Runs predictions on test split and computes evaluation metrics.
        """
        logger.info(f"Running evaluation metrics for model '{name}'...")
        try:
            y_pred = model.predict(X_test)
            
            # Predict probabilities if supported
            if hasattr(model, "predict_proba"):
                y_prob_raw = model.predict_proba(X_test)
                if isinstance(y_prob_raw, np.ndarray):
                    y_prob = y_prob_raw[:, 1]
                else:
                    y_prob = [p[1] for p in y_prob_raw]
            else:
                y_prob = y_pred
                
            metrics = calculate_classification_metrics(y_test, y_pred, y_prob)
            
            # Save confusion matrix plot
            self._save_confusion_matrix(name, y_test, y_pred)
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to evaluate model '{name}': {str(e)}")
            raise ModelEvaluationError(f"Model evaluation failed for {name}: {str(e)}")

    def _save_confusion_matrix(self, name, y_true, y_pred):
        """
        Generates and saves confusion matrix heatmap.
        """
        try:
            cm = confusion_matrix(y_true, y_pred)
            plt.figure(figsize=(6, 5))
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Approved (0)', 'Rejected (1)'],
                yticklabels=['Approved (0)', 'Rejected (1)']
            )
            plt.title(f"Confusion Matrix - {name}")
            plt.ylabel("Actual")
            plt.xlabel("Predicted")
            plt.tight_layout()
            
            # Save to reports folder
            os.makedirs(self.reports_dir, exist_ok=True)
            plot_path = os.path.join(self.reports_dir, f"{name}_confusion_matrix.png")
            plt.savefig(plot_path, dpi=300)
            plt.close()
            logger.info(f"Confusion matrix plot saved for {name} to {plot_path}")
        except Exception as e:
            logger.error(f"Failed to save confusion matrix plot for {name}: {str(e)}")

    def save_roc_curves(self, models_dict, X_test, y_test):
        """
        Plots combined ROC curves of all models and saves the figure.
        """
        logger.info("Plotting combined ROC curves...")
        try:
            plt.figure(figsize=(8, 6))
            
            for name, model in models_dict.items():
                if hasattr(model, "predict_proba"):
                    y_prob = model.predict_proba(X_test)
                    if isinstance(y_prob, np.ndarray):
                        y_prob = y_prob[:, 1]
                    else:
                        y_prob = [p[1] for p in y_prob]
                else:
                    y_prob = model.predict(X_test)
                    
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                auc_val = roc_auc_score(y_test, y_prob)
                
                plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.4f})")
                
            plt.plot([0, 1], [0, 1], 'k--', label="Random Guess")
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("Combined ROC Curves")
            plt.legend(loc="lower right")
            plt.grid(True)
            plt.tight_layout()
            
            plot_path = os.path.join(self.reports_dir, "combined_roc_curves.png")
            plt.savefig(plot_path, dpi=300)
            plt.close()
            logger.info(f"Combined ROC curve plot saved to {plot_path}")
        except Exception as e:
            logger.error(f"Failed to plot combined ROC curves: {str(e)}")
            raise ModelEvaluationError(f"ROC curves plot failed: {str(e)}")
ClassModelEvaluator = ModelEvaluator

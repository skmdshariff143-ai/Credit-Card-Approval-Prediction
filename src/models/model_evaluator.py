import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, roc_curve, classification_report
)
from src.utils.logger import get_logger
from src.utils.exceptions import ModelEvaluationError
from src.utils.helpers import load_yaml

logger = get_logger(__name__)

class ModelEvaluator:
    """
    Computes performance metrics, creates heatmaps and ROC plots,
    compares multiple models, and writes comparison reports.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        self.reports_dir = self.config["paths"].get("reports_dir")
        self.figures_dir = self.config["paths"].get("figures_dir")
        self.comparison_path = self.config["paths"].get("comparison_report")
        
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.figures_dir, exist_ok=True)
        
        self.results = []
        
    def evaluate_model(self, name, model, X_test, y_test):
        """
        Computes all standard classification metrics for a model and logs them.
        """
        logger.info(f"Evaluating model '{name}' on test split...")
        try:
            y_pred = model.predict(X_test)
            # Try to get prediction probabilities if supported (Logistic Regression, RF, XGBoost)
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)
                if isinstance(y_prob, np.ndarray):
                    y_prob = y_prob[:, 1]
                else:
                    y_prob = [p[1] for p in y_prob]
            else:
                y_prob = y_pred

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            roc_auc = roc_auc_score(y_test, y_prob)
            
            logger.info(f"Metrics for {name}:")
            logger.info(f"  Accuracy:  {accuracy:.4f}")
            logger.info(f"  Precision: {precision:.4f}")
            logger.info(f"  Recall:    {recall:.4f}")
            logger.info(f"  F1-Score:  {f1:.4f}")
            logger.info(f"  ROC-AUC:   {roc_auc:.4f}")
            
            # Print full classification report
            report = classification_report(y_test, y_pred, output_dict=True)
            
            # Save results list
            self.results.append({
                'Model': name,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'ROC-AUC': roc_auc
            })
            
            # Plot confusion matrix
            self._plot_confusion_matrix(name, y_test, y_pred)
            
            return {
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'ROC-AUC': roc_auc
            }
            
        except Exception as e:
            logger.error(f"Failed to evaluate model '{name}': {str(e)}")
            raise ModelEvaluationError(f"Model evaluation failed for {name}: {str(e)}")

    def _plot_confusion_matrix(self, name, y_test, y_pred):
        """
        Plots and saves confusion matrix as a Seaborn heatmap.
        """
        try:
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(6, 5))
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Approved (0)', 'Rejected (1)'], 
                yticklabels=['Approved (0)', 'Rejected (1)']
            )
            plt.title(f'Confusion Matrix - {name}')
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.tight_layout()
            
            plot_path = os.path.join(self.figures_dir, f"{name}_confusion_matrix.png")
            plt.savefig(plot_path, dpi=300)
            plt.close()
            logger.info(f"Confusion matrix plot saved for {name} to {plot_path}")
        except Exception as e:
            logger.error(f"Failed to plot confusion matrix for {name}: {str(e)}")

    def plot_roc_curves(self, models_dict, X_test, y_test):
        """
        Plots ROC curves for all models on the same plot and saves the figure.
        """
        logger.info("Plotting combined ROC curves...")
        try:
            plt.figure(figsize=(8, 6))
            
            for name, model in models_dict.items():
                if hasattr(model, "predict_proba"):
                    y_prob = model.predict_proba(X_test)[:, 1]
                else:
                    y_prob = model.predict(X_test)
                    
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                auc_val = roc_auc_score(y_test, y_prob)
                
                plt.plot(fpr, tpr, label=f'{name} (AUC = {auc_val:.4f})')
                
            plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic (ROC) Curves')
            plt.legend(loc="lower right")
            plt.grid(True)
            plt.tight_layout()
            
            plot_path = os.path.join(self.figures_dir, "combined_roc_curves.png")
            plt.savefig(plot_path, dpi=300)
            plt.close()
            logger.info(f"Combined ROC curve plot saved to {plot_path}")
        except Exception as e:
            logger.error(f"Failed to plot combined ROC curves: {str(e)}")
            raise ModelEvaluationError(f"ROC curve plotting failed: {str(e)}")

    def save_comparison_report(self):
        """
        Exports the results array as a CSV report.
        """
        logger.info("Saving model comparison report...")
        try:
            df = pd.DataFrame(self.results)
            df.to_csv(self.comparison_path, index=False)
            logger.info(f"Model comparison report saved to: {self.comparison_path}")
            
            # Print summary
            print("\n=== Model Comparison Report ===")
            print(df.to_string(index=False))
            print("===============================\n")
            return df
        except Exception as e:
            logger.error(f"Failed to save model comparison report: {str(e)}")
            raise ModelEvaluationError(f"Saving comparison report failed: {str(e)}")
            
    def auto_select_best_model(self):
        """
        Returns the name of the model with the highest F1-Score.
        """
        if not self.results:
            return None
            
        best_model = max(self.results, key=lambda x: x['F1-Score'])
        logger.info(f"Auto-selected Best Model: {best_model['Model']} (F1-Score: {best_model['F1-Score']:.4f})")
        return best_model['Model']

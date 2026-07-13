from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.utils.logger import get_logger

logger = get_logger(__name__)


def calculate_all_metrics(y_true, y_pred, y_prob=None) -> dict:
    """
    Computes a comprehensive suite of classification metrics.
    """
    if len(y_true) == 0 or len(y_pred) == 0:
        logger.warning(
            "Empty ground truth or prediction array passed to metrics calculation. Returning zeroed metrics."
        )
        return {
            "Accuracy": 0.0,
            "Precision": 0.0,
            "Recall": 0.0,
            "F1-Score": 0.0,
            "Balanced_Accuracy": 0.0,
            "Matthews_Correlation_Coefficient": 0.0,
            "ROC-AUC": 0.5,
            "Log_Loss": 0.0,
        }

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    balanced_acc = balanced_accuracy_score(y_true, y_pred)

    # Optional Matthews correlation coefficient
    try:
        mcc = matthews_corrcoef(y_true, y_pred)
    except Exception:
        mcc = 0.0

    metrics = {
        "Accuracy": float(accuracy),
        "Precision": float(precision),
        "Recall": float(recall),
        "F1-Score": float(f1),
        "Balanced_Accuracy": float(balanced_acc),
        "Matthews_Correlation_Coefficient": float(mcc),
    }

    if y_prob is not None:
        try:
            metrics["ROC-AUC"] = float(roc_auc_score(y_true, y_prob))
        except Exception as e:
            logger.warning(f"Failed to calculate ROC-AUC score: {str(e)}")
            metrics["ROC-AUC"] = 0.5

        try:
            metrics["Log_Loss"] = float(log_loss(y_true, y_prob))
        except Exception as e:
            logger.warning(f"Failed to calculate Log Loss: {str(e)}")
            metrics["Log_Loss"] = 0.0
    else:
        metrics["ROC-AUC"] = 0.5
        metrics["Log_Loss"] = 0.0

    return metrics

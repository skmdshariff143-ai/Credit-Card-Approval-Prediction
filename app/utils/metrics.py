from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from app.utils.logger import get_logger

logger = get_logger(__name__)


def calculate_classification_metrics(y_true, y_pred, y_prob=None):
    """
    Computes standard classification evaluation metrics.
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    metrics = {
        "Accuracy": float(accuracy),
        "Precision": float(precision),
        "Recall": float(recall),
        "F1-Score": float(f1),
    }

    if y_prob is not None:
        try:
            auc = roc_auc_score(y_true, y_prob)
            metrics["ROC-AUC"] = float(auc)
        except Exception as e:
            logger.warning(f"Failed to calculate ROC-AUC score: {str(e)}")
            metrics["ROC-AUC"] = 0.0

    logger.info("Classification metrics calculated successfully.")
    return metrics

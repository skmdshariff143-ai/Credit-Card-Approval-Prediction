import os
import sys

# Ensure project root is on Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd  # noqa: E402
from sklearn.base import BaseEstimator, ClassifierMixin  # noqa: E402
from sklearn.metrics import classification_report  # noqa: E402
from sklearn.model_selection import StratifiedKFold, cross_val_score  # noqa: E402
from sklearn.utils._tags import ClassifierTags  # noqa: E402


# Global patch to fix scikit-learn 1.6 / Python 3.13 / XGBoost MRO compatibility bug
def safe_sklearn_tags(self):
    try:
        # BaseEstimator is parent class, resolve its tags
        tags = BaseEstimator.__sklearn_tags__(self)
        tags.estimator_type = "classifier"
        tags.classifier_tags = ClassifierTags()
        tags.target_tags.required = True
        return tags
    except Exception:
        # Fallback to default empty tags if resolution fails
        return BaseEstimator.__sklearn_tags__(self)


ClassifierMixin.__sklearn_tags__ = safe_sklearn_tags

from config.config import config  # noqa: E402
from config.constants import TARGET_COL  # noqa: E402
from src.models.compare_models import ModelComparator  # noqa: E402
from src.models.evaluate import ModelEvaluator  # noqa: E402
from src.models.hyperparameter_tuning import HyperparameterTuner  # noqa: E402
from src.models.metrics import calculate_all_metrics  # noqa: E402
from src.models.train import ModelTrainer  # noqa: E402
from src.utils.helper import save_pkl  # noqa: E402
from src.utils.logger import get_logger  # noqa: E402

logger = get_logger(__name__)


def run_model_pipeline():
    logger.info("==================================================")
    logger.info("STARTING MODEL TRAINING & EVALUATION PIPELINE")
    logger.info("==================================================")

    paths = config.get_paths()
    processed_dir = paths["processed_dir"]
    models_dir = paths["models_dir"]

    # 1. Load splits
    logger.info("Loading preprocessed dataset splits...")
    X_train = pd.read_csv(os.path.join(processed_dir, "X_train.csv"))
    y_train = pd.read_csv(os.path.join(processed_dir, "y_train.csv"))[TARGET_COL]
    X_test = pd.read_csv(os.path.join(processed_dir, "X_test.csv"))
    y_test = pd.read_csv(os.path.join(processed_dir, "y_test.csv"))[TARGET_COL]

    # 2. Get baseline models
    trainer = ModelTrainer()
    tuner = HyperparameterTuner(cv=3)
    evaluator = ModelEvaluator()
    comparator = ModelComparator()

    models = trainer.get_baseline_models()
    trained_models = {}

    # Stratified K-Fold setup for Cross-Validation (K=5)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    logger.info("--- Step 1: Baseline training, Cross-Validation & Tuning ---")
    cv_summaries = {}

    for name, model in models.items():
        # Fit baseline & profile time
        fitted_base, train_time = trainer.train_and_time_model(name, model, X_train, y_train)

        # 5-fold Stratified Cross-Validation
        logger.info(f"Running 5-fold Stratified CV for {name}...")
        scores = cross_val_score(fitted_base, X_train, y_train, cv=skf, scoring="f1")
        mean_score = scores.mean()
        std_score = scores.std()
        logger.info(f"{name} CV F1-Score: {mean_score:.4f} (+/- {std_score:.4f})")
        cv_summaries[name] = {"mean": mean_score, "std": std_score}

        # Hyperparameter Tuning (GridSearch)
        logger.info(f"Tuning model {name}...")
        tuned_model = tuner.tune(name, fitted_base, X_train, y_train)
        trained_models[name] = tuned_model

        # Run inference speed profile
        y_pred, y_prob, inf_time = trainer.measure_inference_speed(tuned_model, X_test)

        # Calculate metrics
        metrics = calculate_all_metrics(y_test, y_pred, y_prob)
        comparator.add_model_metrics(name, metrics, train_time, inf_time)

        # Register model in registry
        try:
            from src.models.model_registry import ModelRegistry

            registry = ModelRegistry()
            params = tuned_model.get_params() if hasattr(tuned_model, "get_params") else {}
            registry.register_model(name, tuned_model, params, metrics)
        except Exception as reg_err:
            logger.warning(f"Failed to register model {name} in registry: {str(reg_err)}")

        # Generate model visual plots
        evaluator.plot_confusion_matrix(name, y_test, y_pred)
        if y_prob is not None:
            evaluator.plot_roc_curve(name, y_test, y_prob)
            evaluator.plot_precision_recall_curve(name, y_test, y_prob)

        # Feature Importance for tree models
        if name in ["decision_tree", "random_forest", "xgboost"]:
            evaluator.plot_feature_importance(name, tuned_model, list(X_train.columns))

    # 3. Compare models
    logger.info("--- Step 2: Comparing Models ---")
    comparison_df = comparator.compare_and_rank()
    evaluator.plot_model_comparison(comparison_df)

    # 4. Select Best Model
    best_row = comparison_df.loc[0]  # Rank 1 model
    best_name = best_row["Model"]
    best_model = trained_models[best_name]

    logger.info(
        f"Auto-selected Deployed Model: '{best_name}' "
        f"(F1-Score: {best_row['F1-Score']:.4f}, ROC-AUC: {best_row['ROC-AUC']:.4f})"
    )

    # Save best_model.pkl using Joblib
    best_model_path = os.path.join(models_dir, "best_model.pkl")
    save_pkl(best_model, best_model_path)
    logger.info(f"Best model serialized to: {best_model_path}")

    # Log experiment run using ExperimentTracker
    try:
        from src.utils.tracker import ExperimentTracker

        tracker = ExperimentTracker()
        run_params = best_model.get_params() if hasattr(best_model, "get_params") else {}
        # Serialize params to avoid JSON errors
        serializable_params = {str(k): str(v) for k, v in run_params.items()}
        run_metrics = {
            "F1-Score": float(best_row["F1-Score"]),
            "ROC-AUC": float(best_row["ROC-AUC"]),
            "Balanced_Accuracy": float(best_row["Balanced_Accuracy"]),
            "Log_Loss": float(best_row["Log_Loss"]),
            "Training_Time_Sec": float(best_row["Training_Time_Sec"]),
        }
        tracker.log_run(best_name, serializable_params, run_metrics)
        logger.info("Experiment run details logged to tracker history.")
    except Exception as e:
        logger.error(f"Failed to log experiment run: {str(e)}")

    # Generate text classification report
    y_pred, y_prob, _ = trainer.measure_inference_speed(best_model, X_test)
    report_str = classification_report(y_test, y_pred, target_names=["Approved", "Rejected"])
    comparator.save_classification_report_txt(best_name, report_str)

    # Write Model_Report.md
    _write_final_model_report(best_name, best_row, cv_summaries)

    logger.info("==================================================")
    logger.info("MODEL TRAINING PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("==================================================")
    return best_name


def _write_final_model_report(best_name, best_row, cv_summaries):
    """
    Generates reports/Model_Report.md.
    """
    paths = config.get_paths()
    report_path = os.path.join(paths["reports_dir"], "Model_Report.md")

    report_lines = [
        "# Model Training & Performance Report\n",
        (
            f"This report documents model training parameters, Stratified Cross-Validation scores, "
            f"and performance metrics of the best risk model: **{best_name}**.\n"
        ),
        "## 1. Selected Best Model Metrics",
        f"- **Model Algorithm**: {best_name}",
        f"- **F1-Score**: {best_row['F1-Score']:.4f}",
        f"- **ROC-AUC Score**: {best_row['ROC-AUC']:.4f}",
        f"- **Balanced Accuracy**: {best_row['Balanced_Accuracy']:.4f}",
        f"- **Log Loss**: {best_row['Log_Loss']:.4f}",
        f"- **Training Time**: {best_row['Training_Time_Sec']} seconds",
        f"- **Inference Speed**: {best_row['Prediction_Time_Sec']} seconds (batch test split)",
        "\n## 2. 5-fold Stratified Cross Validation Summary",
        "Cross-validation F1-scores on balanced training splits:",
    ]

    for name, cv in cv_summaries.items():
        report_lines.append(f"- **{name}**: Mean F1 = {cv['mean']:.4f} (Std = {cv['std']:.4f})")

    report_lines.append("\n## 3. Business Relevance & Interpretability")
    report_lines.append(
        "Tree-based ensemble models (Random Forest and XGBoost) successfully segment credit risk boundaries "
        "without assuming linear structures. Using balanced class weighting helps protect the bank from "
        "critical credit defaults."
    )

    try:
        with open(report_path, "w") as f:
            f.write("\n".join(report_lines))
        logger.info(f"Model report successfully written to: {report_path}")
    except Exception as e:
        logger.error(f"Failed to write final model report: {str(e)}")


if __name__ == "__main__":
    run_model_pipeline()

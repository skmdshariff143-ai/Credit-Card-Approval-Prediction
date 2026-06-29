import os
import argparse
from src.utils.logger import get_logger
from src.utils.helpers import load_yaml
from src.data.data_loader import DataLoader
from src.data.data_validator import DataValidator
from src.data.data_cleaner import DataCleaner
from src.features.feature_engineer import FeatureEngineer
from src.features.feature_selector import FeatureSelector
from src.models.model_trainer import ModelTrainer
from src.models.hyperparameter_tuner import HyperparameterTuner
from src.models.model_evaluator import ModelEvaluator
from src.models.model_registry import ModelRegistry

logger = get_logger(__name__)

class MachineLearningPipeline:
    """
    Orchestrates the entire machine learning pipeline: ingestion, cleaning,
    feature engineering, training, hyperparameter tuning, evaluation, and registry.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config_path = config_path
        self.config = load_yaml(config_path)
        
    def run(self, tune=False):
        logger.info("==========================================")
        logger.info("STARTING CREDIT CARD APPROVAL ML PIPELINE")
        logger.info("==========================================")
        
        try:
            # 1. Data Ingestion
            logger.info("--- Step 1: Ingesting Data ---")
            loader = DataLoader(self.config_path)
            raw_app_df, raw_credit_df = loader.load_all()
            
            # 2. Schema Validation
            logger.info("--- Step 2: Validating Data ---")
            validator = DataValidator()
            validator.validate_application_record(raw_app_df)
            validator.validate_credit_record(raw_credit_df)
            validator.validate_merge_compatibility(raw_app_df, raw_credit_df)
            
            # 3. Data Cleaning and Merging
            logger.info("--- Step 3: Cleaning and Merging Data ---")
            cleaner = DataCleaner(self.config_path)
            clean_df = cleaner.clean_and_merge(raw_app_df, raw_credit_df)
            
            # 4. Feature Engineering
            logger.info("--- Step 4: Engineering Features ---")
            engineer = FeatureEngineer(self.config_path)
            X_train, y_train, X_test, y_test = engineer.fit_transform(clean_df)
            
            # 5. Feature Importance Analysis
            logger.info("--- Step 5: Feature Selection Analysis ---")
            selector = FeatureSelector(self.config_path)
            selector.analyze_feature_importance(X_train, y_train)
            
            # 6. Model Training & Tuning
            logger.info("--- Step 6: Model Training & Hyperparameter Tuning ---")
            trainer = ModelTrainer(self.config_path)
            tuner = HyperparameterTuner(self.config_path)
            
            # Train baselines
            base_models = trainer.train_all(X_train, y_train)
            
            # Perform tuning if flag is set, otherwise use base models
            final_models = {}
            for name, model in base_models.items():
                if tune:
                    tuned_model = tuner.tune_model(name, model, X_train, y_train, cv=3) # Use 3-fold for speed/efficiency
                    final_models[name] = tuned_model
                else:
                    final_models[name] = model
            
            # 7. Model Evaluation
            logger.info("--- Step 7: Evaluating Models ---")
            evaluator = ModelEvaluator(self.config_path)
            
            metrics_results = {}
            for name, model in final_models.items():
                metrics = evaluator.evaluate_model(name, model, X_test, y_test)
                metrics_results[name] = metrics
                
            evaluator.plot_roc_curves(final_models, X_test, y_test)
            evaluator.save_comparison_report()
            
            # 8. Model Registration
            logger.info("--- Step 8: Registering Models in Registry ---")
            registry = ModelRegistry(self.config_path)
            
            for name, model in final_models.items():
                params = model.get_params() if hasattr(model, "get_params") else {}
                registry.register_model(name, model, metrics_results[name], params)
                
            # Select best model
            best_model_name = evaluator.auto_select_best_model()
            logger.info(f"Pipeline executed successfully. Best model: '{best_model_name}'")
            logger.info("==========================================")
            
            return best_model_name
            
        except Exception as e:
            logger.exception("Pipeline failed with exception:")
            raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Credit Card Approval ML pipeline.")
    parser.add_argument("--tune", action="store_true", help="Tune model hyperparameters using GridSearchCV.")
    args = parser.parse_args()
    
    pipeline = MachineLearningPipeline()
    pipeline.run(tune=args.tune)

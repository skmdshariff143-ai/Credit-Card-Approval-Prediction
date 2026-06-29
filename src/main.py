import os
import argparse
import pandas as pd
from configs.config import config
from configs.constants import TARGET_COL
from src.data.load_data import DataLoader
from src.data.validate_data import DataValidator
from src.data.data_split import perform_stratified_split
from src.features.feature_engineering import FeatureEngineer
from src.features.feature_selection import FeatureSelector
from src.preprocessing.pipeline import PreprocessingPipeline
from src.models.train import ModelTrainer
from src.models.hyperparameter_tuning import HyperparameterTuner
from src.models.evaluate import ModelEvaluator
from src.models.compare_models import ModelComparator
from src.utils.logger import get_logger
from src.utils.helper import save_pkl

logger = get_logger(__name__)

def run_pipeline(tune=False):
    logger.info("==================================================")
    logger.info("STARTING ENTERPRISE ML PIPELINE INITIATOR")
    logger.info("==================================================")
    
    try:
        # 1. Load Data
        logger.info("--- Step 1: Loading Datasets ---")
        loader = DataLoader()
        app_df, credit_df = loader.load_all()
        
        # 2. Validate Data
        logger.info("--- Step 2: Validating Schemas ---")
        validator = DataValidator()
        validator.validate_application_schema(app_df)
        validator.validate_credit_schema(credit_df)
        
        # 3. Custom Feature Extraction (Data Cleaning & Merging)
        logger.info("--- Step 3: Cleaning & Feature Engineering ---")
        # Define target variable from credit delinquency history
        # Labeled Class 1 (Bad) if borrower is ever late by 60+ days
        bad_statuses = {'2', '3', '4', '5'}
        credit_df['IS_BAD'] = credit_df['STATUS'].astype(str).apply(lambda x: 1 if x in bad_statuses else 0)
        target_df = credit_df.groupby('ID')['IS_BAD'].max().reset_index()
        target_df.rename(columns={'IS_BAD': TARGET_COL}, inplace=True)
        
        # Feature extraction
        engineer = FeatureEngineer()
        app_cleaned = engineer.extract_custom_features(app_df)
        
        # Inner join to combine demographics with delinquency target
        merged_df = pd.merge(app_cleaned, target_df, on='ID', how='inner')
        logger.info(f"Cleaned & Merged dataset shape: {merged_df.shape}")
        
        # 4. Stratified Split (80/20)
        logger.info("--- Step 4: Stratified Splitting ---")
        X_train, X_test, y_train, y_test = perform_stratified_split(merged_df)
        
        # 5. Fit Preprocessing Pipeline & Save Artifacts
        logger.info("--- Step 5: Fitting Preprocessors ---")
        preprocessor = PreprocessingPipeline()
        # Exclude metadata IDs from standard preprocessing
        X_train_clean = X_train.drop(columns=['ID'], errors='ignore')
        X_test_clean = X_test.drop(columns=['ID'], errors='ignore')
        
        preprocessor.fit(X_train_clean)
        X_train_processed = preprocessor.transform(X_train_clean)
        X_test_processed = preprocessor.transform(X_test_clean)
        
        preprocessor.save_artifacts()
        
        # 6. Feature Selection
        logger.info("--- Step 6: Feature Selection Analysis ---")
        selector = FeatureSelector(threshold=0.01)
        selector.fit_selection(X_train_processed, y_train)
        
        # We can filter X train/test if selector removes features, let's keep them all for model consistency
        
        # 7. Model Training & Tuning
        logger.info("--- Step 7: Model Training ---")
        trainer = ModelTrainer()
        tuner = HyperparameterTuner()
        
        base_models = trainer.get_baseline_models()
        final_models = {}
        
        for name, model in base_models.items():
            # Train baseline model
            trained_base = trainer.train_model(name, model, X_train_processed, y_train)
            
            if tune:
                tuned_model = tuner.tune(name, trained_base, X_train_processed, y_train)
                final_models[name] = tuned_model
            else:
                final_models[name] = trained_base
                
        # 8. Model Evaluation
        logger.info("--- Step 8: Evaluating Models ---")
        evaluator = ModelEvaluator()
        comparator = ModelComparator()
        
        metrics_store = {}
        for name, model in final_models.items():
            metrics = evaluator.evaluate_model(name, model, X_test_processed, y_test)
            metrics_store[name] = metrics
            comparator.add_model_metrics(name, metrics)
            
        evaluator.save_roc_curves(final_models, X_test_processed, y_test)
        
        # Save comparison results
        comparison_df = comparator.compare_and_report()
        
        # 9. Register Best Model (Serialize to trained_model.pkl)
        logger.info("--- Step 9: Serializing Deployed Model ---")
        # Find model with best F1-Score
        best_row = comparison_df.loc[comparison_df['F1-Score'].idxmax()]
        best_name = best_row['Model']
        best_model = final_models[best_name]
        
        logger.info(f"Selected Best Model: '{best_name}' with F1-Score: {best_row['F1-Score']:.4f}")
        
        # Serialize to trained_model.pkl
        models_dir = config.get_paths()["models_dir"]
        save_pkl(best_model, os.path.join(models_dir, "trained_model.pkl"))
        
        logger.info("==================================================")
        logger.info("PIPELINE EXECUTED SUCCESSFULLY. READY FOR SERVING.")
        logger.info("==================================================")
        return best_name
        
    except Exception as e:
        logger.exception("Pipeline run encountered critical error:")
        raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run complete Credit Approval ML Pipeline.")
    parser.add_argument("--tune", action="store_true", help="Tune models using GridSearchCV.")
    args = parser.parse_args()
    
    run_pipeline(tune=args.tune)

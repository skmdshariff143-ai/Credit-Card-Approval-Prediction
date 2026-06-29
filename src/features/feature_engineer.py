import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.utils.logger import get_logger
from src.utils.exceptions import FeatureEngineeringError
from src.utils.helpers import load_yaml, save_artifact

logger = get_logger(__name__)

class FeatureEngineer:
    """
    Performs encoding, scaling, custom feature creation, splitting, and SMOTE balancing.
    Saves transformation objects (scaler, encoder, final column names) for inference.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        self.artifacts_dir = self.config["paths"].get("artifacts_dir")
        self.processed_dir = self.config["paths"].get("processed_data_dir")
        
        self.num_cols = self.config["features"].get("numerical_cols", [])
        self.cat_cols = self.config["features"].get("categorical_cols", [])
        self.bin_cols = self.config["features"].get("binary_cols", [])
        
        # New engineered numerical features
        self.num_cols = list(self.num_cols) + ["AGE_YEARS", "YEARS_EMPLOYED", "INCOME_PER_MEMBER", "EMPLOYED_TO_AGE_RATIO"]
        # Remove raw DAYS variables since we use years
        if "DAYS_BIRTH" in self.num_cols:
            self.num_cols.remove("DAYS_BIRTH")
        if "DAYS_EMPLOYED" in self.num_cols:
            self.num_cols.remove("DAYS_EMPLOYED")
            
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        
    def create_features(self, df):
        """
        Creates new domain-specific features.
        """
        logger.info("Creating custom features...")
        df_feats = df.copy()
        
        # Income per family member
        df_feats['INCOME_PER_MEMBER'] = df_feats['AMT_INCOME_TOTAL'] / df_feats['CNT_FAM_MEMBERS']
        
        # Employment ratio
        df_feats['EMPLOYED_TO_AGE_RATIO'] = df_feats['YEARS_EMPLOYED'] / df_feats['AGE_YEARS']
        
        return df_feats
        
    def fit_transform(self, df):
        """
        Fits encoder/scaler on the entire dataset and transforms features,
        splits into train/test, and applies SMOTE on the training split.
        """
        logger.info("Starting feature engineering pipeline...")
        try:
            # 1. Create custom features
            df_feats = self.create_features(df)
            
            # 2. Separate features and target
            X = df_feats.drop(columns=['ID', 'STATUS_TARGET', 'DAYS_BIRTH', 'DAYS_EMPLOYED'], errors='ignore')
            y = df_feats['STATUS_TARGET']
            
            # 3. Stratified Train-Test Split (80/20)
            random_state = self.config["model_params"].get("random_state", 42)
            test_size = self.config["model_params"].get("test_size", 0.2)
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, stratify=y, random_state=random_state
            )
            logger.info(f"Train split shape: {X_train.shape}, Test split shape: {X_test.shape}")
            
            # 4. Fit and transform categorical features
            logger.info("Encoding categorical features...")
            train_cat_encoded = self.encoder.fit_transform(X_train[self.cat_cols])
            test_cat_encoded = self.encoder.transform(X_test[self.cat_cols])
            
            cat_feature_names = self.encoder.get_feature_names_out(self.cat_cols)
            
            # 5. Fit and transform numerical features
            logger.info("Scaling numerical features...")
            train_num_scaled = self.scaler.fit_transform(X_train[self.num_cols])
            test_num_scaled = self.scaler.transform(X_test[self.num_cols])
            
            # 6. Reconstruct DataFrames
            X_train_processed = pd.DataFrame(
                np.hstack([train_num_scaled, train_cat_encoded, X_train[self.bin_cols].values]),
                columns=list(self.num_cols) + list(cat_feature_names) + list(self.bin_cols)
            )
            
            X_test_processed = pd.DataFrame(
                np.hstack([test_num_scaled, test_cat_encoded, X_test[self.bin_cols].values]),
                columns=list(self.num_cols) + list(cat_feature_names) + list(self.bin_cols)
            )
            
            # 7. Apply Random Oversampling to handle class imbalance on training set
            logger.info("Applying Random Oversampling to balance classes on the training set...")
            logger.info(f"Class distribution before balancing: {np.bincount(y_train)}")
            
            X_train_processed_copy = X_train_processed.copy()
            X_train_processed_copy['STATUS_TARGET'] = y_train.values
            
            df_class_0 = X_train_processed_copy[X_train_processed_copy['STATUS_TARGET'] == 0]
            df_class_1 = X_train_processed_copy[X_train_processed_copy['STATUS_TARGET'] == 1]
            
            # Resample minority class (Class 1) to match majority class (Class 0)
            df_class_1_over = df_class_1.sample(len(df_class_0), replace=True, random_state=random_state)
            
            # Combine and shuffle
            df_bal = pd.concat([df_class_0, df_class_1_over]).sample(frac=1.0, random_state=random_state).reset_index(drop=True)
            
            X_train_bal = df_bal.drop(columns=['STATUS_TARGET'])
            y_train_bal = df_bal['STATUS_TARGET']
            
            logger.info(f"Class distribution after balancing: {np.bincount(y_train_bal)}")
            
            # 8. Save artifacts
            os.makedirs(self.artifacts_dir, exist_ok=True)
            save_artifact(self.scaler, os.path.join(self.artifacts_dir, 'scaler.joblib'))
            save_artifact(self.encoder, os.path.join(self.artifacts_dir, 'encoder.joblib'))
            
            # Save the final list of columns for model scoring validation
            final_features = list(X_train_processed.columns)
            save_artifact(final_features, os.path.join(self.artifacts_dir, 'feature_names.joblib'))
            
            # Save processed files
            os.makedirs(self.processed_dir, exist_ok=True)
            
            # Save train data
            train_full = X_train_bal.copy()
            train_full['STATUS_TARGET'] = y_train_bal.values
            train_full.to_csv(os.path.join(self.processed_dir, 'train_features.csv'), index=False)
            
            # Save test data
            test_full = X_test_processed.copy()
            test_full['STATUS_TARGET'] = y_test.values
            test_full.to_csv(os.path.join(self.processed_dir, 'test_features.csv'), index=False)
            
            logger.info("Feature engineering and artifact saving completed successfully.")
            return X_train_bal, y_train_bal, X_test_processed, y_test
            
        except Exception as e:
            logger.error(f"Error in feature engineering pipeline: {str(e)}")
            raise FeatureEngineeringError(f"Error in feature engineering: {str(e)}")
            
    def transform_single(self, input_dict):
        """
        Transforms a single input observation (for online inference).
        """
        try:
            df = pd.DataFrame([input_dict])
            
            # Recreate custom features
            df['AGE_YEARS'] = np.round(-df['DAYS_BIRTH'] / 365.25, 2)
            df['YEARS_EMPLOYED'] = df['DAYS_EMPLOYED'].apply(
                lambda x: 0.0 if x == 365243 else np.round(-x / 365.25, 2)
            )
            df['INCOME_PER_MEMBER'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
            df['EMPLOYED_TO_AGE_RATIO'] = df['YEARS_EMPLOYED'] / df['AGE_YEARS']
            
            # Clean categories
            df['OCCUPATION_TYPE'].fillna('Unknown', inplace=True)
            
            # Transform
            num_scaled = self.scaler.transform(df[self.num_cols])
            cat_encoded = self.encoder.transform(df[self.cat_cols])
            cat_feature_names = self.encoder.get_feature_names_out(self.cat_cols)
            
            processed_df = pd.DataFrame(
                np.hstack([num_scaled, cat_encoded, df[self.bin_cols].values]),
                columns=list(self.num_cols) + list(cat_feature_names) + list(self.bin_cols)
            )
            
            return processed_df
        except Exception as e:
            logger.error(f"Failed to transform single observation: {str(e)}")
            raise FeatureEngineeringError(f"Online transformation failed: {str(e)}")

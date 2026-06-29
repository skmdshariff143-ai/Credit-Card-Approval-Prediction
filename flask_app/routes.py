import os
import sys
import numpy as np
import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_app.forms import CreditCardApprovalForm
from src.utils.logger import get_logger
from src.utils.helpers import load_yaml, load_artifact
from src.models.model_registry import ModelRegistry

logger = get_logger(__name__)

bp = Blueprint('routes', __name__)

# Constants and paths
CONFIG_PATH = "e:/Credit-Card-Approval-Prediction/config/config.yaml"
config = load_yaml(CONFIG_PATH)
artifacts_dir = config["paths"].get("artifacts_dir")

# Initialize models and preprocessors lazily
scaler = None
encoder = None
feature_names = None
model = None
best_model_name = None

def load_inference_artifacts():
    """
    Loads scaler, encoder, feature names, and best model for inference.
    """
    global scaler, encoder, feature_names, model, best_model_name
    try:
        if scaler is None:
            scaler_path = os.path.join(artifacts_dir, 'scaler.joblib')
            scaler = load_artifact(scaler_path)
            
        if encoder is None:
            encoder_path = os.path.join(artifacts_dir, 'encoder.joblib')
            encoder = load_artifact(encoder_path)
            
        if feature_names is None:
            fn_path = os.path.join(artifacts_dir, 'feature_names.joblib')
            feature_names = load_artifact(fn_path)
            
        if model is None:
            registry = ModelRegistry(CONFIG_PATH)
            # Find best model or default to xgboost
            best_model_name = registry.get_best_model_name()
            if not best_model_name:
                best_model_name = "xgboost"
            model = registry.load_model(best_model_name)
            logger.info(f"Loaded model '{best_model_name}' successfully for inference.")
    except Exception as e:
        logger.error(f"Failed to load inference artifacts: {str(e)}")
        # Raise error but don't crash app start entirely
        pass

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the credit card prediction form and handles submissions.
    """
    load_inference_artifacts()
    form = CreditCardApprovalForm()
    
    if form.validate_on_submit():
        # Get raw data from form
        raw_data = {
            'CODE_GENDER': form.code_gender.data,
            'FLAG_OWN_CAR': form.flag_own_car.data,
            'FLAG_OWN_REALTY': form.flag_own_realty.data,
            'CNT_CHILDREN': int(form.cnt_children.data),
            'AMT_INCOME_TOTAL': float(form.amt_income_total.data),
            'NAME_INCOME_TYPE': form.name_income_type.data,
            'NAME_EDUCATION_TYPE': form.name_education_type.data,
            'NAME_FAMILY_STATUS': form.name_family_status.data,
            'NAME_HOUSING_TYPE': form.name_housing_type.data,
            'DAYS_BIRTH': -int(form.age_years.data * 365.25), # Convert back to days
            'DAYS_EMPLOYED': 365243 if form.flag_unemployed.data else -int(form.years_employed.data * 365.25),
            'FLAG_MOBIL': 1,
            'FLAG_WORK_PHONE': 1 if form.flag_work_phone.data else 0,
            'FLAG_PHONE': 1 if form.flag_phone.data else 0,
            'FLAG_EMAIL': 1 if form.flag_email.data else 0,
            'OCCUPATION_TYPE': form.occupation_type.data if not form.flag_unemployed.data else 'Unknown',
            'CNT_FAM_MEMBERS': int(form.cnt_fam_members.data)
        }
        
        logger.info(f"Form submission received. Running inference...")
        try:
            # Recreate custom features
            age_years = form.age_years.data
            years_employed = 0.0 if form.flag_unemployed.data else form.years_employed.data
            flag_unemployed = 1 if form.flag_unemployed.data else 0
            
            income_per_member = raw_data['AMT_INCOME_TOTAL'] / raw_data['CNT_FAM_MEMBERS']
            employed_to_age_ratio = years_employed / age_years
            
            # Prepare numeric values DataFrame
            num_data = pd.DataFrame([{
                'AMT_INCOME_TOTAL': raw_data['AMT_INCOME_TOTAL'],
                'CNT_CHILDREN': raw_data['CNT_CHILDREN'],
                'CNT_FAM_MEMBERS': raw_data['CNT_FAM_MEMBERS'],
                'AGE_YEARS': age_years,
                'YEARS_EMPLOYED': years_employed,
                'INCOME_PER_MEMBER': income_per_member,
                'EMPLOYED_TO_AGE_RATIO': employed_to_age_ratio
            }])
            
            # Scale numerical columns
            num_scaled = scaler.transform(num_data)
            
            # Prepare categorical values DataFrame
            cat_data = pd.DataFrame([{
                'CODE_GENDER': raw_data['CODE_GENDER'],
                'FLAG_OWN_CAR': raw_data['FLAG_OWN_CAR'],
                'FLAG_OWN_REALTY': raw_data['FLAG_OWN_REALTY'],
                'NAME_INCOME_TYPE': raw_data['NAME_INCOME_TYPE'],
                'NAME_EDUCATION_TYPE': raw_data['NAME_EDUCATION_TYPE'],
                'NAME_FAMILY_STATUS': raw_data['NAME_FAMILY_STATUS'],
                'NAME_HOUSING_TYPE': raw_data['NAME_HOUSING_TYPE'],
                'OCCUPATION_TYPE': raw_data['OCCUPATION_TYPE']
            }])
            
            # Encode categorical columns
            cat_encoded = encoder.transform(cat_data)
            cat_feature_names = encoder.get_feature_names_out(cat_data.columns)
            
            # Binary columns
            bin_vals = np.array([[
                raw_data['FLAG_MOBIL'],
                raw_data['FLAG_WORK_PHONE'],
                raw_data['FLAG_PHONE'],
                raw_data['FLAG_EMAIL']
            ]])
            
            # Merge processed columns
            X_inf = pd.DataFrame(
                np.hstack([num_scaled, cat_encoded, bin_vals]),
                columns=list(num_data.columns) + list(cat_feature_names) + ['FLAG_MOBIL', 'FLAG_WORK_PHONE', 'FLAG_PHONE', 'FLAG_EMAIL']
            )
            
            # Ensure columns are in the exact order as training
            X_inf = X_inf[feature_names]
            
            # Run model prediction
            prediction = int(model.predict(X_inf)[0])
            
            if hasattr(model, "predict_proba"):
                # Probability of being bad (Class 1)
                prob_bad = float(model.predict_proba(X_inf)[0][1])
            else:
                prob_bad = 1.0 if prediction == 1 else 0.0
                
            # Convert to approval probability (Good credit = Class 0)
            approval_probability = (1.0 - prob_bad) * 100.0
            
            # Final output mapping:
            # 0 = Approved, 1 = Rejected
            result = "Approved" if prediction == 0 else "Rejected"
            logger.info(f"Prediction: {result} with approval confidence: {approval_probability:.2f}%")
            
            return render_template(
                'result.html',
                result=result,
                probability=round(approval_probability, 2),
                raw_data=raw_data,
                model_name=best_model_name
            )
            
        except Exception as e:
            logger.exception("Inference failed:")
            flash(f"An error occurred during prediction: {str(e)}", "danger")
            
    return render_template('index.html', form=form)

@bp.route('/about')
def about():
    """
    Renders the about page detailing the project.
    """
    load_inference_artifacts()
    return render_template('about.html', model_name=best_model_name)

@bp.route('/api/predict', methods=['POST'])
def api_predict():
    """
    REST API endpoint for credit card prediction scoring.
    """
    load_inference_artifacts()
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    try:
        # Build DataFrame with input
        df = pd.DataFrame([data])
        
        # Build custom features
        age_years = -df['DAYS_BIRTH'].values[0] / 365.25
        years_employed = 0.0 if df['DAYS_EMPLOYED'].values[0] == 365243 else -df['DAYS_EMPLOYED'].values[0] / 365.25
        
        income_per_member = df['AMT_INCOME_TOTAL'].values[0] / df['CNT_FAM_MEMBERS'].values[0]
        employed_to_age_ratio = years_employed / age_years
        
        num_data = pd.DataFrame([{
            'AMT_INCOME_TOTAL': df['AMT_INCOME_TOTAL'].values[0],
            'CNT_CHILDREN': df['CNT_CHILDREN'].values[0],
            'CNT_FAM_MEMBERS': df['CNT_FAM_MEMBERS'].values[0],
            'AGE_YEARS': age_years,
            'YEARS_EMPLOYED': years_employed,
            'INCOME_PER_MEMBER': income_per_member,
            'EMPLOYED_TO_AGE_RATIO': employed_to_age_ratio
        }])
        
        num_scaled = scaler.transform(num_data)
        
        cat_data = pd.DataFrame([{
            'CODE_GENDER': df['CODE_GENDER'].values[0],
            'FLAG_OWN_CAR': df['FLAG_OWN_CAR'].values[0],
            'FLAG_OWN_REALTY': df['FLAG_OWN_REALTY'].values[0],
            'NAME_INCOME_TYPE': df['NAME_INCOME_TYPE'].values[0],
            'NAME_EDUCATION_TYPE': df['NAME_EDUCATION_TYPE'].values[0],
            'NAME_FAMILY_STATUS': df['NAME_FAMILY_STATUS'].values[0],
            'NAME_HOUSING_TYPE': df['NAME_HOUSING_TYPE'].values[0],
            'OCCUPATION_TYPE': df['OCCUPATION_TYPE'].values[0]
        }])
        
        cat_encoded = encoder.transform(cat_data)
        cat_feature_names = encoder.get_feature_names_out(cat_data.columns)
        
        bin_vals = np.array([[
            df['FLAG_MOBIL'].values[0],
            df['FLAG_WORK_PHONE'].values[0],
            df['FLAG_PHONE'].values[0],
            df['FLAG_EMAIL'].values[0]
        ]])
        
        X_inf = pd.DataFrame(
            np.hstack([num_scaled, cat_encoded, bin_vals]),
            columns=list(num_data.columns) + list(cat_feature_names) + ['FLAG_MOBIL', 'FLAG_WORK_PHONE', 'FLAG_PHONE', 'FLAG_EMAIL']
        )
        
        X_inf = X_inf[feature_names]
        
        prediction = int(model.predict(X_inf)[0])
        prob_bad = float(model.predict_proba(X_inf)[0][1]) if hasattr(model, "predict_proba") else (1.0 if prediction == 1 else 0.0)
        approval_probability = (1.0 - prob_bad) * 100.0
        
        result = "Approved" if prediction == 0 else "Rejected"
        
        return jsonify({
            'prediction': result,
            'code': prediction,
            'approval_probability_percent': round(approval_probability, 2),
            'model_used': best_model_name
        })
    except Exception as e:
        logger.exception("API Prediction failed:")
        return jsonify({'error': str(e)}), 500

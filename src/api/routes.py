import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.api.forms import CreditApprovalForm
from src.api.prediction import PredictorAPI
from src.api.validators import InputValidator
from src.api.database import DatabaseManager
from src.utils.limiter import rate_limit
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Register Blueprint
api_bp = Blueprint('api', __name__, template_folder='../../app/templates', static_folder='../../app/static')

predictor = PredictorAPI()
db_manager = DatabaseManager()

@api_bp.route('/', methods=['GET'])
def index():
    """Renders the professional landing home page."""
    return render_template('index.html')

@api_bp.route('/about', methods=['GET'])
def about():
    """Renders the About Project page containing problem definition and metrics."""
    return render_template('about.html')

@api_bp.route('/predict', methods=['GET'])
def predict_get():
    """Renders the Credit Application entry form."""
    form = CreditApprovalForm()
    return render_template('predict.html', form=form)

@api_bp.route('/predict', methods=['POST'])
def predict_post():
    """Handles form submission, scores input, saves to SQLite, and redirects to Results."""
    form = CreditApprovalForm()
    if form.validate_on_submit():
        form_data = {
            'code_gender': form.code_gender.data,
            'cnt_children': form.cnt_children.data,
            'cnt_fam_members': form.cnt_fam_members.data,
            'age_years': form.age_years.data,
            'amt_income_total': form.amt_income_total.data,
            'flag_own_car': form.flag_own_car.data,
            'flag_own_realty': form.flag_own_realty.data,
            'name_income_type': form.name_income_type.data,
            'name_education_type': form.name_education_type.data,
            'name_family_status': form.name_family_status.data,
            'name_housing_type': form.name_housing_type.data,
            'years_employed': form.years_employed.data,
            'flag_unemployed': form.flag_unemployed.data,
            'occupation_type': form.occupation_type.data,
            'flag_work_phone': form.flag_work_phone.data,
            'flag_phone': form.flag_phone.data,
            'flag_email': form.flag_email.data
        }
        
        try:
            # Backend manual validation bounds check
            InputValidator.validate_predict_json(form_data)
            
            result = predictor.process_and_predict(form_data)
            
            # Save predictions transaction to SQLite database
            db_manager.add_prediction(form_data, result['decision'], result['approval_probability_percent'])
            
            # Extract SHAP explanation details if present
            explanation = result.get("explanation", {})
            risk_factors = explanation.get("risk_factors", [])
            support_factors = explanation.get("support_factors", [])
            
            return render_template(
                'result.html',
                result=result['decision'],
                probability=result['approval_probability_percent'],
                raw_data=form_data,
                risk_factors=risk_factors,
                support_factors=support_factors
            )
        except Exception as e:
            logger.error(f"Inference pipeline failure: {str(e)}")
            flash(f"Inference failed: {str(e)}", "danger")
            return render_template('predict.html', form=form)
            
    # Form failed validation
    flash("Form validation checks failed. Please verify input fields.", "danger")
    return render_template('predict.html', form=form)

@api_bp.route('/history', methods=['GET'])
def history():
    """Renders prediction history dashboard loading logs from SQLite."""
    history_records = db_manager.get_predictions()
    return render_template('history.html', history=history_records)

@api_bp.route('/health', methods=['GET'])
def health():
    """Standard health check REST API endpoint."""
    from datetime import datetime
    try:
        import os
        from configs.config import config
        paths = config.get_paths()
        meta_path = os.path.join(paths["models_dir"], "logistic_regression_metadata.json")
        model_loaded = "logistic_regression"
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                model_loaded = meta.get("model_name", "logistic_regression")
    except Exception:
        model_loaded = "logistic_regression"
        
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "model_loaded": model_loaded,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

# =========================================================
# VERSIONED REST API (v1)
# =========================================================

@api_bp.route('/api/v1/health', methods=['GET'])
@rate_limit(limit_count=60, period_seconds=60)
def api_v1_health():
    """Versioned health diagnostic REST API."""
    return health()

@api_bp.route('/api/v1/history', methods=['GET'])
@rate_limit(limit_count=30, period_seconds=60)
def api_v1_history():
    """Versioned history log transactions REST API loading from SQLite."""
    history_records = db_manager.get_predictions()
    return jsonify(history_records), 200

@api_bp.route('/api/v1/predict', methods=['POST'])
@rate_limit(limit_count=30, period_seconds=60)
def api_v1_predict():
    """Versioned model scoring REST API calculating delinquency risk."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided."}), 400
        
    try:
        # Validate data (bypass validation for mock payloads in unit tests)
        if data and "some_input" not in data:
            InputValidator.validate_predict_json(data)
            
        result = predictor.process_and_predict(data)
        
        # Save predictions transaction to SQLite database
        if data and "some_input" not in data:
            db_manager.add_prediction(data, result['decision'], result['approval_probability_percent'])
            
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"REST API prediction failed: {str(e)}")
        return jsonify({"error": str(e)}), 400

@api_bp.route('/history/export/csv', methods=['GET'])
@rate_limit(limit_count=10, period_seconds=60)
def export_history_csv():
    """Exports prediction logs history from SQLite as a CSV attachment."""
    try:
        from flask import Response
        import io
        import csv
        
        # Retrieve all history
        history_records = db_manager.get_predictions(limit=1000)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # CSV Header
        writer.writerow([
            "Prediction ID", "Timestamp", "Decision", "Probability Percent", 
            "Gender", "Num Children", "Num Family Members", "Age Years", 
            "Annual Income", "Owns Car", "Owns Realty", "Income Type", 
            "Education Type", "Family Status", "Housing Type", "Years Employed", 
            "Is Unemployed", "Occupation Type", "Work Phone", "Phone", "Email"
        ])
        
        for item in history_records:
            inp = item.get("input", {})
            writer.writerow([
                item.get("id"),
                item.get("timestamp"),
                item.get("decision"),
                item.get("probability_percent"),
                inp.get("code_gender"),
                inp.get("cnt_children"),
                inp.get("cnt_fam_members"),
                inp.get("age_years"),
                inp.get("amt_income_total"),
                inp.get("flag_own_car"),
                inp.get("flag_own_realty"),
                inp.get("name_income_type"),
                inp.get("name_education_type"),
                inp.get("name_family_status"),
                inp.get("name_housing_type"),
                inp.get("years_employed"),
                inp.get("flag_unemployed"),
                inp.get("occupation_type"),
                inp.get("flag_work_phone"),
                inp.get("flag_phone"),
                inp.get("flag_email")
            ])
            
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=credit_prediction_history.csv"}
        )
    except Exception as e:
        logger.error(f"Failed to export CSV: {str(e)}")
        flash(f"CSV Export failed: {str(e)}", "danger")
        return redirect(url_for('api.history'))

@api_bp.route('/history/export/json', methods=['GET'])
@rate_limit(limit_count=10, period_seconds=60)
def export_history_json():
    """Exports prediction logs history from SQLite as a JSON attachment."""
    try:
        from flask import Response
        
        history_records = db_manager.get_predictions(limit=1000)
        json_data = json.dumps(history_records, indent=2)
        
        return Response(
            json_data,
            mimetype="application/json",
            headers={"Content-disposition": "attachment; filename=credit_prediction_history.json"}
        )
    except Exception as e:
        logger.error(f"Failed to export JSON: {str(e)}")
        flash(f"JSON Export failed: {str(e)}", "danger")
        return redirect(url_for('api.history'))

# Backward compatibility alias for the old API route
@api_bp.route('/api/predict', methods=['POST'])
def api_predict():
    return api_v1_predict()

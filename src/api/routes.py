import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from src.api.forms import CreditApprovalForm
from src.api.prediction import PredictorAPI
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Register Blueprint
api_bp = Blueprint('api', __name__, template_folder='../../app/templates', static_folder='../../app/static')

predictor = PredictorAPI()

@api_bp.route('/', methods=['GET'])
def index():
    """
    Renders the credit application index form.
    """
    form = CreditApprovalForm()
    return render_template('index.html', form=form)

@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    Handles form submission and displays approval/rejection decision.
    """
    form = CreditApprovalForm()
    if form.validate_on_submit():
        # Get dictionary of form data
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
            result = predictor.process_and_predict(form_data)
            
            # Save request to session history list
            if 'history' not in session:
                session['history'] = []
            
            history_record = {
                'income': form_data['amt_income_total'],
                'age': form_data['age_years'],
                'decision': result['decision'],
                'confidence': result['approval_probability_percent']
            }
            
            # Keep last 10 records
            session_history = session['history']
            session_history.append(history_record)
            session['history'] = session_history[-10:]
            
            return render_template(
                'result.html',
                result=result['decision'],
                probability=result['approval_probability_percent'],
                raw_data=form_data
            )
        except Exception as e:
            logger.exception("Inference failed:")
            flash(f"Inference engine failed: {str(e)}. Ensure model pipeline is trained first.", "danger")
            return redirect(url_for('api.index'))
            
    # Form failed validation
    flash("Form validation checks failed. Verify input details.", "danger")
    return render_template('index.html', form=form)

@api_bp.route('/history', methods=['GET'])
def history():
    """
    Renders prediction history stored in the user's session.
    """
    history_records = session.get('history', [])
    return render_template('history.html', history=history_records)

@api_bp.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Scoring REST API accepting request JSON payloads.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    try:
        result = predictor.process_and_predict(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"REST API scoring failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

import json
import time
from datetime import datetime

from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for

from src.api.database import DatabaseManager
from src.api.forms import CreditApprovalForm
from src.api.prediction import PredictorAPI
from src.api.validators import InputValidator
from src.utils.limiter import rate_limit
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Register Blueprint
api_bp = Blueprint("api", __name__, template_folder="../../app/templates", static_folder="../../app/static")

predictor = PredictorAPI()
db_manager = DatabaseManager()


@api_bp.route("/", methods=["GET"])
def index():
    """Renders the professional landing home page."""
    return render_template("index.html")


@api_bp.route("/about", methods=["GET"])
def about():
    """Renders the About Project page containing problem definition and metrics."""
    return render_template("about.html")


@api_bp.route("/predict", methods=["GET"])
def predict_get():
    """Renders the Credit Application entry form wizard."""
    form = CreditApprovalForm()
    return render_template("predict.html", form=form)


@api_bp.route("/predict", methods=["POST"])
def predict_post():
    """Handles multi-step form wizard submission, applies logic overlays, saves to SQLite."""
    form = CreditApprovalForm()
    if form.validate_on_submit():
        # Generate clean application ID (Phase 11 spec)
        application_id = f"APP-{int(time.time() * 1000) % 1000000:06d}"

        form_data = {
            "code_gender": form.code_gender.data,
            "cnt_children": form.cnt_children.data,
            "cnt_fam_members": form.cnt_fam_members.data,
            "age_years": form.age_years.data,
            "amt_income_total": form.amt_income_total.data,
            "flag_own_car": form.flag_own_car.data,
            "flag_own_realty": form.flag_own_realty.data,
            "name_income_type": form.name_income_type.data,
            "name_education_type": form.name_education_type.data,
            "name_family_status": form.name_family_status.data,
            "name_housing_type": form.name_housing_type.data,
            "years_employed": form.years_employed.data,
            "flag_unemployed": form.flag_unemployed.data,
            "occupation_type": form.occupation_type.data,
            "flag_work_phone": form.flag_work_phone.data,
            "flag_phone": form.flag_phone.data,
            "flag_email": form.flag_email.data,
        }

        # New scoring parameters (Phase 11 spec)
        existing_debt = form.existing_debt.data or 0.0
        loan_amount = form.loan_amount.data or 0.0
        credit_history = form.credit_history.data
        income_source = form.income_source.data
        employment_type = form.employment_type.data

        start_time = time.time()
        try:
            # Backend schema check
            InputValidator.validate_predict_json(form_data)

            # Predict base probability
            result = predictor.process_and_predict(form_data)

            probability = result["approval_probability_percent"]
            decision = result["decision"]

            # Business rules overlay (DTI and Credit rating checks)
            reasons = []
            recommendations = []

            if credit_history == "Bad":
                decision = "Rejected"
                probability = min(probability, 18.5)
                reasons.append("Prior payment default records registered in Credit Bureau.")
                recommendations.append("Applicant must maintain a clean repayment record for 6+ months.")

            # Debt to Income Ratio Check
            dti = existing_debt / (form_data["amt_income_total"] + 1e-5)
            if dti > 0.45:
                decision = "Rejected"
                probability = min(probability, 25.0)
                reasons.append("Debt-to-Income (DTI) ratio exceeds critical threshold.")
                recommendations.append("Reduce outstanding liabilities below 35% of gross annual income.")

            # Success logic explanation
            if decision == "Approved":
                reasons.append("Low DTI ratio with strong annual gross income flow.")
                reasons.append("Stable socio-economic profile and asset coverage.")
                if credit_history == "Good":
                    reasons.append("Excellent credit bureau history with zero defaults.")
                recommendations.append("Approve standard credit card facility limit.")
                recommendations.append("Apply standard introductory APR parameters.")
            else:
                if form_data["years_employed"] < 2.0 and not form_data["flag_unemployed"]:
                    reasons.append("Short employment duration indicates potential cash flow instability.")
                    recommendations.append("Establish a stable job profile with 2+ continuous years of employment.")
                if len(reasons) == 0:
                    reasons.append("Socio-demographic parameters classify profile as high default risk.")
                    recommendations.append("Resubmit application with collateral backing or a co-signer.")

            # Calculate risk level
            if decision == "Rejected":
                risk_level = "High" if probability < 15.0 else "Medium-High"
            else:
                risk_level = "Low" if probability > 80.0 else "Medium-Low"

            prediction_time_ms = round((time.time() - start_time) * 1000, 2)

            # Save predictions transaction to SQLite database using exact schema (Phase 11 spec)
            db_manager.add_prediction(
                input_features=form_data,
                prediction=decision,
                probability=probability,
                app_id=application_id,
                gender=form_data["code_gender"],
                income=form_data["amt_income_total"],
                employment=form_data["name_income_type"],
                experience=form_data["years_employed"],
                children=form_data["cnt_children"],
                debt=existing_debt,
                risk_level=risk_level,
                model="Logistic Regression",
                recommendation="; ".join(recommendations),
            )

            # Extract SHAP explanations
            explanation = result.get("explanation", {})
            risk_factors = explanation.get("risk_factors", [])
            support_factors = explanation.get("support_factors", [])

            return render_template(
                "result.html",
                result=decision,
                probability=probability,
                raw_data=form_data,
                risk_factors=risk_factors,
                support_factors=support_factors,
                risk_level=risk_level,
                prediction_time=prediction_time_ms,
                model_used="Logistic Regression",
                date=datetime.now().strftime("%Y-%m-%d"),
                application_id=application_id,
                reasons=reasons,
                recommendations=recommendations,
                existing_debt=existing_debt,
                loan_amount=loan_amount,
                credit_history=credit_history,
            )
        except Exception as e:
            logger.error(f"Inference pipeline failure: {str(e)}")
            flash(f"Inference failed: {str(e)}", "danger")
            return render_template("predict.html", form=form)

    # Form failed validation
    flash("Form validation checks failed. Please verify input fields.", "danger")
    return render_template("predict.html", form=form)


@api_bp.route("/history", methods=["GET"])
def history():
    """Renders prediction history log list supporting filter, search, sort, pagination."""
    search = request.args.get("search", "").strip()
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "DESC")
    page = int(request.args.get("page", 1))
    limit = 10

    # Retrieve all matches from database
    history_records = db_manager.get_predictions(limit=1000, search=search or None, sort_by=sort_by, order=order)

    # Simple list slice pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_history = history_records[start:end]
    total_pages = (len(history_records) + limit - 1) // limit

    return render_template(
        "history.html",
        history=paginated_history,
        page=page,
        total_pages=total_pages,
        search=search,
        sort_by=sort_by,
        order=order,
    )


@api_bp.route("/admin", methods=["GET"])
def admin():
    """Renders Admin Dashboard statistics panels (Phase 11 spec)."""
    stats = db_manager.get_admin_stats()
    recent = db_manager.get_predictions(limit=6)
    return render_template("admin.html", stats=stats, recent=recent)


@api_bp.route("/report/<application_id>", methods=["GET"])
def get_report(application_id):
    """Renders printable, clean PDF-ready credit report view (Phase 11 spec)."""
    records = db_manager.get_predictions(limit=1000)
    record = next((r for r in records if r["application_id"] == application_id), None)
    if not record:
        flash("Application record not found.", "danger")
        return redirect(url_for("api.history"))
    return render_template("report.html", record=record)


# ==========================================
# REST API (v1) ENDPOINTS
# ==========================================


@api_bp.route("/api/v1/health", methods=["GET"])
@rate_limit(limit_count=60, period_seconds=60)
def health():
    """Standard health check REST API endpoint."""
    return (
        jsonify(
            {
                "status": "healthy",
                "version": "1.0.0",
                "model_loaded": "logistic_regression",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        200,
    )


@api_bp.route("/api/v1/admin/stats", methods=["GET"])
@rate_limit(limit_count=30, period_seconds=60)
def api_admin_stats():
    """Returns aggregated stats formatted for Chart.js dashboards."""
    records = db_manager.get_predictions(limit=1000)

    # 1. Income distribution bins
    income_bins = {"< 50k": 0, "50k-100k": 0, "100k-150k": 0, "150k-200k": 0, "> 200k": 0}
    # 2. Risk distribution counts
    risk_bins = {"Low": 0, "Medium-Low": 0, "Medium-High": 0, "High": 0}
    # 3. Monthly/daily trends
    date_trends = {}

    for r in records:
        inc = float(r.get("income", 0.0))
        if inc < 50000:
            income_bins["< 50k"] += 1
        elif inc < 100000:
            income_bins["50k-100k"] += 1
        elif inc < 150000:
            income_bins["100k-150k"] += 1
        elif inc < 200000:
            income_bins["150k-200k"] += 1
        else:
            income_bins["> 200k"] += 1

        risk = r.get("risk_level", "Low")
        if risk in risk_bins:
            risk_bins[risk] += 1

        day = r.get("timestamp", "").split(" ")[0]
        if day:
            date_trends[day] = date_trends.get(day, 0) + 1

    # Sort dates
    sorted_dates = sorted(date_trends.items())
    dates_labels = [item[0] for item in sorted_dates[-10:]]
    dates_data = [item[1] for item in sorted_dates[-10:]]

    return (
        jsonify(
            {
                "income_labels": list(income_bins.keys()),
                "income_data": list(income_bins.values()),
                "risk_labels": list(risk_bins.keys()),
                "risk_data": list(risk_bins.values()),
                "trend_labels": dates_labels,
                "trend_data": dates_data,
            }
        ),
        200,
    )


@api_bp.route("/history/export/csv", methods=["GET"])
@rate_limit(limit_count=10, period_seconds=60)
def export_history_csv():
    """Exports prediction logs history from SQLite as a CSV attachment."""
    try:
        import csv
        import io

        # Retrieve all history
        history_records = db_manager.get_predictions(limit=1000)

        output = io.StringIO()
        writer = csv.writer(output)

        # CSV Header
        writer.writerow(
            [
                "Prediction ID",
                "Timestamp",
                "Gender",
                "Annual Income",
                "Employment",
                "Years Experience",
                "Number of Children",
                "Outstanding Debt",
                "Decision",
                "Probability",
                "Risk Level",
                "Model",
            ]
        )

        for item in history_records:
            writer.writerow(
                [
                    item.get("application_id"),
                    item.get("timestamp"),
                    item.get("gender"),
                    item.get("income"),
                    item.get("employment"),
                    item.get("experience"),
                    item.get("children"),
                    item.get("debt"),
                    item.get("prediction"),
                    item.get("probability"),
                    item.get("risk_level"),
                    item.get("model"),
                ]
            )

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=credit_prediction_history.csv"},
        )
    except Exception as e:
        logger.error(f"Failed to export CSV: {str(e)}")
        flash(f"CSV Export failed: {str(e)}", "danger")
        return redirect(url_for("api.history"))


@api_bp.route("/history/export/json", methods=["GET"])
@rate_limit(limit_count=10, period_seconds=60)
def export_history_json():
    """Exports prediction logs history from SQLite as a JSON attachment."""
    try:
        history_records = db_manager.get_predictions(limit=1000)
        json_data = json.dumps(history_records, indent=2)

        return Response(
            json_data,
            mimetype="application/json",
            headers={"Content-disposition": "attachment; filename=credit_prediction_history.json"},
        )
    except Exception as e:
        logger.error(f"Failed to export JSON: {str(e)}")
        flash(f"JSON Export failed: {str(e)}", "danger")
        return redirect(url_for("api.history"))


@api_bp.route("/api/predict", methods=["POST"])
def api_predict():
    """Backward compatibility scoring API endpoint."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided."}), 400
    try:
        result = predictor.process_and_predict(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/health", methods=["GET"])
def legacy_health():
    """Legacy health check endpoint for backwards compatibility."""
    return health()


@api_bp.route("/api/v1/history", methods=["GET"])
def legacy_api_v1_history():
    """Legacy JSON history logs list endpoint for backwards compatibility."""
    records = db_manager.get_predictions(limit=1000)
    return jsonify(records), 200

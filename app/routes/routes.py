import json
import os
import time
from datetime import datetime

from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.database.database import DatabaseManager
from app.routes.forms import CreditApprovalForm
from app.services.prediction import PredictorAPI
from app.routes.validators import InputValidator
from app.utils.limiter import rate_limit
from app.utils.logger import get_logger

logger = get_logger(__name__)

START_TIME = time.time()

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
    model_metrics = None
    best_model_name = "Unknown"
    try:
        from config.config import config
        metrics_path = os.path.join(config.get_paths()["models_dir"], "model_metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                raw_metrics = json.load(f)
                model_metrics = []
                mapping = {
                    "logistic_regression": "Logistic Regression",
                    "decision_tree": "Decision Tree",
                    "random_forest": "Random Forest",
                    "xgboost": "XGBoost",
                }
                for row in raw_metrics:
                    mapped_row = row.copy()
                    model_key = str(row.get("Model", "")).lower()
                    mapped_row["Model"] = mapping.get(model_key, row.get("Model"))
                    model_metrics.append(mapped_row)
        best_model_name = predictor.get_model_name()
    except Exception as e:
        logger.warning(f"Could not load model metrics or name: {str(e)}")

    return render_template("about.html", model_metrics=model_metrics, best_model_name=best_model_name)


@api_bp.route("/predict", methods=["GET"])
@login_required
def predict_get():
    """Renders the Credit Application entry form wizard."""
    form = CreditApprovalForm()
    return render_template("predict.html", form=form)


@api_bp.route("/predict", methods=["POST"])
@login_required
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

            # Extract explanations
            explanation = result.get("explanation", {})
            risk_factors = explanation.get("risk_factors", [])
            support_factors = explanation.get("support_factors", [])

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
                model=predictor.get_model_name(),
                recommendation="; ".join(recommendations),
                user_id=current_user.id if current_user.is_authenticated else None,
                explanation=explanation,
            )

            return render_template(
                "result.html",
                result=decision,
                probability=probability,
                raw_data=form_data,
                risk_factors=risk_factors,
                support_factors=support_factors,
                risk_level=risk_level,
                prediction_time=prediction_time_ms,
                model_used=predictor.get_model_name(),
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
@login_required
def history():
    """Renders prediction history log list supporting filter, search, sort, pagination."""
    search = request.args.get("search", "").strip()
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "DESC")
    decision = request.args.get("decision", "All").strip()
    risk_level = request.args.get("risk_level", "All").strip()
    page = int(request.args.get("page", 1))
    limit = 10

    # Retrieve user's predictions from database
    history_records = db_manager.get_user_predictions(
        user_id=current_user.id,
        limit=1000,
        search=search or None,
        sort_by=sort_by,
        order=order,
        decision=decision,
        risk_level=risk_level,
    )

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
        decision=decision,
        risk_level=risk_level,
    )


@api_bp.route("/history/delete/<application_id>", methods=["POST"])
@login_required
def delete_history_entry(application_id):
    """Deletes a single prediction history entry for the logged-in user."""
    success = db_manager.delete_prediction(application_id, current_user.id)
    if success:
        flash(f"Application record {application_id} successfully deleted.", "success")
    else:
        flash(f"Failed to delete record {application_id} or unauthorized.", "danger")
    return redirect(url_for("api.history"))


@api_bp.route("/history/clear", methods=["POST"])
@login_required
def clear_user_history():
    """Clears all prediction logs and reports for the current user."""
    db_manager.clear_user_history(current_user.id)
    flash("Your entire evaluation history log has been cleared.", "success")
    return redirect(url_for("api.history"))


@api_bp.route("/admin", methods=["GET"])
@login_required
def admin():
    """Renders Admin Dashboard statistics panels (Phase 11 spec)."""
    stats = db_manager.get_admin_stats()
    recent = db_manager.get_predictions(limit=6)
    return render_template("admin.html", stats=stats, recent=recent)


@api_bp.route("/report/<application_id>", methods=["GET"])
@login_required
def get_report(application_id):
    """Renders printable, clean PDF-ready credit report view (Persisted Reports table)."""
    # Fetch report directly from SQLite reports table without user_id filter for ownership validation
    report = db_manager.get_report_by_app_id(application_id)
    if not report:
        flash("Application credit report not found.", "danger")
        return redirect(url_for("api.history"))

    # Security: check ownership if user_id is set on the report
    if report["user_id"] is not None and report["user_id"] != current_user.id:
        flash("Unauthorized access to this credit report.", "danger")
        return redirect(url_for("api.history"))

    # Map report schema structure to match what report.html expects
    record = {
        "application_id": report["application_id"],
        "timestamp": report["timestamp"],
        "gender": report["inputs"].get("code_gender", "Unknown"),
        "income": report["inputs"].get("amt_income_total", 0.0),
        "employment": report["inputs"].get("name_income_type", "Unknown"),
        "experience": report["inputs"].get("years_employed", 0.0),
        "children": report["inputs"].get("cnt_children", 0),
        "debt": report["inputs"].get("existing_debt", 0.0),
        "prediction": report["prediction"],
        "probability": report["confidence"],
        "risk_level": "Low" if report["prediction"] == "Approved" else "High",
        "model": report["model_used"],
        "recommendation": "Manual review required",
        "input": report["inputs"],
        "explanation": report["explanation"],
    }

    # Retrieve risk_level and recommendations from the prediction_history table to keep it accurate
    try:
        hist_rec = db_manager.get_user_predictions(current_user.id, limit=1, search=application_id)
        if hist_rec:
            record["risk_level"] = hist_rec[0]["risk_level"]
            record["recommendation"] = hist_rec[0]["recommendation"]
    except Exception:
        pass

    return render_template("report.html", record=record)


# ==========================================
# REST API (v1) ENDPOINTS
# ==========================================


@api_bp.route("/api/v1/health", methods=["GET"])
@rate_limit(limit_count=60, period_seconds=60)
def health():
    """Standard health check REST API endpoint with model, database, and uptime information."""
    from src.models.predict import _predictor

    # Model status
    model_status = "loaded" if (_predictor.model is not None and _predictor.pipeline is not None) else "not_loaded"

    # Database connectivity status
    database_status = "connected" if db_manager.check_connection() else "disconnected"

    # Uptime duration formatting
    uptime_seconds = time.time() - START_TIME
    if uptime_seconds < 60:
        uptime_str = f"{uptime_seconds:.1f}s"
    elif uptime_seconds < 3600:
        uptime_str = f"{int(uptime_seconds // 60)}m {int(uptime_seconds % 60)}s"
    else:
        uptime_str = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m {int(uptime_seconds % 60)}s"

    # Determine loaded model name dynamically
    try:
        model_loaded_name = _predictor.get_model_name().lower().replace(" ", "_")
        if model_loaded_name == "unknown":
            model_loaded_name = "logistic_regression"
    except Exception:
        model_loaded_name = "logistic_regression"

    return (
        jsonify(
            {
                "status": "healthy",
                "model": model_status,
                "model_loaded": model_loaded_name,
                "database": database_status,
                "uptime": uptime_str,
                "version": "1.0.0",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        200,
    )


@api_bp.route("/version", methods=["GET"])
def version_endpoint():
    """Returns application and model version metadata."""
    return (
        jsonify(
            {
                "app_name": "Credit Card Approval Prediction",
                "version": "1.0.0",
                "flask_version": "3.0.x",
                "python_version": "3.13",
                "model_version": "1.0.0",
                "model_type": "logistic_regression",
            }
        ),
        200,
    )


@api_bp.route("/startup", methods=["GET"])
def startup_diagnostics():
    """Returns startup diagnostics about system dependencies and file structures."""
    import sys

    from app.services.predict import _predictor

    diagnostics = {
        "status": "completed",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "python_path": sys.path,
        "environment": os.getenv("FLASK_ENV", "development"),
        "database": {
            "path": db_manager.db_path,
            "exists": os.path.exists(db_manager.db_path),
            "healthy": db_manager.check_connection(),
        },
        "model_files": {
            "best_model_exists": os.path.exists(_predictor.model_path),
            "pipeline_exists": os.path.exists(_predictor.pipeline_path),
            "loaded": _predictor.model is not None and _predictor.pipeline is not None,
        },
    }
    return jsonify(diagnostics), 200


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
    monthly_trends = {}

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
            if len(day) >= 7:
                month = day[:7]  # YYYY-MM
                monthly_trends[month] = monthly_trends.get(month, 0) + 1

    # Sort dates
    sorted_dates = sorted(date_trends.items())
    dates_labels = [item[0] for item in sorted_dates[-10:]]
    dates_data = [item[1] for item in sorted_dates[-10:]]

    # Sort months
    sorted_months = sorted(monthly_trends.items())
    months_labels = [item[0] for item in sorted_months[-12:]]
    months_data = [item[1] for item in sorted_months[-12:]]

    return (
        jsonify(
            {
                "income_labels": list(income_bins.keys()),
                "income_data": list(income_bins.values()),
                "risk_labels": list(risk_bins.keys()),
                "risk_data": list(risk_bins.values()),
                "trend_labels": dates_labels,
                "trend_data": dates_data,
                "monthly_labels": months_labels,
                "monthly_data": months_data,
            }
        ),
        200,
    )


@api_bp.route("/history/export/csv", methods=["GET"])
@login_required
@rate_limit(limit_count=10, period_seconds=60)
def export_history_csv():
    """Exports prediction logs history from SQLite as a CSV attachment."""
    try:
        import csv
        import io

        # Retrieve only current user's history
        history_records = db_manager.get_user_predictions(user_id=current_user.id, limit=1000)

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
@login_required
@rate_limit(limit_count=10, period_seconds=60)
def export_history_json():
    """Exports prediction logs history from SQLite as a JSON attachment."""
    try:
        # Retrieve only current user's history
        history_records = db_manager.get_user_predictions(user_id=current_user.id, limit=1000)
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

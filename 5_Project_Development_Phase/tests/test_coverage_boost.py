import json
import os
import time
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from werkzeug.security import generate_password_hash

from app.database.database import DatabaseManager
from app.database.history import HistoryManager
from app.services.prediction import PredictorAPI
from app.services.explainability import ExplanationEngine
from src.models.hyperparameter_tuning import HyperparameterTuner
from src.models.metrics import calculate_all_metrics
from app.services.predict import RiskPredictor
from src.models.train import ModelTrainer
from app.utils.exceptions import ModelTrainingError as AppModelTrainingError
from src.utils.exceptions import ModelTrainingError
from app.utils.helper import load_pkl, save_json, save_pkl
from app.utils.tracker import ExperimentTracker
from src.visualization.plots import VizPlotter


def _login_test_client(app, client):
    """Creates a test user and logs in via the client session."""
    with app.app_context():
        db = DatabaseManager()
        # Delete user if exists to guarantee clean slate
        with db._get_connection() as conn:
            conn.execute("DELETE FROM users WHERE username = ? OR email = ?", ("route_test_user", "routetest@test.com"))
            conn.commit()
        db.create_user(
            username="route_test_user",
            email="routetest@test.com",
            password_hash=generate_password_hash("testpass123", method="scrypt"),
            full_name="Route Tester",
            role="Administrator",
        )
    client.post(
        "/auth/login",
        data={
            "email": "routetest@test.com",
            "password": "testpass123",
            "submit": "Sign In",
        },
        follow_redirects=True,
    )


@patch("src.models.predict._predictor.load_pipeline")
def test_create_app_preload_exception(mock_load):
    """Verifies that an exception during app preload is logged and handled cleanly."""
    mock_load.side_effect = Exception("Model load failure")
    from app.app import create_app

    app = create_app()
    assert app is not None


# ----------------------------------------------------
# 2. src/api/database.py tests
# ----------------------------------------------------


def test_database_manager_check_connection_exception():
    """Verifies check_connection returns False on failure."""
    db = DatabaseManager()
    with patch.object(db, "_get_connection") as mock_get_conn:
        mock_get_conn.side_effect = Exception("Connection refused")
        assert db.check_connection() is False


def test_database_manager_add_prediction_new_signature(tmp_path):
    """Verifies add_prediction handles the new signature format cleanly."""
    db = DatabaseManager()
    row_id = db.add_prediction(
        input_features="APP-TEST99",
        prediction="Approved",
        probability=85.0,
        gender="F",
        income=250000.0,  # > 200k to cover routes.py line 343
        employment="Commercial associate",
        experience=5.0,
        children=1,
        debt=1500.0,
        risk_level="Low",
        model="Logistic Regression",
        recommendation="Approved facility",
    )
    assert row_id is not None
    records = db.get_predictions(search="APP-TEST99")
    assert len(records) > 0
    assert records[0]["income"] == 250000.0


def test_database_manager_get_predictions_invalid_sort(tmp_path):
    """Verifies fallback sorting field when invalid parameters are passed."""
    db = DatabaseManager()
    records = db.get_predictions(sort_by="invalid_field", order="INVALID")
    assert isinstance(records, list)


# ----------------------------------------------------
# 3. src/api/history.py tests
# ----------------------------------------------------


def test_history_manager_read_valid_json(tmp_path):
    """Verifies HistoryManager reads valid JSON file (covers line 26)."""
    history_file = os.path.join(tmp_path, "prediction_history.json")
    with open(history_file, "w") as f:
        json.dump([{"test": "data"}], f)
    with patch("config.config.config.get_paths") as mock_paths:
        mock_paths.return_value = {"processed_dir": str(tmp_path)}
        manager = HistoryManager()
        assert len(manager.get_history()) == 1


def test_history_manager_read_corrupted_json(tmp_path):
    """Verifies HistoryManager fallback on corrupted JSON files."""
    history_file = os.path.join(tmp_path, "prediction_history.json")
    with open(history_file, "w") as f:
        f.write("invalid json contents")

    with patch("config.config.config.get_paths") as mock_paths:
        mock_paths.return_value = {"processed_dir": str(tmp_path)}
        manager = HistoryManager()
        assert manager.get_history() == []


@patch("builtins.open")
def test_history_manager_save_exception(mock_open):
    """Verifies exception handling during history saving."""
    mock_open.side_effect = Exception("Write permission denied")
    manager = HistoryManager()
    manager.save_history()


def test_history_manager_clear(tmp_path):
    """Verifies history clearing method."""
    with patch("config.config.config.get_paths") as mock_paths:
        mock_paths.return_value = {"processed_dir": str(tmp_path)}
        manager = HistoryManager()
        manager.add_entry({"gender": "M"}, "Approved", 90.0)
        assert len(manager.get_history()) > 0
        manager.clear_history()
        assert len(manager.get_history()) == 0


# ----------------------------------------------------
# 4. src/api/prediction.py tests
# ----------------------------------------------------


@patch("app.services.predict.InferenceEngine.predict")
def test_predictor_api_exception(mock_predict):
    """Verifies PredictorAPI raises ModelTrainingError on prediction pipeline failures."""
    mock_predict.side_effect = Exception("Pipeline failure")
    api = PredictorAPI()
    with pytest.raises(AppModelTrainingError):
        api.process_and_predict({"code_gender": "M"})


# ----------------------------------------------------
# 5. src/api/routes.py tests
# ----------------------------------------------------


def test_routes_dti_rejection(tmp_path):
    """Verifies DTI threshold business rule logic rejects applicants with high debt-to-income."""
    from app.app import create_app

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with patch("app.routes.routes.predictor.process_and_predict") as mock_predict:
        mock_predict.return_value = {
            "approval_probability_percent": 90.0,
            "decision": "Approved",
            "explanation": {"risk_factors": [], "support_factors": []},
        }
        with app.test_client() as client:
            _login_test_client(app, client)
            response = client.post(
                "/predict",
                data={
                    "code_gender": "M",
                    "cnt_children": 0,
                    "cnt_fam_members": 1,
                    "age_years": 30,
                    "amt_income_total": 20000,
                    "flag_own_car": "N",
                    "flag_own_realty": "N",
                    "name_income_type": "Working",
                    "name_education_type": "Secondary / secondary special",
                    "name_family_status": "Single / not married",
                    "name_housing_type": "House / apartment",
                    "years_employed": 5.0,
                    "occupation_type": "Laborers",
                    "existing_debt": 15000,  # DTI = 0.75 > 0.45
                    "loan_amount": 1000,
                    "credit_history": "Good",
                    "income_source": "Salary",
                    "employment_type": "Full-time",
                },
            )
            assert response.status_code == 200
            assert b"Rejected" in response.data
            assert b"Debt-to-Income (DTI) ratio" in response.data


def test_routes_bad_credit_rejection(tmp_path):
    """Verifies that Bad credit history immediately results in rejection."""
    from app.app import create_app

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with patch("app.routes.routes.predictor.process_and_predict") as mock_predict:
        mock_predict.return_value = {"approval_probability_percent": 90.0, "decision": "Approved"}
        with app.test_client() as client:
            _login_test_client(app, client)
            response = client.post(
                "/predict",
                data={
                    "code_gender": "M",
                    "cnt_children": 0,
                    "cnt_fam_members": 1,
                    "age_years": 30,
                    "amt_income_total": 50000,
                    "flag_own_car": "N",
                    "flag_own_realty": "N",
                    "name_income_type": "Working",
                    "name_education_type": "Secondary / secondary special",
                    "name_family_status": "Single / not married",
                    "name_housing_type": "House / apartment",
                    "years_employed": 5.0,
                    "occupation_type": "Laborers",
                    "existing_debt": 1000,
                    "loan_amount": 1000,
                    "credit_history": "Bad",
                    "income_source": "Salary",
                    "employment_type": "Full-time",
                },
            )
            assert response.status_code == 200
            assert b"Rejected" in response.data
            assert b"Prior payment default records" in response.data


def test_routes_short_employment_rejection(tmp_path):
    """Verifies that rejection is accompanied by short employment reason if years_employed < 2."""
    from app.app import create_app

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with patch("app.routes.routes.predictor.process_and_predict") as mock_predict:
        mock_predict.return_value = {
            "approval_probability_percent": 12.0,
            "decision": "Rejected",
            "explanation": {"risk_factors": [], "support_factors": []},
        }
        with app.test_client() as client:
            _login_test_client(app, client)
            response = client.post(
                "/predict",
                data={
                    "code_gender": "M",
                    "cnt_children": 0,
                    "cnt_fam_members": 1,
                    "age_years": 30,
                    "amt_income_total": 50000,
                    "flag_own_car": "N",
                    "flag_own_realty": "N",
                    "name_income_type": "Working",
                    "name_education_type": "Secondary / secondary special",
                    "name_family_status": "Single / not married",
                    "name_housing_type": "House / apartment",
                    "years_employed": 1.0,  # < 2.0
                    "occupation_type": "Laborers",
                    "existing_debt": 1000,
                    "loan_amount": 1000,
                    "credit_history": "Good",
                    "income_source": "Salary",
                    "employment_type": "Full-time",
                },
            )
            assert response.status_code == 200
            assert b"Short employment duration" in response.data


def test_routes_no_reasons_rejection(tmp_path):
    """Verifies default risk profile reason when rejection occurs without specific debt/history/employment flags."""
    from app.app import create_app

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with patch("app.routes.routes.predictor.process_and_predict") as mock_predict:
        mock_predict.return_value = {
            "approval_probability_percent": 12.0,
            "decision": "Rejected",
            "explanation": {"risk_factors": [], "support_factors": []},
        }
        with app.test_client() as client:
            _login_test_client(app, client)
            response = client.post(
                "/predict",
                data={
                    "code_gender": "M",
                    "cnt_children": 0,
                    "cnt_fam_members": 1,
                    "age_years": 30,
                    "amt_income_total": 50000,
                    "flag_own_car": "N",
                    "flag_own_realty": "N",
                    "name_income_type": "Working",
                    "name_education_type": "Secondary / secondary special",
                    "name_family_status": "Single / not married",
                    "name_housing_type": "House / apartment",
                    "years_employed": 5.0,  # >= 2.0 (no short employment reason)
                    "occupation_type": "Laborers",
                    "existing_debt": 1000,
                    "loan_amount": 1000,
                    "credit_history": "Good",
                    "income_source": "Salary",
                    "employment_type": "Full-time",
                },
            )
            assert response.status_code == 200
            assert b"Socio-demographic parameters classify profile" in response.data


def test_routes_prediction_pipeline_exception_handling(tmp_path):
    """Verifies that route captures predictor exceptions and displays flash warning."""
    from app.app import create_app

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with patch("app.routes.routes.predictor.process_and_predict") as mock_predict:
        mock_predict.side_effect = Exception("Model prediction failed completely")
        with app.test_client() as client:
            _login_test_client(app, client)
            response = client.post(
                "/predict",
                data={
                    "code_gender": "M",
                    "cnt_children": 0,
                    "cnt_fam_members": 1,
                    "age_years": 30,
                    "amt_income_total": 50000,
                    "flag_own_car": "N",
                    "flag_own_realty": "N",
                    "name_income_type": "Working",
                    "name_education_type": "Secondary / secondary special",
                    "name_family_status": "Single / not married",
                    "name_housing_type": "House / apartment",
                    "years_employed": 5.0,
                    "occupation_type": "Laborers",
                    "existing_debt": 1000,
                    "loan_amount": 1000,
                    "credit_history": "Good",
                    "income_source": "Salary",
                    "employment_type": "Full-time",
                },
            )
            assert response.status_code == 200
            assert b"Inference failed:" in response.data


def test_routes_health_check_uptime_formatting():
    """Verifies uptime calculations display minutes and hours formatting."""
    from app.app import create_app

    app = create_app()

    # Test case 1: uptime in minutes (< 3600 seconds)
    with patch("app.routes.routes.START_TIME", time.time() - 150):
        with app.test_client() as client:
            response = client.get("/api/v1/health")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "2m" in data["uptime"]

    # Test case 2: uptime in hours (>= 3600 seconds)
    with patch("app.routes.routes.START_TIME", time.time() - 5000):
        with app.test_client() as client:
            response = client.get("/api/v1/health")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "1h 23m" in data["uptime"]


def test_routes_api_predict_empty_payload():
    """Verifies api endpoint returns 400 when missing payload (covers routes.py line 459)."""
    from app.app import create_app

    app = create_app()
    with app.test_client() as client:
        with patch("flask.Request.get_json", return_value=None):
            response = client.post("/api/predict", json=None)
            assert response.status_code == 400


@patch("app.routes.routes.predictor.process_and_predict")
def test_routes_api_predict_exception(mock_predict):
    """Verifies API endpoint returns 400 on prediction failure."""
    from app.app import create_app

    app = create_app()
    mock_predict.side_effect = Exception("Prediction error")
    with app.test_client() as client:
        response = client.post("/api/predict", json={"code_gender": "M"})
        assert response.status_code == 400
        assert b"Prediction error" in response.data


# ----------------------------------------------------
# 6. src/visualization/plots.py tests
# ----------------------------------------------------


def test_viz_plotter_exceptions(tmp_path):
    """Verifies VizPlotter methods do not crash the execution flow when invalid parameters are given."""
    plotter = VizPlotter()
    plotter.plot_distribution(None, "invalid_col", "invalid.png")
    plotter.plot_target_balance(None, "invalid.png")
    plotter.plot_correlation_heatmap(None, "invalid.png")
    plotter.plot_categorical_vs_target(None, "invalid_col", "invalid_target", "invalid.png")
    plotter.plot_numeric_vs_target_box(None, "invalid_col", "invalid_target", "invalid.png")
    plotter.plot_outliers_boxplot(None, "invalid_col", "invalid.png")


def test_viz_plotter_all_methods_success(tmp_path):
    """
    Verifies VizPlotter runs successfully for all methods,
    then triggers save exceptions (covers lines 92-102, 114-122).
    """
    plotter = VizPlotter()
    df = pd.DataFrame({"income": [50000, 100000, 150000], "gender": ["M", "F", "M"], "target": [0, 1, 0]})

    # Use invalid file path with null bytes to trigger save exceptions after executing layout code
    plotter.plot_distribution(df, "income", "\0invalid.png")
    plotter.plot_target_balance(df["target"], "\0invalid.png")
    plotter.plot_correlation_heatmap(df, "\0invalid.png")
    plotter.plot_categorical_vs_target(df, "gender", "target", "\0invalid.png")
    plotter.plot_numeric_vs_target_box(df, "income", "target", "\0invalid.png")
    plotter.plot_outliers_boxplot(df, "income", "\0invalid.png")


# ----------------------------------------------------
# 7. src/models/predict.py tests
# ----------------------------------------------------


def test_risk_predictor_validate_input_missing():
    """Verifies validate_input detects missing required inputs."""
    pred = RiskPredictor()
    assert pred.validate_input({"code_gender": "M"}) is False


@patch("app.services.predict.load_pkl")
def test_risk_predictor_predict_proba_shapes(mock_load):
    """Verifies that predict handles diverse model prediction probability shapes (covers lines 89-90)."""
    mock_model = MagicMock()
    mock_pipeline = MagicMock()
    mock_load.side_effect = [mock_pipeline, mock_model]

    pred = RiskPredictor()

    # Case 1: predict_proba returns 1D array
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [0.15]
    res1 = pred.predict(pd.DataFrame([{"code_gender": "M"}]))
    assert res1["decision"] == "Approved"

    # Case 2: predict_proba returns empty list (falls back to 0.0)
    mock_model.predict_proba.return_value = []
    res2 = pred.predict(pd.DataFrame([{"code_gender": "M"}]))
    assert res2["approval_probability_percent"] == 100.0

    # Case 3: predict_proba returns unconvertible string (covers lines 89-90)
    mock_model.predict_proba.return_value = ["invalid"]
    res3 = pred.predict(pd.DataFrame([{"code_gender": "M"}]))
    assert res3["approval_probability_percent"] == 100.0


@patch("app.services.predict.load_pkl")
def test_risk_predictor_predict_explanation_exception(mock_load):
    """Verifies that explain_instance failures are handled gracefully (covers lines 98-100)."""
    mock_model = MagicMock()
    mock_pipeline = MagicMock()
    mock_load.side_effect = [mock_pipeline, mock_model]

    pred = RiskPredictor()
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [0.15]

    with patch("app.services.predict.ExplanationEngine.explain_instance") as mock_explain:
        mock_explain.side_effect = Exception("Surrogate failure")
        res = pred.predict(pd.DataFrame([{"code_gender": "M"}]))
        assert res["explanation"] == {"error": "Surrogate failure"}


def test_risk_predictor_multiple_rows():
    """Verifies prediction with multiple records (covers line 107)."""
    pred = RiskPredictor()
    raw_data = {
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "N",
        "FLAG_OWN_REALTY": "N",
        "CNT_CHILDREN": 0,
        "AMT_INCOME_TOTAL": 50000.0,
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Secondary / secondary special",
        "NAME_FAMILY_STATUS": "Single / not married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "DAYS_BIRTH": -30 * 365,
        "DAYS_EMPLOYED": -5 * 365,
        "FLAG_MOBIL": 1,
        "FLAG_WORK_PHONE": 0,
        "FLAG_PHONE": 0,
        "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Laborers",
        "CNT_FAM_MEMBERS": 1,
    }
    df = pd.DataFrame([raw_data, raw_data])
    res = pred.predict(df)
    assert isinstance(res, list)


@patch("app.services.predict.load_pkl")
def test_risk_predictor_predict_no_proba(mock_load):
    """Verifies risk probability fallback logic when predict_proba attribute does not exist."""
    mock_model = MagicMock()
    mock_pipeline = MagicMock()
    delattr(mock_model, "predict_proba")
    mock_load.side_effect = [mock_pipeline, mock_model]

    pred = RiskPredictor()
    mock_model.predict.return_value = [1]
    res = pred.predict(pd.DataFrame([{"code_gender": "M"}]))
    assert res["decision"] == "Rejected"

    probs = pred.predict_probability(pd.DataFrame([{"code_gender": "M"}]))
    assert probs == [1.0]


# ----------------------------------------------------
# 8. src/models/explainability.py tests
# ----------------------------------------------------


def test_explanation_engine_decision_methods():
    """
    Verifies local surrogates fallback decision methods (decision_function/predict)
    when model has no predict_proba.
    """
    mock_pipeline = MagicMock()
    mock_pipeline.get_feature_names_out.return_value = ["num__val"]
    mock_pipeline.transform.return_value = [[1.5]]

    # Case 1: Model has decision_function
    mock_model1 = MagicMock()
    delattr(mock_model1, "coef_")
    delattr(mock_model1, "predict_proba")
    mock_model1.decision_function.return_value = [0.6] * 50

    engine1 = ExplanationEngine(mock_model1, mock_pipeline)
    res1 = engine1.explain_instance(pd.DataFrame([{"val": 1.5}]))
    assert "risk_factors" in res1

    # Case 2: Model has only predict
    mock_model2 = MagicMock()
    delattr(mock_model2, "coef_")
    delattr(mock_model2, "predict_proba")
    delattr(mock_model2, "decision_function")
    mock_model2.predict.return_value = [1] * 50

    engine2 = ExplanationEngine(mock_model2, mock_pipeline)
    res2 = engine2.explain_instance(pd.DataFrame([{"val": 1.5}]))
    assert "risk_factors" in res2


def test_explanation_engine_clean_names():
    """Verifies that clean presentation name rules correctly map raw feature inputs."""
    mock_pipeline = MagicMock()
    mock_pipeline.get_feature_names_out.return_value = [
        "num__CODE_GENDER",
        "num__OWN_REALTY",
        "num__OWN_CAR",
        "num__INCOME_TOTAL",
    ]
    mock_pipeline.transform.return_value = [[1.0, 1.0, 1.0, 1.0]]

    mock_model = MagicMock()
    mock_model.coef_ = [[1.0, 1.0, 1.0, 1.0]]
    mock_model.intercept_ = [0.5]

    engine = ExplanationEngine(mock_model, mock_pipeline)
    res = engine.explain_instance(pd.DataFrame([{"val": 1.0}]))

    features = [f["feature"] for f in res["risk_factors"]]
    assert "Gender" in features
    assert "Owns Property" in features
    assert "Owns Car" in features
    assert "Annual Income" in features


def test_explanation_engine_exception():
    """Verifies exception handling inside explain_instance (covers lines 108-110)."""
    engine = ExplanationEngine(None, None)
    res = engine.explain_instance(None)
    assert "error" in res


# ----------------------------------------------------
# 9. src/models/hyperparameter_tuning.py tests
# ----------------------------------------------------


def test_hyperparameter_tuner_fallback():
    """Verifies tuning logs warning and returns model immediately if tuning is not defined."""
    tuner = HyperparameterTuner()
    mock_model = MagicMock()
    res = tuner.tune("invalid_model", mock_model, None, None)
    assert res == mock_model


def test_hyperparameter_tuner_exception():
    """Verifies tuning handles tuning exceptions and returns baseline model."""
    tuner = HyperparameterTuner()
    mock_model = MagicMock()
    res = tuner.tune("logistic_regression", mock_model, None, None)
    assert res == mock_model


# ----------------------------------------------------
# 10. src/models/metrics.py tests
# ----------------------------------------------------


def test_calculate_all_metrics_fallbacks():
    """Verifies MCC and probability metrics fail-safe fallbacks."""
    res = calculate_all_metrics([], [])
    assert res["Matthews_Correlation_Coefficient"] == 0.0

    res2 = calculate_all_metrics([0, 1], [0, 1], y_prob=None)
    assert res2["ROC-AUC"] == 0.5
    assert res2["Log_Loss"] == 0.0


# ----------------------------------------------------
# 11. src/models/train.py tests
# ----------------------------------------------------


def test_model_trainer_train_exception():
    """Verifies that model training errors trigger ModelTrainingError exception."""
    trainer = ModelTrainer()
    mock_model = MagicMock()
    mock_model.fit.side_effect = Exception("Fit error")
    with pytest.raises(ModelTrainingError):
        trainer.train_and_time_model("test_model", mock_model, None, None)


# ----------------------------------------------------
# 12. src/utils/helper.py tests
# ----------------------------------------------------


def test_helper_pkl_exceptions():
    """Verifies helper pkl methods handle dump/load failures cleanly."""
    from app.utils.exceptions import DataPreprocessingError as AppDataPreprocessingError

    with pytest.raises(AppDataPreprocessingError):
        save_pkl(lambda x: x, "/invalid_dir/test.pkl")

    config_path = (
        "config/config.py" if os.path.exists("config/config.py") else "5_Project_Development_Phase/config/config.py"
    )
    with pytest.raises(AppDataPreprocessingError):
        load_pkl(config_path)


def test_helper_json_exceptions(tmp_path):
    """Verifies helper json methods handle dump/load failures cleanly."""
    unserializable = {"val": {1, 2, 3}}
    with pytest.raises(TypeError):
        save_json(unserializable, os.path.join(tmp_path, "out.json"))


# ----------------------------------------------------
# 13. src/utils/tracker.py tests
# ----------------------------------------------------


def test_experiment_tracker_corrupted_json(tmp_path):
    """Verifies ExperimentTracker fallback on corrupted runs file."""
    runs_file = os.path.join(tmp_path, "runs.json")
    with open(runs_file, "w") as f:
        json.dump({"key": "val"}, f)

    with patch("config.config.config.get_paths") as mock_paths:
        mock_paths.return_value = {"logs_dir": str(tmp_path)}
        tracker = ExperimentTracker()
        tracker.log_run("LR", {}, {})
        assert len(tracker.get_runs()) == 1


def test_experiment_tracker_no_file(tmp_path):
    """Verifies get_runs returns empty list when runs file does not exist."""
    with patch("config.config.config.get_paths") as mock_paths:
        mock_paths.return_value = {"logs_dir": str(tmp_path)}
        tracker = ExperimentTracker()
        assert tracker.get_runs() == []

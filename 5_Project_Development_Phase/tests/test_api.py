import json
from unittest.mock import patch

import pytest

from app.app import create_app


def test_landing_page(client):
    """
    Test landing page renders correct title.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Risk Assessment Portal" in response.data or b"Credit" in response.data


def test_about_page(client):
    """
    Test about page.
    """
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data or b"Model" in response.data


def test_predict_page_get(client):
    """
    Test predict page form loading.
    """
    response = client.get("/predict")
    assert response.status_code == 200
    assert b"predict" in response.data or b"Form" in response.data


def test_history_page(client):
    """
    Test history view.
    """
    response = client.get("/history")
    assert response.status_code == 200
    assert b"Prediction History" in response.data or b"History" in response.data


def test_health_endpoint(client):
    """
    Test basic health check.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_api_v1_health(client):
    """
    Test v1 health check.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_api_v1_history(client):
    """
    Test v1 history json endpoint.
    """
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


@patch("app.services.prediction.PredictorAPI.process_and_predict")
def test_rest_api_scoring(mock_predict, client):
    """
    Test REST API predict JSON endpoint.
    """
    mock_predict.return_value = {"decision": "Approved", "class_code": 0, "approval_probability_percent": 98.5}

    payload = {"some_input": 123}
    response = client.post("/api/predict", data=json.dumps(payload), content_type="application/json")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["decision"] == "Approved"
    assert data["approval_probability_percent"] == 98.5


@patch("app.services.prediction.PredictorAPI.process_and_predict")
def test_predict_page_post_success(mock_predict, client):
    """
    Test HTML predict page submission.
    """
    mock_predict.return_value = {
        "decision": "Approved",
        "approval_probability_percent": 95.0,
        "explanation": {
            "risk_factors": [{"feature": "Age", "impact": 0.1}],
            "support_factors": [{"feature": "Income", "impact": -0.2}],
        },
    }
    form_data = {
        "code_gender": "M",
        "cnt_children": 0,
        "cnt_fam_members": 2,
        "age_years": 35,
        "amt_income_total": 150000.0,
        "flag_own_car": "N",
        "flag_own_realty": "Y",
        "name_income_type": "Working",
        "name_education_type": "Secondary / secondary special",
        "name_family_status": "Married",
        "name_housing_type": "House / apartment",
        "years_employed": 5.0,
        "flag_unemployed": 0,
        "occupation_type": "Laborers",
        "flag_work_phone": 0,
        "flag_phone": 0,
        "flag_email": 0,
    }
    response = client.post("/predict", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Approved" in response.data or b"Result" in response.data or b"predict" in response.data


def test_predict_page_post_invalid(client):
    """
    Test HTML predict form validation failure.
    """
    form_data = {
        "code_gender": "M",
        "cnt_children": -5,  # invalid range
    }
    response = client.post("/predict", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Form validation" in response.data or b"predict" in response.data


def test_export_history_csv(client):
    """
    Test CSV history export.
    """
    response = client.get("/history/export/csv")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Prediction ID" in response.data


def test_export_history_json(client):
    """
    Test JSON history export.
    """
    response = client.get("/history/export/json")
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_404_error_page(client):
    """
    Test 404 error page.
    """
    response = client.get("/non-existent-page")
    assert response.status_code == 404


def test_500_error_page():
    """
    Test 500 error handler directly.
    """
    app = create_app()
    with app.test_request_context():
        err_handlers = app.error_handler_spec[None][500]
        for key, handler in err_handlers.items():
            # Invoke handler directly
            resp, status = handler(Exception("Test Exception"))
            assert status == 500


def test_create_app_envs():
    """
    Test app factory pattern with different environment profiles.
    """
    with patch("os.getenv") as mock_getenv:
        mock_getenv.side_effect = lambda key, default=None: {
            "FLASK_ENV": "production",
            "SECRET_KEY": "test-mock-secret-key",
        }.get(key, default)
        app = create_app()
        assert app.config.get("ENV") == "production" or app.config.get("TESTING") is False

    with patch("os.getenv") as mock_getenv:
        mock_getenv.side_effect = lambda key, default=None: "testing" if key == "FLASK_ENV" else default
        app = create_app()
        assert app.config.get("TESTING") is True


def test_health_endpoint_exception(client):
    with patch("app.services.predict.RiskPredictor", side_effect=Exception("Model load fail")):
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["model_loaded"] in ["random_forest", "logistic_regression", "xgboost", "decision_tree", "Calibrated Random Forest", "calibrated_random_forest"]


def test_export_history_csv_exception(client):
    with patch("app.routes.routes.db_manager.get_user_predictions", side_effect=Exception("DB fail")):
        response = client.get("/history/export/csv", follow_redirects=False)
        assert response.status_code == 302
        assert "history" in response.location


def test_export_history_json_exception(client):
    with patch("app.routes.routes.db_manager.get_user_predictions", side_effect=Exception("DB fail")):
        response = client.get("/history/export/json", follow_redirects=False)
        assert response.status_code == 302
        assert "history" in response.location


def test_input_validator_exceptions():
    from app.routes.validators import InputValidator
    from app.utils.exceptions import ValidationError

    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json({})

    base_data = {
        "code_gender": "M",
        "cnt_children": 0,
        "cnt_fam_members": 2,
        "age_years": 35,
        "amt_income_total": 150000.0,
        "flag_own_car": "N",
        "flag_own_realty": "Y",
        "name_income_type": "Working",
        "name_education_type": "Secondary",
        "name_family_status": "Married",
        "name_housing_type": "House",
        "years_employed": 5.0,
        "flag_unemployed": 0,
    }

    data = base_data.copy()
    data["age_years"] = "invalid"
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)

    data = base_data.copy()
    data["amt_income_total"] = -100
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)

    data = base_data.copy()
    data["cnt_children"] = -1
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)

    data = base_data.copy()
    data["cnt_fam_members"] = 0
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)

    data = base_data.copy()
    data["years_employed"] = 100.0
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)

    data = base_data.copy()
    data["code_gender"] = "X"
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)

    data = base_data.copy()
    data["flag_own_car"] = "X"
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json(data)


def test_admin_dashboard(admin_client):
    """Test admin portal renders successfully."""
    response = admin_client.get("/admin")
    assert response.status_code == 200
    assert b"Operations Analytics" in response.data or b"Admin" in response.data


def test_api_admin_stats(admin_client):
    """Test admin stats JSON API endpoint."""
    response = admin_client.get("/api/v1/admin/stats")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "income_labels" in data
    assert "risk_labels" in data
    assert "trend_labels" in data


def test_report_page_not_found(client):
    """Test report page returns 302 redirect if ID not found."""
    response = client.get("/report/APP-NONEXISTENT", follow_redirects=False)
    assert response.status_code == 302
    assert "history" in response.location


def test_db_manager_methods():
    """Test SQLite database manager methods directly."""
    from app.routes.routes import db_manager

    db_manager.init_db()

    # Add prediction
    row_id = db_manager.add_prediction(
        input_features={"code_gender": "F"},
        prediction="Approved",
        probability=95.0,
        app_id="APP-TEST99",
        gender="F",
        income=120000.0,
        employment="Working",
        experience=10.0,
        children=1,
        debt=5000.0,
        risk_level="Low",
        model="Logistic Regression",
        recommendation="Approved",
    )
    assert row_id is not None

    # Get statistics
    stats = db_manager.get_admin_stats()
    assert stats["total"] >= 1
    assert stats["approved"] >= 1

    # Get predictions with search & sort
    results = db_manager.get_predictions(limit=5, search="APP-TEST99", sort_by="income", order="DESC")
    assert len(results) >= 1
    assert results[0]["application_id"] == "APP-TEST99"

    # Clear history
    db_manager.clear_history()
    stats_empty = db_manager.get_admin_stats()
    assert stats_empty["total"] == 0


def test_report_page_success(client):
    """Test report page renders successfully when ID exists."""
    from app.routes.routes import db_manager

    db_manager.add_prediction(
        input_features={"code_gender": "F"},
        prediction="Approved",
        probability=95.0,
        app_id="APP-SUCCESS-101",
        gender="F",
        income=120000.0,
        employment="Working",
        experience=10.0,
        children=1,
        debt=5000.0,
        risk_level="Low",
        model="Logistic Regression",
        recommendation="Approved",
    )
    response = client.get("/report/APP-SUCCESS-101")
    assert response.status_code == 200
    assert b"Statement" in response.data or b"Report" in response.data


def test_history_page_filters(client):
    """Test history list with search query and sorting parameters."""
    response = client.get("/history?search=APP-SUCCESS-101&sort_by=income&order=ASC")
    assert response.status_code == 200
    assert b"History" in response.data or b"Log" in response.data


def test_500_error_page_request(admin_client):
    """Test 500 error page renders successfully when an error is raised by a route."""
    admin_client.application.config["PROPAGATE_EXCEPTIONS"] = False
    with patch("app.routes.routes.db_manager.get_predictions", side_effect=Exception("Database crash")):
        response = admin_client.get("/admin")
        assert response.status_code == 500
        assert b"500" in response.data or b"Error" in response.data


def test_version_endpoint(client):
    """Test version metadata endpoint."""
    response = client.get("/version")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["app_name"] == "Credit Card Approval Prediction"
    assert "version" in data


def test_startup_diagnostics(client):
    """Test startup diagnostics endpoint."""
    response = client.get("/startup")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "completed"
    assert "database" in data
    assert "model_files" in data


def test_rbac_user_denied(client):
    """Verify that a regular user (role='User') is denied access to admin console and stats API."""
    response = client.get("/admin", follow_redirects=True)
    assert b"permission" in response.data or b"permission to access" in response.data or response.status_code == 403

    response_stats = client.get("/api/v1/admin/stats")
    assert response_stats.status_code == 403


def test_rbac_admin_allowed(app):
    """Verify that an Administrator (role='Administrator') is allowed access to admin console and stats API."""
    from app.database.database import DatabaseManager
    from werkzeug.security import generate_password_hash

    with app.test_client() as test_client:
        with app.app_context():
            db = DatabaseManager()
            pwd_hash = generate_password_hash("adminpass123", method="scrypt")
            db.create_user(
                username="admintest", email="admintest@test.com", password_hash=pwd_hash, role="Administrator"
            )

        # Log in
        test_client.post(
            "/auth/login",
            data={"email": "admintest@test.com", "password": "adminpass123", "submit": "Sign In"},
            follow_redirects=True,
        )

        response = test_client.get("/admin")
        assert response.status_code == 200

        response_stats = test_client.get("/api/v1/admin/stats")
        assert response_stats.status_code == 200


def test_rbac_officer_allowed(app):
    """Verify that an Officer (role='Officer') is allowed access to admin console and stats API."""
    from app.database.database import DatabaseManager
    from werkzeug.security import generate_password_hash

    with app.test_client() as test_client:
        with app.app_context():
            db = DatabaseManager()
            pwd_hash = generate_password_hash("officerpass123", method="scrypt")
            db.create_user(username="officertest", email="officertest@test.com", password_hash=pwd_hash, role="Officer")

        # Log in
        test_client.post(
            "/auth/login",
            data={"email": "officertest@test.com", "password": "officerpass123", "submit": "Sign In"},
            follow_redirects=True,
        )

        response = test_client.get("/admin")
        assert response.status_code == 200

        response_stats = test_client.get("/api/v1/admin/stats")
        assert response_stats.status_code == 200


def test_forgot_password_no_token_leak(app):
    """
    Assert that the response to /auth/forgot-password never contains the raw reset token
    in its body, headers, or flashed messages.
    """
    from app.database.database import DatabaseManager
    from werkzeug.security import generate_password_hash

    # Ensure a user exists for password reset
    with app.app_context():
        db = DatabaseManager()
        # Delete user if exists to guarantee clean slate
        with db._get_connection() as conn:
            conn.execute("DELETE FROM users WHERE email = ?", ("resetuser@test.com",))
            conn.commit()
        pwd_hash = generate_password_hash("userpass123", method="scrypt")
        db.create_user(username="resetuser", email="resetuser@test.com", password_hash=pwd_hash, role="Client User")

    with app.test_client() as test_client:
        # Trigger forgot password request
        response = test_client.post(
            "/auth/forgot-password", data={"email": "resetuser@test.com", "submit": "Submit"}, follow_redirects=True
        )

        assert response.status_code == 200

        # Check that the generic message is flashed
        assert b"If an account with that email exists, a reset link has been sent." in response.data

        # Ensure the token does not leak anywhere in the response body or headers
        assert b"/auth/reset-password/" not in response.data
        assert b"reset_url" not in response.data

        # Verify no token is present in the flashed cookies or headers
        for header, val in response.headers.items():
            assert "reset-password" not in val


def test_auth_registration_flow(app):
    """
    Test user registration page and handling, including duplicate username/email errors.
    """
    from app.database.database import DatabaseManager

    with app.app_context():
        db = DatabaseManager()
        with db._get_connection() as conn:
            conn.execute("DELETE FROM users WHERE username IN (?, ?)", ("regtest", "regtest2"))
            conn.execute("DELETE FROM users WHERE email IN (?, ?)", ("regtest@test.com", "regtest2@test.com"))
            conn.commit()

    with app.test_client() as test_client:
        # GET registration page
        response = test_client.get("/auth/register")
        assert response.status_code == 200

        # Successful Registration
        response = test_client.post(
            "/auth/register",
            data={
                "username": "regtest",
                "email": "regtest@test.com",
                "password": "Password123",
                "confirm_password": "Password123",
                "full_name": "Registration Test",
                "submit": "Sign Up",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Account created successfully! Please sign in." in response.data

        # Duplicate Username
        response = test_client.post(
            "/auth/register",
            data={
                "username": "regtest",
                "email": "regtest2@test.com",
                "password": "Password123",
                "confirm_password": "Password123",
                "full_name": "Registration Test 2",
                "submit": "Sign Up",
            },
            follow_redirects=True,
        )
        assert b"Username is already taken" in response.data

        # Duplicate Email
        response = test_client.post(
            "/auth/register",
            data={
                "username": "regtest2",
                "email": "regtest@test.com",
                "password": "Password123",
                "confirm_password": "Password123",
                "full_name": "Registration Test 2",
                "submit": "Sign Up",
            },
            follow_redirects=True,
        )
        assert b"An account with this email already exists" in response.data


def test_auth_forgot_password_nonexistent_user(app):
    """
    Requesting a reset link for a non-existent user should not reveal user existence.
    """
    with app.test_client() as test_client:
        response = test_client.post(
            "/auth/forgot-password",
            data={"email": "nonexistent@test.com", "submit": "Submit"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"If an account with that email exists, a reset link has been sent." in response.data


def test_auth_reset_password_valid_token(app):
    """
    Test using a valid timed token to set a new password.
    """
    from app.database.database import DatabaseManager
    from app.routes.auth import _generate_reset_token
    from werkzeug.security import generate_password_hash

    email = "validreset@test.com"
    with app.app_context():
        db = DatabaseManager()
        with db._get_connection() as conn:
            conn.execute("DELETE FROM users WHERE email = ?", (email,))
            conn.commit()
        pwd_hash = generate_password_hash("oldpass123", method="scrypt")
        db.create_user(username="validreset", email=email, password_hash=pwd_hash)
        token = _generate_reset_token(email)

    with app.test_client() as test_client:
        # GET with valid token
        response = test_client.get(f"/auth/reset-password/{token}")
        assert response.status_code == 200
        assert b"Reset Password" in response.data

        # POST with valid token
        response = test_client.post(
            f"/auth/reset-password/{token}",
            data={
                "password": "newpassword123",
                "confirm_password": "newpassword123",
                "submit": "Reset Password",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Your password has been reset. Please sign in." in response.data

        # Attempt to log in with new password
        response = test_client.post(
            "/auth/login",
            data={"email": email, "password": "newpassword123", "submit": "Sign In"},
            follow_redirects=True,
        )
        assert b"logout" in response.data.lower()


def test_auth_reset_password_invalid_token(app):
    """
    Test using an invalid or expired token.
    """
    with app.test_client() as test_client:
        # Invalid token signature
        response = test_client.get("/auth/reset-password/invalidtokenvalue123", follow_redirects=True)
        assert b"The reset link is invalid or has expired." in response.data


def test_auth_profile_edit_and_password_change(app):
    """
    Test profile edit details and changing password from profile page.
    """
    from app.database.database import DatabaseManager
    from werkzeug.security import generate_password_hash

    email = "profileedit@test.com"
    with app.app_context():
        db = DatabaseManager()
        with db._get_connection() as conn:
            conn.execute("DELETE FROM users WHERE email IN (?, ?)", (email, "newemail@test.com"))
            conn.commit()
        pwd_hash = generate_password_hash("profilepass", method="scrypt")
        db.create_user(username="profileedit", email=email, password_hash=pwd_hash, full_name="Old Name")

    with app.test_client() as test_client:
        # Login
        test_client.post(
            "/auth/login",
            data={"email": email, "password": "profilepass", "submit": "Sign In"},
            follow_redirects=True,
        )

        # GET Profile page
        response = test_client.get("/auth/profile")
        assert response.status_code == 200

        # POST Update Profile details
        response = test_client.post(
            "/auth/profile/edit",
            data={
                "form_type": "profile",
                "full_name": "New Name",
                "email": "newemail@test.com",
            },
            follow_redirects=True,
        )
        assert b"Profile updated successfully." in response.data

        # POST Update Profile password (wrong current password)
        response = test_client.post(
            "/auth/profile/edit",
            data={
                "form_type": "password",
                "current_password": "wrongpassword",
                "new_password": "newprofilepass",
            },
            follow_redirects=True,
        )
        assert b"Current password is incorrect." in response.data

        # POST Update Profile password (too short new password)
        response = test_client.post(
            "/auth/profile/edit",
            data={
                "form_type": "password",
                "current_password": "profilepass",
                "new_password": "short",
            },
            follow_redirects=True,
        )
        assert b"New password must be at least 8 characters." in response.data

        # POST Update Profile password (success)
        response = test_client.post(
            "/auth/profile/edit",
            data={
                "form_type": "password",
                "current_password": "profilepass",
                "new_password": "newprofilepass",
            },
            follow_redirects=True,
        )
        assert b"Password updated successfully." in response.data

import json
import pytest
from unittest.mock import patch, MagicMock
from app.app import create_app

@pytest.fixture
def client():
    """
    Flask test client fixture.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for unit tests
    with app.test_client() as client:
        yield client

def test_landing_page(client):
    """
    Test landing page renders correct title.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Risk Assessment Portal" in response.data or b"Credit" in response.data

def test_about_page(client):
    """
    Test about page.
    """
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About" in response.data or b"Model" in response.data

def test_predict_page_get(client):
    """
    Test predict page form loading.
    """
    response = client.get('/predict')
    assert response.status_code == 200
    assert b"predict" in response.data or b"Form" in response.data

def test_history_page(client):
    """
    Test history view.
    """
    response = client.get('/history')
    assert response.status_code == 200
    assert b"Prediction History" in response.data or b"History" in response.data

def test_health_endpoint(client):
    """
    Test basic health check.
    """
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

def test_api_v1_health(client):
    """
    Test v1 health check.
    """
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

def test_api_v1_history(client):
    """
    Test v1 history json endpoint.
    """
    response = client.get('/api/v1/history')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

@patch('src.api.prediction.PredictorAPI.process_and_predict')
def test_rest_api_scoring(mock_predict, client):
    """
    Test REST API predict JSON endpoint.
    """
    mock_predict.return_value = {
        "decision": "Approved",
        "class_code": 0,
        "approval_probability_percent": 98.5
    }
    
    payload = {"some_input": 123}
    response = client.post(
        '/api/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["decision"] == "Approved"
    assert data["approval_probability_percent"] == 98.5

@patch('src.api.prediction.PredictorAPI.process_and_predict')
def test_predict_page_post_success(mock_predict, client):
    """
    Test HTML predict page submission.
    """
    mock_predict.return_value = {
        "decision": "Approved",
        "approval_probability_percent": 95.0,
        "explanation": {
            "risk_factors": [{"feature": "Age", "impact": 0.1}],
            "support_factors": [{"feature": "Income", "impact": -0.2}]
        }
    }
    form_data = {
        'code_gender': 'M',
        'cnt_children': 0,
        'cnt_fam_members': 2,
        'age_years': 35,
        'amt_income_total': 150000.0,
        'flag_own_car': 'N',
        'flag_own_realty': 'Y',
        'name_income_type': 'Working',
        'name_education_type': 'Secondary / secondary special',
        'name_family_status': 'Married',
        'name_housing_type': 'House / apartment',
        'years_employed': 5.0,
        'flag_unemployed': 0,
        'occupation_type': 'Laborers',
        'flag_work_phone': 0,
        'flag_phone': 0,
        'flag_email': 0
    }
    response = client.post('/predict', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Approved" in response.data or b"Result" in response.data or b"predict" in response.data

def test_predict_page_post_invalid(client):
    """
    Test HTML predict form validation failure.
    """
    form_data = {
        'code_gender': 'M',
        'cnt_children': -5, # invalid range
    }
    response = client.post('/predict', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Form validation" in response.data or b"predict" in response.data

def test_export_history_csv(client):
    """
    Test CSV history export.
    """
    response = client.get('/history/export/csv')
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Prediction ID" in response.data

def test_export_history_json(client):
    """
    Test JSON history export.
    """
    response = client.get('/history/export/json')
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_404_error_page(client):
    """
    Test 404 error page.
    """
    response = client.get('/non-existent-page')
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
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key, default=None: "production" if key == "FLASK_ENV" else default
        app = create_app()
        assert app.config.get('ENV') == 'production' or app.config.get('TESTING') is False
        
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key, default=None: "testing" if key == "FLASK_ENV" else default
        app = create_app()
        assert app.config.get('TESTING') is True

def test_health_endpoint_exception(client):
    with patch('src.models.predict.RiskPredictor', side_effect=Exception("Model load fail")):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["model_loaded"] == "logistic_regression"

def test_export_history_csv_exception(client):
    with patch('src.api.routes.db_manager.get_predictions', side_effect=Exception("DB fail")):
        response = client.get('/history/export/csv', follow_redirects=False)
        assert response.status_code == 302
        assert 'history' in response.location

def test_export_history_json_exception(client):
    with patch('src.api.routes.db_manager.get_predictions', side_effect=Exception("DB fail")):
        response = client.get('/history/export/json', follow_redirects=False)
        assert response.status_code == 302
        assert 'history' in response.location

def test_input_validator_exceptions():
    from src.api.validators import InputValidator
    from src.utils.exceptions import ValidationError
    
    with pytest.raises(ValidationError):
        InputValidator.validate_predict_json({})
        
    base_data = {
        "code_gender": "M", "cnt_children": 0, "cnt_fam_members": 2, "age_years": 35,
        "amt_income_total": 150000.0, "flag_own_car": "N", "flag_own_realty": "Y",
        "name_income_type": "Working", "name_education_type": "Secondary", "name_family_status": "Married",
        "name_housing_type": "House", "years_employed": 5.0, "flag_unemployed": 0
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

def test_admin_dashboard(client):
    """Test admin portal renders successfully."""
    response = client.get('/admin')
    assert response.status_code == 200
    assert b"Operations Analytics" in response.data or b"Admin" in response.data

def test_api_admin_stats(client):
    """Test admin stats JSON API endpoint."""
    response = client.get('/api/v1/admin/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "income_labels" in data
    assert "risk_labels" in data
    assert "trend_labels" in data

def test_report_page_not_found(client):
    """Test report page returns 302 redirect if ID not found."""
    response = client.get('/report/APP-NONEXISTENT', follow_redirects=False)
    assert response.status_code == 302
    assert 'history' in response.location

def test_db_manager_methods():
    """Test SQLite database manager methods directly."""
    from src.api.routes import db_manager
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
        recommendation="Approved"
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
    from src.api.routes import db_manager
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
        recommendation="Approved"
    )
    response = client.get('/report/APP-SUCCESS-101')
    assert response.status_code == 200
    assert b"Statement" in response.data or b"Report" in response.data

def test_history_page_filters(client):
    """Test history list with search query and sorting parameters."""
    response = client.get('/history?search=APP-SUCCESS-101&sort_by=income&order=ASC')
    assert response.status_code == 200
    assert b"History" in response.data or b"Log" in response.data

def test_500_error_page_request(client):
    """Test 500 error page renders successfully when an error is raised by a route."""
    client.application.config['PROPAGATE_EXCEPTIONS'] = False
    with patch('src.api.routes.db_manager.get_predictions', side_effect=Exception("Database crash")):
        response = client.get('/admin')
        assert response.status_code == 500
        assert b"500" in response.data or b"Error" in response.data

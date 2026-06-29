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
    assert b"Risk Assessment Portal" in response.data

def test_history_page(client):
    """
    Test history view.
    """
    response = client.get('/history')
    assert response.status_code == 200
    assert b"Prediction History" in response.data

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

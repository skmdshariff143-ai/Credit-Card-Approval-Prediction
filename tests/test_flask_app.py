import json
import pytest
from unittest.mock import patch, MagicMock

@patch('flask_app.routes.model')
@patch('flask_app.routes.scaler')
@patch('flask_app.routes.encoder')
@patch('flask_app.routes.feature_names')
def test_home_page_route(mock_names, mock_enc, mock_scaler, mock_model, flask_test_client):
    """
    Test that the home page renders the form.
    """
    response = flask_test_client.get('/')
    assert response.status_code == 200
    assert b"Credit Card Application Portal" in response.data

@patch('flask_app.routes.model')
@patch('flask_app.routes.scaler')
@patch('flask_app.routes.encoder')
@patch('flask_app.routes.feature_names')
def test_about_page_route(mock_names, mock_enc, mock_scaler, mock_model, flask_test_client):
    """
    Test that the about page renders.
    """
    response = flask_test_client.get('/about')
    assert response.status_code == 200
    assert b"About CreditGuard AI" in response.data

@patch('flask_app.routes.model')
@patch('flask_app.routes.scaler')
@patch('flask_app.routes.encoder')
@patch('flask_app.routes.feature_names')
def test_api_predict_route(mock_names, mock_enc, mock_scaler, mock_model, flask_test_client):
    """
    Test that the REST API predict endpoint processes JSON input and returns predictions.
    """
    # Mock model and preprocessor behaviors
    mock_model.predict.return_value = [0] # Class 0 = Approved
    mock_model.predict_proba.return_value = [[0.85, 0.15]] # 85% class 0, 15% class 1
    mock_names.__getitem__.return_value = ['AMT_INCOME_TOTAL', 'AGE_YEARS']
    mock_scaler.transform.return_value = [[0.5, -0.2, 0.1, 0.0, 1.2, -0.5, 0.3]]
    mock_enc.transform.return_value = [[1, 0, 0, 0, 0, 1, 0, 0]]
    mock_enc.get_feature_names_out.return_value = ['cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8']
    
    # Mock data matching the API schema
    payload = {
        'CODE_GENDER': 'F',
        'FLAG_OWN_CAR': 'N',
        'FLAG_OWN_REALTY': 'Y',
        'CNT_CHILDREN': 0,
        'AMT_INCOME_TOTAL': 150000.0,
        'NAME_INCOME_TYPE': 'Working',
        'NAME_EDUCATION_TYPE': 'Higher education',
        'NAME_FAMILY_STATUS': 'Married',
        'NAME_HOUSING_TYPE': 'House / apartment',
        'DAYS_BIRTH': -12000,
        'DAYS_EMPLOYED': -2000,
        'FLAG_MOBIL': 1,
        'FLAG_WORK_PHONE': 0,
        'FLAG_PHONE': 1,
        'FLAG_EMAIL': 0,
        'OCCUPATION_TYPE': 'Core staff',
        'CNT_FAM_MEMBERS': 2.0
    }
    
    response = flask_test_client.post(
        '/api/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
    assert data['prediction'] == 'Approved'
    assert 'approval_probability_percent' in data
    assert data['approval_probability_percent'] == 85.0

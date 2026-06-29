import os
import pytest
import pandas as pd
import numpy as np
from flask_app.app import create_app

@pytest.fixture
def mock_app_df():
    """
    Fixture returning a mock application record DataFrame.
    """
    df = pd.DataFrame({
        'ID': [5008804, 5008805, 5008806],
        'CODE_GENDER': ['M', 'F', 'F'],
        'FLAG_OWN_CAR': ['Y', 'N', 'Y'],
        'FLAG_OWN_REALTY': ['Y', 'Y', 'N'],
        'CNT_CHILDREN': [0, 1, 2],
        'AMT_INCOME_TOTAL': [120000.0, 200000.0, 150000.0],
        'NAME_INCOME_TYPE': ['Working', 'Pensioner', 'State servant'],
        'NAME_EDUCATION_TYPE': ['Secondary / secondary special', 'Higher education', 'Higher education'],
        'NAME_FAMILY_STATUS': ['Married', 'Single / not married', 'Married'],
        'NAME_HOUSING_TYPE': ['House / apartment', 'House / apartment', 'With parents'],
        'DAYS_BIRTH': [-12000, -20000, -15000],
        'DAYS_EMPLOYED': [-2000, 365243, -4000],
        'FLAG_MOBIL': [1, 1, 1],
        'FLAG_WORK_PHONE': [0, 1, 0],
        'FLAG_PHONE': [1, 0, 1],
        'FLAG_EMAIL': [0, 0, 1],
        'OCCUPATION_TYPE': ['Laborers', np.nan, 'Core staff'],
        'CNT_FAM_MEMBERS': [2.0, 1.0, 4.0]
    })
    return df

@pytest.fixture
def mock_credit_df():
    """
    Fixture returning a mock credit record DataFrame.
    """
    df = pd.DataFrame({
        'ID': [5008804, 5008804, 5008805, 5008805, 5008806, 5008806],
        'MONTHS_BALANCE': [0, -1, 0, -1, 0, -1],
        'STATUS': ['C', '0', '1', '2', 'X', 'C'] # 5008805 has status '2' (late 60+ days) -> Bad (1)
    })
    return df

@pytest.fixture
def flask_test_client():
    """
    Fixture returning a Flask test client.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for unit testing simplicity
    
    with app.test_client() as client:
        yield client

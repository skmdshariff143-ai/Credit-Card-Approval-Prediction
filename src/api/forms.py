from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, FloatField, SelectField, BooleanField, SubmitField
)
from wtforms.validators import DataRequired, NumberRange, Optional

class CreditApprovalForm(FlaskForm):
    """
    Form for validating user inputs on the Flask web application.
    Matches features from the model feature store.
    """
    # Personal Info
    code_gender = SelectField(
        'Gender',
        choices=[('F', 'Female'), ('M', 'Male')],
        validators=[DataRequired()]
    )
    
    cnt_children = IntegerField(
        'Number of Children',
        validators=[NumberRange(min=0, max=20, message="Children count must be between 0 and 20.")],
        default=0
    )
    
    cnt_fam_members = IntegerField(
        'Family Size',
        validators=[NumberRange(min=1, max=25, message="Family size must be between 1 and 25.")],
        default=1
    )
    
    age_years = FloatField(
        'Age (in Years)',
        validators=[NumberRange(min=18.0, max=100.0, message="Applicant must be at least 18 years old.")],
        default=30.0
    )
    
    # Financial background
    amt_income_total = FloatField(
        'Annual Income ($)',
        validators=[NumberRange(min=1000.0, max=10000000.0, message="Income must be greater than $1,000.")],
        default=150000.0
    )
    
    flag_own_car = SelectField(
        'Owns Car',
        choices=[('N', 'No'), ('Y', 'Yes')],
        validators=[DataRequired()]
    )
    
    flag_own_realty = SelectField(
        'Owns Property',
        choices=[('Y', 'Yes'), ('N', 'No')],
        validators=[DataRequired()]
    )
    
    name_income_type = SelectField(
        'Income Type',
        choices=[
            ('Working', 'Working'),
            ('Commercial associate', 'Commercial associate'),
            ('Pensioner', 'Pensioner'),
            ('State servant', 'State servant'),
            ('Student', 'Student')
        ],
        validators=[DataRequired()]
    )
    
    name_education_type = SelectField(
        'Education Level',
        choices=[
            ('Secondary / secondary special', 'Secondary / secondary special'),
            ('Higher education', 'Higher education'),
            ('Incomplete higher', 'Incomplete higher'),
            ('Lower secondary', 'Lower secondary'),
            ('Academic degree', 'Academic degree')
        ],
        validators=[DataRequired()]
    )
    
    name_family_status = SelectField(
        'Family Status',
        choices=[
            ('Married', 'Married'),
            ('Single / not married', 'Single / not married'),
            ('Civil marriage', 'Civil marriage'),
            ('Separated', 'Separated'),
            ('Widow', 'Widow')
        ],
        validators=[DataRequired()]
    )
    
    name_housing_type = SelectField(
        'Housing Type',
        choices=[
            ('House / apartment', 'House / apartment'),
            ('With parents', 'With parents'),
            ('Municipal apartment', 'Municipal apartment'),
            ('Rented apartment', 'Rented apartment'),
            ('Office apartment', 'Office apartment'),
            ('Co-op apartment', 'Co-op apartment')
        ],
        validators=[DataRequired()]
    )
    
    # Professional Profile
    years_employed = FloatField(
        'Years of Employment',
        validators=[NumberRange(min=0.0, max=60.0, message="Years of employment must be between 0 and 60.")],
        default=5.0
    )
    
    flag_unemployed = BooleanField(
        'Is Unemployed / Retired',
        default=False
    )
    
    occupation_type = SelectField(
        'Occupation Type',
        choices=[
            ('Unknown', 'Unknown / Pensioner'),
            ('Laborers', 'Laborers'),
            ('Core staff', 'Core staff'),
            ('Sales staff', 'Sales staff'),
            ('Managers', 'Managers'),
            ('Drivers', 'Drivers'),
            ('High skill tech staff', 'High skill tech staff'),
            ('Accountants', 'Accountants'),
            ('Medicine staff', 'Medicine staff'),
            ('Cooking staff', 'Cooking staff'),
            ('Security staff', 'Security staff'),
            ('Cleaning staff', 'Cleaning staff'),
            ('Private service staff', 'Private service staff'),
            ('Low-skill Laborers', 'Low-skill Laborers'),
            ('Waiters/barmen staff', 'Waiters/barmen staff'),
            ('Secretaries', 'Secretaries'),
            ('HR staff', 'HR staff'),
            ('Realty agents', 'Realty agents'),
            ('IT staff', 'IT staff')
        ],
        validators=[Optional()]
    )
    
    # Contact flags
    flag_work_phone = BooleanField('Has Work Phone', default=False)
    flag_phone = BooleanField('Has Personal Phone', default=False)
    flag_email = BooleanField('Has Email Address', default=False)
    
    submit = SubmitField('Submit Application')

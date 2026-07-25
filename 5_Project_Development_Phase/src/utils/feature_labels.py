"""
Central Feature Label Translation Registry
Maps raw encoded column names to human-readable plain-English strings.
"""

FEATURE_LABEL_MAP = {
    # Categorical One-Hot Encodings
    "FLAG_OWN_REALTY_N": "Does Not Own Real Estate",
    "FLAG_OWN_REALTY_Y": "Owns Real Estate Property",
    "FLAG_OWN_CAR_N": "Does Not Own Vehicle",
    "FLAG_OWN_CAR_Y": "Owns Personal Vehicle",
    "CODE_GENDER_M": "Male Applicant",
    "CODE_GENDER_F": "Female Applicant",
    "NAME_INCOME_TYPE_Working": "Employed (Working Salary)",
    "NAME_INCOME_TYPE_Commercial associate": "Commercial / Business Associate",
    "NAME_INCOME_TYPE_Pensioner": "Pensioner / Retiree",
    "NAME_INCOME_TYPE_State servant": "State / Public Civil Servant",
    "NAME_INCOME_TYPE_Student": "Student Status",
    "NAME_EDUCATION_TYPE_Higher education": "Higher Education Degree",
    "NAME_EDUCATION_TYPE_Secondary / secondary special": "Secondary / Vocational Education",
    "NAME_EDUCATION_TYPE_Incomplete higher": "Incomplete Higher Education",
    "NAME_EDUCATION_TYPE_Lower secondary": "Lower Secondary Education",
    "NAME_EDUCATION_TYPE_Academic degree": "Postgraduate Academic Degree",
    "NAME_FAMILY_STATUS_Married": "Married Status",
    "NAME_FAMILY_STATUS_Single / not married": "Single / Unmarried",
    "NAME_FAMILY_STATUS_Civil marriage": "Civil Partnership",
    "NAME_FAMILY_STATUS_Separated": "Separated Status",
    "NAME_FAMILY_STATUS_Widow": "Widowed Status",
    "NAME_HOUSING_TYPE_House / apartment": "Owns/Rents House or Apartment",
    "NAME_HOUSING_TYPE_With parents": "Living With Parents",
    "NAME_HOUSING_TYPE_Municipal apartment": "Municipal Social Housing",
    "NAME_HOUSING_TYPE_Rented apartment": "Rented Private Apartment",
    "NAME_HOUSING_TYPE_Office apartment": "Employer Office Apartment",
    "NAME_HOUSING_TYPE_Co-op apartment": "Cooperative Housing Apartment",
    "OCCUPATION_TYPE_Laborers": "Laborer / Manual Worker",
    "OCCUPATION_TYPE_Core staff": "Core Technical / Professional Staff",
    "OCCUPATION_TYPE_Sales staff": "Sales Representative / Staff",
    "OCCUPATION_TYPE_Managers": "Management Executive",
    "OCCUPATION_TYPE_Drivers": "Commercial Driver",
    "OCCUPATION_TYPE_High skill tech staff": "High-Skilled Tech Specialist",
    "OCCUPATION_TYPE_Accountants": "Certified Accountant / Financial Officer",
    "OCCUPATION_TYPE_Medicine staff": "Medical / Healthcare Staff",
    "OCCUPATION_TYPE_Cooking staff": "Culinary / Food Service Staff",
    "OCCUPATION_TYPE_Security staff": "Security Guard / Officer",
    "OCCUPATION_TYPE_Cleaning staff": "Sanitation / Cleaning Staff",
    "OCCUPATION_TYPE_Private service staff": "Private Service Staff",
    "OCCUPATION_TYPE_Low-skill Laborers": "Entry-Level Manual Laborer",
    "OCCUPATION_TYPE_Secretaries": "Executive Secretary / Admin",
    "OCCUPATION_TYPE_Waiters/barmen staff": "Hospitality / Waitstaff",
    "OCCUPATION_TYPE_HR staff": "Human Resources Specialist",
    "OCCUPATION_TYPE_IT staff": "Information Technology Specialist",
    "OCCUPATION_TYPE_Realty agents": "Real Estate Agent / Broker",
    "OCCUPATION_TYPE_Missing": "Unspecified / Missing Occupation",

    # Continuous & Engineered Features
    "AMT_INCOME_TOTAL": "Total Annual Income ($)",
    "CNT_CHILDREN": "Number of Dependent Children",
    "CNT_FAM_MEMBERS": "Total Household Family Members",
    "AGE_YEARS": "Applicant Age (Years)",
    "YEARS_EMPLOYED": "Employment Duration (Years)",
    "INCOME_PER_MEMBER": "Per Capita Household Income ($)",
    "EMPLOYED_TO_AGE_RATIO": "Career Stability Ratio",
    "FINANCIAL_STABILITY_SCORE": "Financial Stability Score",
    "FLAG_PHONE": "Telephone Contact Provided",
    "FLAG_WORK_PHONE": "Work Phone Provided",
    "FLAG_EMAIL": "Email Address Provided",
    "FLAG_UNEMPLOYED": "Unemployment Flag",
    "INCOME_GROUP_low": "Low Income Bracket",
    "INCOME_GROUP_medium": "Medium Income Bracket",
    "INCOME_GROUP_high": "High Income Bracket",
    "INCOME_GROUP_very_high": "Very High Income Bracket",
    "AGE_GROUP_young": "Young Adult (<30 yrs)",
    "AGE_GROUP_middle_aged": "Middle Age (30-50 yrs)",
    "AGE_GROUP_senior": "Senior (>50 yrs)",
    "EXPERIENCE_BUCKET_entry": "Entry-Level History (<3 yrs)",
    "EXPERIENCE_BUCKET_mid": "Mid-Level History (3-10 yrs)",
    "EXPERIENCE_BUCKET_senior": "Senior History (>10 yrs)",
}


def get_feature_label(raw_feature: str) -> str:
    """Returns human-readable plain English label for a raw feature name."""
    if raw_feature in FEATURE_LABEL_MAP:
        return FEATURE_LABEL_MAP[raw_feature]
    cleaned = raw_feature.replace("_", " ").title()
    return cleaned

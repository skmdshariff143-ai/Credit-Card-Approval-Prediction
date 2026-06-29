# Central Constants configuration

# Random State
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Dataset Columns definition
ID_COL = "ID"
TARGET_COL = "STATUS_TARGET"

NUMERICAL_COLS = [
    "AMT_INCOME_TOTAL",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS"
]

CATEGORICAL_COLS = [
    "CODE_GENDER",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE"
]

BINARY_COLS = [
    "FLAG_MOBIL",
    "FLAG_WORK_PHONE",
    "FLAG_PHONE",
    "FLAG_EMAIL"
]

# Engineered numerical fields
ENGINEERED_NUMERICAL_COLS = [
    "AMT_INCOME_TOTAL",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",
    "AGE_YEARS",
    "YEARS_EMPLOYED",
    "INCOME_PER_MEMBER",
    "EMPLOYED_TO_AGE_RATIO"
]

# Credit delinquency labels
# Target definition: late by 60+ days -> Rejected (Class 1)
# STATUS in ['2', '3', '4', '5']
DELINQUENT_STATUSES = {'2', '3', '4', '5'}

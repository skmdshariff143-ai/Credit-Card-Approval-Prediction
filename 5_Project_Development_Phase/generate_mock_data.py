"""
⚠️ NOTICE: TEST & CI FIXTURE GENERATOR ONLY ⚠️

This script generates synthetic mock datasets (5,000 lightweight records) EXCLUSIVELY for:
1. Fast local unit test execution (`pytest`).
2. Continuous Integration (CI/CD) automated testing pipelines.

DO NOT USE THIS SCRIPT OR ITS OUTPUT TO TRAIN PRODUCTION MACHINE LEARNING MODELS.
The canonical production models in `models/` are trained on the official Kaggle dataset
(application_record.csv ~438,557 rows, credit_record.csv ~1,048,575 rows).
"""

import os

import numpy as np
import pandas as pd


def generate_data(num_applicants=5000, seed=42):
    np.random.seed(seed)
    print("Generating synthetic Credit Card Approval Prediction dataset (FIXTURES ONLY)...")

    # 1. Generate Application Records
    # IDs starting from 5008804 (matching Kaggle range)
    ids = np.arange(5008804, 5008804 + num_applicants)

    genders = np.random.choice(["M", "F"], size=num_applicants, p=[0.35, 0.65])
    own_car = np.random.choice(["Y", "N"], size=num_applicants, p=[0.4, 0.6])
    own_realty = np.random.choice(["Y", "N"], size=num_applicants, p=[0.7, 0.3])

    # Children count (mostly 0, 1, 2, occasionally 3+)
    children = np.random.choice([0, 1, 2, 3, 4], size=num_applicants, p=[0.70, 0.20, 0.08, 0.015, 0.005])

    # Income (log-normal distribution to be realistic)
    income_base = np.random.lognormal(mean=12.0, sigma=0.5, size=num_applicants)
    income = np.round(income_base * 1.5, -2)  # Round to nearest 100

    income_types = np.random.choice(
        ["Working", "Commercial associate", "Pensioner", "State servant", "Student"],
        size=num_applicants,
        p=[0.53, 0.23, 0.17, 0.068, 0.002],
    )

    education_types = np.random.choice(
        [
            "Secondary / secondary special",
            "Higher education",
            "Incomplete higher",
            "Lower secondary",
            "Academic degree",
        ],
        size=num_applicants,
        p=[0.71, 0.25, 0.03, 0.009, 0.001],
    )

    family_statuses = np.random.choice(
        ["Married", "Single / not married", "Civil marriage", "Separated", "Widow"],
        size=num_applicants,
        p=[0.69, 0.13, 0.08, 0.06, 0.04],
    )

    housing_types = np.random.choice(
        [
            "House / apartment",
            "With parents",
            "Municipal apartment",
            "Rented apartment",
            "Office apartment",
            "Co-op apartment",
        ],
        size=num_applicants,
        p=[0.89, 0.04, 0.03, 0.02, 0.015, 0.005],
    )

    # Days birth (negative values, age between 20 and 70)
    age_years = np.random.uniform(20, 70, size=num_applicants)
    days_birth = -np.round(age_years * 365.25).astype(int)

    # Days employed (negative values, or 365243 for pensioners/unemployed)
    days_employed = []
    for i in range(num_applicants):
        inc_type = income_types[i]
        if inc_type == "Pensioner" or np.random.rand() < 0.02:
            days_employed.append(365243)
        else:
            # Empl length between 0 and 40 years, capped at age-18
            max_empl = age_years[i] - 18
            empl_years = np.random.uniform(0, max(max_empl, 1))
            days_employed.append(-int(np.round(empl_years * 365.25)))
    days_employed = np.array(days_employed)

    # Flags
    flag_mobil = np.ones(num_applicants, dtype=int)  # Always 1 in dataset
    flag_work_phone = np.random.choice([0, 1], size=num_applicants, p=[0.78, 0.22])
    flag_phone = np.random.choice([0, 1], size=num_applicants, p=[0.71, 0.29])
    flag_email = np.random.choice([0, 1], size=num_applicants, p=[0.91, 0.09])

    # Occupation type (includes missing values represented as NaN)
    occupations = [
        "Laborers",
        "Core staff",
        "Sales staff",
        "Managers",
        "Drivers",
        "High skill tech staff",
        "Accountants",
        "Medicine staff",
        "Cooking staff",
        "Security staff",
        "Cleaning staff",
        "Private service staff",
        "Low-skill Laborers",
        "Waiters/barmen staff",
        "Secretaries",
        "HR staff",
        "Realty agents",
        "IT staff",
    ]
    occupation_probs = [
        0.28,
        0.15,
        0.14,
        0.12,
        0.08,
        0.05,
        0.04,
        0.04,
        0.02,
        0.02,
        0.015,
        0.015,
        0.01,
        0.005,
        0.005,
        0.004,
        0.003,
        0.003,
    ]

    occupation_type = []
    for i in range(num_applicants):
        if days_employed[i] == 365243:
            occupation_type.append(np.nan)
        else:
            if np.random.rand() < 0.30:  # 30% missing values
                occupation_type.append(np.nan)
            else:
                occupation_type.append(np.random.choice(occupations, p=occupation_probs))

    # Family members (usually children + spouse + self)
    cnt_fam_members = []
    for i in range(num_applicants):
        status = family_statuses[i]
        child_cnt = children[i]
        if status in ["Married", "Civil marriage"]:
            cnt_fam_members.append(float(child_cnt + 2))
        else:
            cnt_fam_members.append(float(child_cnt + 1))
    cnt_fam_members = np.array(cnt_fam_members)

    app_df = pd.DataFrame(
        {
            "ID": ids,
            "CODE_GENDER": genders,
            "FLAG_OWN_CAR": own_car,
            "FLAG_OWN_REALTY": own_realty,
            "CNT_CHILDREN": children,
            "AMT_INCOME_TOTAL": income,
            "NAME_INCOME_TYPE": income_types,
            "NAME_EDUCATION_TYPE": education_types,
            "NAME_FAMILY_STATUS": family_statuses,
            "NAME_HOUSING_TYPE": housing_types,
            "DAYS_BIRTH": days_birth,
            "DAYS_EMPLOYED": days_employed,
            "FLAG_MOBIL": flag_mobil,
            "FLAG_WORK_PHONE": flag_work_phone,
            "FLAG_PHONE": flag_phone,
            "FLAG_EMAIL": flag_email,
            "OCCUPATION_TYPE": occupation_type,
            "CNT_FAM_MEMBERS": cnt_fam_members,
        }
    )

    # 2. Generate Credit Records
    # For each applicant, generate a history of months (between 5 and 60 months)
    credit_records = []

    # Define a risk score for each applicant to make the label correlated with features
    for idx, row in app_df.iterrows():
        app_id = row["ID"]
        # Risk factors
        risk_score = 0.0

        # Unemployed/Pensioners have slightly higher risk or lower depending on income
        if row["DAYS_EMPLOYED"] == 365243:
            risk_score += 0.15

        # Lower income -> higher risk
        if row["AMT_INCOME_TOTAL"] < 100000:
            risk_score += 0.25
        elif row["AMT_INCOME_TOTAL"] > 250000:
            risk_score -= 0.15

        # More children -> higher risk
        risk_score += 0.05 * row["CNT_CHILDREN"]

        # Education -> higher education has lower risk
        if row["NAME_EDUCATION_TYPE"] == "Higher education":
            risk_score -= 0.1
        elif row["NAME_EDUCATION_TYPE"] == "Lower secondary":
            risk_score += 0.2

        # Gender factor (empirical pattern: males slightly higher default rate in some sets)
        if row["CODE_GENDER"] == "M":
            risk_score += 0.05

        # Limit risk score between 0.05 and 0.8
        risk_prob = np.clip(0.05 + risk_score, 0.02, 0.85)

        # Number of months of credit history
        num_months = np.random.randint(5, 61)
        months_balance = np.arange(-num_months + 1, 1)

        # Determine if this applicant will ever default
        is_defaulter = np.random.rand() < risk_prob

        # Status distribution:
        # C: paid off
        # X: no loan
        # 0: 1-29 days past due
        # 1: 30-59 days past due
        # 2: 60-89 days past due
        # 3: 90-119 days past due
        # 4: 120-149 days past due
        # 5: 150+ days past due

        for m in months_balance:
            if is_defaulter:
                # If defaulter, higher chance of late payment statuses
                status = np.random.choice(
                    ["C", "X", "0", "1", "2", "3", "4", "5"], p=[0.25, 0.05, 0.40, 0.15, 0.08, 0.04, 0.02, 0.01]
                )
            else:
                # If non-defaulter, mostly C, X, 0, occasionally 1 (under 60 days)
                status = np.random.choice(["C", "X", "0", "1"], p=[0.45, 0.10, 0.42, 0.03])
            credit_records.append({"ID": app_id, "MONTHS_BALANCE": m, "STATUS": status})

    credit_df = pd.DataFrame(credit_records)

    # Save files to data/raw/
    raw_dir = "e:\\Credit-Card-Approval-Prediction\\data\\raw"
    os.makedirs(raw_dir, exist_ok=True)

    app_df.to_csv(os.path.join(raw_dir, "application_record.csv"), index=False)
    credit_df.to_csv(os.path.join(raw_dir, "credit_record.csv"), index=False)

    print(f"Saved application_record.csv with shape: {app_df.shape}")
    print(f"Saved credit_record.csv with shape: {credit_df.shape}")


if __name__ == "__main__":
    generate_data()

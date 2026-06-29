from setuptools import setup, find_packages

setup(
    name="credit_card_approval_prediction",
    version="1.0.0",
    description="An end-to-end machine learning project to predict credit card application approval.",
    author="Mahammad Shariff Shaik",
    author_email="sk.md.shariff143@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "xgboost",
        "flask",
        "joblib",
        "python-dotenv",
        "pyyaml",
        "pytest",
        "wtforms",
        "flask-wtf"
    ],
    python_requires=">=3.10",
)

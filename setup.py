from setuptools import setup, find_packages

setup(
    name="credit_card_approval_prediction",
    version="1.0.0",
    description="Enterprise Machine Learning project for predicting credit card approval status.",
    author="Mahammad Shariff Shaik",
    author_email="sk.md.shariff143@gmail.com",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "xgboost>=2.0.0",
        "joblib>=1.3.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "requests>=2.31.0",
        "scipy>=1.11.0",
        "imbalanced-learn>=0.11.0"
    ],
    python_requires=">=3.10",
)

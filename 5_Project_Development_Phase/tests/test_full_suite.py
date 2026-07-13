import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# Mock ibm_watson_machine_learning module before importing components that import it
mock_wml = MagicMock()
sys.modules["ibm_watson_machine_learning"] = mock_wml

# Import components to test
from config.config import config  # noqa: E402
from config.constants import TARGET_COL  # noqa: E402
from app.database.history import HistoryManager  # noqa: E402
from app.routes.validators import InputValidator  # noqa: E402
from src.data.data_split import perform_stratified_split  # noqa: E402
from src.data.dataset_info import DatasetMetadataGenerator  # noqa: E402
from src.data.load_data import DataLoader  # noqa: E402
from src.data.validate_data import DataValidator  # noqa: E402
from src.deployment.deploy import run_ibm_deployment  # noqa: E402
from src.deployment.ibm_cloud import IBMCloudManager  # noqa: E402
from src.features.feature_engineering import FeatureEngineer as FeatureEngineerModule  # noqa: E402
from src.features.feature_selection import FeatureSelector  # noqa: E402
from src.models.compare_models import ModelComparator  # noqa: E402
from src.models.evaluate import ModelEvaluator  # noqa: E402
from src.models.hyperparameter_tuning import HyperparameterTuner  # noqa: E402
from src.models.metrics import calculate_all_metrics  # noqa: E402
from src.models.model_registry import ModelRegistry  # noqa: E402
from src.models.train import ModelTrainer  # noqa: E402
from src.preprocessing.duplicates import DuplicateHandler  # noqa: E402
from src.preprocessing.encoding import CategoricalEncoder  # noqa: E402
from src.preprocessing.feature_engineering import FeatureEngineer as PreprocessFeatureEngineer  # noqa: E402
from src.preprocessing.pipeline import PreprocessingPipeline  # noqa: E402
from src.preprocessing.scaling import NumericalScaler  # noqa: E402
from src.utils.exceptions import (  # noqa: E402
    DataLoadingError,
)
from app.utils.helper import load_json, load_pkl, save_json, save_pkl  # noqa: E402
from app.utils.tracker import ExperimentTracker  # noqa: E402
from src.visualization.eda import calculate_missing_matrix, generate_summary_stats  # noqa: E402
from src.visualization.plots import VizPlotter  # noqa: E402


@pytest.fixture
def mock_app_df():
    return pd.DataFrame(
        {
            "ID": [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010],
            "CODE_GENDER": ["M", "F", "M", "F", "F", "M", "F", "M", "F", "M"],
            "FLAG_OWN_CAR": ["Y", "N", "N", "Y", "N", "Y", "Y", "N", "N", "Y"],
            "FLAG_OWN_REALTY": ["Y", "Y", "N", "N", "Y", "N", "Y", "Y", "N", "N"],
            "CNT_CHILDREN": [0, 1, 2, -1, 0, 1, 0, 3, 2, 0],
            "AMT_INCOME_TOTAL": [
                120000.0,
                90000.0,
                300000.0,
                -150000.0,
                200000.0,
                180000.0,
                150000.0,
                250000.0,
                350000.0,
                110000.0,
            ],
            "NAME_INCOME_TYPE": [
                "Working",
                "Commercial associate",
                "Pensioner",
                "Working",
                "State servant",
                "Working",
                "Commercial associate",
                "Pensioner",
                "Working",
                "Working",
            ],
            "NAME_EDUCATION_TYPE": [
                "Secondary / secondary special",
                "Higher education",
                "Incomplete higher",
                "Secondary / secondary special",
                "Higher education",
                "Secondary / secondary special",
                "Higher education",
                "Secondary / secondary special",
                "Higher education",
                "Secondary / secondary special",
            ],
            "NAME_FAMILY_STATUS": [
                "Married",
                "Single / not married",
                "Civil marriage",
                "Married",
                "Single / not married",
                "Married",
                "Single / not married",
                "Civil marriage",
                "Married",
                "Single / not married",
            ],
            "NAME_HOUSING_TYPE": [
                "House / apartment",
                "House / apartment",
                "Rented apartment",
                "House / apartment",
                "House / apartment",
                "House / apartment",
                "House / apartment",
                "Rented apartment",
                "House / apartment",
                "House / apartment",
            ],
            "DAYS_BIRTH": [-12000, -15000, -20000, -10000, -18000, -11000, -16000, -19000, -12000, -14000],
            "DAYS_EMPLOYED": [-1200, -3000, 365243, -500, -1000, -1500, -200, 365243, -400, -1800],
            "FLAG_MOBIL": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "FLAG_WORK_PHONE": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            "FLAG_PHONE": [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            "FLAG_EMAIL": [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            "OCCUPATION_TYPE": [
                "Laborers",
                np.nan,
                np.nan,
                "Core staff",
                "Accountants",
                "Laborers",
                np.nan,
                np.nan,
                "Core staff",
                "Laborers",
            ],
            "CNT_FAM_MEMBERS": [2, 1, 3, 1, 2, 3, 1, 4, 3, 2],
        }
    )


@pytest.fixture
def mock_credit_df():
    return pd.DataFrame(
        {
            "ID": [10001, 10001, 10002, 10003, 10004, 10005, 10005, 10006, 10007, 10008, 10009, 10010],
            "MONTHS_BALANCE": [0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            "STATUS": ["0", "1", "C", "5", "X", "2", "0", "0", "0", "0", "0", "0"],
        }
    )


# --- DATA SECTION TESTS ---


def test_data_loader_errors():
    loader = DataLoader()
    loader.app_path = "non_existent_app.csv"
    loader.credit_path = "non_existent_credit.csv"

    with pytest.raises(DataLoadingError):
        loader.load_application_records()

    with pytest.raises(DataLoadingError):
        loader.load_credit_records()


@patch("pandas.read_csv")
def test_data_loader_success(mock_read_csv, mock_app_df, mock_credit_df):
    mock_read_csv.side_effect = [mock_app_df, mock_credit_df]
    loader = DataLoader()
    app, credit = loader.load_all()
    assert app.shape[0] == 10
    assert credit.shape[0] == 12


def test_data_validator(mock_app_df, mock_credit_df, tmp_path):
    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }
    # Mock config paths
    with patch.object(config, "get_paths", return_value=mock_paths):
        validator = DataValidator()
        res = validator.validate_dataset(mock_app_df, mock_credit_df)
        assert res is True
        assert os.path.exists(os.path.join(tmp_path, "Validation_Report.md"))


def test_dataset_metadata_generator(mock_app_df, mock_credit_df, tmp_path):
    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }
    with patch.object(config, "get_paths", return_value=mock_paths):
        gen = DatasetMetadataGenerator()
        with patch.object(gen.loader, "load_all", return_value=(mock_app_df, mock_credit_df)):
            with patch.object(gen.loader, "load_application_records", return_value=mock_app_df):
                with patch.object(gen.loader, "load_credit_records", return_value=mock_credit_df):
                    meta = gen.generate_and_save_metadata()
                    assert "application_records" in meta
                    assert os.path.exists(os.path.join(tmp_path, "dataset_metadata.json"))


def test_data_split(mock_app_df):
    # Add target column
    mock_app_df[TARGET_COL] = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    X_train, X_test, y_train, y_test = perform_stratified_split(mock_app_df)
    assert len(X_train) == 8
    assert len(X_test) == 2


# --- PREPROCESSING SECTION TESTS ---


def test_preprocessing_pipeline_end_to_end(mock_app_df, mock_credit_df, tmp_path):
    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }
    # Path configuration
    with patch.object(config, "get_paths", return_value=mock_paths):
        pipeline = PreprocessingPipeline()
        # Mock load raw on DataLoader class to avoid MagicMock pickling issues on pipeline instance
        with patch("src.preprocessing.pipeline.DataLoader.load_all", return_value=(mock_app_df, mock_credit_df)):
            # Execute pipeline
            train_shape, test_shape = pipeline.execute_full_pipeline()

            # Assert splits saved
            assert os.path.exists(os.path.join(tmp_path, "X_train.csv"))
            assert os.path.exists(os.path.join(tmp_path, "y_train.csv"))
            assert os.path.exists(os.path.join(tmp_path, "X_test.csv"))
            assert os.path.exists(os.path.join(tmp_path, "y_test.csv"))

            # Test inference transformation
            raw_single = mock_app_df.iloc[[0]].copy()
            trans_single = pipeline.transform(raw_single)
            assert trans_single.shape[0] == 1
            assert len(trans_single.columns) == len(pipeline.feature_names)


def test_categorical_encoder():
    encoder = CategoricalEncoder()
    df = pd.DataFrame({"cat": ["A", "B", "A", np.nan]})
    encoder.fit(df, ["cat"])
    encoded = encoder.transform(df)
    assert "cat_A" in encoded.columns
    assert "cat_B" in encoded.columns


def test_numerical_scaler():
    scaler = NumericalScaler()
    df = pd.DataFrame({"num": [10.0, 20.0, 30.0]})
    scaler.fit(df, ["num"])
    scaled = scaler.transform(df)
    assert pytest.approx(scaled["num"].mean(), abs=1e-5) == 0.0


def test_preprocess_feature_engineer(mock_app_df):
    engineer = PreprocessFeatureEngineer()
    res = engineer.transform(mock_app_df)
    assert "AGE_YEARS" in res.columns
    assert "YEARS_EMPLOYED" in res.columns
    assert "INCOME_PER_MEMBER" in res.columns
    assert "FINANCIAL_STABILITY_SCORE" in res.columns


def test_feature_selector(mock_app_df, tmp_path):
    mock_app_df[TARGET_COL] = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }
    with patch.object(config, "get_paths", return_value=mock_paths):
        selector = FeatureSelector()
        features = ["DAYS_BIRTH", "DAYS_EMPLOYED"]
        selector.fit_selection(mock_app_df[features], mock_app_df[TARGET_COL])
        selected = selector.transform(mock_app_df[features])
        assert len(selected.columns) > 0
        assert os.path.exists(os.path.join(tmp_path, "Feature_Selection_Ranking.csv"))


# --- MODELS SECTION TESTS ---


def test_model_trainer():
    trainer = ModelTrainer()
    # Baseline checks
    baselines = trainer.get_baseline_models()
    assert "logistic_regression" in baselines

    # Train and time
    X = pd.DataFrame({"feat1": [1.0, 2.0, 3.0, 4.0], "feat2": [2.0, 1.0, 4.0, 3.0]})
    y = pd.Series([0, 1, 0, 1])
    model, t = trainer.train_and_time_model("logistic_regression", baselines["logistic_regression"], X, y)
    assert t > 0

    # Measure inference speed
    y_pred, y_prob, inf_t = trainer.measure_inference_speed(model, X)
    assert len(y_pred) == 4
    assert inf_t > 0


def test_model_comparator(tmp_path):
    mock_paths = {
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
    }
    with patch.object(config, "get_paths", return_value=mock_paths):
        comp = ModelComparator()
        metrics = {"Accuracy": 0.8, "Precision": 0.7, "Recall": 0.9, "F1-Score": 0.79, "ROC-AUC": 0.85, "Log_Loss": 0.3}
        comp.add_model_metrics("test_model", metrics, 1.2, 0.05)
        df = comp.compare_and_rank()
        assert df.shape[0] == 1
        assert df.loc[0, "Model"] == "test_model"


def test_hyperparameter_tuner():
    tuner = HyperparameterTuner(cv=2)
    trainer = ModelTrainer()
    baselines = trainer.get_baseline_models()
    X = pd.DataFrame({"feat1": [1.0, 2.0, 3.0, 4.0], "feat2": [2.0, 1.0, 4.0, 3.0]})
    y = pd.Series([0, 1, 0, 1])

    tuned = tuner.tune("logistic_regression", baselines["logistic_regression"], X, y)
    assert tuned is not None


def test_model_registry(tmp_path):
    with patch.object(config, "get_paths", return_value={"models_dir": str(tmp_path)}):
        reg = ModelRegistry()
        X = pd.DataFrame({"feat1": [1.0, 2.0, 3.0, 4.0]})
        y = pd.Series([0, 1, 0, 1])
        trainer = ModelTrainer()
        model, _ = trainer.train_and_time_model(
            "logistic_regression", trainer.get_baseline_models()["logistic_regression"], X, y
        )

        reg.register_model("logistic_regression", model, {"C": 1.0}, {"F1": 0.8})
        assert os.path.exists(os.path.join(tmp_path, "trained", "logistic_regression.pkl"))
        assert os.path.exists(os.path.join(tmp_path, "trained", "logistic_regression_metadata.json"))


# --- UTILS SECTION TESTS ---


def test_experiment_tracker(tmp_path):
    with patch.object(config, "get_paths", return_value={"logs_dir": str(tmp_path)}):
        tracker = ExperimentTracker()
        tracker.log_run("log_reg", {"C": 1.0}, {"F1": 0.75})
        runs = tracker.get_runs()
        assert len(runs) == 1
        assert runs[0]["model_name"] == "log_reg"


def test_helpers(tmp_path):
    test_file = os.path.join(tmp_path, "test.pkl")
    data = {"test": 123}
    save_pkl(data, test_file)
    loaded = load_pkl(test_file)
    assert loaded["test"] == 123

    json_file = os.path.join(tmp_path, "test.json")
    save_json(data, json_file)
    loaded_json = load_json(json_file)
    assert loaded_json["test"] == 123


# --- VISUALIZATION SECTION TESTS ---


@patch("matplotlib.pyplot.savefig")
def test_eda_visualizer(mock_savefig, mock_app_df):
    vis = VizPlotter()
    vis.plot_distribution(mock_app_df, "AMT_INCOME_TOTAL", "test_dist.png")
    vis.plot_target_balance(mock_app_df["CNT_CHILDREN"], "test_balance.png")
    assert mock_savefig.called


def test_eda_summary(mock_app_df):
    summary = generate_summary_stats(mock_app_df)
    assert summary is not None
    missing = calculate_missing_matrix(mock_app_df)
    assert missing is not None


# --- DEPLOYMENT SECTION TESTS ---


@patch("requests.post")
def test_ibm_cloud_manager(mock_post):
    manager = IBMCloudManager()
    manager.api_key = "mock_key"
    manager.scoring_url = "mock_url"

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "mock_token", "predictions": [{"values": [[0]]}]}

    token = manager.get_iam_token()
    assert token == "mock_token"


@patch("src.deployment.deploy.APIClient")
def test_run_ibm_deployment(mock_client, tmp_path):
    with patch.object(config, "get_paths", return_value={"models_dir": str(tmp_path)}):
        # Create a mock file
        model_file = os.path.join(tmp_path, "trained_model.pkl")
        with open(model_file, "wb") as f:
            f.write(b"mock_data")

        with patch.object(config, "IBM_API_KEY", "mock_key"):
            with patch.object(config, "IBM_SPACE_ID", "mock_space"):
                run_ibm_deployment()
                assert mock_client.called


# --- API SECTION TESTS ---


def test_history_manager(tmp_path):
    with patch.object(config, "get_paths", return_value={"processed_dir": str(tmp_path)}):
        mgr = HistoryManager()
        payload = {"gender": "M", "income": 100000}
        mgr.add_entry(payload, "Approved", 95.0)
        logs = mgr.get_history()
        assert len(logs) == 1
        assert logs[0]["decision"] == "Approved"


def test_input_validator():
    # Valid data
    valid_data = {
        "code_gender": "M",
        "cnt_children": 0,
        "cnt_fam_members": 2,
        "age_years": 35,
        "amt_income_total": 150000.0,
        "flag_own_car": "N",
        "flag_own_realty": "Y",
        "name_income_type": "Working",
        "name_education_type": "Secondary / secondary special",
        "name_family_status": "Married",
        "name_housing_type": "House / apartment",
        "years_employed": 5.0,
        "flag_unemployed": 0,
        "occupation_type": "Laborers",
        "flag_work_phone": 0,
        "flag_phone": 0,
        "flag_email": 0,
    }

    # Check returns True
    assert InputValidator.validate_predict_json(valid_data) is True

    # Invalid data
    invalid_data = valid_data.copy()
    invalid_data["age_years"] = 10
    from app.utils.exceptions import ValidationError as AppValidationError

    with pytest.raises(AppValidationError):
        InputValidator.validate_predict_json(invalid_data)


def test_classification_metrics():
    from app.utils.metrics import calculate_classification_metrics

    y_true = [0, 1, 0, 1]
    y_pred = [0, 1, 1, 1]
    y_prob = [0.1, 0.9, 0.8, 0.7]
    metrics = calculate_classification_metrics(y_true, y_pred, y_prob)
    assert "Accuracy" in metrics
    assert "ROC-AUC" in metrics


def test_drift_validator():
    from src.data.validation import DataValidator as DriftValidator

    dv = DriftValidator()
    df = pd.DataFrame(
        {
            "code_gender": ["M", "F"],
            "cnt_children": [0, 1],
            "cnt_fam_members": [1.0, 2.0],
            "age_years": [30.0, 40.0],
            "amt_income_total": [100000.0, 120000.0],
            "flag_own_car": ["N", "Y"],
            "flag_own_realty": ["Y", "N"],
            "name_income_type": ["Working", "Pensioner"],
            "name_education_type": ["Secondary", "Higher"],
            "name_family_status": ["Married", "Single"],
            "name_housing_type": ["House", "House"],
            "years_employed": [2.0, 5.0],
            "flag_unemployed": [0, 0],
        }
    )
    assert dv.validate_schema(df) is True

    ref = pd.Series([1, 2, 3, 4, 5])
    tgt = pd.Series([1.1, 2.1, 3.1, 4.1, 5.1])
    psi = dv.calculate_drift_psi(ref, tgt)
    assert psi >= 0.0


def test_feature_engineer_features(mock_app_df):

    engineer = FeatureEngineerModule()
    res = engineer.extract_custom_features(mock_app_df)
    assert "AGE_YEARS" in res.columns
    assert "YEARS_EMPLOYED" in res.columns
    assert "INCOME_PER_MEMBER" in res.columns
    assert "EMPLOYED_TO_AGE_RATIO" in res.columns


@patch("matplotlib.pyplot.savefig")
@patch("src.main.cross_val_score")
def test_main_pipeline_run(mock_cv_score, mock_savefig, tmp_path):
    from sklearn.linear_model import LogisticRegression

    from src.main import run_model_pipeline

    mock_cv_score.return_value = np.array([0.8, 0.82, 0.81, 0.83, 0.82])

    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }

    # Write dummy processed split files
    X_train = pd.DataFrame({"feat1": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})
    y_train = pd.DataFrame({TARGET_COL: [0, 0, 1, 1, 0, 0, 0, 1, 0, 0]})
    X_test = pd.DataFrame({"feat1": [1.5, 2.5, 3.5, 4.5]})
    y_test = pd.DataFrame({TARGET_COL: [0, 0, 1, 1]})

    X_train.to_csv(os.path.join(tmp_path, "X_train.csv"), index=False)
    y_train.to_csv(os.path.join(tmp_path, "y_train.csv"), index=False)
    X_test.to_csv(os.path.join(tmp_path, "X_test.csv"), index=False)
    y_test.to_csv(os.path.join(tmp_path, "y_test.csv"), index=False)

    with patch.object(config, "get_paths", return_value=mock_paths):
        with patch(
            "src.main.ModelTrainer.get_baseline_models", return_value={"logistic_regression": LogisticRegression()}
        ):
            with patch("src.main.HyperparameterTuner.tune", side_effect=lambda name, model, X, y: model.fit(X, y)):
                best_name = run_model_pipeline()
                assert best_name == "logistic_regression"
                assert os.path.exists(os.path.join(tmp_path, "best_model.pkl"))
                assert os.path.exists(os.path.join(tmp_path, "Model_Report.md"))


def test_explanation_engine():
    from sklearn.linear_model import LogisticRegression

    from app.services.explainability import ExplanationEngine

    # Mock preprocessor/pipeline
    mock_pipeline = MagicMock()
    mock_pipeline.transform.return_value = np.array([[0.5, 0.2]])
    mock_pipeline.get_feature_names_out.return_value = ["num__feat1", "num__feat2"]

    # Mock model
    mock_model = LogisticRegression()
    mock_model.coef_ = np.array([[1.5, -2.0]])
    mock_model.intercept_ = np.array([0.1])

    engine = ExplanationEngine(mock_model, mock_pipeline)
    res = engine.explain_instance(pd.DataFrame([{"feat1": 1}]))

    assert "intercept" in res
    assert "risk_factors" in res
    assert len(res["risk_factors"]) > 0
    assert len(res["support_factors"]) > 0


def test_explanation_engine_surrogate():
    from app.services.explainability import ExplanationEngine

    # Mock preprocessor/pipeline
    mock_pipeline = MagicMock()
    mock_pipeline.transform.return_value = np.array([[0.5, 0.2]])
    mock_pipeline.get_feature_names_out.return_value = ["num__feat1", "num__feat2"]

    # Mock model without coef_ (triggers surrogate paths)
    mock_model = MagicMock()
    # It must return shape (50, 2) on predict_proba
    mock_model.predict_proba.return_value = np.array([[0.7, 0.3]] * 50)
    # Remove coef_ attribute if MagicMock auto-creates it
    if hasattr(mock_model, "coef_"):
        del mock_model.coef_

    engine = ExplanationEngine(mock_model, mock_pipeline)
    res = engine.explain_instance(pd.DataFrame([{"feat1": 1}]))

    assert "intercept" in res
    assert "risk_factors" in res
    assert len(res["risk_factors"]) > 0 or len(res["support_factors"]) > 0


@patch("app.services.predict.load_pkl")
@patch("os.path.exists")
def test_predictor_api(mock_exists, mock_load):
    from app.services.prediction import PredictorAPI

    mock_exists.return_value = True

    mock_pipeline = MagicMock()
    mock_pipeline.transform.return_value = pd.DataFrame([[0.5, 1.2]], columns=["feat_1", "feat_2"])
    mock_pipeline.feature_names = ["feat_1", "feat_2"]

    mock_clf = MagicMock()
    mock_clf.predict.return_value = [0]
    mock_clf.predict_proba.return_value = [[0.95, 0.05]]

    mock_load.side_effect = [mock_pipeline, mock_clf]

    api = PredictorAPI()
    form_data = {
        "code_gender": "M",
        "cnt_children": 0,
        "cnt_fam_members": 2,
        "age_years": 35,
        "amt_income_total": 150000.0,
        "flag_own_car": "N",
        "flag_own_realty": "Y",
        "name_income_type": "Working",
        "name_education_type": "Secondary",
        "name_family_status": "Married",
        "name_housing_type": "House",
        "years_employed": 5.0,
        "flag_unemployed": 0,
        "occupation_type": "Laborers",
        "flag_work_phone": 0,
        "flag_phone": 0,
        "flag_email": 0,
    }

    with patch("app.database.history.HistoryManager.add_entry") as mock_add_entry:
        res = api.process_and_predict(form_data)
        assert res["decision"] == "Approved"
        assert mock_add_entry.called


@patch("matplotlib.pyplot.savefig")
def test_viz_plotter_all_methods(mock_savefig, tmp_path, mock_app_df):
    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }
    with patch.object(config, "get_paths", return_value=mock_paths):
        plotter = VizPlotter()
        plotter.plot_distribution(mock_app_df, "AMT_INCOME_TOTAL", "dist.png")
        plotter.plot_target_balance(mock_app_df["CNT_CHILDREN"], "balance.png")
        plotter.plot_correlation_heatmap(mock_app_df, "corr.png")
        plotter.plot_categorical_vs_target(mock_app_df, "CODE_GENDER", TARGET_COL, "cat_vs_tgt.png")
        plotter.plot_numeric_vs_target_box(mock_app_df, "AMT_INCOME_TOTAL", TARGET_COL, "num_vs_tgt.png")
        plotter.plot_outliers_boxplot(mock_app_df, "AMT_INCOME_TOTAL", "outliers.png")
        assert mock_savefig.called


@patch("matplotlib.pyplot.savefig")
def test_model_evaluator_all_methods(mock_savefig, tmp_path):
    mock_paths = {
        "raw_dir": Path(tmp_path),
        "processed_dir": Path(tmp_path),
        "models_dir": Path(tmp_path),
        "reports_dir": Path(tmp_path),
        "logs_dir": Path(tmp_path),
    }
    with patch.object(config, "get_paths", return_value=mock_paths):
        evaluator = ModelEvaluator()
        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 0, 1]
        y_prob = [0.1, 0.9, 0.2, 0.8]

        evaluator.plot_confusion_matrix("test", y_true, y_pred)
        evaluator.plot_roc_curve("test", y_true, y_prob)
        evaluator.plot_precision_recall_curve("test", y_true, y_prob)

        # Test feature importance
        mock_model = MagicMock()
        mock_model.feature_importances_ = np.array([0.5, 0.5])
        evaluator.plot_feature_importance("test", mock_model, ["f1", "f2"])

        # Test comparison
        comp_df = pd.DataFrame({"Model": ["test"], "F1-Score": [0.8], "ROC-AUC": [0.85]})
        evaluator.plot_model_comparison(comp_df)
        assert mock_savefig.called


def test_experiment_tracker_invalid_json(tmp_path):
    with patch.object(config, "get_paths", return_value={"logs_dir": str(tmp_path)}):
        tracker = ExperimentTracker()
        # Write corrupted JSON
        with open(tracker.runs_path, "w") as f:
            f.write("corrupted JSON")

        # Logging a run should handle it gracefully
        tracker.log_run("log_reg", {"C": 1.0}, {"F1": 0.75})
        runs = tracker.get_runs()
        assert len(runs) == 1
        assert runs[0]["model_name"] == "log_reg"

        # Test get_runs exception by corrupting it again
        with open(tracker.runs_path, "w") as f:
            f.write("corrupted JSON")
        assert tracker.get_runs() == []


@patch("src.models.predict.load_pkl")
@patch("os.path.exists")
def test_predict_methods_and_wrappers(mock_exists, mock_load):
    from src.models.predict import (
        RiskPredictor,
        load_model,
        load_pipeline,
        predict,
        predict_probability,
        validate_input,
    )

    mock_exists.return_value = True

    mock_pipeline = MagicMock()
    mock_pipeline.transform.side_effect = lambda x: x

    mock_clf = MagicMock()
    mock_clf.predict.return_value = [0]
    mock_clf.predict_proba.return_value = np.array([[0.95, 0.05]])

    mock_load.side_effect = [mock_pipeline, mock_clf, mock_pipeline, mock_clf]

    # Instantiate RiskPredictor
    predictor = RiskPredictor()

    # Test predict_probability
    df = pd.DataFrame([[0.5, 1.2]], columns=["feat_1", "feat_2"])
    probs = predictor.predict_probability(df)
    assert probs == [0.05]

    # Test functional wrappers
    from src.models.predict import _predictor

    _predictor.pipeline = None
    _predictor.model = None

    pipe = load_pipeline()
    assert pipe == mock_pipeline

    model = load_model()
    assert model == mock_clf

    valid = validate_input(
        {
            "code_gender": "M",
            "cnt_children": 0,
            "cnt_fam_members": 2,
            "age_years": 35,
            "amt_income_total": 150000.0,
            "flag_own_car": "N",
            "flag_own_realty": "Y",
            "name_income_type": "Working",
            "name_education_type": "Secondary",
            "name_family_status": "Married",
            "name_housing_type": "House",
            "years_employed": 5.0,
            "flag_unemployed": 0,
        }
    )
    assert valid is True

    preds = predict(df)
    assert preds["decision"] == "Approved"

    probs2 = predict_probability(df)
    assert probs2 == [0.05]


def test_calculate_all_metrics_exceptions():
    # Calling with invalid probability format should trigger warnings and fallbacks
    metrics = calculate_all_metrics([0, 1], [0, 1], ["invalid", "prob"])
    assert metrics["ROC-AUC"] == 0.5
    assert metrics["Log_Loss"] == 0.0


@patch("requests.post")
def test_ibm_cloud_manager_score_online(mock_post):
    manager = IBMCloudManager()
    manager.api_key = "mock_key"
    manager.scoring_url = "mock_url"

    # Mock iam token request & scoring request
    mock_resp1 = MagicMock()
    mock_resp1.status_code = 200
    mock_resp1.json.return_value = {"access_token": "mock_token"}

    mock_resp2 = MagicMock()
    mock_resp2.status_code = 200
    mock_resp2.json.return_value = {"predictions": [{"values": [[0]]}]}

    mock_post.side_effect = [mock_resp1, mock_resp2]

    res = manager.score_online({"feat1": 0.5})
    assert "predictions" in res


def test_ibm_cloud_manager_errors():
    from src.utils.exceptions import CloudDeploymentError

    manager = IBMCloudManager()
    manager.api_key = None
    with pytest.raises(CloudDeploymentError):
        manager.get_iam_token()

    manager.api_key = "mock_key"
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.text = "Unauthorized"
        mock_post.return_value = mock_resp
        with pytest.raises(CloudDeploymentError):
            manager.get_iam_token()

    manager.scoring_url = None
    with pytest.raises(CloudDeploymentError):
        manager.score_online({"feat": 1.0})


def test_helpers_exceptions(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_pkl("non_existent.pkl")

    # Write invalid pickle
    invalid_pkl = os.path.join(tmp_path, "invalid.pkl")
    with open(invalid_pkl, "w") as f:
        f.write("invalid data")
    from app.utils.exceptions import DataPreprocessingError as AppDataPreprocessingError

    with pytest.raises(AppDataPreprocessingError):
        load_pkl(invalid_pkl)

    with pytest.raises(FileNotFoundError):
        load_json("non_existent.json")

    # Write invalid JSON
    invalid_json = os.path.join(tmp_path, "invalid.json")
    with open(invalid_json, "w") as f:
        f.write("invalid data")
    with pytest.raises(Exception):
        load_json(invalid_json)


def test_duplicate_handler_with_duplicates():
    df = pd.DataFrame({"a": [1, 1], "b": [2, 2]})
    handler = DuplicateHandler()
    res = handler.remove_duplicates(df)
    assert len(res) == 1
    assert handler.duplicate_count == 1


def test_data_split_exceptions():
    from src.data.data_split import perform_stratified_split
    from src.utils.exceptions import DataPreprocessingError

    with pytest.raises(DataPreprocessingError):
        perform_stratified_split(pd.DataFrame({"a": [1, 2]}))

    df = pd.DataFrame({"a": [1], TARGET_COL: [0]})
    with pytest.raises(DataPreprocessingError):
        perform_stratified_split(df)

import os

from ibm_watson_machine_learning import APIClient

from config.config import config
from src.utils.exceptions import CloudDeploymentError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_ibm_deployment():
    """
    Orchestrates the registration and deployment of local pkl models to Watson Machine Learning space.
    """
    logger.info("Starting Watson ML deployment pipeline...")

    api_key = config.IBM_API_KEY
    url = config.IBM_URL
    space_id = config.IBM_SPACE_ID

    if not api_key or api_key == "dummy_key":
        logger.warning("IBM WML credentials missing. Skipping cloud registration.")
        return None

    try:
        wml_credentials = {"apikey": api_key, "url": url}
        client = APIClient(wml_credentials)
        client.set.default_space(space_id)

        # Deploy model
        model_path = os.path.join(config.get_paths()["models_dir"], "trained_model.pkl")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found for upload: {model_path}")

        logger.info(f"Uploading model binary {model_path} to IBM Watson WML repository...")
        software_spec_uid = client.software_specifications.get_id_by_name("runtime-22.2-py3.10")

        meta_props = {
            client.repository.ModelMetaNames.NAME: "CreditCardApprovalPredictionModel",
            client.repository.ModelMetaNames.TYPE: "scikit-learn_1.1",
            client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: software_spec_uid,
        }

        model_details = client.repository.store_model(model=model_path, meta_props=meta_props)
        model_uid = client.repository.get_model_id(model_details)
        logger.info(f"Model uploaded successfully. WML UID: {model_uid}")

        # Create deployment
        logger.info("Creating online deployment space...")
        dep_props = {
            client.deployments.ConfigurationMetaNames.NAME: "CreditCardApprovalPredictionOnline",
            client.deployments.ConfigurationMetaNames.ONLINE: {},
        }
        dep_details = client.deployments.create(artifact_uid=model_uid, meta_props=dep_props)
        scoring_url = client.deployments.get_scoring_href(dep_details)

        logger.info(f"Watson ML Online scoring endpoint ready: {scoring_url}")
        return scoring_url
    except Exception as e:
        logger.error(f"Watson ML deployment failed: {str(e)}")
        raise CloudDeploymentError(f"Cloud deployment runner failed: {str(e)}")


if __name__ == "__main__":
    run_ibm_deployment()

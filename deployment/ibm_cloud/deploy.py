import os
import yaml
from dotenv import load_dotenv
from ibm_watson_machine_learning import APIClient
from src.utils.logger import get_logger
from src.utils.exceptions import CloudDeploymentError
from src.models.model_registry import ModelRegistry

logger = get_logger(__name__)

# Load config
CONFIG_PATH = "e:/Credit-Card-Approval-Prediction/config/config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

def deploy_to_ibm_wml():
    """
    Connects to IBM Watson Machine Learning service, registers the best trained model,
    and deploys it as an online web service.
    """
    logger.info("Initializing IBM Watson Machine Learning deployment...")
    
    # Get credentials from environment
    api_key = os.getenv("IBM_API_KEY")
    url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
    space_id = os.getenv("IBM_SPACE_ID")
    
    if not api_key or api_key == "dummy_key":
        logger.error("IBM_API_KEY is not configured or contains dummy values. Skipping active cloud deployment.")
        raise CloudDeploymentError("IBM API Key is not set or contains dummy values. Configure .env file.")
        
    if not space_id or space_id == "dummy_space_id":
        logger.error("IBM_SPACE_ID is not configured. Skipping active cloud deployment.")
        raise CloudDeploymentError("IBM Watson ML Space ID is not set. Configure .env file.")
        
    try:
        # 1. Authenticate WML client
        wml_credentials = {
            "apikey": api_key,
            "url": url
        }
        client = APIClient(wml_credentials)
        
        # 2. Set default deployment space
        client.set.default_space(space_id)
        logger.info(f"Connected to Watson ML space: {space_id}")
        
        # 3. Find the best model in local registry
        registry = ModelRegistry(CONFIG_PATH)
        best_name = registry.get_best_model_name()
        if not best_name:
            best_name = "xgboost"
            
        model_filepath = os.path.join(config["paths"]["models_dir"], f"{best_name}.joblib")
        logger.info(f"Deploying best local model '{best_name}' from path: {model_filepath}")
        
        # 4. Define model metadata
        software_spec_uid = client.software_specifications.get_id_by_name("runtime-22.2-py3.10")
        
        model_props = {
            client.repository.ModelMetaNames.NAME: f"CreditCardApproval_{best_name}",
            client.repository.ModelMetaNames.DESCRIPTION: "Model to predict credit card application approval.",
            client.repository.ModelMetaNames.TYPE: "scikit-learn_1.1",
            client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: software_spec_uid
        }
        
        # 5. Store model in Watson ML repository
        logger.info("Uploading model to Watson ML repository...")
        model_details = client.repository.store_model(
            model=model_filepath,
            meta_props=model_props
        )
        model_uid = client.repository.get_model_id(model_details)
        logger.info(f"Model stored successfully with Watson ML UID: {model_uid}")
        
        # 6. Deploy model as an online endpoint
        logger.info("Creating online deployment...")
        deployment_props = {
            client.deployments.ConfigurationMetaNames.NAME: f"CreditCardApproval_OnlineEndpoint",
            client.deployments.ConfigurationMetaNames.ONLINE: {}
        }
        
        deployment_details = client.deployments.create(
            artifact_uid=model_uid,
            meta_props=deployment_props
        )
        deployment_uid = client.deployments.get_uid(deployment_details)
        scoring_url = client.deployments.get_scoring_href(deployment_details)
        
        logger.info(f"Model deployed successfully!")
        logger.info(f"Deployment UID: {deployment_uid}")
        logger.info(f"Scoring Endpoint URL: {scoring_url}")
        
        return scoring_url, deployment_uid
        
    except Exception as e:
        logger.error(f"Failed to deploy to IBM Watson ML: {str(e)}")
        raise CloudDeploymentError(f"IBM Watson ML deployment failed: {str(e)}")

if __name__ == "__main__":
    try:
        deploy_to_ibm_wml()
    except Exception as e:
        print(f"Error during WML deployment: {str(e)}")

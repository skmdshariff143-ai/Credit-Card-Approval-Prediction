import os
import json
import requests
from dotenv import load_dotenv
from src.utils.logger import get_logger
from src.utils.exceptions import CloudDeploymentError

logger = get_logger(__name__)

# Load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

class IBMCloudScorer:
    """
    Handles request formatting and prediction execution against a deployed IBM Watson ML online endpoint.
    """
    def __init__(self):
        self.api_key = os.getenv("IBM_API_KEY")
        self.scoring_url = os.getenv("IBM_SCORING_URL") # Provided after deploy runs
        self.url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
        
    def get_access_token(self):
        """
        Retrieves a temporary IAM access token from IBM Cloud.
        """
        logger.info("Requesting IAM Access Token from IBM Cloud...")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={self.api_key}"
        
        try:
            # IAM oauth token service URL
            token_url = "https://iam.cloud.ibm.com/identity/token"
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch IAM Token: {response.text}")
                raise CloudDeploymentError(f"IBM Cloud IAM Token request failed: {response.text}")
                
            token = response.json().get("access_token")
            logger.info("Successfully retrieved access token.")
            return token
        except Exception as e:
            logger.error(f"Failed to fetch IAM Token: {str(e)}")
            raise CloudDeploymentError(f"IBM Cloud authentication failed: {str(e)}")

    def score(self, processed_record_dict):
        """
        Formats features and requests predictions from the deployed cloud endpoint.
        """
        if not self.scoring_url:
            raise CloudDeploymentError("IBM_SCORING_URL is not set in environmental variables.")
            
        try:
            token = self.get_access_token()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            # Format inputs for Watson ML endpoint
            # WML expects columns names and values list
            fields = list(processed_record_dict.keys())
            values = [list(processed_record_dict.values())]
            
            payload = {
                "input_data": [{
                    "fields": fields,
                    "values": values
                }]
            }
            
            logger.info(f"Sending scoring payload to: {self.scoring_url}")
            response = requests.post(self.scoring_url, json=payload, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Scoring request failed: {response.text}")
                raise CloudDeploymentError(f"Scoring request failed: {response.text}")
                
            result = response.json()
            logger.info("Scoring response received successfully.")
            return result
            
        except Exception as e:
            logger.error(f"Failed to score against IBM WML: {str(e)}")
            raise CloudDeploymentError(f"Scoring failed: {str(e)}")

import os
import requests
from configs.config import config
from src.utils.logger import get_logger
from src.utils.exceptions import CloudDeploymentError

logger = get_logger(__name__)

class IBMCloudManager:
    """
    Manages authentications, model uploads, and online scoring calls against IBM Watson ML.
    """
    def __init__(self):
        self.api_key = config.IBM_API_KEY
        self.url = config.IBM_URL
        self.space_id = config.IBM_SPACE_ID
        self.scoring_url = config.IBM_SCORING_URL
        
    def get_iam_token(self) -> str:
        """
        Retrieves temporary access token from IBM Cloud IAM service.
        """
        logger.info("Retrieving IBM IAM Access Token...")
        if not self.api_key or self.api_key == "dummy_key":
            raise CloudDeploymentError("IBM API Key is not set in environment.")
            
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={self.api_key}"
        
        try:
            token_url = "https://iam.cloud.ibm.com/identity/token"
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"IAM Token request failed: {response.text}")
                raise CloudDeploymentError(f"IBM Authentication failed: {response.text}")
                
            token = response.json().get("access_token")
            logger.info("IAM Token retrieved successfully.")
            return token
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise CloudDeploymentError(f"IBM WML Auth error: {str(e)}")

    def score_online(self, processed_record_dict) -> dict:
        """
        Submits preprocessed features payload to online Watson ML endpoint.
        """
        logger.info("Submitting online scoring request to IBM Watson ML...")
        if not self.scoring_url or self.scoring_url == "dummy_scoring_url":
            raise CloudDeploymentError("Scoring endpoint URL is not configured.")
            
        try:
            token = self.get_iam_token()
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            fields = list(processed_record_dict.keys())
            values = [list(processed_record_dict.values())]
            
            payload = {
                "input_data": [{
                    "fields": fields,
                    "values": values
                }]
            }
            
            response = requests.post(self.scoring_url, json=payload, headers=headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"Scoring failed: {response.text}")
                raise CloudDeploymentError(f"Scoring response error: {response.text}")
                
            result = response.json()
            logger.info("Scoring response received successfully from IBM WML.")
            return result
        except Exception as e:
            logger.error(f"IBM WML scoring call failed: {str(e)}")
            raise CloudDeploymentError(f"Cloud scoring failed: {str(e)}")

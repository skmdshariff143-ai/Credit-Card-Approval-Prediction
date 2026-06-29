import os
import json
from datetime import datetime
from src.utils.logger import get_logger
from src.utils.helpers import load_yaml, save_artifact, load_artifact

logger = get_logger(__name__)

class ModelRegistry:
    """
    Manages loading, saving, and metadata registration of models.
    """
    def __init__(self, config_path="e:/Credit-Card-Approval-Prediction/config/config.yaml"):
        self.config = load_yaml(config_path)
        self.models_dir = self.config["paths"].get("models_dir")
        
    def register_model(self, name, model, metrics, params):
        """
        Saves a model to the registry along with a metadata JSON file.
        """
        logger.info(f"Registering model '{name}' in model registry...")
        try:
            os.makedirs(self.models_dir, exist_ok=True)
            
            # Save model binary
            model_path = os.path.join(self.models_dir, f"{name}.joblib")
            save_artifact(model, model_path)
            
            # Prepare metadata
            metadata = {
                "model_name": name,
                "date_registered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "parameters": {k: str(v) for k, v in params.items()},
                "metrics": {k: float(v) if isinstance(v, (int, float)) else str(v) for k, v in metrics.items()}
            }
            
            # Save metadata
            meta_path = os.path.join(self.models_dir, f"{name}_metadata.json")
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=4)
                
            logger.info(f"Model '{name}' and metadata registered successfully at: {self.models_dir}")
        except Exception as e:
            logger.error(f"Failed to register model '{name}': {str(e)}")
            raise

    def load_model(self, name):
        """
        Loads a model by name from the registry.
        """
        model_path = os.path.join(self.models_dir, f"{name}.joblib")
        logger.info(f"Loading model '{name}' from registry path: {model_path}")
        return load_artifact(model_path)
        
    def get_best_model_name(self):
        """
        Finds the registered model name with the highest F1-Score from metadata JSON files.
        """
        best_name = None
        best_score = -1.0
        
        try:
            if not os.path.exists(self.models_dir):
                return None
                
            for file in os.listdir(self.models_dir):
                if file.endswith("_metadata.json"):
                    meta_path = os.path.join(self.models_dir, file)
                    with open(meta_path, "r") as f:
                        meta = json.load(f)
                        f1 = meta.get("metrics", {}).get("F1-Score", 0.0)
                        if f1 > best_score:
                            best_score = f1
                            best_name = meta.get("model_name")
            logger.info(f"Registry found best model: '{best_name}' with F1-Score: {best_score:.4f}")
            return best_name
        except Exception as e:
            logger.error(f"Failed to query best model from registry: {str(e)}")
            return None

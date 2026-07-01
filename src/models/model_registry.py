import os
from datetime import datetime

from configs.config import config
from src.utils.helper import save_json, save_pkl
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelRegistry:
    """
    Manages registration and versioning of trained model objects, parameters, and metadata.
    """

    def __init__(self):
        paths = config.get_paths()
        self.models_dir = paths["models_dir"]

    def register_model(self, name: str, model, params: dict, metrics: dict):
        """
        Serializes model and writes metadata description file.
        """
        logger.info(f"Registering model '{name}' inside model registry...")

        # Save model pkl
        model_path = os.path.join(self.models_dir, f"{name}.pkl")
        save_pkl(model, model_path)

        # Write metadata
        metadata = {
            "model_name": name,
            "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parameters": {k: str(v) for k, v in params.items()},
            "metrics": {k: float(v) if isinstance(v, (int, float)) else str(v) for k, v in metrics.items()},
        }

        meta_path = os.path.join(self.models_dir, f"{name}_metadata.json")
        save_json(metadata, meta_path)
        logger.info(f"Registered model '{name}' and metadata successfully.")

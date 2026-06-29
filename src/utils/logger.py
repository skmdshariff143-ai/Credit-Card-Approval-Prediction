import os
import yaml
import logging.config
from pathlib import Path

# Load config path
configs_dir = Path(__file__).resolve().parent.parent.parent / "configs"
yaml_path = configs_dir / "logging.yaml"
logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"

# Ensure logs dir exists
os.makedirs(logs_dir, exist_ok=True)

if os.path.exists(yaml_path):
    with open(yaml_path, 'r') as f:
        log_config = yaml.safe_load(f)
        
        # Override log file path to ensure absolute naming
        if "handlers" in log_config and "file" in log_config["handlers"]:
            log_config["handlers"]["file"]["filename"] = str(logs_dir / "app.log")
            
        logging.config.dictConfig(log_config)
else:
    # Fallback to basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )

def get_logger(name):
    """
    Returns a logger instance configure according to configurations/logging.yaml.
    """
    return logging.getLogger(name)

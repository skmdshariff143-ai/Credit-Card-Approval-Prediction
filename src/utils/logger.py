import logging
import yaml
import os
from config.logging_config import setup_logging

# Load config to get log file path and level
config_path = "e:/Credit-Card-Approval-Prediction/config/config.yaml"
log_file = "e:/Credit-Card-Approval-Prediction/logs/project.log"
log_level_str = "INFO"

if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
            if cfg and "logging" in cfg:
                log_file = cfg["logging"].get("log_file", log_file)
                log_level_str = cfg["logging"].get("level", log_level_str)
    except Exception:
        pass

# Map string level to logging level
log_level = getattr(logging, log_level_str.upper(), logging.INFO)

# Run setup
setup_logging(log_file_path=log_file, log_level=log_level)

def get_logger(logger_name):
    """
    Returns a configured logger with the given name.
    """
    return logging.getLogger(logger_name)

import json
import os
from datetime import datetime

from config.config import config


class ExperimentTracker:
    """
    Lightweight enterprise ML experiment tracker logging run parameters, metrics, and models.
    """

    def __init__(self):
        paths = config.get_paths()
        self.runs_path = os.path.join(paths["logs_dir"], "runs.json")
        os.makedirs(os.path.dirname(self.runs_path), exist_ok=True)

    def log_run(self, model_name: str, parameters: dict, metrics: dict):
        """Logs a single training run into history file."""
        run_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_name": model_name,
            "parameters": parameters,
            "metrics": metrics,
        }

        runs = []
        if os.path.exists(self.runs_path):
            try:
                with open(self.runs_path, "r") as f:
                    runs = json.load(f)
                    if not isinstance(runs, list):
                        runs = []
            except Exception:
                runs = []

        runs.append(run_record)
        with open(self.runs_path, "w") as f:
            json.dump(runs, f, indent=4)

    def get_runs(self) -> list:
        """Retrieves list of all logged runs."""
        if not os.path.exists(self.runs_path):
            return []
        try:
            with open(self.runs_path, "r") as f:
                return json.load(f)
        except Exception:
            return []

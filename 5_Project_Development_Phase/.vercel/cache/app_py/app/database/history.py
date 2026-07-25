import json
import os
from datetime import datetime

from config.config import config
from app.utils.logger import get_logger

logger = get_logger(__name__)


class HistoryManager:
    """
    Manages in-memory and local file persistence of credit risk scoring history.
    """

    def __init__(self):
        paths = config.get_paths()
        # Direct folder models/ or processed/
        self.history_path = os.path.join(paths["processed_dir"], "prediction_history.json")
        self.history = self._load_history()

    def _load_history(self) -> list:
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to read history JSON file: {str(e)}")
                return []
        return []

    def save_history(self):
        try:
            with open(self.history_path, "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to write history JSON file: {str(e)}")

    def add_entry(self, input_data: dict, decision: str, probability: float):
        """
        Formats and inserts a new prediction scoring event.
        """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input": {k: v for k, v in input_data.items() if k != "ID"},
            "decision": decision,
            "probability_percent": round(probability, 2),
        }
        # Insert at front of history list
        self.history.insert(0, entry)
        # Limit history to top 50 records
        self.history = self.history[:50]
        self.save_history()
        logger.info(f"Logged prediction history entry: decision={decision}")

    def get_history(self) -> list:
        return self.history

    def clear_history(self):
        self.history = []
        self.save_history()
        logger.info("Cleared all prediction history.")

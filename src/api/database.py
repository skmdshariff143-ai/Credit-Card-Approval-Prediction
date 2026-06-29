import sqlite3
import json
import os
from datetime import datetime
from configs.config import config

class DatabaseManager:
    """
    Manages SQLite storage for application prediction history.
    """
    def __init__(self):
        paths = config.get_paths()
        self.db_path = os.path.join(paths["logs_dir"], "prediction_history.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes the database schema if it does not exist."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    input_features TEXT NOT NULL,
                    prediction TEXT NOT NULL,
                    probability REAL NOT NULL
                )
            """)
            conn.commit()

    def add_prediction(self, input_features: dict, prediction: str, probability: float) -> int:
        """Saves a scoring record into the history database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        input_json = json.dumps(input_features)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO predictions (timestamp, input_features, prediction, probability) VALUES (?, ?, ?, ?)",
                (timestamp, input_json, prediction, probability)
            )
            conn.commit()
            return cursor.lastrowid

    def get_predictions(self, limit: int = 50) -> list:
        """Retrieves a list of previous scoring sessions."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, timestamp, input_features, prediction, probability FROM predictions ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            history_list = []
            for row in rows:
                history_list.append({
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "input": json.loads(row["input_features"]),
                    "decision": row["prediction"],
                    "probability_percent": row["probability"]
                })
            return history_list

    def clear_history(self):
        """Clears all logged history transactions."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM predictions")
            conn.commit()

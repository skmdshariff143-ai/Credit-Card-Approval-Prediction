import json
import os
import sqlite3
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
            # Core prediction history table (Phase 11 spec)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prediction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    income REAL NOT NULL,
                    employment TEXT NOT NULL,
                    experience REAL NOT NULL,
                    children INTEGER NOT NULL,
                    debt REAL NOT NULL,
                    prediction TEXT NOT NULL,
                    probability REAL NOT NULL,
                    risk_level TEXT NOT NULL,
                    model TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    raw_input TEXT
                )
            """)

            # Backwards compatibility table
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

    def add_prediction(
        self,
        input_features,
        prediction=None,
        probability=None,
        app_id=None,
        gender=None,
        income=None,
        employment=None,
        experience=None,
        children=None,
        debt=None,
        risk_level=None,
        model=None,
        recommendation=None,
    ) -> int:
        """Saves a scoring record into the history database (supports old & new signatures)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Old Signature Compatibility check
        if isinstance(input_features, dict) and prediction is not None and probability is not None:
            raw_input = input_features
            app_id = app_id or f"APP-{abs(hash(str(raw_input) + timestamp)) % 1000000:06d}"
            gender = gender or raw_input.get("code_gender", "Unknown")
            income = income or float(raw_input.get("amt_income_total", 0.0))
            employment = employment or raw_input.get("name_income_type", "Unknown")
            experience = experience or float(raw_input.get("years_employed", 0.0))
            children = children or int(raw_input.get("cnt_children", 0))
            debt = debt or float(raw_input.get("existing_debt", 0.0))
            risk_level = risk_level or ("High" if prediction == "Rejected" else "Low")
            model = model or "logistic_regression"
            recommendation = recommendation or (
                "Manual review required" if prediction == "Rejected" else "Auto-approved credit facility"
            )
        else:
            # 2. New Signature mapping
            app_id = input_features
            raw_input = {
                "code_gender": gender,
                "amt_income_total": income,
                "name_income_type": employment,
                "years_employed": experience,
                "cnt_children": children,
                "existing_debt": debt,
            }
            risk_level = risk_level or "Low"
            model = model or "logistic_regression"
            recommendation = recommendation or "Approved"

        raw_json = json.dumps(raw_input)

        with self._get_connection() as conn:
            # Insert into predictions (compat)
            conn.execute(
                "INSERT INTO predictions (timestamp, input_features, prediction, probability) VALUES (?, ?, ?, ?)",
                (timestamp, raw_json, prediction, probability),
            )

            # Insert into prediction_history (new spec)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO prediction_history (
                    application_id, timestamp, gender, income, employment, experience, children, debt, prediction, probability, risk_level, model, recommendation, raw_input
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    app_id,
                    timestamp,
                    gender,
                    income,
                    employment,
                    experience,
                    children,
                    debt,
                    prediction,
                    probability,
                    risk_level,
                    model,
                    recommendation,
                    raw_json,
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def get_predictions(self, limit: int = 50, search: str = None, sort_by: str = "id", order: str = "DESC") -> list:
        """Retrieves history from database supporting filter, search, sorting."""
        query = "SELECT * FROM prediction_history"
        params = []

        if search:
            query += " WHERE application_id LIKE ? OR gender LIKE ? OR employment LIKE ? OR prediction LIKE ?"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])

        # Allowed sort fields to prevent SQL injection
        allowed_sorts = {"id", "timestamp", "income", "prediction", "probability", "risk_level"}
        if sort_by not in allowed_sorts:
            sort_by = "id"
        if order not in {"ASC", "DESC"}:
            order = "DESC"

        query += f" ORDER BY {sort_by} {order} LIMIT ?"
        params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

            history_list = []
            for row in rows:
                history_list.append(
                    {
                        "id": row["id"],
                        "application_id": row["application_id"],
                        "timestamp": row["timestamp"],
                        "gender": row["gender"],
                        "income": row["income"],
                        "employment": row["employment"],
                        "experience": row["experience"],
                        "children": row["children"],
                        "debt": row["debt"],
                        "prediction": row["prediction"],
                        "decision": row["prediction"],  # compat
                        "probability": row["probability"],
                        "probability_percent": row["probability"],  # compat
                        "risk_level": row["risk_level"],
                        "model": row["model"],
                        "recommendation": row["recommendation"],
                        "input": json.loads(row["raw_input"]) if row["raw_input"] else {},
                    }
                )
            return history_list

    def get_admin_stats(self) -> dict:
        """Calculates statistics for admin dashboard metrics."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Total Predictions
            cursor.execute("SELECT COUNT(*) FROM prediction_history")
            total = cursor.fetchone()[0] or 0

            # Approved Count
            cursor.execute("SELECT COUNT(*) FROM prediction_history WHERE prediction = 'Approved'")
            approved = cursor.fetchone()[0] or 0

            # Rejected Count
            cursor.execute("SELECT COUNT(*) FROM prediction_history WHERE prediction = 'Rejected'")
            rejected = cursor.fetchone()[0] or 0

            # Averages
            cursor.execute("SELECT AVG(income) FROM prediction_history")
            avg_income = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT AVG(debt) FROM prediction_history")
            avg_debt = cursor.fetchone()[0] or 0.0

            # Calculate approval rate
            approval_rate = (approved / total * 100.0) if total > 0 else 0.0

            return {
                "total": total,
                "approved": approved,
                "rejected": rejected,
                "approval_rate": round(approval_rate, 2),
                "avg_income": round(avg_income, 2),
                "avg_debt": round(avg_debt, 2),
            }

    def clear_history(self):
        """Clears all logged history transactions."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM prediction_history")
            conn.execute("DELETE FROM predictions")
            conn.commit()

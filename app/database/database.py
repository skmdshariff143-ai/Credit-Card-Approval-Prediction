import json
import os
import sqlite3
from datetime import datetime

from config.config import config


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
                    raw_input TEXT,
                    explanation TEXT
                )
            """)

            # Backwards compatibility table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    input_features TEXT NOT NULL,
                    prediction TEXT NOT NULL,
                    probability REAL NOT NULL,
                    model TEXT,
                    explanation TEXT
                )
            """)
            # Create performance indexes for search and sorting
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_app_id ON prediction_history(application_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_timestamp ON prediction_history(timestamp);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_income ON prediction_history(income);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_risk ON prediction_history(risk_level);")

            # Authentication: users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    is_admin INTEGER DEFAULT 0
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")

            # Add user_id column to prediction_history (safe migration)
            try:
                conn.execute("ALTER TABLE prediction_history ADD COLUMN user_id INTEGER REFERENCES users(id)")
            except sqlite3.OperationalError:
                pass  # Column already exists

            # Add explanation column to prediction_history (safe migration)
            try:
                conn.execute("ALTER TABLE prediction_history ADD COLUMN explanation TEXT")
            except sqlite3.OperationalError:
                pass  # Column already exists

            # Add model and explanation columns to predictions (safe migration)
            try:
                conn.execute("ALTER TABLE predictions ADD COLUMN model TEXT")
            except sqlite3.OperationalError:
                pass  # Column already exists
            try:
                conn.execute("ALTER TABLE predictions ADD COLUMN explanation TEXT")
            except sqlite3.OperationalError:
                pass  # Column already exists

            # New reports table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id TEXT NOT NULL UNIQUE REFERENCES prediction_history(application_id) ON DELETE CASCADE,
                    timestamp TEXT NOT NULL,
                    inputs TEXT NOT NULL,
                    prediction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    model_used TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    user_id INTEGER REFERENCES users(id)
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_reports_app_id ON reports(application_id);")

            conn.commit()

    def check_connection(self) -> bool:
        """Verifies database connectivity."""
        try:
            with self._get_connection() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    # ==================================================================
    # User Management Methods (Authentication)
    # ==================================================================

    def create_user(self, username, email, password_hash, full_name=None):
        """Creates a new user account. Returns user id or None on conflict."""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO users (username, email, password_hash, full_name, created_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (username, email, password_hash, full_name,
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                )
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None

    def get_user_by_id(self, user_id):
        """Retrieves a user record by primary key."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_email(self, email):
        """Retrieves a user record by email address."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_username(self, username):
        """Retrieves a user record by username."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_user_password(self, user_id, new_password_hash):
        """Updates a user's password hash."""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_password_hash, user_id),
            )
            conn.commit()

    def update_user_profile(self, user_id, full_name, email):
        """Updates a user's profile details."""
        with self._get_connection() as conn:
            try:
                conn.execute(
                    "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
                    (full_name, email, user_id),
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # Email conflict

    # ==================================================================
    # Per-User Prediction Methods
    # ==================================================================

    def get_user_predictions(self, user_id, limit=50, search=None, sort_by="id", order="DESC", decision=None, risk_level=None):
        """Retrieves prediction history filtered by user_id, with searching and filters."""
        query = "SELECT * FROM prediction_history WHERE user_id = ?"
        params = [user_id]

        if search:
            query += " AND (application_id LIKE ? OR gender LIKE ? OR employment LIKE ? OR prediction LIKE ?)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])

        if decision and decision != "All":
            query += " AND prediction = ?"
            params.append(decision)

        if risk_level and risk_level != "All":
            query += " AND risk_level = ?"
            params.append(risk_level)

        allowed_sorts = {"id", "timestamp", "income", "prediction", "probability", "risk_level", "application_id"}
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
                row_dict = dict(row)
                explanation_data = {}
                if "explanation" in row_dict and row_dict["explanation"]:
                    try:
                        explanation_data = json.loads(row_dict["explanation"])
                    except Exception:
                        pass
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
                        "decision": row["prediction"],
                        "probability": row["probability"],
                        "probability_percent": row["probability"],
                        "risk_level": row["risk_level"],
                        "model": row["model"],
                        "recommendation": row["recommendation"],
                        "input": json.loads(row["raw_input"]) if row["raw_input"] else {},
                        "explanation": explanation_data,
                    }
                )
            return history_list

    def get_user_stats(self, user_id):
        """Calculates per-user prediction statistics."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM prediction_history WHERE user_id = ?", (user_id,))
            total = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM prediction_history WHERE user_id = ? AND prediction = 'Approved'", (user_id,))
            approved = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM prediction_history WHERE user_id = ? AND prediction = 'Rejected'", (user_id,))
            rejected = cursor.fetchone()[0] or 0

            approval_rate = (approved / total * 100.0) if total > 0 else 0.0

            return {
                "total": total,
                "approved": approved,
                "rejected": rejected,
                "approval_rate": round(approval_rate, 2),
            }

    # ==================================================================
    # Original Methods (unchanged)
    # ==================================================================

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
        user_id=None,
        explanation=None,
    ) -> int:
        """Saves a scoring record into the history database, including predictions, history, and reports."""
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
        explanation_json = json.dumps(explanation) if explanation else None

        with self._get_connection() as conn:
            # Insert into predictions (compat)
            conn.execute(
                "INSERT INTO predictions (timestamp, input_features, prediction, probability, model, explanation) VALUES (?, ?, ?, ?, ?, ?)",
                (timestamp, raw_json, prediction, probability, model, explanation_json),
            )

            # Insert into prediction_history (new spec)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO prediction_history (
                    application_id, timestamp, gender, income, employment,
                    experience, children, debt, prediction, probability,
                    risk_level, model, recommendation, raw_input, user_id, explanation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    user_id,
                    explanation_json,
                ),
            )

            # Insert into reports table
            confidence_val = float(probability) if probability is not None else 0.0
            conn.execute(
                """
                INSERT OR REPLACE INTO reports (
                    application_id, timestamp, inputs, prediction, confidence, model_used, explanation, user_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    app_id,
                    timestamp,
                    raw_json,
                    prediction,
                    confidence_val,
                    model,
                    explanation_json or "{}",
                    user_id,
                ),
            )

            conn.commit()
            return cursor.lastrowid

    def get_predictions(self, limit: int = 50, search: str = None, sort_by: str = "id", order: str = "DESC", decision=None, risk_level=None) -> list:
        """Retrieves history from database supporting filter, search, sorting."""
        query = "SELECT * FROM prediction_history"
        params = []
        where_clauses = []

        if search:
            where_clauses.append("(application_id LIKE ? OR gender LIKE ? OR employment LIKE ? OR prediction LIKE ?)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])

        if decision and decision != "All":
            where_clauses.append("prediction = ?")
            params.append(decision)

        if risk_level and risk_level != "All":
            where_clauses.append("risk_level = ?")
            params.append(risk_level)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Allowed sort fields to prevent SQL injection
        allowed_sorts = {"id", "timestamp", "income", "prediction", "probability", "risk_level", "application_id"}
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
                row_dict = dict(row)
                explanation_data = {}
                if "explanation" in row_dict and row_dict["explanation"]:
                    try:
                        explanation_data = json.loads(row_dict["explanation"])
                    except Exception:
                        pass
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
                        "explanation": explanation_data,
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
            conn.execute("DELETE FROM reports")
            conn.commit()

    def delete_prediction(self, application_id, user_id) -> bool:
        """Deletes a specific prediction history entry and its associated report."""
        with self._get_connection() as conn:
            # Delete from history
            cursor = conn.execute(
                "DELETE FROM prediction_history WHERE application_id = ? AND user_id = ?",
                (application_id, user_id),
            )
            # Delete from reports
            conn.execute(
                "DELETE FROM reports WHERE application_id = ? AND user_id = ?",
                (application_id, user_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def clear_user_history(self, user_id) -> bool:
        """Clears all prediction history and reports for a specific user."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM prediction_history WHERE user_id = ?", (user_id,))
            conn.execute("DELETE FROM reports WHERE user_id = ?", (user_id,))
            conn.commit()
            return True

    def get_report_by_app_id(self, application_id, user_id=None) -> dict:
        """Retrieves report data directly from reports table."""
        query = "SELECT * FROM reports WHERE application_id = ?"
        params = [application_id]
        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)

        with self._get_connection() as conn:
            row = conn.execute(query, tuple(params)).fetchone()
            if row:
                row_dict = dict(row)
                return {
                    "id": row_dict["id"],
                    "application_id": row_dict["application_id"],
                    "timestamp": row_dict["timestamp"],
                    "inputs": json.loads(row_dict["inputs"]) if row_dict["inputs"] else {},
                    "prediction": row_dict["prediction"],
                    "confidence": row_dict["confidence"],
                    "model_used": row_dict["model_used"],
                    "explanation": json.loads(row_dict["explanation"]) if row_dict["explanation"] else {},
                    "user_id": row_dict["user_id"],
                }
            return None


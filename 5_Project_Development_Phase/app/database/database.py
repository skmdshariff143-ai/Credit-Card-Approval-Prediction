import json
import os
import sqlite3
import contextlib
from datetime import datetime

from config.config import config

# Dynamic psycopg2 import support for backend-agnostic behavior
try:
    import psycopg2
    import psycopg2.extras
    from psycopg2 import IntegrityError as PgIntegrityError
except ImportError:
    psycopg2 = None
    PgIntegrityError = None

# Backend-agnostic IntegrityError tuple
INTEGRITY_ERRORS = (sqlite3.IntegrityError,)
if PgIntegrityError is not None:
    INTEGRITY_ERRORS += (PgIntegrityError,)


class DatabaseManager:
    """
    Manages dual database backends (SQLite / Supabase Postgres)
    for application prediction history and authentication.
    """

    def __init__(self):
        # Determine engine mode based on SUPABASE_DB_URL presence
        self.db_url = os.getenv("SUPABASE_DB_URL")
        self.use_postgres = bool(self.db_url)

        if not self.use_postgres:
            paths = config.get_paths()
            self.db_path = os.path.join(paths["logs_dir"], "prediction_history.db")
            try:
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            except Exception:
                pass

        try:
            self.init_db()
        except Exception as e:
            # Under read-only environments (like Vercel build stages), ignore write failure
            import logging

            logging.getLogger(__name__).warning(f"Database initialization deferred/ignored: {str(e)}")

    def _get_connection(self):
        if self.use_postgres:
            if psycopg2 is None:
                raise ImportError("psycopg2 is not installed but SUPABASE_DB_URL is configured.")
            # Remove "?pgbouncer=true" or other query parameters because psycopg2 does not support them in DSN
            url = self.db_url
            if "?" in url:
                url = url.split("?")[0]
            # Use DictCursor to emulate sqlite3.Row index/string key access
            conn = psycopg2.connect(url, cursor_factory=psycopg2.extras.DictCursor)
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn

    @contextlib.contextmanager
    def _connection(self):
        """Context manager to ensure connections are closed after use, preventing serverless leaks."""
        conn = self._get_connection()
        try:
            yield conn
        finally:
            conn.close()

    def _prepare_query(self, query: str) -> str:
        """Translates standard SQLite '?' parameters to PostgreSQL '%s' parameters if active."""
        if self.use_postgres:
            return query.replace("?", "%s")
        return query

    def init_db(self):
        """Initializes the database schema if it does not exist."""
        if self.use_postgres:
            migration_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "5_Project_Development_Phase",
                "migrations",
                "001_init_supabase.sql",
            )
            if not os.path.exists(migration_path):
                migration_path = os.path.join(config.BASE_DIR, "migrations", "001_init_supabase.sql")

            with open(migration_path, "r", encoding="utf-8") as f:
                sql = f.read()

            with self._connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()

            # Seed default users for Postgres
            self._seed_default_users_postgres()
        else:
            with self._connection() as conn:
                cursor = conn.cursor()
                self._create_prediction_tables(cursor)
                self._create_user_tables(cursor)
                self._run_user_migrations(cursor)
                self._seed_default_users(cursor)
                self._run_prediction_migrations(cursor)
                conn.commit()

    def _create_prediction_tables(self, cursor):
        # Core prediction history table (Phase 11 spec)
        cursor.execute("""
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
        cursor.execute("""
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
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_app_id ON prediction_history(application_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_timestamp ON prediction_history(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_income ON prediction_history(income);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_hist_risk ON prediction_history(risk_level);")

    def _create_user_tables(self, cursor):
        # Authentication: users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                full_name TEXT,
                role TEXT NOT NULL DEFAULT 'User',
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                last_login TEXT,
                status TEXT NOT NULL DEFAULT 'Active',
                is_admin INTEGER DEFAULT 0
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")

    def _run_user_migrations(self, cursor):
        # Add columns to users (safe migration for existing db)
        for col_name, col_type in [
            ("name", "TEXT"),
            ("full_name", "TEXT"),
            ("role", "TEXT NOT NULL DEFAULT 'User'"),
            ("last_login", "TEXT"),
            ("status", "TEXT NOT NULL DEFAULT 'Active'"),
        ]:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass

    def _seed_default_users(self, cursor):
        from werkzeug.security import generate_password_hash

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_pwd = os.getenv("ADMIN_PASSWORD")
        officer_email = os.getenv("OFFICER_EMAIL")
        officer_pwd = os.getenv("OFFICER_PASSWORD")
        demo_email = os.getenv("DEMO_EMAIL")
        demo_pwd = os.getenv("DEMO_PASSWORD")

        default_users = []
        if admin_email and admin_pwd:
            default_users.append(
                (os.getenv("ADMIN_USERNAME", "admin"), admin_email, admin_pwd, "Admin", "Administrator")
            )
        if officer_email and officer_pwd:
            default_users.append(
                (os.getenv("OFFICER_USERNAME", "officer"), officer_email, officer_pwd, "Loan Officer", "Officer")
            )
        if demo_email and demo_pwd:
            default_users.append((os.getenv("DEMO_USERNAME", "demo"), demo_email, demo_pwd, "Demo User", "User"))

        for username, email, pwd, name, role in default_users:
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if not cursor.fetchone():
                pwd_hash = generate_password_hash(pwd, method="scrypt")
                cursor.execute(
                    """INSERT INTO users (username, email, password_hash, name, full_name, role, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        username,
                        email,
                        pwd_hash,
                        name,
                        name,
                        role,
                        "Active",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )

    def _seed_default_users_postgres(self):
        from werkzeug.security import generate_password_hash

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_pwd = os.getenv("ADMIN_PASSWORD")
        officer_email = os.getenv("OFFICER_EMAIL")
        officer_pwd = os.getenv("OFFICER_PASSWORD")
        demo_email = os.getenv("DEMO_EMAIL")
        demo_pwd = os.getenv("DEMO_PASSWORD")

        default_users = []
        if admin_email and admin_pwd:
            default_users.append(
                (os.getenv("ADMIN_USERNAME", "admin"), admin_email, admin_pwd, "Admin", "Administrator")
            )
        if officer_email and officer_pwd:
            default_users.append(
                (os.getenv("OFFICER_USERNAME", "officer"), officer_email, officer_pwd, "Loan Officer", "Officer")
            )
        if demo_email and demo_pwd:
            default_users.append((os.getenv("DEMO_USERNAME", "demo"), demo_email, demo_pwd, "Demo User", "User"))

        with self._connection() as conn:
            with conn.cursor() as cursor:
                for username, email, pwd, name, role in default_users:
                    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                    if not cursor.fetchone():
                        pwd_hash = generate_password_hash(pwd, method="scrypt")
                        cursor.execute(
                            """INSERT INTO users (username, email, password_hash,
                               name, full_name, role, status, created_at)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                username,
                                email,
                                pwd_hash,
                                name,
                                name,
                                role,
                                "Active",
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            ),
                        )
            conn.commit()

    def _run_prediction_migrations(self, cursor):
        try:
            cursor.execute("ALTER TABLE prediction_history ADD COLUMN user_id INTEGER REFERENCES users(id)")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE prediction_history ADD COLUMN explanation TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE predictions ADD COLUMN model TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute("ALTER TABLE predictions ADD COLUMN explanation TEXT")
        except sqlite3.OperationalError:
            pass

        cursor.execute("""
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
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reports_app_id ON reports(application_id);")

    def check_connection(self) -> bool:
        """Verifies database connectivity."""
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            return True
        except Exception:
            return False

    def update_last_login(self, user_id):
        """Updates the last login timestamp for a user."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                self._prepare_query("UPDATE users SET last_login = ? WHERE id = ?"),
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id),
            )
            conn.commit()
            cursor.close()

    def create_user(self, username, email, password_hash, name=None, role="User", status="Active", full_name=None):
        """Creates a new user account. Returns user id or None on conflict."""
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                display_name = name or full_name or username
                cursor.execute(
                    self._prepare_query(
                        """INSERT INTO users (username, email, password_hash, name, full_name, role, status, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                    ),
                    (
                        username,
                        email,
                        password_hash,
                        display_name,
                        display_name,
                        role,
                        status,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )
                conn.commit()
                if self.use_postgres:
                    cursor.execute("SELECT LASTVAL()")
                    user_id = cursor.fetchone()[0]
                else:
                    user_id = cursor.lastrowid
                return user_id
            except INTEGRITY_ERRORS:
                return None
            finally:
                cursor.close()

    def get_user_by_id(self, user_id):
        """Retrieves a user record by primary key."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query("SELECT * FROM users WHERE id = ?"), (user_id,))
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row else None

    def get_user_by_email(self, email):
        """Retrieves a user record by email address."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query("SELECT * FROM users WHERE email = ?"), (email,))
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row else None

    def get_user_by_username(self, username):
        """Retrieves a user record by username."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query("SELECT * FROM users WHERE username = ?"), (username,))
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row else None

    def update_user_password(self, user_id, new_password_hash):
        """Updates a user's password hash."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                self._prepare_query("UPDATE users SET password_hash = ? WHERE id = ?"),
                (new_password_hash, user_id),
            )
            conn.commit()
            cursor.close()

    def update_user_profile(self, user_id, full_name, email):
        """Updates a user's profile details."""
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    self._prepare_query("UPDATE users SET full_name = ?, email = ? WHERE id = ?"),
                    (full_name, email, user_id),
                )
                conn.commit()
                return True
            except INTEGRITY_ERRORS:
                return False
            finally:
                cursor.close()

    def get_user_predictions(
        self, user_id, limit=50, search=None, sort_by="id", order="DESC", decision=None, risk_level=None
    ):
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

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query(query), tuple(params))
            rows = cursor.fetchall()
            cursor.close()

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
        with self._connection() as conn:
            cursor = conn.cursor()

            cursor.execute(self._prepare_query("SELECT COUNT(*) FROM prediction_history WHERE user_id = ?"), (user_id,))
            total = cursor.fetchone()[0] or 0

            cursor.execute(
                self._prepare_query(
                    "SELECT COUNT(*) FROM prediction_history WHERE user_id = ? AND prediction = 'Approved'"
                ),
                (user_id,),
            )
            approved = cursor.fetchone()[0] or 0

            cursor.execute(
                self._prepare_query(
                    "SELECT COUNT(*) FROM prediction_history WHERE user_id = ? AND prediction = 'Rejected'"
                ),
                (user_id,),
            )
            rejected = cursor.fetchone()[0] or 0

            cursor.execute(
                self._prepare_query("SELECT AVG(probability) FROM prediction_history WHERE user_id = ?"), (user_id,)
            )
            avg_prob = cursor.fetchone()[0]
            avg_prob = float(avg_prob) if avg_prob is not None else 0.0

            cursor.close()

            approval_rate = (approved / total * 100.0) if total > 0 else 0.0

            return {
                "total": total,
                "approved": approved,
                "rejected": rejected,
                "approval_rate": round(approval_rate, 2),
                "total_predictions": total,
                "total_approved": approved,
                "total_rejected": rejected,
                "avg_probability": avg_prob,
            }

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

        with self._connection() as conn:
            cursor = conn.cursor()

            # Insert into predictions (compat)
            cursor.execute(
                self._prepare_query(
                    "INSERT INTO predictions (timestamp, input_features, prediction, probability, model, explanation) "
                    "VALUES (?, ?, ?, ?, ?, ?)"
                ),
                (timestamp, raw_json, prediction, probability, model, explanation_json),
            )

            # Insert into prediction_history (new spec - Postgres uses ON CONFLICT, SQLite uses INSERT OR REPLACE)
            if self.use_postgres:
                cursor.execute(
                    """
                    INSERT INTO prediction_history (
                        application_id, timestamp, gender, income, employment,
                        experience, children, debt, prediction, probability,
                        risk_level, model, recommendation, raw_input, user_id, explanation
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (application_id) DO UPDATE SET
                        timestamp = EXCLUDED.timestamp,
                        gender = EXCLUDED.gender,
                        income = EXCLUDED.income,
                        employment = EXCLUDED.employment,
                        experience = EXCLUDED.experience,
                        children = EXCLUDED.children,
                        debt = EXCLUDED.debt,
                        prediction = EXCLUDED.prediction,
                        probability = EXCLUDED.probability,
                        risk_level = EXCLUDED.risk_level,
                        model = EXCLUDED.model,
                        recommendation = EXCLUDED.recommendation,
                        raw_input = EXCLUDED.raw_input,
                        user_id = EXCLUDED.user_id,
                        explanation = EXCLUDED.explanation
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
            else:
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
            if self.use_postgres:
                cursor.execute(
                    """
                    INSERT INTO reports (
                        application_id, timestamp, inputs, prediction, confidence, model_used, explanation, user_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (application_id) DO UPDATE SET
                        timestamp = EXCLUDED.timestamp,
                        inputs = EXCLUDED.inputs,
                        prediction = EXCLUDED.prediction,
                        confidence = EXCLUDED.confidence,
                        model_used = EXCLUDED.model_used,
                        explanation = EXCLUDED.explanation,
                        user_id = EXCLUDED.user_id
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
            else:
                cursor.execute(
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

            # Fetch last row id
            if self.use_postgres:
                cursor.execute("SELECT LASTVAL()")
                last_id = cursor.fetchone()[0]
            else:
                last_id = cursor.lastrowid

            cursor.close()
            return last_id

    def get_predictions(
        self,
        limit: int = 50,
        search: str = None,
        sort_by: str = "id",
        order: str = "DESC",
        decision=None,
        risk_level=None,
    ) -> list:
        """Retrieves history from database supporting filter, search, sorting."""
        query, params = self._build_predictions_query(limit, search, sort_by, order, decision, risk_level)
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query(query), tuple(params))
            rows = cursor.fetchall()
            cursor.close()
            return [self._parse_prediction_row(row) for row in rows]

    def _build_predictions_query(self, limit, search, sort_by, order, decision, risk_level):
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
        return query, params

    def _parse_prediction_row(self, row):
        row_dict = dict(row)
        explanation_data = {}
        if "explanation" in row_dict and row_dict["explanation"]:
            try:
                explanation_data = json.loads(row_dict["explanation"])
            except Exception:
                pass
        return {
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

    def get_admin_stats(self) -> dict:
        """Calculates statistics for admin dashboard metrics."""
        with self._connection() as conn:
            cursor = conn.cursor()

            # Total Predictions
            cursor.execute(self._prepare_query("SELECT COUNT(*) FROM prediction_history"))
            total = cursor.fetchone()[0] or 0

            # Approved Count
            cursor.execute(self._prepare_query("SELECT COUNT(*) FROM prediction_history WHERE prediction = 'Approved'"))
            approved = cursor.fetchone()[0] or 0

            # Rejected Count
            cursor.execute(self._prepare_query("SELECT COUNT(*) FROM prediction_history WHERE prediction = 'Rejected'"))
            rejected = cursor.fetchone()[0] or 0

            # Averages
            cursor.execute(self._prepare_query("SELECT AVG(income) FROM prediction_history"))
            avg_income = cursor.fetchone()[0] or 0.0

            cursor.execute(self._prepare_query("SELECT AVG(debt) FROM prediction_history"))
            avg_debt = cursor.fetchone()[0] or 0.0

            cursor.close()

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
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query("DELETE FROM prediction_history"))
            cursor.execute(self._prepare_query("DELETE FROM predictions"))
            cursor.execute(self._prepare_query("DELETE FROM reports"))
            conn.commit()
            cursor.close()

    def delete_prediction(self, application_id, user_id) -> bool:
        """Deletes a specific prediction history entry and its associated report."""
        with self._connection() as conn:
            cursor = conn.cursor()
            # Delete from history
            cursor.execute(
                self._prepare_query("DELETE FROM prediction_history WHERE application_id = ? AND user_id = ?"),
                (application_id, user_id),
            )
            rows_deleted = cursor.rowcount if not self.use_postgres else cursor.statusmessage.split()[-1]
            try:
                rows_deleted = int(rows_deleted)
            except Exception:
                rows_deleted = 1

            # Delete from reports
            cursor.execute(
                self._prepare_query("DELETE FROM reports WHERE application_id = ? AND user_id = ?"),
                (application_id, user_id),
            )
            conn.commit()
            cursor.close()
            return rows_deleted > 0

    def clear_user_history(self, user_id) -> bool:
        """Clears all prediction history and reports for a specific user."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query("DELETE FROM prediction_history WHERE user_id = ?"), (user_id,))
            cursor.execute(self._prepare_query("DELETE FROM reports WHERE user_id = ?"), (user_id,))
            conn.commit()
            cursor.close()
            return True

    def get_report_by_app_id(self, application_id, user_id=None) -> dict:
        """Retrieves report data directly from reports table."""
        query = "SELECT * FROM reports WHERE application_id = ?"
        params = [application_id]
        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._prepare_query(query), tuple(params))
            row = cursor.fetchone()
            cursor.close()

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

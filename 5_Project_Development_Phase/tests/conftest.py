"""Shared test fixtures for authenticated and unauthenticated Flask test clients."""

import pytest
from werkzeug.security import generate_password_hash

from app.app import create_app
from app.database.database import DatabaseManager
from app.models.user import User


@pytest.fixture
def app():
    """Create a fresh Flask app instance for testing."""
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False
    return test_app


@pytest.fixture
def client(app):
    """Authenticated Flask test client — auto-logs in a test user."""
    with app.test_client() as test_client:
        with app.app_context():
            # Create a test user in the database
            db = DatabaseManager()
            # Delete first to ensure correct role is assigned
            with db._get_connection() as conn:
                conn.execute("DELETE FROM users WHERE username = ? OR email = ?", ("testrunner", "testrunner@test.com"))
                conn.commit()
            password_hash = generate_password_hash("testpass123", method="scrypt")
            db.create_user(
                username="testrunner",
                email="testrunner@test.com",
                password_hash=password_hash,
                full_name="Test Runner",
                role="User",
            )
            user_row = db.get_user_by_username("testrunner")
            user = User.from_db_row(user_row)

            # Log in by calling the login endpoint directly
            from flask_login import login_user

            # Use the app's test_request_context to log in
            with app.test_request_context():
                login_user(user)

        # Set the session cookie by posting to the login form
        test_client.post(
            "/auth/login",
            data={
                "email": "testrunner@test.com",
                "password": "testpass123",
                "submit": "Sign In",
            },
            follow_redirects=True,
        )

        yield test_client


@pytest.fixture
def anon_client(app):
    """Unauthenticated Flask test client."""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def admin_client(app):
    """Authenticated Flask test client — auto-logs in an Administrator user."""
    with app.test_client() as test_client:
        with app.app_context():
            db = DatabaseManager()
            with db._get_connection() as conn:
                conn.execute("DELETE FROM users WHERE username = ? OR email = ?", ("testadmin", "testadmin@test.com"))
                conn.commit()
            password_hash = generate_password_hash("adminpass123", method="scrypt")
            db.create_user(
                username="testadmin",
                email="testadmin@test.com",
                password_hash=password_hash,
                full_name="Test Admin",
                role="Administrator",
            )
            user_row = db.get_user_by_username("testadmin")
            user = User.from_db_row(user_row)

            from flask_login import login_user

            with app.test_request_context():
                login_user(user)

        test_client.post(
            "/auth/login",
            data={
                "email": "testadmin@test.com",
                "password": "adminpass123",
                "submit": "Sign In",
            },
            follow_redirects=True,
        )

        yield test_client

"""User model implementing Flask-Login's UserMixin for session management."""

from flask_login import UserMixin


class User(UserMixin):
    """
    Represents an authenticated user. Wraps raw SQLite row dicts
    into a Flask-Login compatible object with session persistence.
    """

    def __init__(self, id, username, email, password_hash, full_name=None, created_at=None, is_admin=0):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name or username
        self.created_at = created_at
        self.is_admin = bool(is_admin)

    @staticmethod
    def from_db_row(row):
        """Constructs a User from a database dict row."""
        if row is None:
            return None
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            full_name=row.get("full_name"),
            created_at=row.get("created_at"),
            is_admin=row.get("is_admin", 0),
        )

    @property
    def initials(self):
        """Returns the first letter of full_name for avatar display."""
        name = self.full_name or self.username
        return name[0].upper() if name else "U"

    def __repr__(self):
        return f"<User {self.username} (id={self.id})>"

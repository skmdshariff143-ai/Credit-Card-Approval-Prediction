"""User model implementing Flask-Login's UserMixin for session management."""

from flask_login import UserMixin


class User(UserMixin):
    """
    Represents an authenticated user. Wraps raw SQLite row dicts
    into a Flask-Login compatible object with session persistence.
    """

    def __init__(
        self,
        id,
        username,
        email,
        password_hash,
        name=None,
        created_at=None,
        is_admin=0,
        role="User",
        last_login=None,
        status="Active",
        full_name=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.name = name or full_name or username
        self.full_name = self.name
        self.created_at = created_at
        self.is_admin = bool(is_admin) or (role == "Administrator")
        self.role = role
        self.last_login = last_login
        self.status = status

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
            name=row.get("name") or row.get("full_name"),
            created_at=row.get("created_at"),
            is_admin=row.get("is_admin", 0),
            role=row.get("role", "User"),
            last_login=row.get("last_login"),
            status=row.get("status", "Active"),
            full_name=row.get("full_name"),
        )

    @property
    def initials(self):
        """Returns the first letter of full_name for avatar display."""
        name = self.name or self.username
        return name[0].upper() if name else "U"

    def __repr__(self):
        return f"<User {self.username} (id={self.id})>"

"""Authentication routes: Register, Login, Logout, Forgot/Reset Password, Profile."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.database import DatabaseManager
from app.models.user import User
from app.routes.forms import (
    ForgotPasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

db_manager = DatabaseManager()


# ==================================================================
# Token Utilities
# ==================================================================


def _generate_reset_token(email):
    """Creates a timed token for password reset (30 min expiry)."""
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt="password-reset-salt")


def _verify_reset_token(token, max_age=1800):
    """Decodes a password reset token. Returns email or None."""
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None


# ==================================================================
# Registration
# ==================================================================


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check for existing username
        if db_manager.get_user_by_username(form.username.data.strip()):
            flash("Username is already taken. Please choose another.", "danger")
            return render_template("auth/register.html", form=form)

        # Check for existing email
        if db_manager.get_user_by_email(form.email.data.strip().lower()):
            flash("An account with this email already exists.", "danger")
            return render_template("auth/register.html", form=form)

        # Create user with scrypt password hash
        password_hash = generate_password_hash(form.password.data, method="scrypt")
        user_id = db_manager.create_user(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            password_hash=password_hash,
            full_name=form.full_name.data.strip(),
        )

        if user_id:
            logger.info(f"New user registered: {form.username.data} (id={user_id})")
            flash("Account created successfully! Please sign in.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Registration failed. Please try again.", "danger")

    return render_template("auth/register.html", form=form)


# ==================================================================
# Login
# ==================================================================


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))

    form = LoginForm()
    if form.validate_on_submit():
        row = db_manager.get_user_by_email(form.email.data.strip().lower())

        if row and check_password_hash(row["password_hash"], form.password.data):
            if row.get("status", "Active") != "Active":
                flash("Your account has been deactivated. Please contact support.", "danger")
                return render_template("auth/login.html", form=form)
            user = User.from_db_row(row)
            login_user(user, remember=form.remember_me.data)
            db_manager.update_last_login(user.id)
            logger.info(f"User logged in: {user.username} (id={user.id})")

            # Redirect to the page they were trying to access
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("api.index"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("auth/login.html", form=form)


# ==================================================================
# Logout
# ==================================================================


@auth_bp.route("/logout")
def logout():
    """Logs out the current user and clears the session."""
    if current_user.is_authenticated:
        logger.info(f"User logged out: {current_user.username} (id={current_user.id})")
        logout_user()
        flash("You have been signed out.", "info")
    return redirect(url_for("api.index"))


# ==================================================================
# Forgot Password
# ==================================================================


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Request a password reset token."""
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        row = db_manager.get_user_by_email(form.email.data.strip().lower())

        if row:
            token = _generate_reset_token(row["email"])
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            logger.info(f"Password reset requested for: {row['email']}")
            flash(
                f"A reset link has been generated. In production this would be emailed. "
                f"For now, use this link: {reset_url}",
                "info",
            )
        else:
            # Don't reveal whether the email exists (security)
            flash(
                "If an account with that email exists, a reset link has been sent.",
                "info",
            )

        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html", form=form)


# ==================================================================
# Reset Password
# ==================================================================


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Reset password using a valid timed token."""
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))

    email = _verify_reset_token(token)
    if not email:
        flash("The reset link is invalid or has expired. Please request a new one.", "danger")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        row = db_manager.get_user_by_email(email)
        if row:
            new_hash = generate_password_hash(form.password.data, method="scrypt")
            db_manager.update_user_password(row["id"], new_hash)
            logger.info(f"Password reset completed for: {email}")
            flash("Your password has been reset. Please sign in.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Account not found. Please register.", "danger")
            return redirect(url_for("auth.register"))

    return render_template("auth/reset_password.html", form=form, token=token)


# ==================================================================
# Profile
# ==================================================================


@auth_bp.route("/profile")
@login_required
def profile():
    """User profile page with personal prediction stats."""
    stats = db_manager.get_user_stats(current_user.id)
    recent = db_manager.get_user_predictions(current_user.id, limit=5)
    return render_template("auth/profile.html", stats=stats, recent=recent)


@auth_bp.route("/profile/edit", methods=["POST"])
@login_required
def profile_edit():
    """Update user profile details or password."""
    form_type = request.form.get("form_type", "profile")

    if form_type == "password":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")

        if not current_password or not new_password:
            flash("Current and new passwords are required.", "danger")
            return redirect(url_for("auth.profile"))

        if len(new_password) < 8:
            flash("New password must be at least 8 characters.", "danger")
            return redirect(url_for("auth.profile"))

        row = db_manager.get_user_by_id(current_user.id)
        if not row or not check_password_hash(row["password_hash"], current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("auth.profile"))

        new_hash = generate_password_hash(new_password, method="scrypt")
        db_manager.update_user_password(current_user.id, new_hash)
        flash("Password updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip().lower()

    if not full_name or not email:
        flash("Name and email are required.", "danger")
        return redirect(url_for("auth.profile"))

    existing = db_manager.get_user_by_email(email)
    if existing and existing["id"] != current_user.id:
        flash("That email is already in use by another account.", "danger")
        return redirect(url_for("auth.profile"))

    success = db_manager.update_user_profile(current_user.id, full_name, email)
    if success:
        flash("Profile updated successfully.", "success")
    else:
        flash("Failed to update profile. Please try again.", "danger")

    return redirect(url_for("auth.profile"))

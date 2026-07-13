import os
import smtplib
from email.mime.text import MIMEText
from app.utils.logger import get_logger

logger = get_logger(__name__)


def send_reset_email(email: str, reset_url: str):
    """
    Sends a password reset email.
    If MAIL_SUPPRESS_SEND=1, FLASK_ENV=development, or FLASK_ENV=testing,
    it only logs the link to log/console (does not send real email).
    """
    mail_suppress = os.getenv("MAIL_SUPPRESS_SEND", "0") == "1"
    flask_env = os.getenv("FLASK_ENV", "development")

    # Check if we should suppress sending email
    if mail_suppress or flask_env in ["development", "testing"]:
        logger.info(f"[DEV/TEST MAIL] Password reset requested for {email}. Link: {reset_url}")
        return True

    mail_server = os.getenv("MAIL_SERVER", "localhost")
    mail_port = int(os.getenv("MAIL_PORT", "25"))
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_use_tls = os.getenv("MAIL_USE_TLS", "0") == "1"
    sender = os.getenv("MAIL_DEFAULT_SENDER", "noreply@creditguard.ai")

    body = (
        f"Hello,\n\nYou requested a password reset. Click the link to reset your password:\n"
        f"{reset_url}\n\nIf you did not make this request, please ignore this email."
    )
    msg = MIMEText(body)

    msg["Subject"] = "CreditGuard AI - Password Reset Request"
    msg["From"] = sender
    msg["To"] = email

    try:
        server = smtplib.SMTP(mail_server, mail_port, timeout=5)
        if mail_use_tls:
            server.starttls()
        if mail_username and mail_password:
            server.login(mail_username, mail_password)

        server.sendmail(sender, [email], msg.as_string())
        server.quit()
        logger.info(f"Password reset email sent to: {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {str(e)}")
        # Log to log/console as fallback so the app does not break
        logger.info(f"[FALLBACK MAIL] Reset link for {email}: {reset_url}")
        return False

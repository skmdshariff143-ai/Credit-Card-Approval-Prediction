import os
import sys
from getpass import getpass

# Add the parent directory to sys.path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Try loading env variables via python-dotenv if installed
try:
    from dotenv import load_dotenv

    # Find .env at root or current directory
    load_dotenv()
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

from app.database.database import DatabaseManager
from werkzeug.security import generate_password_hash


def main():
    print("==========================================================")
    print("   CreditGuard AI Database Seeding & Setup Utility")
    print("==========================================================")

    # Initialize the Database Manager and run init_db to create tables
    db = DatabaseManager()
    db.init_db()

    # 1. Administrator credentials
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    # 2. Loan Officer credentials
    officer_username = os.getenv("OFFICER_USERNAME", "officer")
    officer_email = os.getenv("OFFICER_EMAIL")
    officer_password = os.getenv("OFFICER_PASSWORD")

    # 3. Client User credentials
    demo_username = os.getenv("DEMO_USERNAME", "demo")
    demo_email = os.getenv("DEMO_EMAIL")
    demo_password = os.getenv("DEMO_PASSWORD")

    # Fallback to interactive prompts for Admin if variables not set
    if not admin_email or not admin_password:
        print("\n[!] Environment variables for Admin account not found.")
        print("Please enter credentials to seed a local Administrator account:")
        admin_email = input("Admin Email: ").strip()
        admin_password = getpass("Admin Password: ").strip()

    if admin_email and admin_password:
        pwd_hash = generate_password_hash(admin_password, method="scrypt")
        user_id = db.create_user(
            username=admin_username,
            email=admin_email,
            password_hash=pwd_hash,
            name="Administrator",
            role="Administrator",
        )
        if user_id:
            print(f"[+] Successfully seeded Administrator: {admin_email}")
        else:
            print(f"[~] Administrator account already exists or conflict for: {admin_email}")

    # Seed Loan Officer if environment variables are set
    if officer_email and officer_password:
        pwd_hash = generate_password_hash(officer_password, method="scrypt")
        user_id = db.create_user(
            username=officer_username, email=officer_email, password_hash=pwd_hash, name="Loan Officer", role="Officer"
        )
        if user_id:
            print(f"[+] Successfully seeded Loan Officer: {officer_email}")
        else:
            print(f"[~] Loan Officer account already exists or conflict for: {officer_email}")

    # Seed Client User if environment variables are set
    if demo_email and demo_password:
        pwd_hash = generate_password_hash(demo_password, method="scrypt")
        user_id = db.create_user(
            username=demo_username, email=demo_email, password_hash=pwd_hash, name="Demo User", role="User"
        )
        if user_id:
            print(f"[+] Successfully seeded Client User: {demo_email}")
        else:
            print(f"[~] Client User account already exists or conflict for: {demo_email}")

    print("\nDatabase seeding completed successfully.")


if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv

# Load environment variables from a .env file (ensuring it's loaded from the project root)
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

class Config:
    """Configuration class for Flask application."""

    # Ensure compatibility with SQLAlchemy (fixing old `postgres://` format)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///fitness_scheduler.db")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://")

    # Disable SQLAlchemy modification tracking to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session security (generate one if not found)
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())

    # Ensure errors are properly propagated in the API
    PROPAGATE_EXCEPTIONS = True
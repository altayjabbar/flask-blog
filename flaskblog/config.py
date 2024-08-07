from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration settings for the Flask application.
    """

    # Secret key for Flask app
    SECRET_KEY: str = getenv("SECRET_KEY", "my_secret")

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI: str = getenv("SQLALCHEMY_DATABASE_URI")

    # Mail server settings
    MAIL_SERVER: str = "smtp.googlemail.com"
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = getenv("app_mail")
    MAIL_PASSWORD: str = getenv("app_pass")

    # Debug mode based on environment
    DEBUG: bool = True if getenv("FLASK_ENV") == "development" else False
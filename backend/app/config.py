import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "cloudcart-development-secret"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cloudcart.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

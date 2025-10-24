import os


class Config:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4-turbo")
    GPT_TEMPERATURE = float(os.getenv("GPT_TEMPERATURE", 0.7))
    GPT_MAX_TOKENS = int(os.getenv("GPT_MAX_TOKENS", 500))

    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173/")
    CORS_ORIGINS = [FRONTEND_URL]

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    APP_NAME = "EarthLens AI Backend"
    VERSION = "1.0.0"

class DevelopmentConfig(Config):
    """Configuration for local development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///dev.db")
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Configuration for production deployment."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")  
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Configuration for automated testing."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    LOG_LEVEL = "DEBUG"

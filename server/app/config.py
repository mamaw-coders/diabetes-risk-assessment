"""
Configuration module for the Flask application.

Supports environment-based configuration via .env file.
"""
import os
from pathlib import Path


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    # Application paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    ARTIFACTS_DIR = BASE_DIR / "artifacts"
    
    # ML Model settings
    MODEL_PATH = os.environ.get(
        "MODEL_PATH", 
        str(ARTIFACTS_DIR / "model.pkl")
    )
    
    # API settings
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


# Configuration mapping
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

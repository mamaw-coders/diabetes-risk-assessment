"""
Diabetes Risk Predictor - Flask Application Factory

This module provides the application factory pattern for creating
Flask application instances with proper configuration.
"""
from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.api import api_bp
from app.api.error_handlers import register_error_handlers


def create_app(config_class=Config):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_class: Configuration class to use (default: Config)
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Load ML model on startup
    with app.app_context():
        from app.models.ml_model import DiabetesModel
        DiabetesModel.get_instance()
    
    return app

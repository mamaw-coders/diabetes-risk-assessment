"""
API Blueprint - Presentation Layer

This module registers all API routes and exports the blueprint.
"""
from flask import Blueprint

api_bp = Blueprint("api", __name__)

# Import routes to register them with the blueprint
from app.api import routes  # noqa: F401, E402

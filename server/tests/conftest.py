"""
Test Configuration - Pytest Fixtures

Provides test fixtures for Flask application testing.
"""
import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app(TestingConfig)
    yield app


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the application."""
    return app.test_cli_runner()


@pytest.fixture
def sample_prediction_request():
    """Sample valid prediction request data."""
    return {
        "age": 45,
        "sex": "male",
        "weight": 85.0,
        "height": 175.0,
        "high_bp": True,
        "high_chol": True,
        "smoker": False,
        "stroke": False,
        "heart_disease": False,
        "phys_activity": True,
        "fruits": True,
        "veggies": True,
        "heavy_alcohol": False,
        "general_health": 3,
        "mental_health": 5,
        "physical_health": 3,
        "difficulty_walking": False,
    }

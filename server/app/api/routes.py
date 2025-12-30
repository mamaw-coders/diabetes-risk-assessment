"""
API Routes - Presentation Layer

Defines HTTP endpoints for the diabetes risk prediction API.
"""
from flask import jsonify, request

from app.api import api_bp
from app.api.schemas import PredictionRequestSchema, PredictionResponseSchema
from app.services.prediction_service import PredictionService

# Initialize schemas
prediction_request_schema = PredictionRequestSchema()
prediction_response_schema = PredictionResponseSchema()


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "diabetes-risk-predictor"
    })


@api_bp.route("/predict", methods=["POST"])
def predict():
    """
    Diabetes risk prediction endpoint.
    
    Accepts health indicators and returns risk assessment.
    
    Request Body:
        - age: int (years)
        - weight: float (kg)
        - height: float (cm)
        - high_bp: bool
        - high_chol: bool
        - smoker: bool
        - stroke: bool
        - heart_disease: bool
        - phys_activity: bool
        - fruits: bool
        - veggies: bool
        - heavy_alcohol: bool
        - general_health: int (1-5)
        - mental_health: int (0-30)
        - physical_health: int (0-30)
        - difficulty_walking: bool
        - sex: str ("male" or "female")
    
    Returns:
        JSON with risk level and probability
    """
    # Validate request data
    errors = prediction_request_schema.validate(request.json or {})
    if errors:
        return jsonify({
            "error": "Validation failed",
            "details": errors
        }), 422
    
    # Load validated data
    data = prediction_request_schema.load(request.json)
    
    # Get prediction from service
    prediction_service = PredictionService()
    result = prediction_service.predict(data)
    
    # Return response
    return jsonify(prediction_response_schema.dump(result))

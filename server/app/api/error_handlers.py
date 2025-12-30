"""
Error Handlers - Global Exception Handling

Provides consistent error responses across the API.
"""
from flask import jsonify
from marshmallow import ValidationError


def register_error_handlers(app):
    """Register global error handlers with the Flask app."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return jsonify({
            "error": "Bad Request",
            "message": str(error.description) if hasattr(error, 'description') else "Invalid request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle validation errors."""
        return jsonify({
            "error": "Validation Error",
            "message": str(error.description) if hasattr(error, 'description') else "Invalid input data"
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors."""
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors."""
        return jsonify({
            "error": "Validation Error",
            "details": error.messages
        }), 422
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle uncaught exceptions."""
        # Log the error in production
        app.logger.error(f"Unhandled exception: {str(error)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }), 500

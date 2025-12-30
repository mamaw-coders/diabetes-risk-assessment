"""
Route Tests - API Endpoint Testing

Tests for the /predict and /health endpoints.
"""
import json


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_service_info(self, client):
        """Health endpoint should return service information."""
        response = client.get("/health")
        data = json.loads(response.data)
        
        assert data["status"] == "healthy"
        assert data["service"] == "diabetes-risk-predictor"


class TestPredictEndpoint:
    """Tests for the prediction endpoint."""
    
    def test_predict_returns_200_with_valid_data(
        self, client, sample_prediction_request
    ):
        """Predict endpoint should return 200 with valid input."""
        response = client.post(
            "/predict",
            data=json.dumps(sample_prediction_request),
            content_type="application/json"
        )
        assert response.status_code == 200
    
    def test_predict_returns_expected_fields(
        self, client, sample_prediction_request
    ):
        """Predict endpoint should return all expected fields."""
        response = client.post(
            "/predict",
            data=json.dumps(sample_prediction_request),
            content_type="application/json"
        )
        data = json.loads(response.data)
        
        assert "risk_level" in data
        assert "probability" in data
        assert "bmi" in data
        assert "bmi_category" in data
        assert "disclaimer" in data
    
    def test_predict_returns_422_with_missing_fields(self, client):
        """Predict endpoint should return 422 when required fields are missing."""
        incomplete_data = {"age": 45}
        
        response = client.post(
            "/predict",
            data=json.dumps(incomplete_data),
            content_type="application/json"
        )
        assert response.status_code == 422
    
    def test_predict_returns_422_with_invalid_age(
        self, client, sample_prediction_request
    ):
        """Predict endpoint should return 422 when age is invalid."""
        sample_prediction_request["age"] = -5
        
        response = client.post(
            "/predict",
            data=json.dumps(sample_prediction_request),
            content_type="application/json"
        )
        assert response.status_code == 422
    
    def test_predict_calculates_correct_bmi(
        self, client, sample_prediction_request
    ):
        """Predict endpoint should calculate BMI correctly."""
        # Weight: 85kg, Height: 175cm
        # BMI = 85 / (1.75)^2 = 27.76
        response = client.post(
            "/predict",
            data=json.dumps(sample_prediction_request),
            content_type="application/json"
        )
        data = json.loads(response.data)
        
        expected_bmi = 85 / (1.75 ** 2)
        assert abs(data["bmi"] - expected_bmi) < 0.1

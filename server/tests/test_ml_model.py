"""
ML Model Tests

Tests for model loading and prediction functionality.
"""
from pathlib import Path

import numpy as np
import pytest


class TestModelLoading:
    """Tests for model loading functionality."""
    
    def test_model_artifact_exists(self):
        """Model artifact file should exist after training."""
        model_path = Path(__file__).parent.parent / "artifacts" / "model.pkl"
        assert model_path.exists(), f"Model file not found at {model_path}"
    
    def test_model_file_has_valid_size(self):
        """Model file should have reasonable size (not empty)."""
        model_path = Path(__file__).parent.parent / "artifacts" / "model.pkl"
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            assert size_mb > 1, f"Model file too small: {size_mb:.2f} MB"
            assert size_mb < 100, f"Model file too large: {size_mb:.2f} MB"


class TestModelMetadata:
    """Tests for model metadata structure."""
    
    @pytest.fixture
    def model_data(self):
        """Load model data from disk."""
        import joblib
        model_path = Path(__file__).parent.parent / "artifacts" / "model.pkl"
        if not model_path.exists():
            pytest.skip("Model file not found - run train_model.py first")
        return joblib.load(model_path)
    
    def test_model_data_has_model_key(self, model_data):
        """Model data should contain 'model' key."""
        assert isinstance(model_data, dict), "Model data should be a dictionary"
        assert "model" in model_data, "Model data should contain 'model' key"
    
    def test_model_data_has_feature_order(self, model_data):
        """Model data should contain feature order."""
        assert "feature_order" in model_data, "Model data should contain 'feature_order'"
        assert len(model_data["feature_order"]) == 21, "Should have 21 features"
    
    def test_model_data_has_metrics(self, model_data):
        """Model data should contain training metrics."""
        assert "metrics" in model_data, "Model data should contain 'metrics'"
        metrics = model_data["metrics"]
        assert "test_recall" in metrics, "Metrics should include test_recall"
        assert "test_roc_auc" in metrics, "Metrics should include test_roc_auc"


class TestModelPrediction:
    """Tests for model prediction functionality."""
    
    @pytest.fixture
    def model(self):
        """Load trained model."""
        import joblib
        model_path = Path(__file__).parent.parent / "artifacts" / "model.pkl"
        if not model_path.exists():
            pytest.skip("Model file not found - run train_model.py first")
        model_data = joblib.load(model_path)
        return model_data["model"]
    
    @pytest.fixture
    def sample_features(self):
        """Sample feature vector for testing."""
        # 21 features in order: HighBP, HighChol, CholCheck, BMI, Smoker, etc.
        return np.array([[
            1, 1, 1, 28.0, 0, 0, 0,  # HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDisease
            1, 1, 1, 0, 1, 0,        # PhysActivity, Fruits, Veggies, HvyAlcohol, AnyHealthcare, NoDocbcCost
            3, 5, 3, 0,              # GenHlth, MentHlth, PhysHlth, DiffWalk
            1, 7, 5, 7               # Sex, Age, Education, Income
        ]])
    
    def test_predict_returns_valid_class(self, model, sample_features):
        """Prediction should return 0 or 1."""
        prediction = model.predict(sample_features)
        assert prediction[0] in [0, 1], f"Invalid prediction: {prediction[0]}"
    
    def test_predict_proba_returns_valid_probabilities(self, model, sample_features):
        """Probability predictions should be between 0 and 1."""
        probabilities = model.predict_proba(sample_features)
        assert probabilities.shape == (1, 2), "Should return probabilities for 2 classes"
        assert 0 <= probabilities[0][0] <= 1, "Probability should be in [0, 1]"
        assert 0 <= probabilities[0][1] <= 1, "Probability should be in [0, 1]"
        assert abs(probabilities[0].sum() - 1.0) < 0.001, "Probabilities should sum to 1"


class TestFeatureOrderConsistency:
    """Tests for feature order consistency between training and inference."""
    
    def test_feature_order_matches_constants(self):
        """Feature order in trained model should match constants.py."""
        import joblib

        from app.utils.constants import FEATURE_ORDER as APP_FEATURE_ORDER
        
        model_path = Path(__file__).parent.parent / "artifacts" / "model.pkl"
        if not model_path.exists():
            pytest.skip("Model file not found - run train_model.py first")
        
        model_data = joblib.load(model_path)
        model_feature_order = model_data["feature_order"]
        
        assert model_feature_order == APP_FEATURE_ORDER, (
            f"Feature order mismatch!\n"
            f"Model: {model_feature_order}\n"
            f"App:   {APP_FEATURE_ORDER}"
        )

"""
ML Model - Data Access Layer

Handles loading, caching, and inference of the trained ML model.
Uses singleton pattern to ensure model is loaded only once.
"""
import os
import joblib
import numpy as np
from typing import Optional
from flask import current_app


class DiabetesModel:
    """
    Singleton class for diabetes prediction model.
    
    Ensures the model is loaded once and reused across requests.
    """
    
    _instance: Optional["DiabetesModel"] = None
    _model = None
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> "DiabetesModel":
        """
        Get the singleton instance, loading the model if necessary.
        
        Returns:
            DiabetesModel instance
        """
        if cls._instance is None:
            cls._instance = cls()
        if cls._model is None:
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self) -> None:
        """
        Load the trained model from disk.
        
        Raises:
            FileNotFoundError: If model file doesn't exist
            Exception: If model fails to load
        """
        try:
            model_path = current_app.config.get("MODEL_PATH")
            
            if not os.path.exists(model_path):
                current_app.logger.warning(
                    f"Model file not found at {model_path}. "
                    "Using mock predictions until model is trained."
                )
                self._model = None
                return
            
            self._model = joblib.load(model_path)
            current_app.logger.info(f"Model loaded successfully from {model_path}")
            
        except Exception as e:
            current_app.logger.error(f"Error loading model: {str(e)}")
            self._model = None
    
    def predict(self, features: np.ndarray) -> int:
        """
        Predict diabetes class (0 or 1).
        
        Args:
            features: NumPy array of shape (1, n_features)
        
        Returns:
            Predicted class (0 = No Diabetes, 1 = Diabetes)
        """
        if self._model is None:
            # Mock prediction for development/testing
            return self._mock_predict(features)
        
        return int(self._model.predict(features)[0])
    
    def predict_proba(self, features: np.ndarray) -> float:
        """
        Predict probability of diabetes.
        
        Args:
            features: NumPy array of shape (1, n_features)
        
        Returns:
            Probability of diabetes (0.0 to 1.0)
        """
        if self._model is None:
            # Mock probability for development/testing
            return self._mock_predict_proba(features)
        
        # Get probability of positive class (diabetes)
        probabilities = self._model.predict_proba(features)
        return float(probabilities[0][1])
    
    def _mock_predict(self, features: np.ndarray) -> int:
        """
        Generate mock prediction when model is not loaded.
        
        Uses simple heuristics based on key features.
        """
        prob = self._mock_predict_proba(features)
        return 1 if prob >= 0.5 else 0
    
    def _mock_predict_proba(self, features: np.ndarray) -> float:
        """
        Generate mock probability when model is not loaded.
        
        Uses BMI and other factors for rough approximation.
        """
        # Extract key features (assuming standard order)
        # This is a simplified mock - actual prediction will use the real model
        bmi = features[0][3] if len(features[0]) > 3 else 25
        high_bp = features[0][0] if len(features[0]) > 0 else 0
        age_cat = features[0][18] if len(features[0]) > 18 else 5
        
        # Simple scoring
        risk_score = 0.0
        
        # BMI impact
        if bmi >= 30:
            risk_score += 0.3
        elif bmi >= 25:
            risk_score += 0.15
        
        # Age impact
        if age_cat >= 9:  # 60+
            risk_score += 0.25
        elif age_cat >= 6:  # 45+
            risk_score += 0.15
        
        # High BP impact
        if high_bp:
            risk_score += 0.2
        
        # Base risk
        risk_score += 0.1
        
        # Clamp to valid range
        return min(max(risk_score, 0.0), 1.0)

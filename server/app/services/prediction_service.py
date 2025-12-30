"""
Prediction Service - Core Business Logic

Orchestrates the prediction workflow from raw input to risk assessment.
"""
from typing import Dict, Any, List

from app.services.preprocessing_service import PreprocessingService
from app.models.ml_model import DiabetesModel
from app.utils.constants import RISK_THRESHOLD, DISCLAIMER_TEXT


class PredictionService:
    """Service for diabetes risk prediction."""
    
    def __init__(self):
        """Initialize the prediction service."""
        self.preprocessing = PreprocessingService()
        self.model = DiabetesModel.get_instance()
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform diabetes risk prediction.
        
        Args:
            input_data: Validated input data from the API
        
        Returns:
            Dictionary containing risk assessment results
        """
        # Calculate BMI
        bmi = self.preprocessing.calculate_bmi(
            weight_kg=input_data["weight"],
            height_cm=input_data["height"]
        )
        bmi_category = self.preprocessing.get_bmi_category(bmi)
        
        # Prepare features for model
        features = self.preprocessing.prepare_features(input_data, bmi)
        
        # Get prediction
        probability = self.model.predict_proba(features)
        risk_level = "HIGH" if probability >= RISK_THRESHOLD else "LOW"
        
        # Identify contributing factors
        contributing_factors = self._identify_contributing_factors(input_data, bmi)
        
        return {
            "risk_level": risk_level,
            "probability": round(probability, 4),
            "bmi": round(bmi, 2),
            "bmi_category": bmi_category,
            "contributing_factors": contributing_factors,
            "disclaimer": DISCLAIMER_TEXT
        }
    
    def _identify_contributing_factors(
        self, 
        input_data: Dict[str, Any], 
        bmi: float
    ) -> List[str]:
        """
        Identify key factors contributing to risk assessment.
        
        Args:
            input_data: User's health data
            bmi: Calculated BMI
        
        Returns:
            List of contributing factor descriptions
        """
        factors = []
        
        # BMI factors
        if bmi >= 30:
            factors.append("Obesity (BMI ≥ 30)")
        elif bmi >= 25:
            factors.append("Overweight (BMI 25-29.9)")
        
        # Medical history
        if input_data.get("high_bp"):
            factors.append("High blood pressure")
        if input_data.get("high_chol"):
            factors.append("High cholesterol")
        if input_data.get("heart_disease"):
            factors.append("History of heart disease")
        if input_data.get("stroke"):
            factors.append("History of stroke")
        
        # Lifestyle
        if not input_data.get("phys_activity"):
            factors.append("Physical inactivity")
        if input_data.get("smoker"):
            factors.append("Smoking history")
        if input_data.get("heavy_alcohol"):
            factors.append("Heavy alcohol consumption")
        
        # Age factor
        age = input_data.get("age", 0)
        if age >= 45:
            factors.append(f"Age ({age} years)")
        
        # General health
        gen_health = input_data.get("general_health", 1)
        if gen_health >= 4:
            factors.append("Poor self-reported health")
        
        return factors[:5]  # Return top 5 factors

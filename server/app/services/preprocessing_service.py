"""
Preprocessing Service - Feature Engineering

Handles BMI calculation, feature normalization, and input transformation.
"""
from typing import Dict, Any, List
import numpy as np

from app.utils.constants import FEATURE_ORDER, AGE_CATEGORIES


class PreprocessingService:
    """Service for preprocessing health data for ML model."""
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """
        Calculate Body Mass Index from weight and height.
        
        Formula: BMI = weight_kg / (height_m)^2
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
        
        Returns:
            Calculated BMI value
        """
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def get_bmi_category(self, bmi: float) -> str:
        """
        Get BMI category based on WHO classifications.
        
        Args:
            bmi: Calculated BMI value
        
        Returns:
            BMI category string
        """
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_age_category(self, age: int) -> int:
        """
        Convert age to BRFSS age category (1-13).
        
        Categories:
        1: 18-24, 2: 25-29, 3: 30-34, 4: 35-39, 5: 40-44,
        6: 45-49, 7: 50-54, 8: 55-59, 9: 60-64, 10: 65-69,
        11: 70-74, 12: 75-79, 13: 80+
        
        Args:
            age: Age in years
        
        Returns:
            Age category (1-13)
        """
        for category, (min_age, max_age) in AGE_CATEGORIES.items():
            if min_age <= age <= max_age:
                return category
        return 13  # 80+ fallback
    
    def prepare_features(
        self, 
        input_data: Dict[str, Any], 
        bmi: float
    ) -> np.ndarray:
        """
        Transform input data into feature vector for model.
        
        Args:
            input_data: Validated user input
            bmi: Calculated BMI
        
        Returns:
            NumPy array of features in correct order
        """
        # Map input to model features
        features = {
            "HighBP": int(input_data["high_bp"]),
            "HighChol": int(input_data["high_chol"]),
            "CholCheck": 1,  # Assume cholesterol check done
            "BMI": bmi,
            "Smoker": int(input_data["smoker"]),
            "Stroke": int(input_data["stroke"]),
            "HeartDiseaseorAttack": int(input_data["heart_disease"]),
            "PhysActivity": int(input_data["phys_activity"]),
            "Fruits": int(input_data["fruits"]),
            "Veggies": int(input_data["veggies"]),
            "HvyAlcoholConsump": int(input_data["heavy_alcohol"]),
            "AnyHealthcare": 1,  # Assume has healthcare
            "NoDocbcCost": 0,  # Assume no cost barrier
            "GenHlth": input_data["general_health"],
            "MentHlth": input_data["mental_health"],
            "PhysHlth": input_data["physical_health"],
            "DiffWalk": int(input_data["difficulty_walking"]),
            "Sex": 1 if input_data["sex"] == "male" else 0,
            "Age": self.get_age_category(input_data["age"]),
            "Education": 5,  # Default to college graduate
            "Income": 7,  # Default to middle income
        }
        
        # Order features according to model training
        feature_vector = [features[name] for name in FEATURE_ORDER]
        
        return np.array(feature_vector).reshape(1, -1)

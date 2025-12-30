"""
Marshmallow Schemas - Request/Response Validation

Defines schemas for API input validation and output serialization.
"""
from marshmallow import Schema, fields, validate, post_load


class PredictionRequestSchema(Schema):
    """Schema for diabetes prediction request validation."""
    
    # Demographics
    age = fields.Integer(
        required=True,
        validate=validate.Range(min=18, max=120),
        metadata={"description": "Age in years"}
    )
    sex = fields.String(
        required=True,
        validate=validate.OneOf(["male", "female"]),
        metadata={"description": "Biological sex"}
    )
    
    # Vitals (for BMI calculation)
    weight = fields.Float(
        required=True,
        validate=validate.Range(min=20, max=500),
        metadata={"description": "Weight in kilograms"}
    )
    height = fields.Float(
        required=True,
        validate=validate.Range(min=50, max=250),
        metadata={"description": "Height in centimeters"}
    )
    
    # Medical History (boolean indicators)
    high_bp = fields.Boolean(
        required=True,
        metadata={"description": "Has high blood pressure"}
    )
    high_chol = fields.Boolean(
        required=True,
        metadata={"description": "Has high cholesterol"}
    )
    smoker = fields.Boolean(
        required=True,
        metadata={"description": "Has smoked at least 100 cigarettes in lifetime"}
    )
    stroke = fields.Boolean(
        required=True,
        metadata={"description": "Ever had a stroke"}
    )
    heart_disease = fields.Boolean(
        required=True,
        metadata={"description": "Has coronary heart disease or myocardial infarction"}
    )
    
    # Lifestyle
    phys_activity = fields.Boolean(
        required=True,
        metadata={"description": "Physical activity in past 30 days"}
    )
    fruits = fields.Boolean(
        required=True,
        metadata={"description": "Consumes fruit 1 or more times per day"}
    )
    veggies = fields.Boolean(
        required=True,
        metadata={"description": "Consumes vegetables 1 or more times per day"}
    )
    heavy_alcohol = fields.Boolean(
        required=True,
        metadata={"description": "Heavy alcohol consumption"}
    )
    
    # Health Status
    general_health = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=5),
        metadata={"description": "General health rating (1=excellent to 5=poor)"}
    )
    mental_health = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=30),
        metadata={"description": "Days of poor mental health in past 30 days"}
    )
    physical_health = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=30),
        metadata={"description": "Days of poor physical health in past 30 days"}
    )
    difficulty_walking = fields.Boolean(
        required=True,
        metadata={"description": "Difficulty walking or climbing stairs"}
    )
    
    @post_load
    def create_prediction_request(self, data, **kwargs):
        """Return validated data as dictionary."""
        return data


class PredictionResponseSchema(Schema):
    """Schema for diabetes prediction response."""
    
    risk_level = fields.String(
        metadata={"description": "Risk classification: LOW or HIGH"}
    )
    probability = fields.Float(
        metadata={"description": "Probability of diabetes (0.0 to 1.0)"}
    )
    bmi = fields.Float(
        metadata={"description": "Calculated BMI"}
    )
    bmi_category = fields.String(
        metadata={"description": "BMI category (Underweight, Normal, Overweight, Obese)"}
    )
    contributing_factors = fields.List(
        fields.String(),
        metadata={"description": "Key factors contributing to risk assessment"}
    )
    disclaimer = fields.String(
        metadata={"description": "Medical disclaimer"}
    )

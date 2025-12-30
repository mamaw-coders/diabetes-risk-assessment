"""
Constants - Application-wide Constants

Defines feature names, thresholds, and configuration values.
"""

# Risk threshold for classification
# Probability >= RISK_THRESHOLD = HIGH risk
RISK_THRESHOLD = 0.5

# Medical disclaimer for responses
DISCLAIMER_TEXT = (
    "This assessment is for informational purposes only and does not constitute "
    "medical advice, diagnosis, or treatment. Please consult a qualified healthcare "
    "provider for proper evaluation and guidance."
)

# Feature order matching the trained model
# These must match the order used during model training
FEATURE_ORDER = [
    "HighBP",
    "HighChol",
    "CholCheck",
    "BMI",
    "Smoker",
    "Stroke",
    "HeartDiseaseorAttack",
    "PhysActivity",
    "Fruits",
    "Veggies",
    "HvyAlcoholConsump",
    "AnyHealthcare",
    "NoDocbcCost",
    "GenHlth",
    "MentHlth",
    "PhysHlth",
    "DiffWalk",
    "Sex",
    "Age",
    "Education",
    "Income",
]

# Age category mapping (BRFSS format)
# Category: (min_age, max_age)
AGE_CATEGORIES = {
    1: (18, 24),
    2: (25, 29),
    3: (30, 34),
    4: (35, 39),
    5: (40, 44),
    6: (45, 49),
    7: (50, 54),
    8: (55, 59),
    9: (60, 64),
    10: (65, 69),
    11: (70, 74),
    12: (75, 79),
    13: (80, 150),  # 80+
}

# BMI categories (WHO classification)
BMI_CATEGORIES = {
    "Underweight": (0, 18.5),
    "Normal": (18.5, 25),
    "Overweight": (25, 30),
    "Obese": (30, 100),
}

# General health mapping
# 1 = Excellent, 2 = Very Good, 3 = Good, 4 = Fair, 5 = Poor
GENERAL_HEALTH_LABELS = {
    1: "Excellent",
    2: "Very Good",
    3: "Good",
    4: "Fair",
    5: "Poor",
}

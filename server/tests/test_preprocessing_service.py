"""
Preprocessing Service Tests

Tests for BMI calculation and feature engineering.
"""
import pytest

from app.services.preprocessing_service import PreprocessingService


class TestBMICalculation:
    """Tests for BMI calculation."""
    
    @pytest.fixture
    def service(self):
        """Create preprocessing service instance."""
        return PreprocessingService()
    
    def test_calculate_bmi_normal_weight(self, service):
        """BMI should be calculated correctly for normal weight."""
        # 70kg, 175cm -> BMI = 70 / 1.75^2 = 22.86
        bmi = service.calculate_bmi(weight_kg=70, height_cm=175)
        assert abs(bmi - 22.86) < 0.1
    
    def test_calculate_bmi_overweight(self, service):
        """BMI should be calculated correctly for overweight."""
        # 90kg, 175cm -> BMI = 29.39
        bmi = service.calculate_bmi(weight_kg=90, height_cm=175)
        assert bmi >= 25 and bmi < 30
    
    def test_calculate_bmi_obese(self, service):
        """BMI should be calculated correctly for obese."""
        # 100kg, 165cm -> BMI = 36.73
        bmi = service.calculate_bmi(weight_kg=100, height_cm=165)
        assert bmi >= 30


class TestBMICategory:
    """Tests for BMI category classification."""
    
    @pytest.fixture
    def service(self):
        """Create preprocessing service instance."""
        return PreprocessingService()
    
    def test_underweight_category(self, service):
        """BMI < 18.5 should be Underweight."""
        assert service.get_bmi_category(17.5) == "Underweight"
    
    def test_normal_category(self, service):
        """BMI 18.5-24.9 should be Normal."""
        assert service.get_bmi_category(22.0) == "Normal"
    
    def test_overweight_category(self, service):
        """BMI 25-29.9 should be Overweight."""
        assert service.get_bmi_category(27.5) == "Overweight"
    
    def test_obese_category(self, service):
        """BMI >= 30 should be Obese."""
        assert service.get_bmi_category(35.0) == "Obese"


class TestAgeCategory:
    """Tests for age category conversion."""
    
    @pytest.fixture
    def service(self):
        """Create preprocessing service instance."""
        return PreprocessingService()
    
    def test_young_adult_category(self, service):
        """Age 18-24 should be category 1."""
        assert service.get_age_category(20) == 1
    
    def test_middle_age_category(self, service):
        """Age 45-49 should be category 6."""
        assert service.get_age_category(47) == 6
    
    def test_senior_category(self, service):
        """Age 65-69 should be category 10."""
        assert service.get_age_category(67) == 10
    
    def test_elderly_category(self, service):
        """Age 80+ should be category 13."""
        assert service.get_age_category(85) == 13

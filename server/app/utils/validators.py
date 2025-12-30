"""
Validators - Input Validation Helpers

Provides reusable validation functions for health data.
"""
from typing import Any, Optional


def validate_positive(value: Any, field_name: str = "value") -> float:
    """
    Validate that a value is a positive number.
    
    Args:
        value: Value to validate
        field_name: Name of field for error messages
    
    Returns:
        The validated value as float
    
    Raises:
        ValueError: If value is not positive
    """
    try:
        num_value = float(value)
        if num_value <= 0:
            raise ValueError(f"{field_name} must be positive, got {value}")
        return num_value
    except (TypeError, ValueError) as e:
        raise ValueError(f"{field_name} must be a positive number: {str(e)}")


def validate_range(
    value: Any,
    min_val: float,
    max_val: float,
    field_name: str = "value"
) -> float:
    """
    Validate that a value is within a specified range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        field_name: Name of field for error messages
    
    Returns:
        The validated value as float
    
    Raises:
        ValueError: If value is outside the range
    """
    try:
        num_value = float(value)
        if not (min_val <= num_value <= max_val):
            raise ValueError(
                f"{field_name} must be between {min_val} and {max_val}, got {value}"
            )
        return num_value
    except (TypeError, ValueError) as e:
        raise ValueError(f"{field_name} validation failed: {str(e)}")


def validate_boolean(value: Any, field_name: str = "value") -> bool:
    """
    Validate and convert a value to boolean.
    
    Args:
        value: Value to validate (accepts bool, int, or string)
        field_name: Name of field for error messages
    
    Returns:
        Boolean value
    
    Raises:
        ValueError: If value cannot be converted to boolean
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        lower = value.lower()
        if lower in ("true", "yes", "1"):
            return True
        if lower in ("false", "no", "0"):
            return False
    raise ValueError(f"{field_name} must be a boolean value, got {value}")

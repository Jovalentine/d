from typing import Union, Any


class MathUtils:
    """Utility class for safe mathematical operations"""
    
    @staticmethod
    def safe_abs(value: Any) -> float:
        if value is None:
            raise TypeError("Cannot calculate absolute value of None")
        return abs(float(value))
    
    @staticmethod
    def safe_subtract(a: Any, b: Any) -> float:
        if a is None or b is None:
            raise TypeError("Cannot subtract None values")
        return float(a) - float(b)
    


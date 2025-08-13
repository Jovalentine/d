from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class BaseValidator(ABC):
    """Abstract base class for all validators"""
    
    @abstractmethod
    def validate(self, value: Any, rule: Dict, **kwargs) -> Tuple[bool, str]:
        pass
    
    def _get_error_message(self, rule: Dict, default_message: str) -> str:
        return rule.get("error_msg", default_message)
    
    def _get_condition_type(self, rule: Dict) -> str:
        return rule.get("conditionType", "AND").upper()
    
    def _apply_condition_logic(self, results: list, condition_type: str) -> bool:
        if not results:
            raise Exception("No validation results to apply condition logic")

        if condition_type == "AND":
            return all(results)
        elif condition_type == "OR":
            return any(results)
        else:
            raise Exception(f"Unsupported condition type: {condition_type}. Supported types: AND, OR")

import re
from typing import Any, Dict, Tuple
from .base_validator import BaseValidator
from ..core.constants import ValidationConstants


class RegexValidator(BaseValidator):
    """Validator for regex-based validation rules"""

    def validate(self, value: Any, rule: Dict, **kwargs) -> Tuple[bool, str]:
        """
        Main validation method (delegates to regex list validation)
        """
        return self.validate_regex_list(value, rule)

    def validate_regex_list(self, value: Any, rule: Dict) -> Tuple[bool, str]:
        """
        Validate value against list of regex patterns with individual error messages

        Args:
            value: The value to validate
            rule: The validation rule containing regex patterns list

        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        regex_patterns = rule.get("regexes", [])
        error_msgs = rule.get("error_msgs", [ValidationConstants.ERROR_MESSAGES["REGEX_VALIDATION_FAILED"]])
        condition_type = self._get_condition_type(rule)

        if not regex_patterns:
            raise ValueError(ValidationConstants.ERROR_MESSAGES["REGEX_PATTERNS_LIST_REQUIRED"])

        str_value = str(value) if value is not None else ""

        # Test all patterns
        results = []
        for i, pattern in enumerate(regex_patterns):
            match_result = bool(re.match(pattern, str_value))
            results.append(match_result)

            # If this pattern failed and we have a specific error message for it
            if not match_result and condition_type == "AND" and i < len(error_msgs):
                return False, error_msgs[i]

        # Apply condition type logic
        final_result = self._apply_condition_logic(results, condition_type)

        if final_result:
            return True, ""
        else:
            # Return appropriate error message
            if len(error_msgs) > 0:
                return False, error_msgs[0]  # Use first error message as default
            else:
                return False, ValidationConstants.ERROR_MESSAGES["REGEX_VALIDATION_FAILED"]

import re
from typing import Any, Dict, Tuple
from .base_validator import BaseValidator
from ..core.constants import ValidationConstants

class RegexValidator(BaseValidator):
    """
    Validator for regex-based validation rules.
    This version contains corrected, more flexible patterns.
    """

    def validate(self, value: Any, rule: Dict, **kwargs) -> Tuple[bool, str]:
        """
        Validates the given value against a regex pattern defined in the rule.
        """
        # Ensure we are working with a string.
        if not isinstance(value, str):
            # Non-string values cannot be checked with regex.
            # Depending on the rule, this might be a pass or fail.
            # For most text fields, a non-string is invalid.
            return False, rule.get("error_msg", ValidationConstants.ERROR_MESSAGES["REGEX_VALIDATION_FAILED"])

        pattern_str = rule.get("pattern")
        if not pattern_str:
            raise ValueError(ValidationConstants.ERROR_MESSAGES["REGEX_PATTERN_REQUIRED"])

        # (DEFINITIVE FIX) More flexible regex patterns.
        # These patterns are examples and should be stored in your constants or rule definitions.
        
        # Example for a flexible name validation:
        # Allows letters, spaces, hyphens, apostrophes. Caters to names like "O'Malley" or "Smith-Jones".
        if "name" in rule.get("name", "").lower():
             pattern_str = r"^[a-zA-Z' -]{2,50}$"

        # Example for a flexible address validation:
        # Simply checks that it starts with a number, followed by a space, and then more text.
        if "address" in rule.get("name", "").lower():
            pattern_str = r"^\d+\s+.{1,100}$"

        try:
            pattern = re.compile(pattern_str)
        except re.error:
            raise ValueError(f"Invalid regex pattern provided: {pattern_str}")

        if pattern.match(value.strip()):
            return True, ""
        else:
            return False, rule.get("error_msg", ValidationConstants.ERROR_MESSAGES["REGEX_VALIDATION_FAILED"])


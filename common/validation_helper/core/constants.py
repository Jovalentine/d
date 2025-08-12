class ValidationConstants:
    """Constants used throughout the validation system"""

    # Default values
    DEFAULT_CONDITION_TYPE = "AND"
    DEFAULT_ERROR_MESSAGE = "Validation failed"

    # Field reference patterns
    FIELD_REFERENCE_PATTERN = r'\b([a-zA-Z_][a-zA-Z0-9_-]*\.[a-zA-Z_][a-zA-Z0-9_-]*(?:\.[a-zA-Z_][a-zA-Z0-9_-]*)*)\b'
    VALUE_REFERENCE_PATTERN = r'\bvalue\b'

    # Mathematical operation patterns
    ABS_SUBTRACT_PATTERN = r'abs\(([^)]+)\s*-\s*([^)]+)\)'

    # Safe evaluation allowed names
    SAFE_EVAL_ALLOWED_NAMES = {
        "__builtins__": {},
        "True": True,
        "False": False,
        "None": None,
        "max": max,
        "min": min
    }
    # Values that should be treated as None/null in expressions
    NULL_PLACEHOLDER_VALUES = {
        "N/A", "n/a", "NA", "na",
        "NULL", "null", "NONE", "none",
        "-", "", "undefined", "UNDEFINED"
    }

    # Error message templates
    ERROR_MESSAGES = {
        "REQUIRED_FIELD": "Field is required",
        "REGEX_VALIDATION_FAILED": "Value does not match required pattern",
        "EXPRESSION_VALIDATION_FAILED": "Expression validation failed",
        "UNSUPPORTED_VALIDATION_TYPE": "Unsupported validation type: {type}. Supported types: {supported_types}",
        "EXPRESSIONS_LIST_REQUIRED": "Expressions list is required for EXPRESSION_TYPE_LIST validation",
        "REGEX_PATTERNS_LIST_REQUIRED": "Regex patterns list not specified",
        "EXPRESSION_EVALUATION_ERROR": "Expression validation error: {error}",
        "REGEX_VALIDATION_ERROR": "Regex validation error: {error}",
        "INVALID_FORMAT": "Invalid format detected",
        "NULL_VALUE_NOT_ALLOWED": "Null or placeholder value not allowed"
    }
import re
from datetime import datetime
from typing import Any, Dict, Tuple
from .base_validator import BaseValidator
from ..core.constants import ValidationConstants
from ..utils.math_utils import MathUtils


class ExpressionValidator(BaseValidator):
    """Validator for expression-based validation rules"""

    def __init__(self):
        """Initialize expression validator with math utilities"""
        self.math_utils = MathUtils()

    def validate(self, value: Any, rule: Dict, **kwargs) -> Tuple[bool, str]:
        """
        Main validation method (delegates to expression list validation)
        """
        return self.validate_expression_list(value, rule, **kwargs)

    def validate_expression_list(self, field_value: Any, rule: Dict, config: Dict,
                               all_data: Dict = None, current_group: str = None,
                               current_field: str = None) -> Tuple[bool, str]:
        """
        Validate using list of expressions with individual error messages

        Args:
            field_value: The value to validate
            rule: The validation rule containing expressions list
            config: Global configuration
            all_data: All data for cross-field validation
            current_group: Current group name
            current_field: Current field name

        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        expressions = rule.get("expressions", [])
        error_msgs = rule.get("error_msgs", [ValidationConstants.ERROR_MESSAGES["EXPRESSION_VALIDATION_FAILED"]])
        condition_type = self._get_condition_type(rule)

        if not expressions:
            raise ValueError(ValidationConstants.ERROR_MESSAGES["EXPRESSIONS_LIST_REQUIRED"])

        # Evaluate all expressions
        results = []
        for i, expr in enumerate(expressions):
            result = self._evaluate_direct_expression(
                expr, field_value, all_data, current_group, current_field, config
            )
            results.append(result)

            # If this expression failed and we have a specific error message for it
            if not result and i < len(error_msgs):
                return False, error_msgs[i]

        # Apply condition type logic
        final_result = self._apply_condition_logic(results, condition_type)

        # Return appropriate error message
        if not final_result:
            if len(error_msgs) > 0:
                return False, error_msgs[0]  # Use first error message as default
            else:
                return False, ValidationConstants.ERROR_MESSAGES["EXPRESSION_VALIDATION_FAILED"]

        return True, ""

    def _evaluate_direct_expression(self, expression: str, field_value: Any, all_data: Dict,
                                   current_group: str, current_field: str, config: Dict) -> bool:
        """
        Evaluate direct Python expressions with field references

        Args:
            expression: The expression to evaluate
            field_value: Current field value
            all_data: All data for cross-field validation
            current_group: Current group name
            current_field: Current field name
            config: Global configuration

        Returns:
            Boolean result of expression evaluation
        """
        # Replace field references with actual values
        processed_expression = self._replace_field_references(
            expression, field_value, all_data, current_group, current_field
        )

        # Execute the processed expression
        return self._execute_direct_expression(processed_expression)

    def _replace_field_references(self, expression: str, field_value: Any, all_data: Dict,
                                 current_group: str, current_field: str) -> str:
        """
        Replace field references like 'mv1.value', 'bos.buyer_name' with actual values

        Args:
            expression: The expression containing field references
            field_value: Current field value
            all_data: All data for cross-field validation
            current_group: Current group name
            current_field: Current field name

        Returns:
            Processed expression with field references replaced
        """
        processed_expression = expression

        # Find all field references using regex pattern
        field_refs = re.findall(ValidationConstants.FIELD_REFERENCE_PATTERN, expression)

        for field_ref in field_refs:
            # Skip malformed references that start with a dot
            if field_ref.startswith('.'):
                # Replace malformed reference with None
                processed_expression = processed_expression.replace(field_ref, 'None')
                continue

            actual_value = self._get_field_value_by_reference(field_ref, all_data, current_group)
            formatted_value = self._format_value_for_direct_expression(actual_value)
            processed_expression = processed_expression.replace(field_ref, formatted_value)

        # Replace standalone 'value' with current field value (only if not already replaced as part of a field reference)
        if re.search(ValidationConstants.VALUE_REFERENCE_PATTERN, processed_expression):
            processed_expression = re.sub(
                ValidationConstants.VALUE_REFERENCE_PATTERN,
                self._format_value_for_direct_expression(field_value),
                processed_expression
            )
        return processed_expression

    def _get_field_value_by_reference(self, field_ref: str, all_data: Dict, current_group: str = None) -> Any:
        """
        Get field value by reference like 'mv1.year' or 'bos.buyer_name.value'

        Args:
            field_ref: Field reference string
            all_data: All data for cross-field validation
            current_group: Current group name

        Returns:
            Field value or None if not found
        """
        if not all_data or "groups" not in all_data:
            return None

        parts = field_ref.split('.')
        if len(parts) < 2:
            return None

        group_name = parts[0]
        field_path = parts[1:]

        groups = all_data["groups"]
        if group_name not in groups:
            return None

        # Navigate through the field path
        current_data = groups[group_name].get("fields", {})

        for part in field_path:
            if isinstance(current_data, dict) and part in current_data:
                current_data = current_data[part]
            else:
                return None

        return current_data

    def _format_value_for_direct_expression(self, value: Any) -> str:
        """
        Format a value for use in direct expressions

        Args:
            value: The value to format (accepts any type including string)

        Returns:
            Formatted string representation for expression evaluation
        """

        # Handle None values
        if value is None:
            return "None"

        # Handle string values
        if isinstance(value, str):
            # Handle empty strings
            if value.strip() == "":
                return "None"

            # Handle placeholder values that should be treated as None (configurable)
            if value.strip() in ValidationConstants.NULL_PLACEHOLDER_VALUES:
                return "None"

            # Escape quotes and wrap in quotes for valid string values
            escaped_value = value.replace("'", "\\'").replace('"', '\\"')
            return f'"{escaped_value}"'

        # Handle other types (numbers, booleans, etc.)
        return str(value)

    def _execute_direct_expression(self, expression: str) -> bool:
        """
        Execute direct Python expression safely

        Args:
            expression: The Python expression to execute

        Returns:
            Boolean result of expression evaluation

                Raises:
            Exception: If expression evaluation fails or if expression is not a string
        """
        # Validate that expression is a string
        if not isinstance(expression, str):
            raise TypeError(f"Expression must be a string, got {type(expression).__name__}: {expression}")

        if not expression.strip():
            raise ValueError("Expression cannot be empty or whitespace only")

        try:
            # Simple date comparison function
            def date_is_future(date_str):
                try:
                    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                    return date_obj.date() >= datetime.now().date()
                except:
                    return False

            # Safe evaluation with essential functions only
            allowed_names = ValidationConstants.SAFE_EVAL_ALLOWED_NAMES.copy()
            allowed_names.update({
                "abs": self.math_utils.safe_abs,
                "safe_subtract": self.math_utils.safe_subtract,
                "date_is_future": date_is_future
            })

            result = eval(expression, allowed_names, {})
            return bool(result)
        except Exception:
            # For any evaluation errors (syntax, runtime, etc.), return False
            # This allows validation to continue even with malformed rules
            return False


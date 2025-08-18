import re
from datetime import datetime
from typing import Any, Dict, Tuple
from decimal import Decimal, InvalidOperation

# This assumes the project structure allows these relative imports.
from .base_validator import BaseValidator
from ..core.constants import ValidationConstants
from ..utils.math_utils import MathUtils


class ExpressionValidator(BaseValidator):
    """
    Validator for expression-based validation rules.
    This definitive version uses a universal normalizer and removes extractor IDs.
    """

    def __init__(self):
        """Initialize expression validator with math utilities."""
        self.math_utils = MathUtils()

    def validate(self, value: Any, rule: Dict, **kwargs) -> Tuple[bool, str]:
        """Main validation method which delegates to the expression list validator."""
        return self.validate_expression_list(value, rule, **kwargs)

    def validate_expression_list(self, field_value: Any, rule: Dict, config: Dict,
                                 all_data: Dict = None, current_group: str = None,
                                 current_field: str = None) -> Tuple[bool, str]:
        """Validates a field using a list of expressions defined in a rule."""
        expressions = rule.get("expressions", [])
        error_msgs = rule.get("error_msgs", [ValidationConstants.ERROR_MESSAGES["EXPRESSION_VALIDATION_FAILED"]])
        condition_type = self._get_condition_type(rule)

        if not expressions:
            raise ValueError(ValidationConstants.ERROR_MESSAGES["EXPRESSIONS_LIST_REQUIRED"])

        results = []
        for i, expr in enumerate(expressions):
            try:
                result = self._evaluate_expression_with_context(expr, field_value, all_data)
                results.append(result)
                if not result and i < len(error_msgs):
                    return False, error_msgs[i]
            except Exception as e:
                print(f"ERROR: Could not validate expression '{expr}'. Reason: {e}")
                results.append(False)
                if i < len(error_msgs):
                    return False, error_msgs[i]
                break

        final_result = self._apply_condition_logic(results, condition_type)
        if not final_result:
            return False, error_msgs[0] if error_msgs else ValidationConstants.ERROR_MESSAGES["EXPRESSION_VALIDATION_FAILED"]

        return True, ""

    def _normalize_for_comparison(self, value: Any) -> Any:
        """A universal normalizer for all string comparisons."""
        if isinstance(value, str):
            return re.sub(r'[^a-z0-9]', '', value.lower())
        return value

    def _get_field_value_by_reference(self, field_ref: str, all_data: Dict) -> Any:
        """Retrieves a field's raw value from the JSON data structure."""
        if not all_data or "data" not in all_data or "attributes" not in all_data["data"] or "groups" not in all_data["data"]["attributes"] or '.' not in field_ref:
            return None
        try:
            group_name_from_ref, field_path_str = field_ref.split('.', 1)
            groups_list = all_data["data"]["attributes"]["groups"]
            if not isinstance(groups_list, list): return None

            target_group = None
            for group in groups_list:
                if isinstance(group, dict) and group.get("name", "").lower() == group_name_from_ref.lower():
                    target_group = group
                    break
            if not target_group: return None

            fields_dict = {k.lower(): v for k, v in target_group.get("fields", {}).items()}
            current_data = None
            field_path = field_path_str.lower().split('.')
            
            if field_path[0] in fields_dict:
                 current_data = fields_dict[field_path[0]]
            else:
                 return None

            while isinstance(current_data, dict) and 'value' in current_data:
                current_data = current_data['value']

            return current_data
        except Exception:
            return None

    def _clean_and_convert_value(self, value: Any) -> Any:
        """
        (DEFINITIVE FIX) Cleans and converts any value before it is used.
        This is now the single point for stripping IDs and handling types.
        """
        if not isinstance(value, str):
            return value # Return non-strings (like None or numbers) immediately.

        # 1. Remove the [Id: ...] metadata string from the extracted value.
        # This regex finds and removes the pattern " [Id: ...]" from the end of the string.
        cleaned_value = re.sub(r'\s*\[Id:.*?\]\s*$', '', value).strip()

        # 2. Check for placeholder values that should be treated as None.
        if cleaned_value.upper() in ValidationConstants.NULL_PLACEHOLDER_VALUES or cleaned_value == "":
            return None

        # 3. Attempt to convert to a number for mathematical comparisons.
        cleaned_for_decimal = re.sub(r'[$,]', '', cleaned_value)
        try:
            return Decimal(cleaned_for_decimal)
        except InvalidOperation:
            # If not a number, return the cleaned string for text comparisons.
            return cleaned_value

    def _sanitize_variable_name(self, field_ref: str) -> str:
        """Converts a field reference into a valid Python identifier."""
        return re.sub(r'[^a-zA-Z0-9_]', '_', field_ref)

    def _evaluate_expression_with_context(self, expression: str, field_value: Any, all_data: Dict) -> bool:
        """Orchestrates the lookup, cleaning, normalization, and safe evaluation."""
        field_refs = sorted(list(set(re.findall(ValidationConstants.FIELD_REFERENCE_PATTERN, expression))), key=len, reverse=True)
        eval_context = {}
        transformed_expression = expression

        for ref in field_refs:
            sanitized_name = self._sanitize_variable_name(ref)
            
            # Get the raw value, either from the current field or by looking it up.
            if ref.lower() == 'value':
                raw_value = field_value
            else:
                raw_value = self._get_field_value_by_reference(ref, all_data)
            
            # Apply the universal cleaning and conversion function.
            cleaned_value = self._clean_and_convert_value(raw_value)
            
            # If the result is a string, normalize it for robust comparison.
            if isinstance(cleaned_value, str):
                final_value = self._normalize_for_comparison(cleaned_value)
            else:
                # For Decimals, dates, None, etc., no further normalization is needed.
                final_value = cleaned_value

            eval_context[sanitized_name] = final_value
            transformed_expression = re.sub(r'\b' + re.escape(ref) + r'\b', sanitized_name, transformed_expression)
            
        return self._execute_safely(transformed_expression, eval_context)

    def _execute_safely(self, expression: str, context: Dict) -> bool:
        """Executes the final expression string in a controlled, safe environment."""
        if not isinstance(expression, str) or not expression.strip():
            return False
        try:
            def date_is_future(date_str):
                if not isinstance(date_str, str): return False
                try:
                    return datetime.strptime(date_str, "%m/%d/%Y").date() >= datetime.now().date()
                except (ValueError, TypeError): return False

            allowed_globals = {
                "__builtins__": {"None": None, "True": True, "False": False},
                **ValidationConstants.SAFE_EVAL_ALLOWED_NAMES,
                "abs": self.math_utils.safe_abs,
                "safe_subtract": self.math_utils.safe_subtract,
                "date_is_future": date_is_future
            }
            result = eval(expression, allowed_globals, context)
            return bool(result)
        except Exception as e:
            print(f"CRITICAL: Failed to evaluate expression='{expression}' with context={context}. Error: {e}")
            return False

    def _get_condition_type(self, rule: Dict) -> str:
        """Determines if multiple expressions should be combined with AND or OR."""
        return rule.get("condition_type", "AND").upper()

    def _apply_condition_logic(self, results: list, condition_type: str) -> bool:
        """Applies the AND/OR logic to a list of boolean results."""
        if not results: return True
        return all(results) if condition_type == "AND" else any(results)

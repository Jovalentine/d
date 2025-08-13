from typing import Dict, Any, List
from .enums import ValidationType
from ..validators.regex_validator import RegexValidator
from ..validators.expression_validator import ExpressionValidator


class ValidationEngine:

    def __init__(self):
        self.regex_validator = RegexValidator()
        self.expression_validator = ExpressionValidator()

    def validate_field(self, field_value: Any, field_config: Dict, config: Dict,
                       all_data: Dict = None, current_group: str = None,
                       current_field: str = None) -> List[str]:
        field_errors = []

        validation_rules = field_config.get("validation_rules", [])
        for rule in validation_rules:
            validation_type = rule.get("validation_type")

            validation_enum = ValidationType(validation_type)

            is_valid, error_msg = self._dispatch_field_validation(
                validation_enum, field_value, rule, config, all_data, current_group, current_field
            )

            if not is_valid:
                field_errors.append(error_msg)
                break

        return field_errors

    def _dispatch_field_validation(self, validation_type: ValidationType, field_value: Any,
                                   rule: Dict, config: Dict, all_data: Dict,
                                   current_group: str, current_field: str) -> tuple:

        match validation_type:
            case ValidationType.REGEX_LIST:
                return self.regex_validator.validate_regex_list(field_value, rule)

            case ValidationType.EXPRESSION_TYPE_LIST:
                return self.expression_validator.validate_expression_list(
                    field_value, rule, config, all_data, current_group, current_field
                )

            case _:
                raise ValueError(f"Unsupported validation type: {validation_type.value}")

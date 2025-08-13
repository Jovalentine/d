from typing import Dict, Tuple, List
from ..validation_helper.core.validation_engine import ValidationEngine


class ValidatorExecution:
    """Main ValidatorExecution class that orchestrates worksheet validation using the new ValidationEngine"""

    def __init__(self):
        self.validation_engine = ValidationEngine()

    def validate_data(self, data: dict, config: Dict) -> Tuple[bool, dict]:
        """Validate worksheet data against configuration rules"""
        config_data = self._extract_validation_config(config)
        if not config_data:
            raise ValueError("No validation rules found in the configuration")

        all_valid = True

        # Initialize group-level exceptions at the top level
        if "bre_exceptions" not in data:
            data["bre_exceptions"] = {}

        # First, handle group-level validations (where groups: [] is empty)
        group_level_rules = self._find_validation_rules(config_data, is_group_level=True)
        for rule in group_level_rules:
            # For group-level validations, we validate against the entire data structure
            field_config = {
                "validation_rules": [rule]
            }
            rule_errors = self.validation_engine.validate_field(
                data, field_config, config_data, data, None, None
            )
            if rule_errors:
                all_valid = False
                rule_id = rule.get("id", "unknown_rule")
                data["bre_exceptions"][rule_id] = "; ".join(rule_errors)

        # Then handle field-level validations
        groups = data.get("groups", {})

        for group_name, group_data in groups.items():
            fields = group_data.get("fields", {})

            for field_name, field_data in fields.items():
                field_value = field_data.get("value") if isinstance(field_data, dict) else field_data

                # Get field-specific rules using the same function
                field_rules = self._find_validation_rules(
                    config_data,
                    is_group_level=False,
                    group_name=group_name,
                    field_name=field_name
                )

                if not field_rules:
                    continue

                field_config = {
                    "validation_rules": field_rules
                }

                try:
                    field_errors = self.validation_engine.validate_field(
                        field_value, field_config, config_data, data, group_name, field_name
                    )

                    if field_errors:
                        all_valid = False
                        data["groups"][group_name]["fields"][field_name]["message"] = "; ".join(field_errors)
                        data["groups"][group_name]["fields"][field_name]["pass"] = False
                except Exception as e:
                    continue

        return all_valid, data

    def _extract_validation_config(self, config: Dict) -> list:
        """Extract validation configuration from config"""
        # The new structure has 'properties' as a list of validation rule groups
        if 'properties' in config:
            return config['properties']
        # Fallback for backward compatibility - return empty list if no properties
        return []

    def _find_validation_rules(self, config_data: list, is_group_level: bool = False,
                               group_name: str = None, field_name: str = None) -> List[Dict]:
        """
        Find validation rules based on the criteria:
        - If is_group_level=True: Find rules where groups is empty or not present
        - If is_group_level=False: Find rules for specific group.field.value pattern
        """
        found_rules = []

        for property_group in config_data:
            validation_rules = property_group.get("validation_rules", [])
            for rule in validation_rules:

                if is_group_level:
                    # Check if groups is empty or not present (indicating top-level validation)
                    groups = rule.get("groups", [])
                    if not groups:  # Empty list means it's a group-level validation
                        converted_rule = self._convert_rule_format(rule)
                        converted_rule["id"] = rule.get("id", "")  # Keep the id for group-level rules
                        found_rules.append(converted_rule)

                else:
                    # Field-level validation: look for rules that match group.field pattern
                    rule_id = rule.get("id", "")
                    target_pattern_prefix = f"{group_name}.{field_name}."

                    # Match both .value and .consistency rules for the field
                    if rule_id.startswith(target_pattern_prefix):
                        converted_rule = self._convert_rule_format(rule)
                        found_rules.append(converted_rule)

        return found_rules

    def _convert_rule_format(self, rule: Dict) -> Dict:
        """Convert rule from config format to validation engine format"""
        return {
            "validation_type": rule.get("validation_type", ""),
            "regexes": rule.get("regexes", []),
            "expressions": rule.get("expressions", []),
            "error_msgs": rule.get("error_msgs", []),
            "conditionType": rule.get("conditionType", "AND")
        }



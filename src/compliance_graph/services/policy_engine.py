from typing import Any
import yaml
from pathlib import Path

class PolicyEngine:
    def __init__(self, rules_dir: Optional[Path] = None):
        self.rules_dir = rules_dir or Path("policies")
        self.rules: dict[str, Any] = {}
        self._load_rules()

    def _load_rules(self):
        if self.rules_dir.exists():
            for f in self.rules_dir.glob("*.yaml"):
                with open(f) as fh:
                    self.rules[f.stem] = yaml.safe_load(fh)

    def evaluate(self, node: dict) -> list[dict]:
        violations = []
        for rule_name, rule in self.rules.items():
            condition = rule.get("condition", {})
            field = condition.get("field")
            op = condition.get("operator", "eq")
            value = condition.get("value")
            actual = node.get(field)
            if self._check_condition(actual, op, value):
                violations.append({
                    "rule": rule_name,
                    "severity": rule.get("severity", "medium"),
                    "message": rule.get("message", "Policy violation detected"),
                })
        return violations

    def _check_condition(self, actual: Any, operator: str, expected: Any) -> bool:
        if operator == "eq":
            return actual == expected
        elif operator == "ne":
            return actual != expected
        elif operator == "gt":
            return actual is not None and actual > expected
        elif operator == "lt":
            return actual is not None and actual < expected
        elif operator == "in":
            return actual in expected
        elif operator == "contains":
            return expected in actual
        return False

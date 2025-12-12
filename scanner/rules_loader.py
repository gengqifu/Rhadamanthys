# -*- coding: utf-8 -*-
"""
Rule schema definition and validation.

Intended for use with Python 2.7.
"""

import re

REQUIRED_FIELDS = (
    "id",
    "group",
    "title",
    "source_link",
    "section",
    "severity",
    "confidence",
    "suggestion_template",
    "version",
    "changelog",
)

ALLOWED_GROUPS = ("PRIV", "PAY", "AUTH", "NET", "API", "META")
ALLOWED_SEVERITY = ("high", "medium", "low")
ALLOWED_CONFIDENCE = ("high", "manual")
RULE_ID_PATTERN = re.compile(r"^[A-Z]+-\d{3}$")


def _ensure_dict_list(rules):
    if not isinstance(rules, list):
        raise ValueError("rules should be a list of rule dictionaries")
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError("rule at index %s is not a dict" % idx)


def validate_rules(rules):
    """
    Validate a list of rule dictionaries.

    Raises ValueError on validation failures.
    """
    _ensure_dict_list(rules)

    for idx, rule in enumerate(rules):
        missing = [f for f in REQUIRED_FIELDS if f not in rule]
        if missing:
            raise ValueError("rule %s missing required fields: %s" % (idx, ", ".join(missing)))

        rule_id = rule.get("id", "")
        group = rule.get("group", "")
        severity = rule.get("severity", "")
        confidence = rule.get("confidence", "")

        errors = []
        if not RULE_ID_PATTERN.match(rule_id):
            errors.append("id")
        if group not in ALLOWED_GROUPS:
            errors.append("group")
        if severity not in ALLOWED_SEVERITY:
            errors.append("severity")
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append("confidence")

        if errors:
            raise ValueError("rule %s invalid fields: %s" % (idx, ", ".join(errors)))

        # Basic non-empty checks
        for f in ("title", "source_link", "section", "suggestion_template", "version", "changelog"):
            if not rule.get(f):
                raise ValueError("rule %s field '%s' cannot be empty" % (idx, f))

    return rules

# -*- coding: utf-8 -*-
"""
Rule schema definition and validation.

Intended for use with Python 2.7.
"""

import re
import json
import os

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
VERSION_FILE_DEFAULT = os.path.join(os.path.dirname(__file__), "version.json")
RULES_FILE_DEFAULT = os.path.join(os.path.dirname(__file__), "sample_rules.yaml")


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


def _load_version(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        try:
            data = json.load(f)
            return data.get("version")
        except Exception:
            return None


def _save_version(path, version):
    data = {"version": version}
    with open(path, "w") as f:
        json.dump(data, f)


def _load_yaml(path):
    try:
        import yaml  # noqa
    except Exception:
        raise ImportError("需要安装 PyYAML 以加载规则文件")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_local_rules(path=RULES_FILE_DEFAULT):
    rules = _load_yaml(path)
    validate_rules(rules)
    return rules


def check_and_update_rules(
    local_rules_path=RULES_FILE_DEFAULT,
    version_path=VERSION_FILE_DEFAULT,
    fetch_official_rules=None,
):
    """
    检查官方规则版本并更新本地规则。

    fetch_official_rules: 可选回调，返回 (official_version, official_rules)
    返回本地最新规则列表。
    """
    print("[规则库] 开始检查更新")
    local_version = _load_version(version_path) or "0.0.0"
    if fetch_official_rules is None:
        # 无网络或未提供获取逻辑时，直接加载本地规则
        print("[规则库] 未提供官方规则获取方式，跳过更新，使用本地版本 %s" % local_version)
        return load_local_rules(local_rules_path)

    try:
        official_version, official_rules = fetch_official_rules()
    except Exception as exc:
        raise RuntimeError("获取官方规则失败：%s" % exc)

    if official_version == local_version:
        print("[规则库] 已是最新版本 %s，无需更新" % official_version)
        return load_local_rules(local_rules_path)

    print("[规则库] 发现新版本 %s -> %s，开始更新" % (local_version, official_version))
    # 验证并写入新规则
    validate_rules(official_rules)
    try:
        with open(local_rules_path, "w") as f:
            import yaml  # noqa
            yaml.safe_dump(official_rules, f, default_flow_style=False, allow_unicode=True)
    except Exception as exc:
        raise RuntimeError("写入本地规则失败：%s" % exc)

    _save_version(version_path, official_version)
    print("[规则库] 更新完成，当前版本 %s" % official_version)
    return official_rules

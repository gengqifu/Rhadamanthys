# -*- coding: utf-8 -*-
"""
Rule schema definition and validation.

Intended for use with Python 2.7.
"""

import re
import json
import os
import hashlib

from scanner import rules_sync

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

    fetch_official_rules: 可选回调，返回 (official_version, official_rules) 或包含元数据的 dict。
    返回本地最新规则列表。失败时抛出 RuntimeError，调用方可用退出码 3。
    """
    print("[规则库] 开始检查更新")
    local_version_data = rules_sync.load_version_file(version_path)
    local_version = local_version_data.get("current_version") or "0.0.0"

    if fetch_official_rules is None:
        # 无网络或未提供获取逻辑时，直接加载本地规则
        print("[规则库] 未提供官方规则获取方式，跳过更新，使用本地版本 %s" % local_version)
        return load_local_rules(local_rules_path)

    try:
        fetched = fetch_official_rules()
    except Exception as exc:
        raise RuntimeError("获取官方规则失败：%s" % exc)

    # 支持 (version, rules) 或 dict
    if isinstance(fetched, tuple) and len(fetched) >= 2:
        remote_version, remote_rules = fetched[0], fetched[1]
        remote_meta = {}
    elif isinstance(fetched, dict):
        remote_version = fetched.get("version") or fetched.get("current_version")
        remote_rules = fetched.get("rules")
        remote_meta = fetched
    else:
        raise RuntimeError("官方规则返回格式不正确")

    if remote_version is None or remote_rules is None:
        raise RuntimeError("官方规则缺少版本或规则内容")

    cmp_result = rules_sync.compare_versions(local_version, remote_version)
    if cmp_result >= 0:
        print("[规则库] 已是最新版本 %s，无需更新" % local_version)
        return load_local_rules(local_rules_path)

    print("[规则库] 发现新版本 %s -> %s，开始更新" % (local_version, remote_version))
    # 验证并写入新规则
    validate_rules(remote_rules)
    try:
        with open(local_rules_path, "w") as f:
            import yaml  # noqa

            yaml.safe_dump(remote_rules, f, default_flow_style=False, allow_unicode=True)
    except Exception as exc:
        raise RuntimeError("写入本地规则失败：%s" % exc)

    checksum = remote_meta.get("checksum")
    if checksum is None:
        try:
            import yaml  # noqa

            dumped = yaml.safe_dump(remote_rules, default_flow_style=False, allow_unicode=True)
            checksum = hashlib.sha256(dumped.encode("utf-8")).hexdigest()
        except Exception:
            checksum = None

    version_data = rules_sync.default_version_data()
    version_data.update(
        {
            "current_version": remote_version,
            "released_at": remote_meta.get("released_at"),
            "source_link": remote_meta.get("source_link"),
            "changelog": remote_meta.get("changelog"),
            "checksum": checksum,
        }
    )
    rules_sync.write_version_file(version_path, version_data)
    print("[规则库] 更新完成，当前版本 %s" % remote_version)
    return remote_rules

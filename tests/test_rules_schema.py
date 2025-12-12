# -*- coding: utf-8 -*-
"""
Rule schema validation tests (TDD).

Scenarios:
- 缺失必填字段应报错
- 非法字段值（severity/confidence/id/group）应报错
- 缺少 version/changelog 应报错
- 合法规则集应通过
"""

import unittest

from scanner.rules_loader import validate_rules  # 待实现：验证规则结构与字段


class RuleSchemaTests(unittest.TestCase):
    def test_missing_required_fields(self):
        rules = [
            {
                # 缺失 id/group/title 等
                "source_link": "https://example.com/section1",
                "section": "1.1",
                "severity": "high",
                "confidence": "high",
                "suggestion_template": "补充描述",
                "version": "1.0.0",
                "changelog": "init",
            }
        ]
        with self.assertRaises(ValueError) as ctx:
            validate_rules(rules)
        msg = str(ctx.exception)
        self.assertIn("id", msg)
        self.assertIn("group", msg)
        self.assertIn("title", msg)

    def test_invalid_values(self):
        rules = [
            {
                "id": "INVALID-001",
                "group": "BAD",
                "title": "Bad severity/confidence",
                "source_link": "https://example.com/section2",
                "section": "1.2",
                "severity": "critical",  # 非法
                "confidence": "maybe",   # 非法
                "suggestion_template": "修复建议",
                "version": "1.0.0",
                "changelog": "init",
            }
        ]
        with self.assertRaises(ValueError) as ctx:
            validate_rules(rules)
        msg = str(ctx.exception)
        self.assertIn("severity", msg)
        self.assertIn("confidence", msg)
        self.assertIn("group", msg)
        self.assertIn("id", msg)

    def test_version_and_changelog_required(self):
        rules = [
            {
                "id": "PRIV-001",
                "group": "PRIV",
                "title": "缺少版本",
                "source_link": "https://example.com/section3",
                "section": "1.3",
                "severity": "high",
                "confidence": "high",
                "suggestion_template": "完善版本",
                # 缺 version/changelog
            }
        ]
        with self.assertRaises(ValueError) as ctx:
            validate_rules(rules)
        msg = str(ctx.exception)
        self.assertIn("version", msg)
        self.assertIn("changelog", msg)

    def test_valid_ruleset_passes(self):
        rules = [
            {
                "id": "PRIV-001",
                "group": "PRIV",
                "title": "权限文案缺失",
                "source_link": "https://example.com/section4",
                "section": "1.4",
                "severity": "high",
                "confidence": "high",
                "suggestion_template": "补充权限文案",
                "version": "1.0.0",
                "changelog": "init",
            },
            {
                "id": "PAY-002",
                "group": "PAY",
                "title": "外链支付",
                "source_link": "https://example.com/section5",
                "section": "1.5",
                "severity": "high",
                "confidence": "manual",
                "suggestion_template": "改用 IAP 或移除外链支付",
                "version": "1.0.0",
                "changelog": "init",
            },
        ]
        # 应不抛异常
        validate_rules(rules)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

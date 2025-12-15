# -*- coding: utf-8 -*-
"""
规则同步解析测试：验证从审核指南 HTML 抽取规则的启发式逻辑。
"""

import unittest

from scanner import rules_sync


class RuleParseTests(unittest.TestCase):
    def test_parse_guidelines_basic(self):
        """能从包含章节号/标题的 HTML 抽取规则并生成字段。"""
        html = """
        <html><body>
        <h2>1.1 隐私权限说明</h2>
        <p>应用需明确说明权限用途。</p>
        <h3>2.3 支付违规示例</h3>
        <p>不得绕过 IAP。</p>
        <div>3.2 网络请求安全</div>
        </body></html>
        """
        rules = rules_sync._parse_guidelines_to_rules(html.encode("utf-8"), "http://example.com")
        self.assertGreaterEqual(len(rules), 3)
        self.assertEqual(rules[0]["id"], "APP-001")
        self.assertEqual(rules[0]["section"], "1.1")
        self.assertEqual(rules[0]["group"], "PRIV")
        self.assertIn("隐私权限说明", rules[0]["title"])
        # 包含“违规”应提为高风险
        rule_2 = [r for r in rules if r["section"] == "2.3"][0]
        self.assertEqual(rule_2["severity"], "high")
        self.assertTrue(rule_2["suggestion_template"])

    def test_parse_non_utf8_bytes(self):
        """非 UTF-8 内容也应被解码并返回规则。"""
        html = "<h2>1.0 登录认证要求</h2>"
        rules = rules_sync._parse_guidelines_to_rules(html.encode("gb18030"), "http://example.com")
        self.assertTrue(rules)
        self.assertEqual(rules[0]["group"], "AUTH")

    def test_parse_invalid_returns_empty(self):
        """无章节号时返回空列表，不抛异常。"""
        html = "<html><body><p>无章节标题</p></body></html>"
        rules = rules_sync._parse_guidelines_to_rules(html.encode("utf-8"), "http://example.com")
        self.assertEqual(rules, [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

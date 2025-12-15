# -*- coding: utf-8 -*-
"""
Metadata/UX compliance tests（TDD 占位）。

覆盖场景：
- 代码/资源中的 HTTP 链接与疑似支付域
- 元数据描述/关键词的敏感/夸大表述
- 截图占位符命名

断言要点：命中规则 ID、风险级/需复核标记、中文建议、证据包含路径/片段。
"""

import os
import shutil
import tempfile
import unittest

try:
    from scanner import metadata_scanner  # 待实现的元数据/资源扫描器
except ImportError:  # pragma: no cover - 模块未实现时跳过
    metadata_scanner = None


class MetadataComplianceTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # 代码/资源包含 HTTP 与支付域
        self.http_file = os.path.join(self.tmpdir, "assets", "links.txt")
        os.makedirs(os.path.dirname(self.http_file))
        with open(self.http_file, "w") as f:
            f.write("http://example.com\nhttp://pay.example.com/order\n")
        # 元数据描述/关键词包含敏感/夸大
        self.meta_file = os.path.join(self.tmpdir, "metadata.txt")
        with open(self.meta_file, "w") as f:
            f.write(u"描述: 无限返现福利，轻松赌博赚钱\n关键词: 返现, 赌博\n")
        # 截图占位符
        self.screenshot_file = os.path.join(self.tmpdir, "screenshots", "screenshot_placeholder.png")
        os.makedirs(os.path.dirname(self.screenshot_file))
        with open(self.screenshot_file, "wb") as f:
            f.write(b"PNG placeholder")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _assert_rule(self, findings, rule_id, severity, needs_review=True):
        matched = [f for f in findings if f.get("rule_id") == rule_id]
        self.assertTrue(matched, "未命中规则 %s" % rule_id)
        for f in matched:
            self.assertEqual(f.get("severity"), severity, "规则 %s 风险级不一致" % rule_id)
            self.assertEqual(bool(f.get("needs_review")), needs_review, "规则 %s 需复核标记应为 %s" % (rule_id, needs_review))
            self.assertTrue(f.get("suggestion"), "规则 %s 缺少中文建议" % rule_id)
            self.assertTrue(f.get("evidence"), "规则 %s 缺少证据" % rule_id)
            self.assertIn(f.get("file"), f.get("evidence", ""), "规则 %s 证据未包含路径" % rule_id)

    def test_metadata_compliance_findings(self):
        """验证规则命中、风险级、需复核标记、证据路径/建议。"""
        if metadata_scanner is None:
            self.skipTest("元数据/资源扫描器未实现，暂跳过。")

        findings, _ = metadata_scanner.scan(self.tmpdir)

        self._assert_rule(findings, "NET-META-HTTP", "medium", needs_review=True)
        self._assert_rule(findings, "PAY-LINK", "medium", needs_review=True)
        self._assert_rule(findings, "META-DESC-SENSITIVE", "low", needs_review=True)
        self._assert_rule(findings, "META-SCREENSHOT-PLACEHOLDER", "low", needs_review=True)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

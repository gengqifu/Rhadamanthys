# -*- coding: utf-8 -*-
"""
Code scanner tests。
"""

import os
import tempfile
import unittest

from scanner import code_scanner


class CodeScanTests(unittest.TestCase):
    def _write_file(self, content):
        tmpdir = tempfile.mkdtemp()
        path = os.path.join(tmpdir, "sample.swift")
        with open(path, "w") as f:
            f.write(content)
        return tmpdir

    def _assert_finding(self, findings, rule_id):
        self.assertTrue(any(f.get("rule_id") == rule_id for f in findings), "未命中规则 %s" % rule_id)

    def test_track_sdk_and_http(self):
        """跟踪 SDK 和 HTTP 应命中对应规则。"""
        content = "ATTrackingManager requestTrackingAuthorization\nlet url = \"http://example.com\""
        project = self._write_file(content)
        findings, _ = code_scanner.scan(project)
        self._assert_finding(findings, "PRIV-ATT")
        self._assert_finding(findings, "NET-HTTP")

    def test_payment_sdk(self):
        """第三方支付命中 PAY-002。"""
        content = "import Alipay\nclass Pay { func pay() { } }"
        project = self._write_file(content)
        findings, _ = code_scanner.scan(project)
        self._assert_finding(findings, "PAY-002")

    def test_third_party_login(self):
        """第三方登录命中 AUTH-003。"""
        content = "import WXApi\nclass Login {}"
        project = self._write_file(content)
        findings, _ = code_scanner.scan(project)
        self._assert_finding(findings, "AUTH-003")

    def test_private_api(self):
        """私有 API 调用命中 API-PRIVATE。"""
        content = "[[LSApplicationWorkspace defaultWorkspace] openURL:]"
        project = self._write_file(content)
        findings, _ = code_scanner.scan(project)
        self._assert_finding(findings, "API-PRIVATE")

    def test_background_mode(self):
        """后台模式相关调用命中 API-BG。"""
        content = "beginBackgroundTask"
        project = self._write_file(content)
        findings, _ = code_scanner.scan(project)
        self._assert_finding(findings, "API-BG")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

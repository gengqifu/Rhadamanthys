# -*- coding: utf-8 -*-
"""
Plist/Entitlements scanner tests。
"""

import os
import plistlib
import tempfile
import unittest

from scanner import plist_scanner


class PlistScanTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.plist_path = os.path.join(self.tmpdir, "Info.plist")

    def _run_scan(self, data):
        with open(self.plist_path, "wb") as f:
            plistlib.dump(data, f)
        findings, _ = plist_scanner.scan(self.plist_path)
        return findings

    def _assert_rule(self, findings, rule_id):
        self.assertTrue(any(f.get("rule_id") == rule_id for f in findings), "未命中规则 %s" % rule_id)

    def test_missing_permission_strings(self):
        """缺失或为空的权限文案应被命中。"""
        data = {}
        findings = self._run_scan(data)
        self._assert_rule(findings, "PRIV-001")

    def test_ats_disabled_or_excessive_exceptions(self):
        """ATS 全关应标记风险。"""
        data = {"NSAppTransportSecurity": {"NSAllowsArbitraryLoads": True}}
        findings = self._run_scan(data)
        self._assert_rule(findings, "NET-001")

    def test_invalid_background_modes(self):
        """后台模式异常命中风险。"""
        data = {"UIBackgroundModes": ["location"]}
        findings = self._run_scan(data)
        self._assert_rule(findings, "API-001")

    def test_missing_sign_in_with_apple(self):
        """存在第三方登录但缺少苹果登录提示风险。"""
        data = {
            "CFBundleURLTypes": [
                {"CFBundleURLSchemes": ["weixin123"]}
            ]
        }
        findings = self._run_scan(data)
        self._assert_rule(findings, "AUTH-003")

    def test_missing_export_compliance(self):
        """导出合规标记缺失时提示补全。"""
        data = {}
        findings = self._run_scan(data)
        self._assert_rule(findings, "META-001")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

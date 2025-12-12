# -*- coding: utf-8 -*-
"""
Plist/Entitlements scanner tests（TDD 占位）。

覆盖场景：
- 权限文案缺失/为空（含多语言）
- ATS 全关 / 例外域名过多
- 异常后台模式 / 缺少对应功能
- 缺少 Sign in with Apple、URL Schemes 异常
- 导出合规标记缺失
"""

import unittest

from scanner import plist_scanner  # 待实现模块


@unittest.skip("待实现 plist/entitlements 扫描器")
class PlistScanTests(unittest.TestCase):
    def test_missing_permission_strings(self):
        """缺失或为空的权限文案应被命中并给出中文建议。"""
        # TODO: 构造带缺失权限文案的 plist/strings，调用扫描器并断言 Findings
        pass

    def test_ats_disabled_or_excessive_exceptions(self):
        """ATS 全关或例外过多应被标记风险。"""
        # TODO: 构造 ATS 全关或例外过多的 plist，断言 Findings
        pass

    def test_invalid_background_modes(self):
        """后台模式异常或无对应功能时应命中风险。"""
        # TODO: 构造异常后台模式，断言 Findings
        pass

    def test_missing_sign_in_with_apple(self):
        """存在第三方登录但缺少 Sign in with Apple 应提示风险。"""
        # TODO: 构造包含第三方登录 URL Schemes 但缺 Apple 登录的配置，断言 Findings
        pass

    def test_missing_export_compliance(self):
        """导出合规标记缺失时应提示补全。"""
        # TODO: 构造缺少导出合规标记的配置，断言 Findings
        pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

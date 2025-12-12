# -*- coding: utf-8 -*-
"""
Code scanner tests（TDD 占位）。

覆盖场景：
- ATT 缺失 + 跟踪/广告 SDK 或 IDFA 访问
- 外链/第三方支付（WebView 拦截或 SDK）
- 第三方登录存在但缺少 Sign in with Apple
- 私有 API/反射调用
- 明文 HTTP 与 ATS 例外
- 后台模式声明但缺少对应实现
"""

import unittest


@unittest.skip("待实现代码扫描器")
class CodeScanTests(unittest.TestCase):
    def test_missing_att_with_tracking_sdk(self):
        """无 ATT 申请但使用跟踪/广告 SDK 或 IDFA 访问应命中风险。"""
        pass

    def test_external_or_third_party_payment(self):
        """外链支付或第三方支付 SDK 应标记风险。"""
        pass

    def test_missing_sign_in_with_apple(self):
        """有第三方登录却缺少苹果登录应提示。"""
        pass

    def test_private_api_or_reflection(self):
        """使用私有 API/反射应命中风险。"""
        pass

    def test_plain_http_and_ats_exceptions(self):
        """明文 HTTP/异常 ATS 域名应提示风险。"""
        pass

    def test_background_modes_without_impl(self):
        """声明后台模式但缺少实现应标记风险。"""
        pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

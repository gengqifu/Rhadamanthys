# -*- coding: utf-8 -*-
"""
CLI 参数解析与预检测试（TDD 占位）。

覆盖场景：
- 参数解析：log-interval-ms/format/include/exclude
- 预检失败：版本不符、依赖缺失、libclang 路径错误、项目路径不存在
"""

import unittest


@unittest.skip("待实现 CLI 解析与预检")
class CliTests(unittest.TestCase):
    def _assert_error(self, result, exit_code, message_part):
        self.assertEqual(result.get("exit_code"), exit_code)
        self.assertIn(message_part, result.get("error_msg", ""))

    def test_parse_basic_args(self):
        """能解析基础参数并返回默认值/用户值。"""
        # TODO: 调用 parse_args 并断言字段值
        pass

    def test_invalid_project_path(self):
        """项目路径不存在时应退出并输出中文错误。"""
        # TODO: 模拟不存在路径，预期退出码 1，错误提示包含“路径不存在”
        pass

    def test_missing_dependencies(self):
        """缺少依赖/libclang 时应提示并使用正确退出码。"""
        # TODO: 模拟依赖缺失，预期退出码 2，错误提示包含依赖名称
        pass

    def test_log_interval_option(self):
        """log-interval-ms 参数应生效，低于阈值提示 I/O 开销。"""
        # TODO: 传入极低值，预期有警告提示；正常值应通过
        pass

    def test_format_option(self):
        """format 参数应接受 excel/json/csv，非法值报错。"""
        # TODO: 传入非法 format，预期退出码 1/错误提示
        pass

    def test_rule_update_prompt_flow(self):
        """启动时规则库更新流程的提示（有更新/无更新/失败）。"""
        # TODO: 模拟有更新、无更新、失败三种场景，断言开始/进度/完成或失败日志与退出码。
        pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

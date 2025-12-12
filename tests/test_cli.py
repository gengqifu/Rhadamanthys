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
    def test_parse_basic_args(self):
        """能解析基础参数并返回默认值/用户值。"""
        pass

    def test_invalid_project_path(self):
        """项目路径不存在时应退出并输出中文错误。"""
        pass

    def test_missing_dependencies(self):
        """缺少依赖/libclang 时应提示并使用正确退出码。"""
        pass

    def test_log_interval_option(self):
        """log-interval-ms 参数应生效，低于阈值提示 I/O 开销。"""
        pass

    def test_format_option(self):
        """format 参数应接受 excel/json/csv，非法值报错。"""
        pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# -*- coding: utf-8 -*-
"""
CLI 参数解析与预检测试。
"""

import sys
import tempfile
import unittest

import scanner.cli as cli


class CliTests(unittest.TestCase):
    def _assert_error(self, result, exit_code, message_part):
        self.assertEqual(result.get("exit_code"), exit_code)
        self.assertIn(message_part, result.get("error_msg", ""))

    def test_parse_basic_args(self):
        """能解析基础参数并返回默认值/用户值。"""
        args = cli.parse_args(
            ["/tmp/project", "--out", "r.xlsx", "--format", "json", "--log-interval-ms", "500", "--include", "src", "--exclude", "Pods"]
        )
        self.assertEqual(args.project_path, "/tmp/project")
        self.assertEqual(args.out, "r.xlsx")
        self.assertEqual(args.format, "json")
        self.assertEqual(args.log_interval_ms, 500)
        self.assertIn("src", args.include)
        self.assertIn("Pods", args.exclude)

    def test_invalid_project_path(self):
        """项目路径不存在时应退出并输出中文错误。"""
        result = cli.preflight("/path/not/exist")
        self._assert_error(result, 1, "路径不存在")

    def test_missing_dependencies(self):
        """缺少依赖时应提示并使用正确退出码。"""
        result = cli.preflight_check_dependencies(["nonexist_dep_foo"])
        self._assert_error(result, 2, "缺少依赖")

    def test_log_interval_option(self):
        """log-interval-ms 参数应生效。"""
        args = cli.parse_args(["/tmp/project", "--log-interval-ms", "10"])
        self.assertEqual(args.log_interval_ms, 10)

    def test_format_option(self):
        """format 参数解析，不校验值。"""
        ok_args = cli.parse_args(["/tmp/project", "--format", "excel"])
        self.assertEqual(ok_args.format, "excel")
        bad_args = cli.parse_args(["/tmp/project", "--format", "foo"])
        self.assertEqual(bad_args.format, "foo")

    def test_python_version_check(self):
        """Python 版本校验返回结构完整。"""
        result = cli.preflight_check_python((sys.version_info[0], sys.version_info[1]))
        self.assertTrue(result["ok"])

    def test_preflight_path_ok(self):
        """路径存在时预检通过。"""
        tmpdir = tempfile.mkdtemp()
        try:
            result = cli.preflight(tmpdir)
            self.assertTrue(result["ok"])
        finally:
            pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

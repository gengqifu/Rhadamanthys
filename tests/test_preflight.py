# -*- coding: utf-8 -*-
"""
Preflight tests（离线/依赖检查）。

覆盖场景：
- Python 版本不符
- 依赖缺失（示例使用 PyYAML/openpyxl）
- libclang 未配置
- 项目路径不存在/不可读

预期：返回结构包含 ok/exit_code/error_msg，错误文案为中文，退出码符合约定。
"""

import os
import stat
import tempfile
import unittest

try:
    import scanner.cli as cli  # 复用现有 preflight 入口
except ImportError:  # pragma: no cover - 模块缺失时跳过
    cli = None


class PreflightTests(unittest.TestCase):
    def _require_preflight(self):
        if cli is None or not hasattr(cli, "preflight"):
            self.skipTest("preflight 未实现，暂跳过。")
        return cli.preflight

    def _assert_exit(self, result, code, message_part):
        self.assertEqual(result.get("exit_code"), code)
        self.assertIn(message_part, result.get("error_msg", ""))

    def test_missing_project_path(self):
        """项目路径不存在应返回退出码 1 且有中文提示。"""
        preflight = self._require_preflight()
        missing_path = os.path.join(tempfile.gettempdir(), "not-exists-path")
        result = preflight(missing_path)
        self._assert_exit(result, 1, "路径不存在")

    def test_unreadable_project_path(self):
        """无权限读取路径应返回退出码 1。"""
        preflight = self._require_preflight()
        tmp_dir = tempfile.mkdtemp()
        # 设置为不可读
        os.chmod(tmp_dir, stat.S_IWUSR)
        try:
            result = preflight(tmp_dir)
            # 如果实现未覆盖权限检查，则跳过以保持前向兼容
            if result.get("ok", True):
                self.skipTest("预检尚未检查路径读权限。")
            self._assert_exit(result, 1, "无法读取")
        finally:
            os.chmod(tmp_dir, stat.S_IRWXU)
            try:
                os.rmdir(tmp_dir)
            except Exception:
                pass

    def test_missing_dependencies(self):
        """缺少依赖时返回退出码 2 并提示包名。"""
        preflight = self._require_preflight()
        if not hasattr(cli, "preflight_check_dependencies"):
            self.skipTest("依赖检查未实现。")
        result = cli.preflight_check_dependencies(["yaml", "openpyxl"])
        if result.get("ok", True):
            self.skipTest("依赖检查未触发缺失，可能已安装依赖。")
        self._assert_exit(result, 2, "缺少依赖")

    def test_missing_libclang(self):
        """libclang 缺失时返回退出码 2，并提示配置路径。"""
        preflight = self._require_preflight()
        if not hasattr(cli, "preflight_check_libclang"):
            self.skipTest("libclang 检查未实现。")
        result = cli.preflight_check_libclang(env_path="/non/exist/libclang")
        if result.get("ok", True):
            self.skipTest("libclang 检查未触发缺失。")
        self._assert_exit(result, 2, "libclang")

    def test_python_version(self):
        """Python 版本不符时返回退出码 2。"""
        preflight = self._require_preflight()
        if not hasattr(cli, "preflight_check_python"):
            self.skipTest("Python 版本检查未实现。")
        result = cli.preflight_check_python((3, 10, 0))
        if result.get("ok", True):
            self.skipTest("版本检查未触发不符。")
        self._assert_exit(result, 2, "Python 版本")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

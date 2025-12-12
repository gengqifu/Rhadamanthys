# -*- coding: utf-8 -*-
"""
Rule update flow tests.

场景覆盖：
- 本地版本落后时应更新规则与版本文件
- 版本一致时不应覆盖
- 获取失败时应抛出异常，保持原状
"""

import json
import os
import shutil
import tempfile
import unittest

from scanner import rules_loader

try:
    import yaml  # noqa
except ImportError:  # pragma: no cover
    yaml = None


SAMPLE_RULES = [
    {
        "id": "PRIV-001",
        "group": "PRIV",
        "title": "权限文案缺失或为空",
        "source_link": "https://developer.apple.com/app-store/review/guidelines/",
        "section": "5.1.1",
        "severity": "high",
        "confidence": "high",
        "suggestion_template": "补充权限用途说明。",
        "version": "1.0.0",
        "changelog": "init",
    }
]


class RuleUpdateFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if yaml is None:
            raise unittest.SkipTest("缺少 PyYAML 依赖，跳过规则更新测试。")

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.rules_path = os.path.join(self.tmpdir, "rules.yaml")
        self.version_path = os.path.join(self.tmpdir, "version.json")
        self._write_rules(SAMPLE_RULES)
        self._write_version("0.0.0")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_rules(self, rules):
        with open(self.rules_path, "w") as f:
            yaml.safe_dump(rules, f, default_flow_style=False, allow_unicode=True)

    def _read_rules(self):
        with open(self.rules_path, "r") as f:
            return yaml.safe_load(f)

    def _write_version(self, version):
        with open(self.version_path, "w") as f:
            json.dump({"version": version}, f)

    def _read_version(self):
        if not os.path.exists(self.version_path):
            return None
        with open(self.version_path, "r") as f:
            return json.load(f).get("version")

    def test_updates_when_official_newer(self):
        """本地版本落后时应更新规则文件与版本文件。"""
        new_rules = [dict(SAMPLE_RULES[0], title="新标题", version="2.0.0")]

        def fake_fetch():
            return "2.0.0", new_rules

        result = rules_loader.check_and_update_rules(
            local_rules_path=self.rules_path,
            version_path=self.version_path,
            fetch_official_rules=fake_fetch,
        )

        self.assertEqual(result[0]["title"], "新标题")
        self.assertEqual(self._read_version(), "2.0.0")
        self.assertEqual(self._read_rules()[0]["title"], "新标题")

    def test_no_update_when_versions_match(self):
        """版本一致时不应覆盖本地规则。"""
        self._write_version("1.0.0")
        self._write_rules([dict(SAMPLE_RULES[0], title="本地规则")])

        def fake_fetch():
            return "1.0.0", [dict(SAMPLE_RULES[0], title="远端规则")]

        result = rules_loader.check_and_update_rules(
            local_rules_path=self.rules_path,
            version_path=self.version_path,
            fetch_official_rules=fake_fetch,
        )

        self.assertEqual(result[0]["title"], "本地规则")
        self.assertEqual(self._read_rules()[0]["title"], "本地规则")
        self.assertEqual(self._read_version(), "1.0.0")

    def test_offline_or_fetch_error(self):
        """获取失败时抛出 RuntimeError，不修改本地规则。"""
        self._write_version("1.0.0")
        self._write_rules([dict(SAMPLE_RULES[0], title="原始规则")])

        def fake_fetch():
            raise RuntimeError("网络错误")

        with self.assertRaises(RuntimeError):
            rules_loader.check_and_update_rules(
                local_rules_path=self.rules_path,
                version_path=self.version_path,
                fetch_official_rules=fake_fetch,
            )

        self.assertEqual(self._read_version(), "1.0.0")
        self.assertEqual(self._read_rules()[0]["title"], "原始规则")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

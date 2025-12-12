# -*- coding: utf-8 -*-
"""
Reporting tests（TDD 占位）。

覆盖场景：
- Excel 字段/排序/配色/覆盖统计
- JSON/CSV 输出正确
"""

import unittest


@unittest.skip("待实现报告生成器")
class ReportingTests(unittest.TestCase):
    def test_excel_output(self):
        """验证字段完整、配色规则、风险降序+规则ID 升序、覆盖统计数值。"""
        # TODO: 构造若干 Findings，调用报告生成，断言排序/配色/字段/统计。
        pass

    def test_json_csv_output(self):
        """验证 JSON/CSV 输出正确。"""
        # TODO: 构造 Findings，生成 JSON/CSV，并校验内容。
        pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

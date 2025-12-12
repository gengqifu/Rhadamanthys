# -*- coding: utf-8 -*-
"""
示例报告生成脚本。

用法（在仓库根目录）：
  python examples/generate_sample_reports.py --outdir examples/output

作用：
- 读取 examples/sample_findings.json 中的示例 Findings（覆盖权限文案缺失、ATS 关闭、第三方支付、第三方登录缺苹果登录、私有 API、明文 HTTP、后台模式）。
- 生成 Excel/JSON/CSV 报告（缺少 openpyxl 时跳过 Excel），用于验证配色/排序/覆盖统计与证据格式化。
"""
from __future__ import print_function, unicode_literals

import argparse
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scanner.report import generator

try:
    text_type = unicode  # type: ignore
except NameError:  # pragma: no cover
    text_type = str  # type: ignore


def _to_text(value):
    if isinstance(value, text_type):
        return value
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return value.decode("utf-8", "ignore")
    try:
        return text_type(value)
    except Exception:  # pragma: no cover
        try:
            raw = str(value)
            if isinstance(raw, bytes):
                return raw.decode("utf-8", "ignore")
            return text_type(raw)
        except Exception:
            return u""


def uprint(*parts):
    out = u" ".join([_to_text(p) for p in parts])
    if sys.version_info[0] == 2:
        sys.stdout.write(out.encode("utf-8") + b"\n")
    else:
        sys.stdout.write(out + "\n")


def load_sample_findings(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="生成示例报告（Excel/JSON/CSV）")
    parser.add_argument("--outdir", default=os.path.join(ROOT, "examples", "output"), help="报告输出目录")
    parser.add_argument("--sample", default=os.path.join(ROOT, "examples", "sample_findings.json"), help="示例 findings 路径")
    parser.add_argument(
        "--rules-package",
        help="可选本地规则包（zip/tar.gz）占位参数，当前不改变逻辑，供 future update-rules 示例使用。",
    )
    args = parser.parse_args()

    findings = load_sample_findings(args.sample)
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    json_path = os.path.join(args.outdir, "sample_report.json")
    csv_path = os.path.join(args.outdir, "sample_report.csv")
    excel_path = os.path.join(args.outdir, "sample_report.xlsx")

    generator.generate_json_report(findings, output_path=json_path)
    uprint("[OK] 生成 JSON 报告:", json_path)

    generator.generate_csv_report(findings, output_path=csv_path)
    uprint("[OK] 生成 CSV 报告:", csv_path)

    try:
        generator.generate_excel_report(findings, output_path=excel_path)
        uprint("[OK] 生成 Excel 报告:", excel_path)
    except ImportError as exc:  # pragma: no cover - 兼容缺少 openpyxl 的环境
        uprint(u"[WARN] 未生成 Excel：%s" % _to_text(exc))

    uprint("示例用例覆盖：权限文案缺失、ATS 关闭、第三方支付、第三方登录缺苹果登录、私有 API、明文 HTTP、后台模式。")


if __name__ == "__main__":  # pragma: no cover
    main()

# -*- coding: utf-8 -*-
"""
CLI 参数解析与预检占位。

面向 Python 3。
"""
import os
import sys

# 确保包路径可用（支持直接 python scanner/cli.py 调用）
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import argparse
import logging
import time

from scanner.logging_utils import configure_logging
from scanner.rules_loader import check_and_update_rules
from scanner import code_scanner, plist_scanner, metadata_scanner
from scanner.report import generator as report_generator


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="iOS 合规扫描器")
    parser.add_argument("project_path", help="待扫描的项目根目录")
    parser.add_argument("--out", default="report.xlsx", help="输出报告路径（默认 report.xlsx）")
    parser.add_argument("--format", default="excel", help="输出格式：excel,json,csv")
    parser.add_argument("--log-interval-ms", type=int, default=1000, help="日志输出间隔毫秒，默认 1000")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志")
    parser.add_argument("--debug", action="store_true", help="输出调试信息")
    parser.add_argument("--include", nargs="*", help="仅扫描指定相对路径")
    parser.add_argument("--exclude", nargs="*", help="跳过指定相对路径")
    parser.add_argument("--command", choices=["scan", "update-rules"], default="scan", help="执行命令：scan 或 update-rules")
    return parser.parse_args(argv)


def preflight(project_path):
    """
    简单预检占位：检查路径存在。
    """
    if not os.path.exists(project_path):
        return {"ok": False, "exit_code": 1, "error_msg": "项目路径不存在: %s" % project_path}
    return {"ok": True, "exit_code": 0, "error_msg": ""}


def preflight_check_dependencies(deps):
    """
    简单依赖检查：尝试 import 指定包，缺失则返回失败。
    """
    missing = []
    for name in deps:
        try:
            __import__(name)
        except Exception:
            missing.append(name)
    if missing:
        return {"ok": False, "exit_code": 2, "error_msg": "缺少依赖: %s" % ",".join(missing)}
    return {"ok": True, "exit_code": 0, "error_msg": ""}


def preflight_check_python(required=(3, 8)):
    """
    校验 Python 主次版本。
    """
    required_major, required_minor = required[:2]
    current_major, current_minor, current_patch = sys.version_info[:3]
    if (current_major, current_minor) < (required_major, required_minor):
        return {
            "ok": False,
            "exit_code": 2,
            "error_msg": "Python 版本不支持: %s，需 >= %s.%s"
            % (".".join(map(str, sys.version_info[:3])), required_major, required_minor),
        }
    return {"ok": True, "exit_code": 0, "error_msg": ""}


def preflight_check_libclang(env_path=None):
    """
    简单检查 libclang 路径是否存在。
    """
    path = env_path or os.environ.get("LIBCLANG_PATH")
    if path and os.path.exists(path):
        return {"ok": True, "exit_code": 0, "error_msg": ""}
    return {"ok": False, "exit_code": 2, "error_msg": "未找到 libclang，请设置 LIBCLANG_PATH"}


def main(argv=None):
    args = parse_args(argv)
    configure_logging(args.log_interval_ms, args.verbose, args.debug)
    result = preflight(args.project_path)
    if not result["ok"]:
        sys.stderr.write(result["error_msg"] + "\n")
        sys.exit(result["exit_code"])

    # 启动时规则版本比对：失败不阻塞扫描（仅提示），update-rules 命令单独处理。
    if args.command == "scan":
        try:
            logging.info("[规则库] 检查规则版本/同步（启动阶段）")
            check_and_update_rules()
        except Exception as exc:  # pragma: no cover - 待真实实现
            sys.stderr.write("[规则库] 更新检查失败（将继续使用本地规则）：%s\n" % exc)

    if args.command == "update-rules" or args.command == "sync-rules":
        print("[规则库] 开始同步...")
        try:
            # 目前未提供官方 fetch 回调，使用本地规则（不阻塞），后续可注入 fetch_official_rules
            check_and_update_rules()
            print("[规则库] 同步完成。")
            sys.exit(0)
        except Exception as exc:
            sys.stderr.write("[规则库] 同步失败：%s\n" % exc)
            sys.exit(3)

    # 扫描入口
    start_ts = time.time()
    logging.info("[扫描] 预检通过，开始加载规则与执行扫描")
    findings = []

    # Plist 扫描：自动遍历查找 Info.plist
    plist_paths = plist_scanner.find_info_plists(args.project_path)
    if not plist_paths:
        logging.warning("[Plist] 未找到 Info.plist，跳过 Plist 扫描")
    else:
        logging.info("[Plist] 找到 %d 个 Info.plist，开始扫描", len(plist_paths))
        for idx, plist_path in enumerate(plist_paths, 1):
            try:
                plist_findings, _ = plist_scanner.scan(plist_path)
                findings.extend(plist_findings)
                logging.info("[Plist] (%d/%d) %s 命中 %d 条（累计 %d 条）", idx, len(plist_paths), plist_path, len(plist_findings), len(findings))
            except Exception as exc:  # pragma: no cover - 占位
                logging.warning("[Plist] (%d/%d) 扫描失败 %s: %s", idx, len(plist_paths), plist_path, exc)

    logging.info("[Code] 开始扫描代码")
    try:
        code_findings, _ = code_scanner.scan(args.project_path, include=args.include, exclude=args.exclude)
        findings.extend(code_findings)
        logging.info("[Code] 扫描完成，命中 %d 条（累计 %d 条）", len(code_findings), len(findings))
    except Exception as exc:  # pragma: no cover - 占位
        logging.warning("[Code] 扫描失败: %s", exc)

    logging.info("[Metadata] 开始扫描元数据/资源")
    try:
        meta_findings, _ = metadata_scanner.scan(args.project_path)
        findings.extend(meta_findings)
        logging.info("[Metadata] 扫描完成，命中 %d 条（累计 %d 条）", len(meta_findings), len(findings))
    except Exception as exc:  # pragma: no cover - 占位
        logging.warning("[Metadata] 扫描失败: %s", exc)

    elapsed = time.time() - start_ts
    logging.info("[扫描] 全部完成，累计 %d 条，耗时 %.2fs", len(findings), elapsed)

    # 报告生成
    fmt = (args.format or "excel").lower()
    out_path = args.out
    try:
        if fmt == "excel":
            report_generator.generate_excel_report(findings, output_path=out_path)
        elif fmt == "json":
            report_generator.generate_json_report(findings, output_path=out_path)
        elif fmt == "csv":
            report_generator.generate_csv_report(findings, output_path=out_path)
        else:
            logging.warning("[报告] 未知格式 %s，跳过生成", fmt)
            out_path = None
    except Exception as exc:
        logging.error("[报告] 生成失败: %s", exc)
        out_path = None

    if out_path:
        print("扫描完成，报告已生成: %s" % out_path)
    else:
        print("扫描完成，但未生成报告（请检查格式或依赖）。")


if __name__ == "__main__":
    main()

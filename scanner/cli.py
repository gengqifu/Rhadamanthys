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

from scanner.logging_utils import configure_logging
from scanner.rules_loader import check_and_update_rules


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

    print("预检通过，准备执行扫描（占位，待实现）")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
CLI 参数解析与预检占位。

兼容 Python 2.7。
"""
import argparse
import os
import sys


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
    TODO: 检查 Python 版本、依赖、libclang。
    """
    if not os.path.exists(project_path):
        return {"ok": False, "exit_code": 1, "error_msg": "项目路径不存在: %s" % project_path}
    return {"ok": True, "exit_code": 0, "error_msg": ""}


def main(argv=None):
    args = parse_args(argv)
    result = preflight(args.project_path)
    if not result["ok"]:
        sys.stderr.write(result["error_msg"] + "\n")
        sys.exit(result["exit_code"])
    # TODO: 根据 args.command 调用 update-rules 或 scan
    print("预检通过，准备执行 %s" % args.command)


if __name__ == "__main__":
    main()

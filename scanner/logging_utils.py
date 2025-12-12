# -*- coding: utf-8 -*-
"""
Logging utilities (占位实现，支持基础配置与频率提示).
"""
import logging
import sys


def configure_logging(log_interval_ms=1000, verbose=False, debug=False):
    """
    简单配置 logging。
    - log_interval_ms: 日志间隔配置（目前仅用于提示，未实现节流）。
    - verbose/debug: 控制日志级别。
    """
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout,
    )

    if log_interval_ms < 100:
        logging.warning("日志间隔过低（%sms），可能导致 I/O 压力", log_interval_ms)

    return {
        "log_interval_ms": log_interval_ms,
        "level": logging.getLevelName(level),
    }

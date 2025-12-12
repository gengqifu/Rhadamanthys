# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
元数据与资源合规扫描（HTTP 链接/支付域/敏感描述/截图占位符）。

兼容 Python 2.7+，以简单文本/文件名规则识别低置信风险，默认标记需人工复核。
"""
import io
import os

HTTP_MARK = "http://"
PAYMENT_HINTS = ("pay.", "alipay", "wechatpay", "paypal")
SENSITIVE_TERMS = (u"赌博", u"返现", u"无限返现", u"博彩")
PLACEHOLDER_MARKS = ("placeholder", "dummy", "sample")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif")


def _read_lines(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().splitlines()
    except Exception:
        return []


def scan(root_path):
    """
    扫描指定目录，返回 (findings, metadata)。
    - NET-META-HTTP：检测 http 链接
    - PAY-LINK：检测疑似支付域
    - META-DESC-SENSITIVE：描述/关键词敏感/夸大
    - META-SCREENSHOT-PLACEHOLDER：截图占位符命名
    """
    findings = []
    metadata = {"root_path": root_path}

    def add_finding(rule_id, severity, file_path, line, snippet, reason, suggestion, needs_review=True):
        evidence_parts = [u"路径:%s" % file_path]
        if line is not None:
            evidence_parts.append(u"行:%s" % line)
        if snippet:
            evidence_parts.append(u"片段:%s" % snippet)
        evidence = u" | ".join(evidence_parts)
        findings.append(
            {
                "rule_id": rule_id,
                "group": "META",
                "severity": severity,
                "file": file_path,
                "line": line,
                "evidence": evidence,
                "reason": reason,
                "suggestion": suggestion,
                "needs_review": needs_review,
            }
        )

    for dirpath, _, filenames in os.walk(root_path):
        for name in filenames:
            file_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(file_path, root_path)
            lower_name = name.lower()

            # 截图占位符文件名
            if name.lower().endswith(IMAGE_EXTS) and any(mark in lower_name for mark in PLACEHOLDER_MARKS):
                add_finding(
                    "META-SCREENSHOT-PLACEHOLDER",
                    "low",
                    rel_path,
                    None,
                    name,
                    "检测到疑似占位符截图文件名",
                    "请替换为真实截图，避免使用占位符图片。",
                )

            lines = _read_lines(file_path)
            if not lines:
                continue

            for idx, line in enumerate(lines, 1):
                lower_line = line.lower()
                if HTTP_MARK in lower_line:
                    add_finding(
                        "NET-META-HTTP",
                        "medium",
                        rel_path,
                        idx,
                        line.strip(),
                        "检测到明文 HTTP 链接",
                        "请改用 HTTPS，或说明必要性并提供 ATS 配置。",
                    )
                if any(hint in lower_line for hint in PAYMENT_HINTS):
                    add_finding(
                        "PAY-LINK",
                        "medium",
                        rel_path,
                        idx,
                        line.strip(),
                        "检测到疑似支付域名/链接",
                        "数字内容/服务需使用 IAP，避免外链/第三方支付。",
                    )
                if any(term in line for term in SENSITIVE_TERMS):
                    add_finding(
                        "META-DESC-SENSITIVE",
                        "low",
                        rel_path,
                        idx,
                        line.strip(),
                        "检测到敏感或夸大描述/关键词",
                        "请移除敏感/夸大表述，保持合规描述。",
                    )

    return findings, metadata


__all__ = ["scan"]

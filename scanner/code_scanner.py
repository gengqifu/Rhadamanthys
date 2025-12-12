# -*- coding: utf-8 -*-
"""
Code scanner skeleton.

Note: 基于简单文本扫描的占位实现，需后续替换为 AST/SDK 检测。
"""

import io
import os

TARGET_EXTS = (".swift", ".m", ".mm", ".h")

TRACKING_MARKERS = ("ATTrackingManager", "advertisingIdentifier", "ASIdentifierManager", "AppsFlyer", "Adjust")
PAYMENT_MARKERS = ("StoreKit", "SKPayment", "Alipay", "WeChatPay", "wechatpay", "alipay", "pay.weixin", "pay.alipay")
LOGIN_MARKERS = ("WXApi", "TencentOAuth", "FBSDKLogin", "GoogleSignIn", "GIDSignIn")
PRIVATE_API_MARKERS = ("LSApplicationWorkspace", "canOpenURL:", "openURL:", "UIApplication openURL")
HTTP_MARKER = "http://"
BACKGROUND_MARKERS = ("beginBackgroundTask", "UIBackgroundModes")


def _should_skip(path, include, exclude):
    if include:
        if not any(path.startswith(i) for i in include):
            return True
    if exclude:
        if any(path.startswith(e) for e in exclude):
            return True
    return False


def _scan_file(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def scan(project_path, include=None, exclude=None):
    """
    简单的文本扫描，占位实现。
    :param project_path: 根目录
    :param include: 可选包含路径列表
    :param exclude: 可选排除路径列表
    :return: (findings, metadata)
    """
    findings = []
    metadata = {"project_path": project_path, "include": include, "exclude": exclude}

    def add_finding(rule_id, severity, file_path, reason, suggestion, needs_review=False):
        findings.append(
            {
                "rule_id": rule_id,
                "severity": severity,
                "file": file_path,
                "line": None,
                "evidence": reason,
                "reason": reason,
                "suggestion": suggestion,
                "needs_review": needs_review,
            }
        )

    for root, dirs, files in os.walk(project_path):
        rel_root = os.path.relpath(root, project_path)
        if _should_skip(rel_root, include, exclude):
            continue
        for name in files:
            if not name.endswith(TARGET_EXTS):
                continue
            file_path = os.path.join(root, name)
            rel_path = os.path.relpath(file_path, project_path)
            if _should_skip(rel_path, include, exclude):
                continue
            content = _scan_file(file_path)
            if not content:
                continue
            lowered = content.lower()

            # ATT / 跟踪
            if any(marker in content for marker in TRACKING_MARKERS):
                add_finding("PRIV-ATT", "medium", rel_path, "检测到跟踪/广告 SDK 或 IDFA 访问", "确保集成 ATT 申请并合规使用。", needs_review=True)

            # 支付
            if any(marker.lower() in lowered for marker in PAYMENT_MARKERS):
                add_finding("PAY-002", "high", rel_path, "检测到外链/第三方支付调用", "数字内容/服务需使用 IAP，移除外链或第三方支付。", needs_review=True)

            # 登录
            if any(marker in content for marker in LOGIN_MARKERS):
                add_finding("AUTH-003", "medium", rel_path, "检测到第三方登录实现", "若使用第三方登录，请提供 Sign in with Apple。", needs_review=True)

            # 私有 API / 反射
            if any(marker in content for marker in PRIVATE_API_MARKERS):
                add_finding("API-PRIVATE", "high", rel_path, "检测到疑似私有 API/反射调用", "移除私有 API，改用公开接口。", needs_review=True)

            # HTTP
            if HTTP_MARKER in lowered:
                add_finding("NET-HTTP", "medium", rel_path, "检测到明文 HTTP 调用", "改用 HTTPS 或配置 ATS 例外说明。", needs_review=True)

            # 后台模式实现（粗略）
            if any(marker in content for marker in BACKGROUND_MARKERS):
                add_finding("API-BG", "low", rel_path, "检测到后台模式相关代码，请确保与 Info.plist 配置匹配", "确保后台声明与实现一致，符合审核要求。", needs_review=True)

    return findings, metadata

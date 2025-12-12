# -*- coding: utf-8 -*-
"""
Plist/Entitlements scanning helpers (skeleton).

Provides loading utilities for Info.plist and Entitlements.
Detection logic to be added separately.
"""

import os
import plistlib


def load_plist(path):
    """Load a plist file and return its dict; raise IOError if missing."""
    if not os.path.exists(path):
        raise IOError("plist not found: %s" % path)
    with open(path, "rb") as f:
        return plistlib.readPlist(f)


def load_entitlements(path):
    """Load an entitlements plist; reuse load_plist for consistency."""
    return load_plist(path)


def scan(plist_path, entitlements_path=None):
    """
    Placeholder scan function.
    Returns (findings, metadata) where findings is a list of rule hits (currently empty).
    """
    plist_data = load_plist(plist_path)
    entitlements_data = load_entitlements(entitlements_path) if entitlements_path else {}

    findings = []

    def add_finding(rule_id, severity, reason, suggestion, needs_review=False):
        findings.append(
            {
                "rule_id": rule_id,
                "severity": severity,
                "file": plist_path,
                "line": None,
                "evidence": reason,
                "reason": reason,
                "suggestion": suggestion,
                "needs_review": needs_review,
            }
        )

    # 权限文案检查（常见权限键）
    permission_keys = [
        "NSCameraUsageDescription",
        "NSPhotoLibraryUsageDescription",
        "NSMicrophoneUsageDescription",
        "NSLocationWhenInUseUsageDescription",
        "NSLocationAlwaysAndWhenInUseUsageDescription",
        "NSLocationAlwaysUsageDescription",
        "NSBluetoothPeripheralUsageDescription",
        "NSContactsUsageDescription",
    ]
    for key in permission_keys:
        if key in plist_data:
            if not plist_data.get(key):
                add_finding(
                    "PRIV-001",
                    "high",
                    "权限文案 %s 为空" % key,
                    "在 Info.plist 中为 %s 添加清晰用途说明。" % key,
                )
        else:
            add_finding(
                "PRIV-001",
                "high",
                "缺少权限文案 %s" % key,
                "在 Info.plist 中添加 %s 并填入用途说明。" % key,
            )

    # ATS 检查
    ats = plist_data.get("NSAppTransportSecurity", {})
    if isinstance(ats, dict):
        allows_arbitrary = ats.get("NSAllowsArbitraryLoads", False)
        exceptions = ats.get("NSExceptionDomains", {})
        if allows_arbitrary:
            add_finding(
                "NET-001",
                "medium",
                "ATS 全局关闭 (NSAllowsArbitraryLoads=true)",
                "建议开启 ATS 或仅为特定域配置例外。",
                needs_review=True,
            )
        elif isinstance(exceptions, dict) and len(exceptions.keys()) > 5:
            add_finding(
                "NET-001",
                "medium",
                "ATS 例外域名过多: %d" % len(exceptions.keys()),
                "精简 ATS 例外域名，仅保留必要域名。",
                needs_review=True,
            )

    # 后台模式检查
    bg_modes = plist_data.get("UIBackgroundModes", [])
    if isinstance(bg_modes, list) and bg_modes:
        risky_modes = set(bg_modes) & set(["location", "audio", "voip"])
        if risky_modes:
            add_finding(
                "API-001",
                "medium",
                "存在后台模式: %s" % ", ".join(risky_modes),
                "确保后台模式有对应功能实现并符合审核要求。",
                needs_review=True,
            )

    # Sign in with Apple / URL Schemes 简单检查
    url_types = plist_data.get("CFBundleURLTypes", [])
    third_party_schemes = ("weixin", "wechat", "qq", "fb", "facebook", "google")
    has_third_party = False
    if isinstance(url_types, list):
        for item in url_types:
            schemes = item.get("CFBundleURLSchemes", []) if isinstance(item, dict) else []
            for s in schemes:
                if isinstance(s, basestring) and any(tp in s.lower() for tp in third_party_schemes):
                    has_third_party = True
                    break
    if has_third_party:
        add_finding(
            "AUTH-003",
            "medium",
            "检测到第三方登录 URL Schemes，需确认提供 Sign in with Apple",
            "如使用第三方登录，请在同等位置提供 Sign in with Apple。",
            needs_review=True,
        )

    # 导出合规标记
    if "ITSAppUsesNonExemptEncryption" not in plist_data:
        add_finding(
            "META-001",
            "low",
            "缺少导出合规标记 ITSAppUsesNonExemptEncryption",
            "在 Info.plist 中明确设置 ITSAppUsesNonExemptEncryption。",
        )

    metadata = {
        "plist_path": plist_path,
        "entitlements_path": entitlements_path,
        "plist_keys": plist_data.keys(),
    }
    return findings, metadata

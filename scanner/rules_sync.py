# -*- coding: utf-8 -*-
"""
规则同步与版本比对接口（基础实现：默认抓取苹果审核指南 HTML 作为版本来源）。
"""

import json
import os
import hashlib

from urllib import request as urllib_request  # type: ignore


VERSION_FIELDS = ("current_version", "released_at", "source_link", "changelog", "checksum")
DEFAULT_SOURCE_LINK = "https://developer.apple.com/cn/app-store/review/guidelines/"


def default_version_data():
    """返回带占位字段的版本信息。"""
    return {k: None for k in VERSION_FIELDS}


def load_version_file(path):
    """读取本地版本文件，返回 dict；不存在时返回空结构。"""
    if not os.path.exists(path):
        return default_version_data()
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except Exception:
            return default_version_data()
    # 补全缺失字段，保持向后兼容
    for key in VERSION_FIELDS:
        if key not in data:
            data[key] = None
    return data


def write_version_file(path, data):
    """写入版本文件（占位，无并发/锁处理）。"""
    normalized = default_version_data()
    normalized.update(data or {})
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, "w") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)
    return path


def compare_versions(local_version, remote_version):
    """
    简单字符串比较占位：返回 -1/0/1。
    后续可改为语义化版本比较。
    """
    lv = local_version or ""
    rv = remote_version or ""
    if lv == rv:
        return 0
    return -1 if lv < rv else 1


def fetch_official_rules(source_link=DEFAULT_SOURCE_LINK, cache_dir=None, local_rules_loader=None):
    """
    从官方源获取规则（基础实现：下载 HTML，用内容哈希作为版本；规则内容需调用方提供 loader）。
    :param source_link: 官方规则源 URL 或离线包路径
    :param cache_dir: 可选缓存目录（保存原始 HTML）
    :param local_rules_loader: 可选回调，提供解析后的规则内容；未提供时返回 None
    :return: dict 包含 version、rules、source_link、released_at、changelog、checksum
    """
    with urllib_request.urlopen(source_link) as resp:
        content = resp.read()
    checksum = hashlib.sha256(content).hexdigest()
    version = checksum[:8]

    if cache_dir:
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cache_path = os.path.join(cache_dir, "appstore_guidelines.html")
        with open(cache_path, "wb") as f:
            f.write(content)

    rules = local_rules_loader() if local_rules_loader else None

    return {
        "version": version,
        "rules": rules,
        "source_link": source_link,
        "released_at": None,
        "changelog": "同步自苹果审核指南 HTML",
        "checksum": checksum,
    }


__all__ = [
    "VERSION_FIELDS",
    "default_version_data",
    "load_version_file",
    "write_version_file",
    "compare_versions",
    "fetch_official_rules",
]

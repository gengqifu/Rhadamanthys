# -*- coding: utf-8 -*-
"""
规则同步与版本比对接口（基础实现：默认抓取苹果审核指南 HTML 作为版本来源）。
"""

import html as html_lib
import json
import os
import hashlib
import re
from typing import List, Dict

from urllib import request as urllib_request  # type: ignore


VERSION_FIELDS = ("current_version", "released_at", "source_link", "changelog", "checksum")
DEFAULT_SOURCE_LINK = "https://developer.apple.com/cn/app-store/review/guidelines/"

_GUIDELINE_SECTION_PATTERN = re.compile(r"^(\d+(?:\.\d+)+)\s+(.+)$")
_BLOCK_TAG_END = re.compile(r"</(h[1-6]|p|li|div|section|article)[^>]*>", re.IGNORECASE)
_TAG_PATTERN = re.compile(r"<[^>]+>")


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

    rules = _parse_guidelines_to_rules(content, source_link)
    parsed_ok = bool(rules)
    fallback_used = False
    if (not rules) and local_rules_loader:
        # 回退到本地规则
        rules = local_rules_loader()
        fallback_used = True

    return {
        "version": version,
        "rules": rules,
        "source_link": source_link,
        "released_at": None,
        "changelog": "同步自苹果审核指南 HTML",
        "checksum": checksum,
        "parsed_ok": parsed_ok,
        "fallback_used": fallback_used,
    }


def _decode_content(content):
    for enc in ("utf-8", "gb18030"):
        try:
            return content.decode(enc)
        except Exception:
            continue
    return content.decode("utf-8", "ignore")


def _guess_group(text: str) -> str:
    lowered = text.lower()
    if any(k in lowered for k in ["privacy", "隐私", "permission"]):
        return "PRIV"
    if any(k in lowered for k in ["pay", "payment", "支付"]):
        return "PAY"
    if any(k in lowered for k in ["login", "sign in", "登录", "认证"]):
        return "AUTH"
    if any(k in lowered for k in ["network", "http", "https", "ats", "网络"]):
        return "NET"
    if "api" in lowered:
        return "API"
    return "META"


def _parse_guidelines_to_rules(content: bytes, source_link: str) -> List[Dict]:
    """
    尝试从审核指南 HTML 中提取规则，按章节号生成规则 ID。
    结构化程度有限，属于启发式抽取；失败时返回空列表。
    """
    try:
        text = _decode_content(content)
    except Exception:
        return []

    # 粗略转为纯文本：块级标签结尾换行，去掉其它标签
    text = _BLOCK_TAG_END.sub("\n", text)
    text = _TAG_PATTERN.sub(" ", text)
    text = html_lib.unescape(text)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    rules = []
    counter = 1
    for line in lines:
        m = _GUIDELINE_SECTION_PATTERN.match(line)
        if not m:
            continue
        section, title = m.group(1), m.group(2)
        rule_id = "APP-%03d" % counter
        counter += 1
        group = _guess_group(title)
        severity = "medium"
        if any(k in title.lower() for k in ["拒绝", "违规", "禁止", "ban", "prohibit"]):
            severity = "high"
        suggestion = "参考审核指南 %s：%s，确保实现与条款要求一致。" % (section, title)
        rules.append(
            {
                "id": rule_id,
                "group": group,
                "title": title,
                "source_link": source_link,
                "section": section,
                "severity": severity,
                "confidence": "manual",
                "suggestion_template": suggestion,
                "version": "1.0.0",
                "changelog": "同步自审核指南章节 %s" % section,
            }
        )

    return rules


__all__ = [
    "VERSION_FIELDS",
    "default_version_data",
    "load_version_file",
    "write_version_file",
    "compare_versions",
    "fetch_official_rules",
]

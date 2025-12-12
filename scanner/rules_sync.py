# -*- coding: utf-8 -*-
"""
规则同步与版本比对接口占位。

目标：
- 提供规则来源描述（URL、版本号、发布日期）。
- 定义版本文件的读写与比对骨架，供 update-rules 命令使用。

注意：目前为接口占位，实际下载/解析逻辑待实现。
"""

import json
import os


def load_version_file(path):
    """读取本地版本文件，返回 dict；不存在时返回空结构。"""
    if not os.path.exists(path):
        return {"current_version": None, "released_at": None, "source_link": None, "changelog": None, "checksum": None}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {"current_version": None, "released_at": None, "source_link": None, "changelog": None, "checksum": None}


def write_version_file(path, data):
    """写入版本文件（占位，无并发/锁处理）。"""
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
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


def fetch_official_rules(source_link, cache_dir=None):
    """
    从官方源获取规则（占位）。
    :param source_link: 官方规则源 URL 或离线包路径
    :param cache_dir: 可选缓存目录
    :return: (rules_content, version_info)
    """
    raise NotImplementedError("规则获取待实现")


__all__ = ["load_version_file", "write_version_file", "compare_versions", "fetch_official_rules"]

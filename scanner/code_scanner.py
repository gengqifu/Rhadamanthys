# -*- coding: utf-8 -*-
"""
Code scanner skeleton.

Note: Detection logic (ATT/支付/登录/私有 API/HTTP/后台模式等) 尚未实现。
This file provides a stub entrypoint to be filled in when analysis utilities are ready.
"""


def scan(project_path, include=None, exclude=None):
    """
    Placeholder code scan function.
    :param project_path: 根目录
    :param include: 可选包含路径列表
    :param exclude: 可选排除路径列表
    :return: (findings, metadata)
    """
    findings = []
    metadata = {"project_path": project_path, "include": include, "exclude": exclude}
    # TODO: 实现遍历与检测逻辑（ATT/支付/登录/私有 API/HTTP/后台模式）
    return findings, metadata

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
    # TODO: implement detection for permissions/ATS/background modes/Sign in with Apple/URL Schemes/export compliance.
    findings = []
    metadata = {"plist_path": plist_path, "entitlements_path": entitlements_path, "plist_keys": plist_data.keys()}
    return findings, metadata

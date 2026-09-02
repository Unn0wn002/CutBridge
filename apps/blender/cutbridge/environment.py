"""Runtime environment diagnostics for CutBridge.

This module contains no network or installation behavior. It only reports the
runtime so users and support logs can identify compatibility problems quickly.
"""

from __future__ import annotations

import platform
import sys
from typing import Any, Dict, Iterable, Tuple

from .version import BLENDER_VERSION_MIN, TARGET_LTS_SERIES, __version__

VersionTuple = Tuple[int, int, int]


def normalize_version(value: Iterable[int]) -> VersionTuple:
    parts = list(value)[:3]
    while len(parts) < 3:
        parts.append(0)
    return int(parts[0]), int(parts[1]), int(parts[2])


def version_string(value: Iterable[int]) -> str:
    major, minor, patch = normalize_version(value)
    return f"{major}.{minor}.{patch}"


def platform_id() -> str:
    """Return Blender-style platform identifiers used by extension repositories."""
    machine = platform.machine().lower()
    is_arm = machine in {"arm64", "aarch64"} or machine.startswith("arm")

    if sys.platform.startswith("win"):
        return "windows-arm64" if is_arm else "windows-x64"
    if sys.platform == "darwin":
        return "macos-arm64" if is_arm else "macos-x64"
    if sys.platform.startswith("linux"):
        return "linux-arm64" if is_arm else "linux-x64"
    return f"{sys.platform}-{machine or 'unknown'}"


def compatibility_status(blender_version: Iterable[int]) -> Dict[str, str]:
    version = normalize_version(blender_version)
    if version < BLENDER_VERSION_MIN:
        return {
            "code": "UNSUPPORTED",
            "label": "Unsupported",
            "detail": f"Requires Blender {version_string(BLENDER_VERSION_MIN)} or newer",
        }

    series = version[:2]
    if series in TARGET_LTS_SERIES:
        return {
            "code": "TARGET_LTS",
            "label": "Target LTS",
            "detail": "Matches a CutBridge LTS compatibility target",
        }

    return {
        "code": "UNVERIFIED",
        "label": "Compatible baseline / unverified",
        "detail": "Meets the minimum version but is not an LTS target in the current test matrix",
    }


def snapshot(bpy_module: Any) -> Dict[str, Any]:
    blender_version = normalize_version(getattr(bpy_module.app, "version", (0, 0, 0)))
    compatibility = compatibility_status(blender_version)
    return {
        "cutbridge_version": __version__,
        "blender_version": version_string(blender_version),
        "python_version": platform.python_version(),
        "platform": platform_id(),
        "compatibility_code": compatibility["code"],
        "compatibility_label": compatibility["label"],
        "compatibility_detail": compatibility["detail"],
        "online_access": bool(getattr(bpy_module.app, "online_access", False)),
        "online_access_overridden": bool(
            getattr(bpy_module.app, "online_access_overridden", False)
        ),
    }

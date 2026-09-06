from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .core import absolute_output_dir, package_name


def issue(level: str, code: str, message: str, fix: str) -> dict:
    return {"level": level, "code": code, "message": message, "fix": fix}


def format_issue(item: dict) -> str:
    """Compact actionable text suitable for Blender operator reports."""
    message = str(item.get("message", "CutBridge validation issue.")).strip()
    fix = str(item.get("fix", "")).strip()
    return f"{message} Fix: {fix}" if fix else message


def package_target(settings) -> Path:
    return absolute_output_dir(settings) / package_name(settings)


def package_target_issues(settings) -> list[dict]:
    """Refuse silent overwrite of an existing versioned CutBridge package."""
    if not getattr(settings, "output_dir", "").strip():
        return []

    try:
        root = package_target(settings)
    except (OSError, RuntimeError, ValueError) as exc:
        return [
            issue(
                "ERROR",
                "OUTPUT_UNAVAILABLE",
                f"Package output path cannot be resolved: {exc}",
                "Choose a valid writable package output directory.",
            )
        ]

    try:
        if root.is_symlink():
            return [
                issue(
                    "ERROR",
                    "PACKAGE_TARGET_SYMLINK",
                    f"Package target is a symbolic link: {root}",
                    "Choose a normal directory or increment the CutBridge version.",
                )
            ]
        if root.exists() and not root.is_dir():
            return [
                issue(
                    "ERROR",
                    "PACKAGE_TARGET_NOT_DIRECTORY",
                    f"Package target already exists and is not a directory: {root}",
                    "Choose another output location or increment the CutBridge version.",
                )
            ]
        if root.is_dir() and any(root.iterdir()):
            return [
                issue(
                    "ERROR",
                    "PACKAGE_EXISTS",
                    f"Package {root.name} already contains data and will not be overwritten.",
                    "Increment Version for a new revision, or deliberately move/remove the existing package first.",
                )
            ]
    except OSError as exc:
        return [
            issue(
                "ERROR",
                "OUTPUT_UNAVAILABLE",
                f"Package target cannot be inspected: {exc}",
                "Check output-directory permissions and path accessibility.",
            )
        ]

    return []


def assert_package_integrity(package_root: Path, manifest: dict, passes: Iterable[str]) -> None:
    """Verify the just-built package has the minimum deterministic handoff structure."""
    manifest_path = package_root / "cutbridge.json"
    if not manifest_path.is_file():
        raise RuntimeError("Package integrity failed: cutbridge.json was not created.")

    try:
        written = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Package integrity failed: cutbridge.json cannot be read: {exc}") from exc

    if written != manifest:
        raise RuntimeError("Package integrity failed: written manifest does not match generated manifest.")
    if written.get("package_name") != package_root.name:
        raise RuntimeError("Package integrity failed: manifest package_name does not match the package folder.")

    required_dirs = [package_root / "preview", package_root / "camera"]
    required_dirs.extend(package_root / "render" / str(name).lower() for name in passes)
    missing = [path.relative_to(package_root).as_posix() for path in required_dirs if not path.is_dir()]
    if missing:
        raise RuntimeError("Package integrity failed: missing folder(s): " + ", ".join(missing))

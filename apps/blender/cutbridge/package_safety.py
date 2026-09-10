from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Iterator

from .core import absolute_output_dir, effective_package_name, studio_preset_issues


def issue(level: str, code: str, message: str, fix: str) -> dict:
    return {"level": level, "code": code, "message": message, "fix": fix}


def format_issue(item: dict) -> str:
    """Compact actionable text suitable for Blender operator reports."""
    message = str(item.get("message", "CutBridge validation issue.")).strip()
    fix = str(item.get("fix", "")).strip()
    return f"{message} Fix: {fix}" if fix else message


def package_target(settings) -> Path:
    return absolute_output_dir(settings) / effective_package_name(settings)


def _iter_package_paths(root: Path) -> Iterator[Path]:
    """Yield package entries lazily so safety checks can stop at first payload."""
    yield from root.rglob("*")


def _first_package_payload_file(root: Path) -> Path | None:
    """Return the first user/render payload without enumerating the full package tree."""
    for path in _iter_package_paths(root):
        if path.is_symlink():
            return path
        if path.is_file() and path.name != "cutbridge.json":
            return path
    return None


def package_target_issues(settings) -> list[dict]:
    """Prevent overwriting rendered/user data while allowing an unrendered scaffold refresh."""
    if not getattr(settings, "output_dir", "").strip():
        return []

    # Preset validation owns preset-specific diagnostics. Avoid producing a
    # second misleading OUTPUT_UNAVAILABLE error for an invalid custom preset.
    if studio_preset_issues(settings):
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
        if root.is_dir():
            payload = _first_package_payload_file(root)
            if payload is not None:
                sample = payload.relative_to(root).as_posix()
                return [
                    issue(
                        "ERROR",
                        "PACKAGE_EXISTS",
                        f"Package {root.name} contains render/user data ({sample}) and will not be overwritten.",
                        "Increment Version for a new revision, or deliberately move/remove the existing package first.",
                    )
                ]
            if (root / "cutbridge.json").is_file():
                return [
                    issue(
                        "WARNING",
                        "PACKAGE_SCAFFOLD_REFRESH",
                        f"Package {root.name} exists but contains no render/user payload; its scaffold can be refreshed safely.",
                        "Increment Version before rendering when this should become a new revision.",
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

    folders = written.get("folders") or {}
    preview_folder = str(folders.get("preview") or "preview")
    camera_folder = str(folders.get("camera") or "camera")
    required_dirs = [package_root / preview_folder, package_root / camera_folder]

    # Pass paths are already normalized package-relative paths in the manifest.
    # Using them here keeps integrity verification aligned with a validated
    # Studio Preset without hard-coding the pre-S9 render folder name.
    manifest_passes = written.get("passes") or []
    pass_paths = {
        str(item.get("name")): str(item.get("path"))
        for item in manifest_passes
        if isinstance(item, dict) and item.get("name") and item.get("path")
    }
    for name in passes:
        relative = pass_paths.get(str(name))
        if not relative:
            raise RuntimeError(f"Package integrity failed: manifest path missing for pass {name}.")
        required_dirs.append(package_root / relative)

    missing = [path.relative_to(package_root).as_posix() for path in required_dirs if not path.is_dir()]
    if missing:
        raise RuntimeError("Package integrity failed: missing folder(s): " + ", ".join(missing))

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Iterator

from .core import absolute_output_dir, build_manifest, effective_package_name, studio_preset_issues


_RENDER_CONTRACT_KEYS = (
    "schema",
    "schema_version",
    "project",
    "episode",
    "scene",
    "cut",
    "take",
    "version",
    "version_label",
    "package_name",
    "fps",
    "resolution",
    "frames",
    "camera",
    "passes",
    "folders",
    "ae",
    "studio_preset",
)


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


def _target_state(settings) -> dict:
    """Inspect the current target once and classify it without mutating Blender state."""
    if not getattr(settings, "output_dir", "").strip():
        return {"kind": "NONE"}

    # Preset validation owns preset-specific diagnostics. Avoid producing a
    # second misleading OUTPUT_UNAVAILABLE error for an invalid custom preset.
    if studio_preset_issues(settings):
        return {"kind": "NONE"}

    try:
        root = package_target(settings)
    except (OSError, RuntimeError, ValueError) as exc:
        return {
            "kind": "ERROR",
            "issue": issue(
                "ERROR",
                "OUTPUT_UNAVAILABLE",
                f"Package output path cannot be resolved: {exc}",
                "Choose a valid writable package output directory.",
            ),
        }

    try:
        if root.is_symlink():
            return {
                "kind": "ERROR",
                "root": root,
                "issue": issue(
                    "ERROR",
                    "PACKAGE_TARGET_SYMLINK",
                    f"Package target is a symbolic link: {root}",
                    "Choose a normal directory or increment the CutBridge version.",
                ),
            }
        if root.exists() and not root.is_dir():
            return {
                "kind": "ERROR",
                "root": root,
                "issue": issue(
                    "ERROR",
                    "PACKAGE_TARGET_NOT_DIRECTORY",
                    f"Package target already exists and is not a directory: {root}",
                    "Choose another output location or increment the CutBridge version.",
                ),
            }
        if root.is_dir():
            payload = _first_package_payload_file(root)
            manifest_path = root / "cutbridge.json"
            if payload is not None:
                return {
                    "kind": "PAYLOAD",
                    "root": root,
                    "payload": payload,
                    "manifest_path": manifest_path if manifest_path.is_file() else None,
                }
            if manifest_path.is_file():
                return {"kind": "SCAFFOLD", "root": root, "manifest_path": manifest_path}
        return {"kind": "NEW", "root": root}
    except OSError as exc:
        return {
            "kind": "ERROR",
            "root": root,
            "issue": issue(
                "ERROR",
                "OUTPUT_UNAVAILABLE",
                f"Package target cannot be inspected: {exc}",
                "Check output-directory permissions and path accessibility.",
            ),
        }


def _render_contract(manifest: dict) -> dict:
    return {key: manifest.get(key) for key in _RENDER_CONTRACT_KEYS}


def _payload_sample(state: dict) -> str:
    root = state["root"]
    payload = state["payload"]
    try:
        return payload.relative_to(root).as_posix()
    except ValueError:
        return str(payload)


def _manifest_matches_current_context(context, state: dict) -> tuple[bool, str]:
    manifest_path = state.get("manifest_path")
    if manifest_path is None:
        return False, "cutbridge.json is missing"
    try:
        written = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"cutbridge.json cannot be verified: {exc}"

    if not isinstance(written, dict):
        return False, "cutbridge.json does not contain a manifest object"

    try:
        expected = build_manifest(context, state["root"])
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as exc:
        return False, f"current CutBridge settings cannot be compared to the package manifest: {exc}"

    if _render_contract(written) != _render_contract(expected):
        return False, "the existing manifest no longer matches the current cut/render settings"
    return True, ""


def package_target_issues(settings) -> list[dict]:
    """Build-Package guard: never overwrite existing rendered/user payload."""
    state = _target_state(settings)
    kind = state["kind"]

    if kind == "ERROR":
        return [state["issue"]]
    if kind == "PAYLOAD":
        root = state["root"]
        sample = _payload_sample(state)
        return [
            issue(
                "ERROR",
                "PACKAGE_EXISTS",
                f"Package {root.name} contains render/user data ({sample}) and will not be overwritten.",
                "For a new revision, increment Version. To keep rendering this already-built version, do not run Build Package again.",
            )
        ]
    if kind == "SCAFFOLD":
        root = state["root"]
        return [
            issue(
                "WARNING",
                "PACKAGE_SCAFFOLD_REFRESH",
                f"Package {root.name} exists but contains no render/user payload; its scaffold can be refreshed safely.",
                "Increment Version before rendering when this should become a new revision.",
            )
        ]
    return []


def package_lifecycle_issues(context) -> list[dict]:
    """General validation/UI lifecycle state, distinct from Build Package overwrite safety.

    A matching package that already contains rendered payload is an INFO state:
    rendering may continue, while Build Package remains protected by
    package_target_issues(). If the existing manifest no longer matches current
    cut/render settings, fail closed so new output is not mixed into that package.
    """
    settings = context.scene.cutbridge
    state = _target_state(settings)
    kind = state["kind"]

    if kind == "ERROR":
        return [state["issue"]]
    if kind == "SCAFFOLD":
        root = state["root"]
        return [
            issue(
                "WARNING",
                "PACKAGE_SCAFFOLD_REFRESH",
                f"Package {root.name} exists but contains no render/user payload; its scaffold can be refreshed safely.",
                "Increment Version before rendering when this should become a new revision.",
            )
        ]
    if kind != "PAYLOAD":
        return []

    root = state["root"]
    sample = _payload_sample(state)
    payload = state["payload"]
    if payload.is_symlink():
        return [
            issue(
                "ERROR",
                "PACKAGE_STATE_MISMATCH",
                f"Package {root.name} contains a symbolic-link payload ({sample}) and cannot be treated as render-ready.",
                "Use a normal package directory and increment Version before creating new output.",
            )
        ]

    matches, detail = _manifest_matches_current_context(context, state)
    if matches:
        return [
            issue(
                "INFO",
                "PACKAGE_RENDER_READY",
                f"Package {root.name} is already built and matches the current cut/render settings. Existing payload sample: {sample}.",
                "Continue Render Animation with this package. Increment Version only when intentionally creating a new revision.",
            )
        ]

    return [
        issue(
            "ERROR",
            "PACKAGE_STATE_MISMATCH",
            f"Package {root.name} already contains render/user data ({sample}), but {detail}.",
            "Restore the settings used by this package or increment Version for a new revision. Do not rebuild or render new output into this existing package with changed settings.",
        )
    ]


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

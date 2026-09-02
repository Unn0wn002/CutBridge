from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterable

import bpy

from .version import __version__

INVALID_FS_CHARS = re.compile(r'[<>:"/\\|?*]+')


def safe_token(value: str, fallback: str) -> str:
    value = (value or "").strip()
    value = INVALID_FS_CHARS.sub("_", value)
    value = re.sub(r"\s+", "_", value)
    return value or fallback


def version_token(version: int) -> str:
    return f"V{int(version):03d}"


def package_name(settings) -> str:
    parts = [
        safe_token(settings.project, "PROJECT"),
        safe_token(settings.episode, "EP00"),
        safe_token(settings.scene_id, "SC000"),
        safe_token(settings.cut, "C000"),
        safe_token(settings.take, "T01"),
        version_token(settings.version),
    ]
    return "_".join(parts)


def extension_for(image_format: str) -> str:
    return {"PNG": ".png", "OPEN_EXR": ".exr", "TIFF": ".tif"}.get(image_format, ".png")


def selected_passes(settings) -> list[str]:
    result = []
    if settings.pass_beauty:
        result.append("BEAUTY")
    if settings.pass_line:
        result.append("LINE")
    if settings.pass_shadow:
        result.append("SHADOW")
    if settings.pass_depth:
        result.append("DEPTH")
    return result


def absolute_output_dir(settings) -> Path:
    # bpy.path.abspath resolves // relative to the current .blend path.
    return Path(bpy.path.abspath(settings.output_dir)).expanduser().resolve()


def validate_scene(context) -> list[dict]:
    scene = context.scene
    s = scene.cutbridge
    issues = []

    def err(code, message, fix):
        issues.append({"level": "ERROR", "code": code, "message": message, "fix": fix})

    def warn(code, message, fix):
        issues.append({"level": "WARNING", "code": code, "message": message, "fix": fix})

    for attr, label in (
        ("project", "Project"),
        ("episode", "Episode"),
        ("scene_id", "Scene"),
        ("cut", "Cut"),
        ("take", "Take"),
    ):
        if not getattr(s, attr).strip():
            err("ID_MISSING", f"{label} is empty.", f"Fill the {label} field.")

    if scene.camera is None:
        err("CAMERA_MISSING", "No active scene camera.", "Assign an active camera in Scene Properties.")

    if scene.render.fps <= 0:
        err("FPS_INVALID", "FPS must be greater than zero.", "Set a valid scene FPS.")

    if scene.frame_end < scene.frame_start:
        err("FRAME_RANGE_INVALID", "Frame end is before frame start.", "Correct the frame range.")

    if scene.render.resolution_x <= 0 or scene.render.resolution_y <= 0:
        err("RESOLUTION_INVALID", "Resolution must be positive.", "Set a valid resolution.")

    if not selected_passes(s):
        err("PASS_MISSING", "No render pass is selected.", "Enable at least one package pass.")

    if not s.output_dir.strip():
        err("OUTPUT_MISSING", "Package output directory is empty.", "Choose a package output directory.")

    if not bpy.data.filepath:
        warn(
            "BLEND_UNSAVED",
            "The .blend file has not been saved yet.",
            "Save the .blend file before using a // relative output path.",
        )

    return issues


def build_manifest(context, package_root: Path) -> dict:
    scene = context.scene
    s = scene.cutbridge
    ext = extension_for(s.image_format)
    passes = []
    for pass_name in selected_passes(s):
        folder_name = pass_name.lower()
        # Sequence path is relative to the package root. AE resolves it from manifest location.
        passes.append(
            {
                "name": pass_name,
                "path": f"render/{folder_name}",
                "sequence_pattern": f"{safe_token(s.cut, 'C000')}_{pass_name}_####{ext}",
                "required": True,
            }
        )

    duration_frames = int(scene.frame_end - scene.frame_start + 1)
    fps = float(scene.render.fps) / float(scene.render.fps_base or 1.0)
    manifest = {
        "schema": "cutbridge-manifest",
        "schema_version": 1,
        "cutbridge_version": __version__,
        "project": s.project,
        "episode": s.episode,
        "scene": s.scene_id,
        "cut": s.cut,
        "take": s.take,
        "version": int(s.version),
        "version_label": version_token(s.version),
        "package_name": package_name(s),
        "fps": fps,
        "resolution": {
            "width": int(scene.render.resolution_x),
            "height": int(scene.render.resolution_y),
            "pixel_aspect": float(scene.render.pixel_aspect_x) / float(scene.render.pixel_aspect_y or 1.0),
        },
        "frames": {
            "start": int(scene.frame_start),
            "end": int(scene.frame_end),
            "count": duration_frames,
        },
        "camera": scene.camera.name if scene.camera else None,
        "source_blend": bpy.path.basename(bpy.data.filepath) if bpy.data.filepath else None,
        "passes": passes,
        "folders": {
            "render": "render",
            "preview": "preview",
            "camera": "camera",
        },
        "ae": {
            "comp_name": f"{safe_token(s.cut, 'C000')}_COMP",
            "layer_order": [p["name"] for p in passes],
        },
    }
    return manifest


def write_manifest(manifest: dict, package_root: Path) -> Path:
    path = package_root / "cutbridge.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def ensure_package_dirs(package_root: Path, passes: Iterable[str]) -> None:
    package_root.mkdir(parents=True, exist_ok=True)
    (package_root / "preview").mkdir(exist_ok=True)
    (package_root / "camera").mkdir(exist_ok=True)
    for pass_name in passes:
        (package_root / "render" / pass_name.lower()).mkdir(parents=True, exist_ok=True)

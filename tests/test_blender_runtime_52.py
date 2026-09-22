"""Runtime registration smoke test executed with the official bpy 5.2.1 wheel."""

from __future__ import annotations

import pathlib
import sys

import bpy

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402
from cutbridge import core, update_ops  # noqa: E402


def is_registered(cls):
    # Blender injects `bl_rna` into successfully registered Python RNA classes.
    return "bl_rna" in cls.__dict__


def assert_clean():
    assert not hasattr(bpy.types.Scene, "cutbridge")
    assert not bpy.app.timers.is_registered(update_ops._startup_update_check)
    for cls in cutbridge.CLASSES:
        assert not is_registered(cls), f"stale RNA class: {cls.__name__}"


def run_cycle():
    cutbridge.register()
    assert hasattr(bpy.types.Scene, "cutbridge")
    assert not bpy.app.timers.is_registered(update_ops._startup_update_check)
    for cls in cutbridge.CLASSES:
        assert is_registered(cls), f"class did not register: {cls.__name__}"

    scene = bpy.context.scene
    if scene is not None:
        settings = scene.cutbridge
        assert hasattr(settings, "per_pass_formats_enabled")
        assert hasattr(settings, "format_depth")
        settings.pass_beauty = True
        settings.pass_depth = True
        settings.image_format = "PNG"
        settings.per_pass_formats_enabled = True
        settings.format_beauty = "PNG"
        settings.format_depth = "OPEN_EXR"
        assert core.effective_pass_image_format(settings, "BEAUTY") == "PNG"
        assert core.effective_pass_image_format(settings, "DEPTH") == "OPEN_EXR"

    cutbridge.unregister()
    assert_clean()


if __name__ == "__main__":
    print("bpy version:", bpy.app.version_string)
    assert bpy.app.version == (5, 2, 1), bpy.app.version_string
    assert_clean()
    run_cycle()
    run_cycle()
    print("CutBridge Blender 5.2 RNA registration: PASS")

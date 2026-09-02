"""Runtime registration smoke test executed with the official bpy 5.2.1 wheel."""

from __future__ import annotations

import pathlib
import sys

import bpy

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402


def assert_clean():
    assert not hasattr(bpy.types.Scene, "cutbridge")
    lookup = getattr(bpy.types.Struct, "bl_rna_get_subclass_py")
    for cls in cutbridge.CLASSES:
        assert lookup(cls.__name__) is None, f"stale RNA class: {cls.__name__}"


def run_cycle():
    cutbridge.register()
    assert hasattr(bpy.types.Scene, "cutbridge")
    assert bpy.types.Struct.bl_rna_get_subclass_py("CUTBRIDGE_AP_Preferences") is not None
    cutbridge.unregister()
    assert_clean()


if __name__ == "__main__":
    print("bpy version:", bpy.app.version_string)
    assert bpy.app.version[:2] == (5, 2), bpy.app.version_string
    assert_clean()
    run_cycle()
    run_cycle()
    print("CutBridge Blender 5.2 RNA registration: PASS")

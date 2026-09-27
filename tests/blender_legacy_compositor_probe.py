"""Focused Blender 4.2/4.5 check for CutBridge's legacy compositor state path.

Run with the target Blender executable:
    blender --background --factory-startup --python tests/blender_legacy_compositor_probe.py
"""

from __future__ import annotations

import pathlib
import sys

import bpy

# This standalone host probe must not create bytecode beside the candidate.
sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "blender"))

import cutbridge  # noqa: E402
from cutbridge.core import (  # noqa: E402
    _capture_render_mapping_state,
    _compositor_tree,
    _restore_render_mapping_state,
)


def main() -> None:
    version = bpy.app.version[:2]
    if version not in {(4, 2), (4, 5)}:
        raise RuntimeError(f"Expected Blender 4.2 or 4.5, got {bpy.app.version_string}")

    scene = bpy.context.scene
    layer = bpy.context.view_layer
    original_use_nodes = scene.use_nodes
    cutbridge.unregister()
    cutbridge.register()
    try:
        scene.use_nodes = False
        state = _capture_render_mapping_state(scene, layer, ("BEAUTY",))
        assert state["legacy_use_nodes"] is False

        tree = _compositor_tree(scene)
        assert tree is scene.node_tree
        assert scene.use_nodes is True

        _restore_render_mapping_state(scene, layer, state)
        assert scene.use_nodes is False
        print(f"CUTBRIDGE_LEGACY_COMPOSITOR_STATE_RESTORE_PASS {bpy.app.version_string}")
    finally:
        scene.use_nodes = original_use_nodes
        cutbridge.unregister()


if __name__ == "__main__":
    main()

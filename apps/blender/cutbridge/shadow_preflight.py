from __future__ import annotations

import bpy

from .core import PASS_MAPPINGS, selected_passes


def _view_layer(context):
    layer = getattr(context, "view_layer", None)
    if layer is not None:
        return layer
    scene = context.scene
    return scene.view_layers[0] if scene.view_layers else None


def _shadow_error(detail: str = "") -> dict:
    message = "Shadow is enabled, but the current render engine/View Layer cannot expose the required Shadow Render Layers output."
    if detail:
        message += f" {detail}"
    return {
        "level": "ERROR",
        "code": "SHADOW_OUTPUT_UNAVAILABLE",
        "message": message,
        "fix": "Use a renderer/View Layer configuration that exposes the Shadow render pass, or disable Shadow.",
    }


def _probe_shadow_socket(scene, layer) -> tuple[bool, str]:
    """Probe the active renderer/View Layer without leaving artist state changed.

    Shadow is a CutBridge-managed pass flag, so validation temporarily enables
    the View Layer pass exactly long enough to inspect a detached Render Layers
    node, then restores the artist's original flag in all cases.
    """
    mapping = PASS_MAPPINGS["SHADOW"]
    attr = mapping["enable_attr"]
    if not attr or not hasattr(layer, attr):
        return False, "The active View Layer does not expose the Shadow pass control."

    original = bool(getattr(layer, attr))
    probe_tree = None
    try:
        setattr(layer, attr, True)
        probe_tree = bpy.data.node_groups.new("CutBridge_Shadow_Preflight", "CompositorNodeTree")
        node = probe_tree.nodes.new("CompositorNodeRLayers")
        node.scene = scene
        if hasattr(node, "layer"):
            node.layer = layer.name
        for socket_name in mapping["socket_names"]:
            if node.outputs.get(socket_name) is not None:
                return True, ""
        return False, "The Render Layers node does not expose a Shadow socket for this renderer."
    except (AttributeError, RuntimeError, TypeError, ValueError) as exc:
        return False, f"CutBridge could not verify the Shadow Render Layers output: {exc}"
    finally:
        try:
            setattr(layer, attr, original)
        except (AttributeError, RuntimeError, TypeError, ValueError):
            pass
        if probe_tree is not None:
            try:
                bpy.data.node_groups.remove(probe_tree)
            except (ReferenceError, RuntimeError):
                pass


def shadow_pass_preflight_issues(context) -> list[dict]:
    """Fail early when selected SHADOW output is unavailable."""
    scene = context.scene
    settings = scene.cutbridge
    if "SHADOW" not in selected_passes(settings):
        return []

    layer = _view_layer(context)
    if layer is None:
        # validate_scene owns VIEW_LAYER_MISSING.
        return []

    supported, detail = _probe_shadow_socket(scene, layer)
    if not supported:
        return [_shadow_error(detail)]
    return []

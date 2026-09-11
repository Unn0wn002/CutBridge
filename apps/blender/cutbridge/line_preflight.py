from __future__ import annotations

import bpy

from .core import PASS_MAPPINGS, selected_passes


def _view_layer(context):
    layer = getattr(context, "view_layer", None)
    if layer is not None:
        return layer
    scene = context.scene
    return scene.view_layers[0] if scene.view_layers else None


def _line_error(detail: str = "") -> dict:
    message = "Line is enabled, but Blender Freestyle output is unavailable in the current View Layer/render setup."
    if detail:
        message += f" {detail}"
    return {
        "level": "ERROR",
        "code": "LINE_OUTPUT_UNAVAILABLE",
        "message": message,
        "fix": "Enable/configure Freestyle with As Render Pass for the active View Layer, or disable Line.",
    }


def _probe_freestyle_socket(scene, layer) -> tuple[bool, str]:
    """Inspect a detached Render Layers node without touching the artist compositor."""
    probe_tree = None
    try:
        probe_tree = bpy.data.node_groups.new("CutBridge_Line_Preflight", "CompositorNodeTree")
        node = probe_tree.nodes.new("CompositorNodeRLayers")
        node.scene = scene
        if hasattr(node, "layer"):
            node.layer = layer.name
        for socket_name in PASS_MAPPINGS["LINE"]["socket_names"]:
            if node.outputs.get(socket_name) is not None:
                return True, ""
        return False, "The active Render Layers output does not expose Freestyle."
    except (AttributeError, RuntimeError, TypeError, ValueError) as exc:
        return False, f"CutBridge could not verify the Freestyle Render Layers output: {exc}"
    finally:
        if probe_tree is not None:
            try:
                bpy.data.node_groups.remove(probe_tree)
            except (ReferenceError, RuntimeError):
                pass


def line_pass_preflight_issues(context) -> list[dict]:
    """Fail early when the selected LINE pass cannot produce a Freestyle output.

    This preflight is intentionally non-destructive: it does not modify the
    scene compositor, render flags, View Layer flags, or Freestyle settings.
    Build Package retains its own socket check as defense-in-depth.
    """
    scene = context.scene
    settings = scene.cutbridge
    if "LINE" not in selected_passes(settings):
        return []

    layer = _view_layer(context)
    if layer is None:
        # validate_scene already owns the canonical VIEW_LAYER_MISSING error.
        return []

    if not hasattr(scene.render, "use_freestyle") or not hasattr(layer, "use_freestyle"):
        return [_line_error("Freestyle is not available for this render engine/View Layer.")]

    if not bool(scene.render.use_freestyle):
        return [_line_error("Freestyle is disabled in Render Properties.")]

    if not bool(layer.use_freestyle):
        return [_line_error("Freestyle is disabled for the active View Layer.")]

    freestyle_settings = getattr(layer, "freestyle_settings", None)
    if freestyle_settings is None:
        return [_line_error("The active View Layer does not expose Freestyle settings.")]

    if hasattr(freestyle_settings, "as_render_pass") and not bool(freestyle_settings.as_render_pass):
        return [_line_error("Freestyle 'As Render Pass' is disabled for the active View Layer.")]

    supported, detail = _probe_freestyle_socket(scene, layer)
    if not supported:
        return [_line_error(detail)]
    return []

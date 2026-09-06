from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterable

import bpy

from .version import __version__

INVALID_FS_CHARS = re.compile(r'[<>:"/\\|?*]+')
MANAGED_NODE_PREFIX = "CUTBRIDGE_"
PENDING_NODE_PREFIX = f"{MANAGED_NODE_PREFIX}PENDING_"

# Logical CutBridge passes intentionally map to renderer/view-layer concepts,
# not to studio-specific node names. Blender exposes the corresponding Render
# Layers sockets only when the pass is supported and enabled by the active
# render engine/view layer.
PASS_MAPPINGS = {
    "BEAUTY": {
        "socket_names": ("Image",),
        "enable_attr": None,
        "socket_type": "RGBA",
    },
    "LINE": {
        "socket_names": ("Freestyle",),
        "enable_attr": "use_freestyle",
        "socket_type": "RGBA",
    },
    "SHADOW": {
        "socket_names": ("Shadow",),
        "enable_attr": "use_pass_shadow",
        "socket_type": "RGBA",
    },
    "DEPTH": {
        "socket_names": ("Depth", "Z"),
        "enable_attr": "use_pass_z",
        "socket_type": "FLOAT",
    },
}


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


def _view_layer(context):
    layer = getattr(context, "view_layer", None)
    if layer is not None:
        return layer
    scene = context.scene
    return scene.view_layers[0] if scene.view_layers else None


def render_mapping_issues(context) -> list[dict]:
    """Return renderer/view-layer capability problems without mutating the scene."""
    scene = context.scene
    settings = scene.cutbridge
    layer = _view_layer(context)
    issues = []

    def err(code, message, fix):
        issues.append({"level": "ERROR", "code": code, "message": message, "fix": fix})

    def warn(code, message, fix):
        issues.append({"level": "WARNING", "code": code, "message": message, "fix": fix})

    if layer is None:
        err("VIEW_LAYER_MISSING", "No active View Layer is available for render mapping.", "Create or enable a View Layer.")
        return issues

    for pass_name in selected_passes(settings):
        mapping = PASS_MAPPINGS[pass_name]
        enable_attr = mapping["enable_attr"]
        if enable_attr and not hasattr(layer, enable_attr):
            err(
                "PASS_MAPPING_UNSUPPORTED",
                f"{pass_name} cannot be enabled on View Layer '{layer.name}' with render engine {scene.render.engine}.",
                "Disable this CutBridge pass or choose a render engine/View Layer that exposes the required pass.",
            )

    if settings.pass_depth and settings.image_format != "OPEN_EXR":
        warn(
            "DEPTH_FORMAT_LOSSY",
            "DEPTH is a floating-point data pass but the selected package format is not OpenEXR.",
            "Prefer OpenEXR when DEPTH values must remain numerically accurate.",
        )

    return issues


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

    issues.extend(render_mapping_issues(context))
    return issues


def _compositor_tree(scene):
    """Return/create the scene compositor tree across Blender 4.2+ and 5.x."""
    if hasattr(scene, "compositing_node_group"):
        tree = scene.compositing_node_group
        if tree is None:
            tree = bpy.data.node_groups.new(f"CutBridge_{scene.name}_Compositor", "CompositorNodeTree")
            scene.compositing_node_group = tree
        scene.render.use_compositing = True
        return tree

    # Blender 4.x compatibility path. scene.node_tree was removed in Blender 5.0.
    scene.use_nodes = True
    return scene.node_tree


def clear_managed_render_outputs(scene) -> None:
    """Remove only compositor nodes owned by CutBridge, preserving artist nodes."""
    tree = getattr(scene, "compositing_node_group", None)
    if tree is None and hasattr(scene, "node_tree"):
        tree = scene.node_tree
    if tree is None:
        return
    for node in list(tree.nodes):
        if node.name.startswith(MANAGED_NODE_PREFIX):
            tree.nodes.remove(node)


def _enable_view_layer_passes(scene, layer, pass_names: Iterable[str]) -> None:
    pass_names = tuple(pass_names)
    if "LINE" in pass_names and hasattr(scene.render, "use_freestyle"):
        scene.render.use_freestyle = True
    for pass_name in pass_names:
        enable_attr = PASS_MAPPINGS[pass_name]["enable_attr"]
        if enable_attr:
            setattr(layer, enable_attr, True)
    try:
        layer.update_render_passes()
    except (AttributeError, RuntimeError):
        # Some engines refresh the sockets when the Render Layers node is created.
        pass


def _find_output_socket(render_layers_node, pass_name: str):
    for socket_name in PASS_MAPPINGS[pass_name]["socket_names"]:
        socket = render_layers_node.outputs.get(socket_name)
        if socket is not None:
            return socket
    return None


def _capture_render_mapping_state(scene, layer, pass_names: Iterable[str]) -> dict:
    """Capture every non-node setting CutBridge may mutate during mapping."""
    pass_names = tuple(pass_names)
    layer_flags = {}
    for pass_name in pass_names:
        enable_attr = PASS_MAPPINGS[pass_name]["enable_attr"]
        if enable_attr and hasattr(layer, enable_attr):
            layer_flags[enable_attr] = getattr(layer, enable_attr)

    return {
        "compositor_tree": getattr(scene, "compositing_node_group", None),
        "use_compositing": getattr(scene.render, "use_compositing", None),
        "use_nodes": getattr(scene, "use_nodes", None),
        "use_freestyle": getattr(scene.render, "use_freestyle", None),
        "layer_flags": layer_flags,
    }


def _restore_render_mapping_state(scene, layer, state: dict, created_tree=None) -> None:
    """Restore render/View Layer flags and a compositor tree created by a failed attempt."""
    if state["use_freestyle"] is not None:
        scene.render.use_freestyle = state["use_freestyle"]
    for attr, value in state["layer_flags"].items():
        setattr(layer, attr, value)
    try:
        layer.update_render_passes()
    except (AttributeError, RuntimeError):
        pass

    if state["use_compositing"] is not None:
        scene.render.use_compositing = state["use_compositing"]
    if state["use_nodes"] is not None and hasattr(scene, "use_nodes"):
        scene.use_nodes = state["use_nodes"]

    if hasattr(scene, "compositing_node_group") and scene.compositing_node_group is not state["compositor_tree"]:
        scene.compositing_node_group = state["compositor_tree"]
    if created_tree is not None and created_tree is not state["compositor_tree"]:
        try:
            bpy.data.node_groups.remove(created_tree)
        except (ReferenceError, RuntimeError):
            pass


def _remove_nodes_by_name(tree, node_names: Iterable[str]) -> None:
    """Remove nodes by stable Blender names; bpy may return different Python proxies."""
    for name in tuple(node_names):
        node = tree.nodes.get(name)
        if node is not None:
            tree.nodes.remove(node)


def configure_render_outputs(context, package_root: Path) -> dict[str, str]:
    """Transactionally replace CutBridge-owned compositor outputs.

    Artist nodes and the previous valid CutBridge mapping remain untouched until
    every selected pass has a usable socket and every replacement output has
    been created successfully. A failed attempt removes only its pending nodes
    and restores all render/View Layer settings it changed.
    """
    scene = context.scene
    settings = scene.cutbridge
    layer = _view_layer(context)
    mapping_errors = [issue for issue in render_mapping_issues(context) if issue["level"] == "ERROR"]
    if mapping_errors:
        raise RuntimeError(mapping_errors[0]["message"])
    if layer is None:
        raise RuntimeError("No active View Layer is available for render mapping.")

    pass_names = selected_passes(settings)
    state = _capture_render_mapping_state(scene, layer, pass_names)
    tree = None
    created_tree = None
    created_names: list[str] = []
    configured = {}

    try:
        tree = _compositor_tree(scene)
        if state["compositor_tree"] is None and getattr(scene, "compositing_node_group", None) is tree:
            created_tree = tree
        _enable_view_layer_passes(scene, layer, pass_names)

        render_layers = tree.nodes.new("CompositorNodeRLayers")
        render_layers.name = f"{PENDING_NODE_PREFIX}RENDER_LAYERS"
        render_layers.label = "CutBridge Render Source (pending)"
        render_layers.scene = scene
        if hasattr(render_layers, "layer"):
            render_layers.layer = layer.name
        render_layers.location = (-420.0, 0.0)
        created_names.append(render_layers.name)

        for index, pass_name in enumerate(pass_names):
            source_socket = _find_output_socket(render_layers, pass_name)
            if source_socket is None:
                expected = "/".join(PASS_MAPPINGS[pass_name]["socket_names"])
                raise RuntimeError(
                    f"{pass_name} mapping is unavailable for render engine {scene.render.engine}; "
                    f"expected Render Layers output {expected}. Disable the pass or change renderer/View Layer settings."
                )

            output_node = tree.nodes.new("CompositorNodeOutputFile")
            output_node.name = f"{PENDING_NODE_PREFIX}OUTPUT_{pass_name}"
            output_node.label = f"CutBridge {pass_name} (pending)"
            output_node.location = (80.0, -220.0 * index)
            created_names.append(output_node.name)

            directory = package_root / "render" / pass_name.lower()
            filename = f"{safe_token(settings.cut, 'C000')}_{pass_name}_####"

            if hasattr(output_node, "file_output_items") and hasattr(output_node, "directory"):
                # Blender 5.x keeps the node format in multilayer EXR mode by
                # default. Each image item can override that format, which is the
                # supported route for independent PNG/OpenEXR/TIFF sequences.
                output_node.directory = str(directory)
                output_node.file_name = ""
                output_node.file_output_items.clear()
                item = output_node.file_output_items.new(PASS_MAPPINGS[pass_name]["socket_type"], filename)
                item.override_node_format = True
                item.format.file_format = settings.image_format
                target_socket = output_node.inputs.get(item.name) or output_node.inputs[0]
            else:
                # Blender 4.2/4.5 compatibility path.
                output_node.base_path = str(directory)
                if len(output_node.file_slots) == 0:
                    target_socket = output_node.file_slots.new("Image")
                else:
                    target_socket = output_node.inputs[0]
                output_node.file_slots[0].path = filename
                output_node.format.file_format = settings.image_format

            tree.links.new(source_socket, target_socket)
            configured[pass_name] = source_socket.name

        # Commit point: every replacement output is valid. Remove previous managed
        # nodes only now, excluding this attempt's pending nodes.
        pending_names = set(created_names)
        for node in list(tree.nodes):
            if node.name.startswith(MANAGED_NODE_PREFIX) and node.name not in pending_names:
                tree.nodes.remove(node)

        pending_render = tree.nodes.get(created_names[0])
        if pending_render is None:
            raise RuntimeError("CutBridge pending Render Layers node disappeared before commit.")
        pending_render.name = f"{MANAGED_NODE_PREFIX}RENDER_LAYERS"
        pending_render.label = "CutBridge Render Source"
        for pass_name, pending_name in zip(pass_names, created_names[1:]):
            output_node = tree.nodes.get(pending_name)
            if output_node is None:
                raise RuntimeError(f"CutBridge pending {pass_name} output disappeared before commit.")
            output_node.name = f"{MANAGED_NODE_PREFIX}OUTPUT_{pass_name}"
            output_node.label = f"CutBridge {pass_name}"

        return configured
    except Exception:
        if tree is not None:
            _remove_nodes_by_name(tree, created_names)
        _restore_render_mapping_state(scene, layer, state, created_tree=created_tree)
        raise


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

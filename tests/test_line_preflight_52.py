"""LINE/Freestyle preflight regression for the official bpy 5.2.1 runtime."""

from __future__ import annotations

import pathlib
import sys

import bpy
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402
from cutbridge.core import clear_managed_render_outputs, configure_render_outputs  # noqa: E402
from cutbridge.diagnostics import diagnostic_parts  # noqa: E402
from cutbridge.line_preflight import line_pass_preflight_issues  # noqa: E402
from cutbridge.operators import _all_validation_issues  # noqa: E402

CAMERA_NAME = "CutBridgeLinePreflightCamera"


@pytest.fixture(scope="module", autouse=True)
def registered_cutbridge():
    cutbridge.unregister()
    cutbridge.register()
    yield
    cutbridge.unregister()


@pytest.fixture
def line_scene(tmp_path):
    scene = bpy.context.scene
    settings = scene.cutbridge
    view_layer = bpy.context.view_layer

    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)
    original_use_compositing = getattr(scene.render, "use_compositing", None)
    original_scene_freestyle = getattr(scene.render, "use_freestyle", None)
    original_layer_freestyle = getattr(view_layer, "use_freestyle", None)
    freestyle_settings = getattr(view_layer, "freestyle_settings", None)
    original_as_render_pass = (
        getattr(freestyle_settings, "as_render_pass")
        if freestyle_settings is not None and hasattr(freestyle_settings, "as_render_pass")
        else None
    )

    camera_data = bpy.data.cameras.new(CAMERA_NAME)
    camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    scene.render.engine = "BLENDER_EEVEE"
    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_start = 1
    scene.frame_end = 24

    settings.language = "EN"
    settings.project = "LinePreflight"
    settings.episode = "EP01"
    settings.scene_id = "SC010"
    settings.cut = "C001"
    settings.take = "T01"
    settings.version = 1
    settings.output_dir = str(tmp_path)
    settings.studio_preset_mode = "MANUAL"
    settings.image_format = "PNG"
    settings.pass_beauty = False
    settings.pass_line = True
    settings.pass_shadow = False
    settings.pass_depth = False
    settings.last_package_path = ""

    assert hasattr(scene.render, "use_freestyle")
    assert hasattr(view_layer, "use_freestyle")
    assert freestyle_settings is not None
    assert hasattr(freestyle_settings, "as_render_pass")

    scene.render.use_freestyle = True
    view_layer.use_freestyle = True

    yield scene, settings, view_layer, freestyle_settings, tmp_path

    clear_managed_render_outputs(scene)
    current_compositor = getattr(scene, "compositing_node_group", None)
    if hasattr(scene, "compositing_node_group"):
        scene.compositing_node_group = original_compositor
    if original_compositor is None and current_compositor is not None and current_compositor.name in bpy.data.node_groups:
        bpy.data.node_groups.remove(current_compositor)

    scene.render.engine = original_engine
    if original_use_compositing is not None:
        scene.render.use_compositing = original_use_compositing
    if original_scene_freestyle is not None:
        scene.render.use_freestyle = original_scene_freestyle
    if original_layer_freestyle is not None:
        view_layer.use_freestyle = original_layer_freestyle
    if original_as_render_pass is not None:
        freestyle_settings.as_render_pass = original_as_render_pass

    scene.camera = None
    bpy.data.objects.remove(camera, do_unlink=True)
    if camera_data.name in bpy.data.cameras:
        bpy.data.cameras.remove(camera_data)


def test_supported_line_configuration_passes_preflight_and_builds(line_scene):
    scene, settings, _, freestyle_settings, _ = line_scene
    freestyle_settings.as_render_pass = True

    issues = line_pass_preflight_issues(bpy.context)
    assert not [item for item in issues if item["code"] == "LINE_OUTPUT_UNAVAILABLE"]

    result = bpy.ops.cutbridge.build_package()
    assert result == {"FINISHED"}
    package_root = pathlib.Path(settings.last_package_path)
    assert (package_root / "cutbridge.json").is_file()
    tree = scene.compositing_node_group
    assert tree.nodes.get("CUTBRIDGE_OUTPUT_LINE") is not None


def test_validate_catches_line_failure_before_build(line_scene):
    _, settings, _, freestyle_settings, output_dir = line_scene
    freestyle_settings.as_render_pass = False

    issues = _all_validation_issues(bpy.context)
    line_errors = [item for item in issues if item["code"] == "LINE_OUTPUT_UNAVAILABLE"]
    assert len(line_errors) == 1
    assert line_errors[0]["level"] == "ERROR"
    assert "As Render Pass" in line_errors[0]["fix"]

    with pytest.raises(RuntimeError, match="Line Pass Cannot Be Generated"):
        bpy.ops.cutbridge.build_package()
    assert settings.last_package_path == ""
    assert not list(output_dir.iterdir())


def test_preflight_probe_preserves_artist_compositor_and_render_state(line_scene):
    scene, _, view_layer, freestyle_settings, _ = line_scene
    freestyle_settings.as_render_pass = True

    tree = scene.compositing_node_group
    if tree is None:
        tree = bpy.data.node_groups.new("CutBridge_Line_Artist_Compositor", "CompositorNodeTree")
        scene.compositing_node_group = tree
    artist = tree.nodes.new("CompositorNodeOutputFile")
    artist.name = "ARTIST_LINE_PREFLIGHT_KEEP"

    before_tree = scene.compositing_node_group
    before_nodes = sorted(node.name for node in tree.nodes)
    before_scene_freestyle = scene.render.use_freestyle
    before_layer_freestyle = view_layer.use_freestyle
    before_as_render_pass = freestyle_settings.as_render_pass
    before_probe_groups = {group.name for group in bpy.data.node_groups if group.name.startswith("CutBridge_Line_Preflight")}

    line_pass_preflight_issues(bpy.context)

    assert scene.compositing_node_group == before_tree
    assert sorted(node.name for node in tree.nodes) == before_nodes
    assert tree.nodes.get("ARTIST_LINE_PREFLIGHT_KEEP") is not None
    assert scene.render.use_freestyle == before_scene_freestyle
    assert view_layer.use_freestyle == before_layer_freestyle
    assert freestyle_settings.as_render_pass == before_as_render_pass
    after_probe_groups = {group.name for group in bpy.data.node_groups if group.name.startswith("CutBridge_Line_Preflight")}
    assert after_probe_groups == before_probe_groups

    tree.nodes.remove(tree.nodes.get("ARTIST_LINE_PREFLIGHT_KEEP"))


def test_build_still_fails_closed_if_preflight_is_bypassed(line_scene):
    scene, _, view_layer, freestyle_settings, output_dir = line_scene
    freestyle_settings.as_render_pass = False

    before_scene_freestyle = scene.render.use_freestyle
    before_layer_freestyle = view_layer.use_freestyle
    before_as_render_pass = freestyle_settings.as_render_pass
    target = output_dir / "bypassed-preflight"

    with pytest.raises(RuntimeError, match="LINE mapping is unavailable"):
        configure_render_outputs(bpy.context, target)

    assert not target.exists()
    assert scene.render.use_freestyle == before_scene_freestyle
    assert view_layer.use_freestyle == before_layer_freestyle
    assert freestyle_settings.as_render_pass == before_as_render_pass
    tree = getattr(scene, "compositing_node_group", None)
    if tree is not None:
        assert not any(node.name.startswith("CUTBRIDGE_PENDING_") for node in tree.nodes)


def test_line_and_depth_diagnostics_are_actionable_in_en_and_ja(line_scene):
    _, _, _, freestyle_settings, _ = line_scene
    freestyle_settings.as_render_pass = False
    issue = line_pass_preflight_issues(bpy.context)[0]

    en = diagnostic_parts("EN", issue)
    ja = diagnostic_parts("JA", issue)
    assert en["title"] == "Line Pass Cannot Be Generated"
    assert en["continue"].startswith("No")
    assert "As Render Pass" in en["fix"]
    assert ja["title"] == "Lineパスを生成できません"
    assert "Line" in ja["continue"]

    depth_issue = {
        "level": "WARNING",
        "code": "DEPTH_FORMAT_LOSSY",
        "message": "legacy technical wording",
        "fix": "legacy fix",
    }
    depth_en = diagnostic_parts("EN", depth_issue)
    depth_ja = diagnostic_parts("JA", depth_issue)
    assert depth_en["title"] == "Depth Format Warning"
    assert "camera-distance" in depth_en["why"]
    assert depth_en["continue"].startswith("Yes")
    assert depth_ja["title"] == "Depth形式の警告"

"""Beauty/Line/Shadow/Depth workflow matrix for official bpy 5.2.1."""

from __future__ import annotations

import json
import pathlib
import sys

import bpy
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402
from cutbridge.core import clear_managed_render_outputs, validate_scene  # noqa: E402
from cutbridge.operators import _all_validation_issues  # noqa: E402


@pytest.fixture(scope="module", autouse=True)
def registered_cutbridge():
    cutbridge.unregister()
    cutbridge.register()
    yield
    cutbridge.unregister()


@pytest.fixture
def four_pass_scene(tmp_path):
    scene = bpy.context.scene
    settings = scene.cutbridge
    layer = bpy.context.view_layer
    freestyle = getattr(layer, "freestyle_settings", None)

    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)
    original_use_compositing = getattr(scene.render, "use_compositing", None)
    original_scene_freestyle = getattr(scene.render, "use_freestyle", None)
    original_layer_freestyle = getattr(layer, "use_freestyle", None)
    original_as_render_pass = (
        getattr(freestyle, "as_render_pass")
        if freestyle is not None and hasattr(freestyle, "as_render_pass")
        else None
    )
    original_shadow = getattr(layer, "use_pass_shadow", None)
    original_depth = getattr(layer, "use_pass_z", None)

    camera_data = bpy.data.cameras.new("CutBridgeFourPassCamera")
    camera = bpy.data.objects.new("CutBridgeFourPassCamera", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    # Cycles exposes the Shadow data pass and supports Freestyle in the 5.2
    # runtime used by the authoritative automated Blender lane.
    scene.render.engine = "CYCLES"
    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_start = 1
    scene.frame_end = 24

    settings.language = "EN"
    settings.project = "FourPass"
    settings.episode = "EP01"
    settings.scene_id = "SC010"
    settings.cut = "C001"
    settings.take = "T01"
    settings.version = 1
    settings.output_dir = str(tmp_path)
    settings.studio_preset_mode = "MANUAL"
    settings.last_package_path = ""

    assert freestyle is not None
    assert hasattr(freestyle, "as_render_pass")
    assert hasattr(scene.render, "use_freestyle")
    assert hasattr(layer, "use_freestyle")
    assert hasattr(layer, "use_pass_shadow")
    assert hasattr(layer, "use_pass_z")
    scene.render.use_freestyle = True
    layer.use_freestyle = True
    freestyle.as_render_pass = True

    yield scene, settings, layer, freestyle

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
        layer.use_freestyle = original_layer_freestyle
    if original_as_render_pass is not None:
        freestyle.as_render_pass = original_as_render_pass
    if original_shadow is not None:
        layer.use_pass_shadow = original_shadow
    if original_depth is not None:
        layer.use_pass_z = original_depth

    scene.camera = None
    bpy.data.objects.remove(camera, do_unlink=True)
    if camera_data.name in bpy.data.cameras:
        bpy.data.cameras.remove(camera_data)


def _select(settings, names: tuple[str, ...], image_format: str):
    enabled = set(names)
    settings.pass_beauty = "BEAUTY" in enabled
    settings.pass_line = "LINE" in enabled
    settings.pass_shadow = "SHADOW" in enabled
    settings.pass_depth = "DEPTH" in enabled
    settings.image_format = image_format


@pytest.mark.parametrize(
    ("names", "image_format"),
    [
        (("BEAUTY",), "PNG"),
        (("BEAUTY", "LINE"), "PNG"),
        (("BEAUTY", "SHADOW"), "PNG"),
        (("DEPTH",), "PNG"),
        (("DEPTH",), "OPEN_EXR"),
        (("BEAUTY", "LINE", "SHADOW"), "PNG"),
        (("BEAUTY", "LINE", "SHADOW", "DEPTH"), "OPEN_EXR"),
    ],
    ids=[
        "beauty",
        "beauty-line",
        "beauty-shadow",
        "depth-png",
        "depth-openexr",
        "beauty-line-shadow",
        "beauty-line-shadow-depth",
    ],
)
def test_pass_matrix_builds_without_silent_omission_or_collision(four_pass_scene, names, image_format):
    scene, settings, _, _ = four_pass_scene
    _select(settings, names, image_format)

    errors = [item for item in _all_validation_issues(bpy.context) if item["level"] == "ERROR"]
    assert errors == []

    result = bpy.ops.cutbridge.build_package()
    assert result == {"FINISHED"}
    package_root = pathlib.Path(settings.last_package_path)
    manifest = json.loads((package_root / "cutbridge.json").read_text(encoding="utf-8"))

    assert [entry["name"] for entry in manifest["passes"]] == list(names)
    assert len({entry["path"] for entry in manifest["passes"]}) == len(names)
    expected_ext = ".exr" if image_format == "OPEN_EXR" else ".png"
    for entry in manifest["passes"]:
        assert entry["path"] == f"render/{entry['name'].lower()}"
        assert entry["sequence_pattern"].endswith(expected_ext)
        assert (package_root / entry["path"]).is_dir()

    tree = scene.compositing_node_group
    for name in names:
        node = tree.nodes.get(f"CUTBRIDGE_OUTPUT_{name}")
        assert node is not None
        if hasattr(node, "file_output_items"):
            assert len(node.file_output_items) == 1
            assert node.file_output_items[0].format.file_format == image_format


def test_depth_png_is_warning_but_depth_openexr_is_not(four_pass_scene):
    _, settings, _, _ = four_pass_scene
    _select(settings, ("DEPTH",), "PNG")
    png_issues = validate_scene(bpy.context)
    assert any(item["code"] == "DEPTH_FORMAT_LOSSY" and item["level"] == "WARNING" for item in png_issues)

    settings.image_format = "OPEN_EXR"
    exr_issues = validate_scene(bpy.context)
    assert not any(item["code"] == "DEPTH_FORMAT_LOSSY" for item in exr_issues)

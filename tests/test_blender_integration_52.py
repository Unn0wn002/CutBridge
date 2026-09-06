"""CutBridge package integration tests for the official bpy 5.2.1 runtime."""

from __future__ import annotations

import json
import pathlib
import sys
from types import SimpleNamespace

import bpy
import pytest
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402
from cutbridge.core import PASS_MAPPINGS, clear_managed_render_outputs, validate_scene  # noqa: E402
from cutbridge.version import __version__  # noqa: E402

MANIFEST_SCHEMA_PATH = ROOT / "packages" / "shared" / "cutbridge-manifest.schema.json"
CAMERA_NAME = "CutBridgeTestCamera"


@pytest.fixture(scope="module", autouse=True)
def registered_cutbridge():
    cutbridge.unregister()
    cutbridge.register()
    yield
    cutbridge.unregister()


@pytest.fixture(autouse=True)
def configured_scene(tmp_path):
    scene = bpy.context.scene
    settings = scene.cutbridge
    view_layer = bpy.context.view_layer
    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)
    original_freestyle = getattr(scene.render, "use_freestyle", None)
    original_pass_state = {
        attr: getattr(view_layer, attr)
        for attr in ("use_freestyle", "use_pass_shadow", "use_pass_z")
        if hasattr(view_layer, attr)
    }

    camera_data = bpy.data.cameras.new(CAMERA_NAME)
    camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_start = 1
    scene.frame_end = 120

    settings.project = "SakuraTest"
    settings.episode = "EP01"
    settings.scene_id = "SC010"
    settings.cut = "C001"
    settings.take = "T01"
    settings.version = 1
    settings.output_dir = str(tmp_path)
    settings.image_format = "PNG"
    settings.pass_beauty = True
    settings.pass_line = False
    settings.pass_shadow = False
    settings.pass_depth = False
    settings.last_package_path = ""

    yield scene, settings, tmp_path

    clear_managed_render_outputs(scene)
    current_compositor = getattr(scene, "compositing_node_group", None)
    if original_compositor is None and current_compositor is not None and current_compositor.name.startswith("CutBridge_"):
        scene.compositing_node_group = None
        bpy.data.node_groups.remove(current_compositor)
    elif hasattr(scene, "compositing_node_group"):
        scene.compositing_node_group = original_compositor

    scene.render.engine = original_engine
    if original_freestyle is not None:
        scene.render.use_freestyle = original_freestyle
    for attr, value in original_pass_state.items():
        setattr(view_layer, attr, value)

    scene.camera = None
    bpy.data.objects.remove(camera, do_unlink=True)
    if camera_data.name in bpy.data.cameras:
        bpy.data.cameras.remove(camera_data)


def _build_and_read_manifest(settings):
    assert bpy.ops.cutbridge.build_package() == {"FINISHED"}
    package_root = pathlib.Path(settings.last_package_path)
    manifest_path = package_root / "cutbridge.json"
    return package_root, manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))


def _assert_validation_failure(expected_code: str, expected_message: str, context=bpy.context):
    issues = validate_scene(context)
    errors = [issue for issue in issues if issue["level"] == "ERROR"]

    assert any(
        issue["code"] == expected_code and expected_message in issue["message"]
        for issue in errors
    )


def _assert_build_operator_rejects(expected_message: str, output_dir: pathlib.Path):
    with pytest.raises(RuntimeError, match=expected_message):
        bpy.ops.cutbridge.build_package()
    assert not any(output_dir.iterdir())


def test_logical_pass_mapping_contract_is_explicit():
    assert set(PASS_MAPPINGS) == {"BEAUTY", "LINE", "SHADOW", "DEPTH"}
    assert PASS_MAPPINGS["BEAUTY"]["socket_names"] == ("Image",)
    assert PASS_MAPPINGS["LINE"]["enable_attr"] == "use_freestyle"
    assert PASS_MAPPINGS["SHADOW"]["enable_attr"] == "use_pass_shadow"
    assert PASS_MAPPINGS["DEPTH"]["enable_attr"] == "use_pass_z"


def test_generated_manifest_uses_canonical_cutbridge_version(configured_scene):
    _, settings, _ = configured_scene

    _, _, manifest = _build_and_read_manifest(settings)

    assert manifest["cutbridge_version"] == __version__
    assert cutbridge.bl_info["version"] == tuple(int(x) for x in __version__.split("."))


def test_generated_manifest_matches_scene_and_json_schema(configured_scene):
    _, settings, _ = configured_scene

    package_root, manifest_path, manifest = _build_and_read_manifest(settings)
    schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(manifest)

    assert manifest_path.is_file()
    assert package_root.name == "SakuraTest_EP01_SC010_C001_T01_V001"
    assert manifest["project"] == "SakuraTest"
    assert manifest["episode"] == "EP01"
    assert manifest["scene"] == "SC010"
    assert manifest["cut"] == "C001"
    assert manifest["take"] == "T01"
    assert manifest["version"] == 1
    assert manifest["version_label"] == "V001"
    assert manifest["fps"] == 24.0
    assert manifest["resolution"] == {
        "width": 1920,
        "height": 1080,
        "pixel_aspect": 1.0,
    }
    assert manifest["frames"] == {"start": 1, "end": 120, "count": 120}
    assert manifest["camera"] == CAMERA_NAME


def test_build_maps_beauty_to_cutbridge_file_output_and_preserves_artist_nodes(configured_scene):
    scene, settings, _ = configured_scene
    package_root, _, _ = _build_and_read_manifest(settings)
    tree = scene.compositing_node_group
    assert tree is not None

    artist_node = tree.nodes.new("CompositorNodeRLayers")
    artist_node.name = "ARTIST_RENDER_LAYERS_KEEP"

    # bpy can return distinct Python proxy objects for the same RNA node, so
    # persistence is checked by its stable Blender name rather than `is`.
    package_root, _, _ = _build_and_read_manifest(settings)
    assert tree.nodes.get("ARTIST_RENDER_LAYERS_KEEP") is not None

    render_layers = tree.nodes.get("CUTBRIDGE_RENDER_LAYERS")
    output = tree.nodes.get("CUTBRIDGE_OUTPUT_BEAUTY")
    assert render_layers is not None
    assert output is not None
    assert output.directory == str(package_root / "render" / "beauty")
    assert output.file_name == ""
    assert len(output.file_output_items) == 1
    item = output.file_output_items[0]
    assert item.name == "C001_BEAUTY_####"
    assert item.override_node_format is True
    assert item.format.file_format == "PNG"
    assert any(
        link.from_node.name == render_layers.name and link.to_node.name == output.name
        for link in tree.links
    )

    tree.nodes.remove(tree.nodes.get("ARTIST_RENDER_LAYERS_KEEP"))


def test_depth_mapping_enables_z_pass_and_uses_exr_output(configured_scene):
    scene, settings, _ = configured_scene
    settings.pass_depth = True
    settings.image_format = "OPEN_EXR"

    package_root, _, _ = _build_and_read_manifest(settings)
    tree = scene.compositing_node_group
    output = tree.nodes.get("CUTBRIDGE_OUTPUT_DEPTH")
    render_layers = tree.nodes.get("CUTBRIDGE_RENDER_LAYERS")

    assert bpy.context.view_layer.use_pass_z is True
    assert output is not None
    assert output.directory == str(package_root / "render" / "depth")
    item = output.file_output_items[0]
    assert item.name == "C001_DEPTH_####"
    assert item.override_node_format is True
    assert item.format.file_format == "OPEN_EXR"
    depth_links = [link for link in tree.links if link.to_node.name == output.name]
    assert len(depth_links) == 1
    assert depth_links[0].from_node.name == render_layers.name
    assert depth_links[0].from_socket.name in {"Depth", "Z"}


@pytest.mark.parametrize(
    ("enabled_passes", "expected_names"),
    [
        ({"beauty"}, ["BEAUTY"]),
        ({"beauty", "depth"}, ["BEAUTY", "DEPTH"]),
    ],
    ids=["beauty", "beauty-depth"],
)
def test_supported_pass_combinations_create_matching_folders_and_manifest_entries(
    configured_scene, enabled_passes, expected_names
):
    _, settings, _ = configured_scene
    settings.pass_beauty = "beauty" in enabled_passes
    settings.pass_line = False
    settings.pass_shadow = False
    settings.pass_depth = "depth" in enabled_passes
    if settings.pass_depth:
        settings.image_format = "OPEN_EXR"

    package_root, _, manifest = _build_and_read_manifest(settings)
    pass_entries = manifest["passes"]

    assert [entry["name"] for entry in pass_entries] == expected_names
    assert [entry["path"] for entry in pass_entries] == [
        f"render/{name.lower()}" for name in expected_names
    ]
    extension = ".exr" if settings.image_format == "OPEN_EXR" else ".png"
    assert [entry["sequence_pattern"] for entry in pass_entries] == [
        f"C001_{name}_####{extension}" for name in expected_names
    ]
    assert all(entry["required"] is True for entry in pass_entries)

    actual_directories = {
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*")
        if path.is_dir()
    }
    expected_directories = {"camera", "preview", "render"} | {
        f"render/{name.lower()}" for name in expected_names
    }
    assert actual_directories == expected_directories


def test_eevee_rejects_line_when_no_freestyle_render_layers_socket_is_exposed(configured_scene):
    scene, settings, output_dir = configured_scene
    scene.render.engine = "BLENDER_EEVEE"
    settings.pass_beauty = False
    settings.pass_line = True

    _assert_build_operator_rejects("LINE mapping is unavailable", output_dir)
    assert scene.render.use_freestyle is True
    assert bpy.context.view_layer.use_freestyle is True


def test_v001_and_v002_coexist_without_overwriting_v001(configured_scene):
    _, settings, _ = configured_scene

    v001_root, v001_manifest_path, _ = _build_and_read_manifest(settings)
    v001_bytes = v001_manifest_path.read_bytes()
    preservation_marker = v001_root / "preserve.txt"
    preservation_marker.write_text("V001 must remain intact", encoding="utf-8")

    settings.version = 2
    v002_root, _, v002_manifest = _build_and_read_manifest(settings)

    assert v001_root.is_dir()
    assert v002_root.is_dir()
    assert v001_root != v002_root
    assert v001_manifest_path.read_bytes() == v001_bytes
    assert preservation_marker.read_text(encoding="utf-8") == "V001 must remain intact"
    assert v002_manifest["version"] == 2
    assert v002_manifest["version_label"] == "V002"


def test_japanese_project_metadata_is_preserved_as_utf8(configured_scene):
    _, settings, _ = configured_scene
    settings.project = "桜プロジェクト"

    _, manifest_path, manifest = _build_and_read_manifest(settings)
    manifest_text = manifest_path.read_text(encoding="utf-8")

    assert manifest["project"] == "桜プロジェクト"
    assert "桜プロジェクト" in manifest_text
    assert "\\u685c" not in manifest_text


def test_depth_mapping_warns_when_not_using_openexr(configured_scene):
    _, settings, _ = configured_scene
    settings.pass_depth = True
    settings.image_format = "PNG"

    issues = validate_scene(bpy.context)
    assert any(
        issue["level"] == "WARNING" and issue["code"] == "DEPTH_FORMAT_LOSSY"
        for issue in issues
    )


def test_validation_rejects_missing_camera(configured_scene):
    scene, _, output_dir = configured_scene
    scene.camera = None

    _assert_validation_failure("CAMERA_MISSING", "No active scene camera")
    _assert_build_operator_rejects("No active scene camera", output_dir)


def test_validation_rejects_empty_cut_id(configured_scene):
    _, settings, output_dir = configured_scene
    settings.cut = "   "

    _assert_validation_failure("ID_MISSING", "Cut is empty")
    _assert_build_operator_rejects("Cut is empty", output_dir)


def test_validation_rejects_invalid_frame_range(configured_scene):
    scene, settings, _ = configured_scene
    invalid_scene = SimpleNamespace(
        cutbridge=settings,
        camera=scene.camera,
        frame_start=120,
        frame_end=1,
        render=scene.render,
        view_layers=scene.view_layers,
    )
    invalid_context = SimpleNamespace(scene=invalid_scene, view_layer=bpy.context.view_layer)

    _assert_validation_failure(
        "FRAME_RANGE_INVALID",
        "Frame end is before frame start",
        context=invalid_context,
    )


def test_validation_rejects_no_selected_passes(configured_scene):
    _, settings, output_dir = configured_scene
    settings.pass_beauty = False
    settings.pass_line = False
    settings.pass_shadow = False
    settings.pass_depth = False

    _assert_validation_failure("PASS_MISSING", "No render pass is selected")
    _assert_build_operator_rejects("No render pass is selected", output_dir)


def test_validation_rejects_missing_output_directory(configured_scene):
    _, settings, output_dir = configured_scene
    settings.output_dir = ""

    _assert_validation_failure("OUTPUT_MISSING", "Package output directory is empty")
    _assert_build_operator_rejects("Package output directory is empty", output_dir)

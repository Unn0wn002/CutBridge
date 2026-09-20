"""S10B producer tests against the official bpy 5.2.1 runtime."""

from __future__ import annotations

import json
import pathlib
import sys

import bpy
import pytest
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402
from cutbridge.camera_handoff import HandoffContractError  # noqa: E402
from cutbridge.core import clear_managed_render_outputs  # noqa: E402
from cutbridge.handoff_3d import (  # noqa: E402
    MARKER_PROPERTY,
    build_handoff_3d,
    handoff_3d_issues,
)

MANIFEST_SCHEMA_PATH = ROOT / "packages" / "shared" / "cutbridge-manifest.schema.json"


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
    original_camera = scene.camera
    original_frame_start = scene.frame_start
    original_frame_end = scene.frame_end
    original_frame = scene.frame_current
    original_fps = scene.render.fps
    original_fps_base = scene.render.fps_base
    original_res_x = scene.render.resolution_x
    original_res_y = scene.render.resolution_y
    original_pa_x = scene.render.pixel_aspect_x
    original_pa_y = scene.render.pixel_aspect_y
    original_compositor = getattr(scene, "compositing_node_group", None)

    camera_data = bpy.data.cameras.new("S10B_Camera")
    camera = bpy.data.objects.new("S10B_Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.frame_start = 1
    scene.frame_end = 3
    scene.frame_set(1)

    settings.project = "S10B"
    settings.episode = "EP01"
    settings.scene_id = "SC010"
    settings.cut = "C001"
    settings.take = "T01"
    settings.version = 1
    settings.output_dir = str(tmp_path)
    settings.studio_preset_mode = "MANUAL"
    settings.image_format = "PNG"
    settings.pass_beauty = True
    settings.pass_line = False
    settings.pass_shadow = False
    settings.pass_depth = False
    settings.last_package_path = ""
    settings.handoff_3d_enabled = True
    settings.handoff_3d_pixels_per_blender_unit = 100.0

    created = []

    def make_empty(name):
        obj = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(obj)
        created.append(obj)
        return obj

    yield scene, settings, camera, make_empty, created, tmp_path

    settings.handoff_3d_enabled = False
    clear_managed_render_outputs(scene)
    current_compositor = getattr(scene, "compositing_node_group", None)
    if original_compositor is None and current_compositor is not None and current_compositor.name.startswith("CutBridge_"):
        scene.compositing_node_group = None
        bpy.data.node_groups.remove(current_compositor)
    elif hasattr(scene, "compositing_node_group"):
        scene.compositing_node_group = original_compositor

    for obj in reversed(created):
        if obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    scene.camera = original_camera
    if camera.name in bpy.data.objects:
        bpy.data.objects.remove(camera, do_unlink=True)
    if camera_data.name in bpy.data.cameras:
        bpy.data.cameras.remove(camera_data)

    scene.frame_start = original_frame_start
    scene.frame_end = original_frame_end
    scene.render.fps = original_fps
    scene.render.fps_base = original_fps_base
    scene.render.resolution_x = original_res_x
    scene.render.resolution_y = original_res_y
    scene.render.pixel_aspect_x = original_pa_x
    scene.render.pixel_aspect_y = original_pa_y
    scene.frame_set(original_frame)


def test_disabled_mode_produces_no_payload(configured_scene):
    _, settings, _, _, _, _ = configured_scene
    settings.handoff_3d_enabled = False
    assert build_handoff_3d(bpy.context) is None


def test_camera_world_sample_uses_s10a_axis_map_and_restores_frame(configured_scene):
    scene, _, camera, _, _, _ = configured_scene
    camera.location = (1.0, 2.0, 3.0)
    scene.frame_set(2)

    payload = build_handoff_3d(bpy.context)

    assert scene.frame_current == 2
    assert payload["schema"] == "cutbridge-handoff-3d"
    assert payload["schema_version"] == 1
    assert payload["space"]["axis_map"] == "blender_xyz_to_ae_x_negz_y"
    samples = payload["camera"]["samples"]
    assert [sample["frame"] for sample in samples] == [1, 2, 3]
    assert [sample["time"] for sample in samples] == pytest.approx([0.0, 1 / 24, 2 / 24], abs=1e-8)
    assert samples[0]["position"] == pytest.approx([1060.0, 240.0, 200.0])
    assert samples[0]["forward"] == pytest.approx([0.0, 1.0, 0.0])
    assert samples[0]["up"] == pytest.approx([0.0, 0.0, 1.0])
    assert samples[0]["horizontal_fov_radians"] > 0
    assert samples[0]["ae_zoom"] > 0


def test_only_marked_empties_are_serialized_and_animation_is_evaluated(configured_scene):
    _, _, _, make_empty, _, _ = configured_scene
    marked = make_empty("S10B_Marked")
    unmarked = make_empty("S10B_Unmarked")
    marked[MARKER_PROPERTY] = True
    unmarked.location.x = 99.0

    marked.location.x = 0.0
    marked.keyframe_insert(data_path="location", frame=1)
    marked.location.x = 2.0
    marked.keyframe_insert(data_path="location", frame=3)

    payload = build_handoff_3d(bpy.context)

    assert [item["name"] for item in payload["nulls"]] == ["S10B_Marked"]
    samples = payload["nulls"][0]["samples"]
    assert samples[0]["position"][0] == pytest.approx(960.0)
    assert samples[-1]["position"][0] == pytest.approx(1160.0)
    assert samples[0]["time"] == pytest.approx(0.0)
    assert samples[-1]["time"] == pytest.approx(2 / 24)


def test_parented_empty_is_baked_in_evaluated_world_space(configured_scene):
    _, _, _, make_empty, _, _ = configured_scene
    parent = make_empty("S10B_Parent")
    child = make_empty("S10B_Child")
    child[MARKER_PROPERTY] = True
    parent.location = (5.0, 0.0, 0.0)
    child.parent = parent
    child.location = (1.0, 0.0, 0.0)

    payload = build_handoff_3d(bpy.context)

    sample = payload["nulls"][0]["samples"][0]
    assert sample["position"][0] == pytest.approx(1560.0)


def test_unsupported_camera_shift_fails_closed(configured_scene):
    _, _, camera, _, _, _ = configured_scene
    camera.data.shift_x = 0.1

    issues = handoff_3d_issues(bpy.context)
    assert any(item["code"] == "HANDOFF_CAMERA_SHIFT_UNSUPPORTED" for item in issues)
    with pytest.raises(HandoffContractError) as excinfo:
        build_handoff_3d(bpy.context)
    assert excinfo.value.code == "HANDOFF_CAMERA_SHIFT_UNSUPPORTED"


def test_marking_non_empty_object_fails_closed(configured_scene):
    _, _, _, _, created, _ = configured_scene
    mesh = bpy.data.meshes.new("S10B_MeshData")
    obj = bpy.data.objects.new("S10B_Mesh", mesh)
    bpy.context.collection.objects.link(obj)
    created.append(obj)
    obj[MARKER_PROPERTY] = True

    issues = handoff_3d_issues(bpy.context)
    assert any(item["code"] == "HANDOFF_MARKER_TYPE_UNSUPPORTED" for item in issues)

    bpy.data.objects.remove(obj, do_unlink=True)
    created.remove(obj)
    bpy.data.meshes.remove(mesh)


def test_reflected_marked_empty_fails_during_baked_sampling(configured_scene):
    _, _, _, make_empty, _, _ = configured_scene
    obj = make_empty("S10B_Reflected")
    obj[MARKER_PROPERTY] = True
    obj.scale = (-1.0, 1.0, 1.0)

    with pytest.raises(HandoffContractError) as excinfo:
        build_handoff_3d(bpy.context)
    assert excinfo.value.code == "HANDOFF_REFLECTION_UNSUPPORTED"


def test_build_package_writes_schema_valid_optional_handoff_block(configured_scene):
    _, settings, _, make_empty, _, _ = configured_scene
    guide = make_empty("S10B_Guide")
    guide[MARKER_PROPERTY] = True
    guide.location = (1.0, 0.0, 0.0)

    assert bpy.ops.cutbridge.build_package() == {"FINISHED"}
    manifest_path = pathlib.Path(settings.last_package_path) / "cutbridge.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(manifest)

    assert manifest["handoff_3d"]["schema"] == "cutbridge-handoff-3d"
    assert manifest["handoff_3d"]["camera"]["name"] == "S10B_Camera"
    assert [item["name"] for item in manifest["handoff_3d"]["nulls"]] == ["S10B_Guide"]

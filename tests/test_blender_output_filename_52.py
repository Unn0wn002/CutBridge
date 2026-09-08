"""Native Blender 5.2 regression for CutBridge File Output sequence naming."""

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
from cutbridge.core import clear_managed_render_outputs  # noqa: E402

CAMERA_NAME = "CutBridgeFilenameCamera"


@pytest.fixture(scope="module", autouse=True)
def registered_cutbridge():
    cutbridge.unregister()
    cutbridge.register()
    yield
    cutbridge.unregister()


def test_openexr_render_filename_matches_manifest_sequence_pattern(tmp_path):
    """A real compositor render must not collapse C001_BEAUTY_####.exr to 0000.exr."""
    scene = bpy.context.scene
    settings = scene.cutbridge

    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)
    original_use_compositing = getattr(scene.render, "use_compositing", None)
    original_camera = scene.camera
    original_frame_start = scene.frame_start
    original_frame_end = scene.frame_end
    original_resolution = (
        scene.render.resolution_x,
        scene.render.resolution_y,
        scene.render.resolution_percentage,
    )

    camera_data = bpy.data.cameras.new(CAMERA_NAME)
    camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
    bpy.context.collection.objects.link(camera)

    try:
        scene.camera = camera
        scene.render.engine = "BLENDER_EEVEE"
        scene.render.resolution_x = 16
        scene.render.resolution_y = 16
        scene.render.resolution_percentage = 100
        scene.frame_start = 0
        scene.frame_end = 0
        scene.frame_set(0)

        settings.project = "FilenameTest"
        settings.episode = "EP01"
        settings.scene_id = "SC001"
        settings.cut = "C001"
        settings.take = "T01"
        settings.version = 1
        settings.output_dir = str(tmp_path)
        settings.image_format = "OPEN_EXR"
        settings.pass_beauty = True
        settings.pass_line = False
        settings.pass_shadow = False
        settings.pass_depth = False
        settings.last_package_path = ""

        assert bpy.ops.cutbridge.build_package() == {"FINISHED"}
        package_root = pathlib.Path(settings.last_package_path)
        manifest = json.loads((package_root / "cutbridge.json").read_text(encoding="utf-8"))
        beauty = manifest["passes"][0]
        assert beauty["sequence_pattern"] == "C001_BEAUTY_####.exr"

        tree = scene.compositing_node_group
        output = tree.nodes.get("CUTBRIDGE_OUTPUT_BEAUTY")
        assert output is not None
        assert output.format.media_type == "IMAGE"
        assert output.file_name == ""
        assert len(output.file_output_items) == 1
        item = output.file_output_items[0]
        assert item.name == "C001_BEAUTY_####"
        assert item.override_node_format is True
        assert item.format.media_type == "IMAGE"
        assert item.format.file_format == "OPEN_EXR"

        assert bpy.ops.render.render() == {"FINISHED"}

        beauty_dir = package_root / beauty["path"]
        expected = beauty_dir / "C001_BEAUTY_0000.exr"
        bare = beauty_dir / "0000.exr"
        assert expected.is_file(), f"expected CutBridge sequence frame was not written: {expected}"
        assert not bare.exists(), "Blender 5.x regressed to a bare frame-number filename"
    finally:
        clear_managed_render_outputs(scene)
        current_compositor = getattr(scene, "compositing_node_group", None)
        if hasattr(scene, "compositing_node_group"):
            scene.compositing_node_group = original_compositor
        if (
            original_compositor is None
            and current_compositor is not None
            and current_compositor.name in bpy.data.node_groups
        ):
            bpy.data.node_groups.remove(current_compositor)

        scene.render.engine = original_engine
        if original_use_compositing is not None:
            scene.render.use_compositing = original_use_compositing
        scene.camera = original_camera
        scene.frame_start = original_frame_start
        scene.frame_end = original_frame_end
        (
            scene.render.resolution_x,
            scene.render.resolution_y,
            scene.render.resolution_percentage,
        ) = original_resolution

        bpy.data.objects.remove(camera, do_unlink=True)
        if camera_data.name in bpy.data.cameras:
            bpy.data.cameras.remove(camera_data)

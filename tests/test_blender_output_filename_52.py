"""Blender 5.2 RNA regression for CutBridge File Output sequence naming."""

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


def test_openexr_file_output_uses_image_media_filename_contract(tmp_path):
    """Blender 5.x must use IMAGE mode so the socket/item name becomes the disk filename prefix.

    The pip-distributed bpy runtime aborts on an actual EEVEE render in GitHub's
    headless runner, so native written-file verification remains a desktop gate.
    This regression guards the exact RNA misconfiguration that produced bare
    0000.exr files in the native test: Multi-Layer EXR media mode.
    """
    scene = bpy.context.scene
    settings = scene.cutbridge

    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)
    original_use_compositing = getattr(scene.render, "use_compositing", None)
    original_camera = scene.camera
    original_frame_start = scene.frame_start
    original_frame_end = scene.frame_end

    camera_data = bpy.data.cameras.new(CAMERA_NAME)
    camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
    bpy.context.collection.objects.link(camera)

    try:
        scene.camera = camera
        scene.render.engine = "BLENDER_EEVEE"
        scene.frame_start = 0
        scene.frame_end = 23

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
        assert pathlib.Path(output.directory) == package_root / "render" / "beauty"
        assert output.format.media_type == "IMAGE"
        assert output.file_name == ""
        assert len(output.file_output_items) == 1

        item = output.file_output_items[0]
        assert item.name == "C001_BEAUTY_####"
        assert item.override_node_format is True
        assert item.format.media_type == "IMAGE"
        assert item.format.file_format == "OPEN_EXR"

        # The node must no longer be configured as MULTILAYER, where Blender
        # interprets the item name as an EXR layer and writes only 0000.exr.
        assert output.format.media_type != "MULTILAYER"
        assert item.name + ".exr" == beauty["sequence_pattern"]
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

        bpy.data.objects.remove(camera, do_unlink=True)
        if camera_data.name in bpy.data.cameras:
            bpy.data.cameras.remove(camera_data)

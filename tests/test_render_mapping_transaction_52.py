"""Transactional render-mapping regression for the official bpy 5.2.1 runtime."""

from __future__ import annotations

import pathlib
import sys

import bpy
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER_APP = ROOT / "apps" / "blender"
sys.path.insert(0, str(BLENDER_APP))

import cutbridge  # noqa: E402
from cutbridge.core import (  # noqa: E402
    clear_managed_render_outputs,
    configure_render_outputs,
)

CAMERA_NAME = "CutBridgeTransactionCamera"


@pytest.fixture(scope="module", autouse=True)
def registered_cutbridge():
    cutbridge.unregister()
    cutbridge.register()
    yield
    cutbridge.unregister()


@pytest.fixture
def configured_scene(tmp_path):
    scene = bpy.context.scene
    settings = scene.cutbridge
    view_layer = bpy.context.view_layer
    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)
    original_use_compositing = getattr(scene.render, "use_compositing", None)
    original_freestyle = getattr(scene.render, "use_freestyle", None)
    original_layer_flags = {
        attr: getattr(view_layer, attr)
        for attr in ("use_freestyle", "use_pass_shadow", "use_pass_z")
        if hasattr(view_layer, attr)
    }

    camera_data = bpy.data.cameras.new(CAMERA_NAME)
    camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    settings.project = "TransactionTest"
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

    yield scene, settings, view_layer, tmp_path

    clear_managed_render_outputs(scene)
    current_compositor = getattr(scene, "compositing_node_group", None)
    if hasattr(scene, "compositing_node_group"):
        scene.compositing_node_group = original_compositor
    if original_compositor is None and current_compositor is not None and current_compositor.name in bpy.data.node_groups:
        bpy.data.node_groups.remove(current_compositor)

    scene.render.engine = original_engine
    if original_use_compositing is not None:
        scene.render.use_compositing = original_use_compositing
    if original_freestyle is not None:
        scene.render.use_freestyle = original_freestyle
    for attr, value in original_layer_flags.items():
        setattr(view_layer, attr, value)

    scene.camera = None
    bpy.data.objects.remove(camera, do_unlink=True)
    if camera_data.name in bpy.data.cameras:
        bpy.data.cameras.remove(camera_data)


def test_failed_later_pass_preserves_previous_mapping_and_render_flags(configured_scene):
    scene, settings, view_layer, tmp_path = configured_scene

    configure_render_outputs(bpy.context, tmp_path / "valid")
    tree = scene.compositing_node_group
    previous_render = tree.nodes.get("CUTBRIDGE_RENDER_LAYERS")
    previous_output = tree.nodes.get("CUTBRIDGE_OUTPUT_BEAUTY")
    assert previous_render is not None
    assert previous_output is not None

    previous_node_names = sorted(
        node.name for node in tree.nodes if node.name.startswith("CUTBRIDGE_")
    )
    previous_directory = previous_output.directory
    previous_item_name = previous_output.file_output_items[0].name
    previous_item_format = previous_output.file_output_items[0].format.file_format

    # EEVEE in the official bpy 5.2.1 test runtime exposes the View Layer
    # Freestyle flag but no Render Layers Freestyle socket. BEAUTY succeeds first,
    # then LINE is the later unsupported pass that used to destroy the old mapping.
    scene.render.engine = "BLENDER_EEVEE"
    settings.pass_line = True
    before_scene_freestyle = scene.render.use_freestyle
    before_layer_freestyle = view_layer.use_freestyle
    before_use_compositing = scene.render.use_compositing

    with pytest.raises(RuntimeError, match="LINE mapping is unavailable"):
        configure_render_outputs(bpy.context, tmp_path / "failed")

    assert scene.compositing_node_group is tree
    assert sorted(node.name for node in tree.nodes if node.name.startswith("CUTBRIDGE_")) == previous_node_names
    assert not any(node.name.startswith("CUTBRIDGE_PENDING_") for node in tree.nodes)

    restored_render = tree.nodes.get("CUTBRIDGE_RENDER_LAYERS")
    restored_output = tree.nodes.get("CUTBRIDGE_OUTPUT_BEAUTY")
    assert restored_render is not None
    assert restored_output is not None
    assert restored_output.directory == previous_directory
    assert restored_output.file_output_items[0].name == previous_item_name
    assert restored_output.file_output_items[0].format.file_format == previous_item_format

    assert scene.render.use_freestyle == before_scene_freestyle
    assert view_layer.use_freestyle == before_layer_freestyle
    assert scene.render.use_compositing == before_use_compositing

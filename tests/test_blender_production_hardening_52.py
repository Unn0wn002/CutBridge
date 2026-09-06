"""Session 3 production-hardening regressions under the official bpy 5.2.1 runtime."""

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
from cutbridge.package_safety import (  # noqa: E402
    assert_package_integrity,
    format_issue,
    package_target_issues,
)

CAMERA_NAME = "CutBridgeProductionHardeningCamera"


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
    original_engine = scene.render.engine
    original_compositor = getattr(scene, "compositing_node_group", None)

    camera_data = bpy.data.cameras.new(CAMERA_NAME)
    camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_start = 1001
    scene.frame_end = 1012

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
    scene.camera = None
    bpy.data.objects.remove(camera, do_unlink=True)
    if camera_data.name in bpy.data.cameras:
        bpy.data.cameras.remove(camera_data)


def _build(settings):
    assert bpy.ops.cutbridge.build_package() == {"FINISHED"}
    root = pathlib.Path(settings.last_package_path)
    manifest = json.loads((root / "cutbridge.json").read_text(encoding="utf-8"))
    return root, manifest


def test_unrendered_scaffold_can_be_refreshed_but_is_explicitly_warned(configured_scene):
    _, settings, _ = configured_scene
    first_root, _ = _build(settings)

    issues = package_target_issues(settings)
    assert [item["code"] for item in issues] == ["PACKAGE_SCAFFOLD_REFRESH"]
    assert issues[0]["level"] == "WARNING"

    second_root, _ = _build(settings)
    assert second_root == first_root


def test_existing_render_payload_blocks_same_version_overwrite(configured_scene):
    _, settings, _ = configured_scene
    root, _ = _build(settings)
    frame = root / "render" / "beauty" / "C001_BEAUTY_1001.png"
    frame.write_bytes(b"rendered-frame-placeholder")

    issues = package_target_issues(settings)
    assert len(issues) == 1
    assert issues[0]["level"] == "ERROR"
    assert issues[0]["code"] == "PACKAGE_EXISTS"
    assert "Increment Version" in issues[0]["fix"]
    assert "Fix:" in format_issue(issues[0])

    with pytest.raises(RuntimeError, match="will not be overwritten"):
        bpy.ops.cutbridge.build_package()
    assert frame.read_bytes() == b"rendered-frame-placeholder"


def test_v001_v002_v003_coexist_with_preserved_prior_payload(configured_scene):
    _, settings, _ = configured_scene
    roots = []

    for version in (1, 2, 3):
        settings.version = version
        root, manifest = _build(settings)
        marker = root / "render" / "beauty" / f"marker-v{version}.txt"
        marker.write_text(f"preserve V{version:03d}", encoding="utf-8")
        roots.append((root, marker, manifest))

    assert len({root for root, _, _ in roots}) == 3
    for version, (root, marker, manifest) in enumerate(roots, start=1):
        assert root.name.endswith(f"V{version:03d}")
        assert marker.read_text(encoding="utf-8") == f"preserve V{version:03d}"
        assert manifest["version"] == version
        assert manifest["version_label"] == f"V{version:03d}"


def test_japanese_metadata_and_windows_invalid_filename_characters_are_safe(configured_scene):
    _, settings, _ = configured_scene
    settings.project = "作品:テスト"
    settings.cut = "C001?JP"

    root, manifest = _build(settings)

    assert "作品_テスト" in root.name
    assert "C001_JP" in root.name
    assert ":" not in root.name
    assert "?" not in root.name
    assert manifest["project"] == "作品:テスト"
    assert manifest["cut"] == "C001?JP"
    assert "作品:テスト" in (root / "cutbridge.json").read_text(encoding="utf-8")


def test_package_integrity_detects_missing_required_folder(configured_scene):
    _, settings, _ = configured_scene
    root, manifest = _build(settings)
    (root / "camera").rmdir()

    with pytest.raises(RuntimeError, match="missing folder.*camera"):
        assert_package_integrity(root, manifest, ["BEAUTY"])

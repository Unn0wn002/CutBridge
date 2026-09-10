from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

bpy = pytest.importorskip("bpy")

from tools.research import s10_blender_probe as probe

# Blender 5.2's camera projection path retains finite-precision camera/RNA math.
# The observed exact-axis fixture error is ~0.0000319 px. Keep this source-side
# allowance independently bounded at 0.00005 px — 1000x tighter than the
# separate 0.05 px native After Effects acceptance gate.
SOURCE_PROJECTION_TOLERANCE_PX = 0.00005


def test_blender_probe_uses_isolated_perspective_camera_and_cleans_up():
    assert probe.PROBE_SCENE_NAME not in bpy.data.scenes
    assert probe.PROBE_CAMERA_NAME not in bpy.data.objects
    report = probe.build_probe_report()
    assert report["schema"] == "cutbridge-s10-spatial-probe"
    assert report["schema_version"] == 1
    assert report["host"] == "blender"
    assert report["camera"]["type"] == "PERSP"
    assert report["camera"]["sensor_fit"] == "HORIZONTAL"
    assert report["camera"]["position_world"] == pytest.approx([0.0, -10.0, 0.0], abs=1e-10)
    assert report["camera"]["right_world"] == pytest.approx([1.0, 0.0, 0.0], abs=1e-10)
    assert report["camera"]["up_world"] == pytest.approx([0.0, 0.0, 1.0], abs=1e-10)
    assert report["camera"]["forward_world"] == pytest.approx([0.0, 1.0, 0.0], abs=1e-10)
    assert probe.PROBE_SCENE_NAME not in bpy.data.scenes
    assert probe.PROBE_CAMERA_NAME not in bpy.data.objects
    assert probe.PROBE_CAMERA_NAME not in bpy.data.cameras


def test_candidate_ae_projection_matches_blender_projection_for_fixture():
    report = probe.build_probe_report()
    for point in report["points"].values():
        assert point["projection_delta_px"] == pytest.approx(
            [0.0, 0.0], abs=SOURCE_PROJECTION_TOLERANCE_PX
        )


def test_blender_angle_x_drives_probe_zoom_and_quantization_is_recorded():
    report = probe.build_probe_report()
    width = report["comp"]["width"]
    angle_x = report["camera"]["angle_x_radians"]
    zoom_from_angle = width / (2.0 * math.tan(angle_x / 2.0))
    assert zoom_from_angle == pytest.approx(report["camera"]["blender_derived_ae_zoom"], abs=1e-9)
    # Blender stores camera RNA values at finite precision. Keep this quantified
    # separately from the native AE projection acceptance test.
    assert abs(report["camera"]["zoom_quantization_delta"]) < 0.001


def test_fixture_preserves_expected_screen_axis_semantics():
    points = probe.build_probe_report()["points"]
    assert points["ORIGIN"]["blender_comp_px"] == pytest.approx(
        [960.0, 540.0], abs=SOURCE_PROJECTION_TOLERANCE_PX
    )
    assert points["X_PLUS"]["blender_comp_px"][0] > points["ORIGIN"]["blender_comp_px"][0]
    assert points["Z_PLUS"]["blender_comp_px"][1] < points["ORIGIN"]["blender_comp_px"][1]
    assert points["Y_PLUS"]["blender_comp_px"] == pytest.approx(
        [960.0, 540.0], abs=SOURCE_PROJECTION_TOLERANCE_PX
    )

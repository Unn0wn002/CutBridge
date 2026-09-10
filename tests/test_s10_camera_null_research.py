from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.research import s10_spatial_math as spatial


def test_candidate_basis_is_right_handed_orthonormal_axis_remap():
    basis = spatial.BLENDER_TO_AE_BASIS
    assert spatial.determinant_3x3(basis) == pytest.approx(1.0)
    assert spatial.blender_to_ae_vector((1, 0, 0)) == pytest.approx((1, 0, 0))
    assert spatial.blender_to_ae_vector((0, 1, 0)) == pytest.approx((0, 0, 1))
    assert spatial.blender_to_ae_vector((0, 0, 1)) == pytest.approx((0, -1, 0))


def test_candidate_point_mapping_uses_comp_center_and_uniform_scale():
    assert spatial.blender_to_ae_point((0, 0, 0), comp_width=1920, comp_height=1080, scale=100) == pytest.approx(
        (960, 540, 0)
    )
    assert spatial.blender_to_ae_point((1, 2, 3), comp_width=1920, comp_height=1080, scale=100) == pytest.approx(
        (1060, 240, 200)
    )


def test_horizontal_fov_and_ae_zoom_are_dimensionally_consistent():
    fov = spatial.horizontal_fov_from_lens(lens_mm=50, sensor_width_mm=36)
    zoom = spatial.ae_zoom_from_horizontal_fov(comp_width=1920, fov_radians=fov)
    assert math.degrees(fov) == pytest.approx(39.597752709, abs=1e-9)
    assert zoom == pytest.approx(1920 * 50 / 36, abs=1e-9)


def test_fixture_default_camera_projection_has_expected_axis_behavior():
    report = spatial.fixture_expected_report()
    points = report["points"]
    assert report["camera"]["ae_position_candidate"] == pytest.approx([960, 540, -1000])
    assert report["camera"]["ae_point_of_interest_candidate"] == pytest.approx([960, 540, 0])
    assert points["ORIGIN"]["expected_comp_px"] == pytest.approx([960, 540])
    assert points["X_PLUS"]["expected_comp_px"][0] > 960
    assert points["X_PLUS"]["expected_comp_px"][1] == pytest.approx(540)
    assert points["Z_PLUS"]["expected_comp_px"][0] == pytest.approx(960)
    assert points["Z_PLUS"]["expected_comp_px"][1] < 540
    assert points["Y_PLUS"]["expected_comp_px"] == pytest.approx([960, 540])


def test_mixed_axis_projection_is_stable_and_depth_aware():
    point = spatial.fixture_expected_report()["points"]["XYZ_PLUS"]
    assert point["ae_world_candidate"] == pytest.approx([1060, 440, 100])
    assert point["expected_comp_px"] == pytest.approx([1202.4242424242, 297.5757575758], abs=1e-9)


def test_frame_to_seconds_preserves_manifest_frame_zero_and_fractional_fps():
    assert spatial.frame_to_seconds(frame=0, frame_start=0, fps=24) == pytest.approx(0)
    assert spatial.frame_to_seconds(frame=24, frame_start=0, fps=24) == pytest.approx(1)
    assert spatial.frame_to_seconds(frame=1001, frame_start=1000, fps=24000 / 1001) == pytest.approx(1001 / 24000)


@pytest.mark.parametrize(
    "call",
    [
        lambda: spatial.blender_to_ae_vector((1, 2), scale=1),
        lambda: spatial.blender_to_ae_vector((1, 2, 3), scale=0),
        lambda: spatial.blender_to_ae_point((1, 2, 3), comp_width=0, comp_height=1080, scale=1),
        lambda: spatial.horizontal_fov_from_lens(lens_mm=0, sensor_width_mm=36),
        lambda: spatial.ae_zoom_from_horizontal_fov(comp_width=1920, fov_radians=0),
        lambda: spatial.frame_to_seconds(frame=1, frame_start=0, fps=0),
        lambda: spatial.project_default_ae_camera((960, 540, -1000), camera_z=-1000, zoom=1000, comp_width=1920, comp_height=1080),
    ],
)
def test_invalid_research_math_fails_closed(call):
    with pytest.raises(ValueError):
        call()

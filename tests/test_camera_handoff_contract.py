import importlib.util
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "apps" / "blender" / "cutbridge" / "camera_handoff.py"

spec = importlib.util.spec_from_file_location("cutbridge_camera_handoff_s10", MODULE_PATH)
handoff = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(handoff)


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def test_axis_mapping_is_explicit_and_right_handed():
    x = handoff.blender_to_ae_direction((1, 0, 0))
    y = handoff.blender_to_ae_direction((0, 1, 0))
    z = handoff.blender_to_ae_direction((0, 0, 1))

    assert x == (1.0, 0.0, 0.0)
    assert y == (0.0, 0.0, 1.0)
    assert z == (0.0, -1.0, 0.0)
    assert _cross(x, y) == z


def test_world_origin_maps_to_composition_center():
    assert handoff.blender_to_ae_position((0, 0, 0), width=1920, height=1080) == (960.0, 540.0, 0.0)


def test_world_axes_map_to_ae_screen_and_depth_directions():
    scale = 100.0
    origin = handoff.blender_to_ae_position((0, 0, 0), width=1920, height=1080, pixels_per_blender_unit=scale)
    plus_x = handoff.blender_to_ae_position((1, 0, 0), width=1920, height=1080, pixels_per_blender_unit=scale)
    plus_y = handoff.blender_to_ae_position((0, 1, 0), width=1920, height=1080, pixels_per_blender_unit=scale)
    plus_z = handoff.blender_to_ae_position((0, 0, 1), width=1920, height=1080, pixels_per_blender_unit=scale)

    assert plus_x[0] - origin[0] == 100.0
    assert plus_y[2] - origin[2] == 100.0
    assert plus_z[1] - origin[1] == -100.0


def test_direction_mapping_does_not_apply_composition_center_or_spatial_scale():
    assert handoff.blender_to_ae_direction((2, 3, 4)) == (2.0, -4.0, 3.0)


def test_normalize_and_point_along_direction_are_euler_free_primitives():
    direction = handoff.normalize_direction((0, 0, 5))
    assert direction == (0.0, 0.0, 1.0)
    assert handoff.point_along_direction((10, 20, 30), direction, 50) == (10.0, 20.0, 80.0)


def test_zero_direction_fails_closed():
    with pytest.raises(handoff.HandoffContractError) as exc:
        handoff.normalize_direction((0, 0, 0))
    assert exc.value.code == "HANDOFF_VECTOR_ZERO"


def test_first_export_frame_maps_to_ae_zero_time():
    assert handoff.frame_to_ae_time(1001, frame_start=1001, fps=24) == 0.0
    assert handoff.frame_to_ae_time(1002, frame_start=1001, fps=24) == pytest.approx(1.0 / 24.0)
    assert handoff.frame_to_ae_time(1024, frame_start=1001, fps=24) == pytest.approx(23.0 / 24.0)


def test_frame_mapping_matches_existing_cutbridge_duration_contract():
    start = 1001
    end = 1024
    fps = 24.0
    count = end - start + 1
    final_key_time = handoff.frame_to_ae_time(end, frame_start=start, fps=fps)
    comp_duration = count / fps

    assert final_key_time == pytest.approx((count - 1) / fps)
    assert comp_duration - final_key_time == pytest.approx(1.0 / fps)


def test_frame_before_export_range_fails_closed():
    with pytest.raises(handoff.HandoffContractError) as exc:
        handoff.frame_to_ae_time(999, frame_start=1001, fps=24)
    assert exc.value.code == "HANDOFF_FRAME_INVALID"


def test_horizontal_fov_to_ae_zoom_math():
    assert handoff.ae_zoom_from_horizontal_fov(width=1920, horizontal_fov_radians=math.pi / 2) == pytest.approx(960.0)
    expected = 1920 / (2 * math.tan(math.radians(50) / 2))
    assert handoff.ae_zoom_from_horizontal_fov(width=1920, horizontal_fov_radians=math.radians(50)) == pytest.approx(expected)


def test_invalid_fov_fails_closed():
    for fov in (0, -1, math.pi, math.inf):
        with pytest.raises(handoff.HandoffContractError) as exc:
            handoff.ae_zoom_from_horizontal_fov(width=1920, horizontal_fov_radians=fov)
        assert exc.value.code in {"HANDOFF_FOV_INVALID", "HANDOFF_VALUE_INVALID"}


def test_mvp_accepts_centered_square_pixel_perspective_camera():
    handoff.validate_mvp_camera_constraints(camera_type="PERSP", pixel_aspect=1.0, shift_x=0.0, shift_y=0.0)


@pytest.mark.parametrize("camera_type", ["ORTHO", "PANO", "CUSTOM"])
def test_mvp_rejects_unproven_camera_types(camera_type):
    with pytest.raises(handoff.HandoffContractError) as exc:
        handoff.validate_mvp_camera_constraints(camera_type=camera_type, pixel_aspect=1.0)
    assert exc.value.code == "HANDOFF_CAMERA_TYPE_UNSUPPORTED"


def test_mvp_rejects_non_square_pixels_until_native_projection_parity_is_proven():
    with pytest.raises(handoff.HandoffContractError) as exc:
        handoff.validate_mvp_camera_constraints(camera_type="PERSP", pixel_aspect=1.2)
    assert exc.value.code == "HANDOFF_PIXEL_ASPECT_UNSUPPORTED"


@pytest.mark.parametrize("shift_x,shift_y", [(0.1, 0), (0, -0.1), (0.01, 0.02)])
def test_mvp_rejects_shifted_camera_sensor(shift_x, shift_y):
    with pytest.raises(handoff.HandoffContractError) as exc:
        handoff.validate_mvp_camera_constraints(
            camera_type="PERSP", pixel_aspect=1.0, shift_x=shift_x, shift_y=shift_y
        )
    assert exc.value.code == "HANDOFF_CAMERA_SHIFT_UNSUPPORTED"


def test_invalid_spatial_scale_fails_closed():
    with pytest.raises(handoff.HandoffContractError) as exc:
        handoff.blender_to_ae_position((0, 0, 0), width=1920, height=1080, pixels_per_blender_unit=0)
    assert exc.value.code == "HANDOFF_SCALE_INVALID"

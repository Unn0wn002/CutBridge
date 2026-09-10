from __future__ import annotations

import math
from typing import Iterable

S10_SCHEMA = "cutbridge-s10-spatial-probe"
S10_SCHEMA_VERSION = 1

# Investigation candidate only. This is NOT a production CutBridge runtime contract.
# Blender world X/Y/Z -> AE composition/world X/Y/Z.
# X remains screen-right, Blender Z-up becomes AE negative-Y (screen up),
# and Blender Y front/back becomes AE Z depth.
BLENDER_TO_AE_BASIS = (
    (1.0, 0.0, 0.0),
    (0.0, 0.0, -1.0),
    (0.0, 1.0, 0.0),
)

FIXTURE = {
    "comp_width": 1920,
    "comp_height": 1080,
    "pixel_aspect": 1.0,
    "fps": 24.0,
    "frame_start": 0,
    "frame_end": 24,
    "spatial_scale": 100.0,
    "camera": {
        "location": (0.0, -10.0, 0.0),
        "rotation_euler_xyz_degrees": (90.0, 0.0, 0.0),
        "lens_mm": 50.0,
        "sensor_width_mm": 36.0,
    },
    "points": {
        "ORIGIN": (0.0, 0.0, 0.0),
        "X_PLUS": (1.0, 0.0, 0.0),
        "Y_PLUS": (0.0, 1.0, 0.0),
        "Z_PLUS": (0.0, 0.0, 1.0),
        "XYZ_PLUS": (1.0, 1.0, 1.0),
    },
}


def _vec3(value: Iterable[float]) -> tuple[float, float, float]:
    items = tuple(float(part) for part in value)
    if len(items) != 3 or not all(math.isfinite(part) for part in items):
        raise ValueError("Expected three finite spatial values.")
    return items


def determinant_3x3(matrix=BLENDER_TO_AE_BASIS) -> float:
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def blender_to_ae_vector(value: Iterable[float], *, scale: float = 1.0) -> tuple[float, float, float]:
    x, y, z = _vec3(value)
    scale = float(scale)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("Spatial scale must be a finite number greater than zero.")
    return (scale * x, -scale * z, scale * y)


def blender_to_ae_point(
    value: Iterable[float],
    *,
    comp_width: float,
    comp_height: float,
    scale: float,
) -> tuple[float, float, float]:
    width = float(comp_width)
    height = float(comp_height)
    if not math.isfinite(width) or not math.isfinite(height) or width <= 0.0 or height <= 0.0:
        raise ValueError("Composition dimensions must be finite numbers greater than zero.")
    x, y, z = blender_to_ae_vector(value, scale=scale)
    return (width / 2.0 + x, height / 2.0 + y, z)


def horizontal_fov_from_lens(*, lens_mm: float, sensor_width_mm: float) -> float:
    lens = float(lens_mm)
    sensor = float(sensor_width_mm)
    if not math.isfinite(lens) or not math.isfinite(sensor) or lens <= 0.0 or sensor <= 0.0:
        raise ValueError("Lens and sensor width must be finite numbers greater than zero.")
    return 2.0 * math.atan(sensor / (2.0 * lens))


def ae_zoom_from_horizontal_fov(*, comp_width: float, fov_radians: float) -> float:
    width = float(comp_width)
    fov = float(fov_radians)
    if not math.isfinite(width) or width <= 0.0:
        raise ValueError("Composition width must be a finite number greater than zero.")
    if not math.isfinite(fov) or fov <= 0.0 or fov >= math.pi:
        raise ValueError("Horizontal FOV must be between 0 and pi radians.")
    return width / (2.0 * math.tan(fov / 2.0))


def ae_zoom_from_blender_lens(*, comp_width: float, lens_mm: float, sensor_width_mm: float) -> float:
    return ae_zoom_from_horizontal_fov(
        comp_width=comp_width,
        fov_radians=horizontal_fov_from_lens(lens_mm=lens_mm, sensor_width_mm=sensor_width_mm),
    )


def frame_to_seconds(*, frame: float, frame_start: float, fps: float) -> float:
    frame_value = float(frame)
    start = float(frame_start)
    rate = float(fps)
    if not all(math.isfinite(value) for value in (frame_value, start, rate)) or rate <= 0.0:
        raise ValueError("Frame, frame_start and fps must be finite; fps must be greater than zero.")
    return (frame_value - start) / rate


def project_default_ae_camera(
    point: Iterable[float],
    *,
    camera_z: float,
    zoom: float,
    comp_width: float,
    comp_height: float,
) -> tuple[float, float]:
    """Project an AE-space point for the S10 fixture camera.

    The research fixture uses a camera centered in the comp, looking along +Z,
    with zero orientation/rotations. This intentionally avoids claiming a
    general AE rotation decomposition before the native gate is complete.
    """
    x, y, z = _vec3(point)
    width = float(comp_width)
    height = float(comp_height)
    camera_z = float(camera_z)
    zoom = float(zoom)
    depth = z - camera_z
    if not all(math.isfinite(value) for value in (width, height, camera_z, zoom, depth)):
        raise ValueError("Projection inputs must be finite.")
    if width <= 0.0 or height <= 0.0 or zoom <= 0.0 or depth <= 0.0:
        raise ValueError("Point must be in front of the S10 fixture camera with positive dimensions/zoom.")
    cx = width / 2.0
    cy = height / 2.0
    return (
        cx + zoom * (x - cx) / depth,
        cy + zoom * (y - cy) / depth,
    )


def fixture_expected_report() -> dict:
    width = FIXTURE["comp_width"]
    height = FIXTURE["comp_height"]
    scale = FIXTURE["spatial_scale"]
    camera = FIXTURE["camera"]
    camera_ae = blender_to_ae_point(camera["location"], comp_width=width, comp_height=height, scale=scale)
    zoom = ae_zoom_from_blender_lens(
        comp_width=width,
        lens_mm=camera["lens_mm"],
        sensor_width_mm=camera["sensor_width_mm"],
    )
    points = {}
    for name, point in FIXTURE["points"].items():
        ae_point = blender_to_ae_point(point, comp_width=width, comp_height=height, scale=scale)
        points[name] = {
            "blender_world": list(point),
            "ae_world_candidate": list(ae_point),
            "expected_comp_px": list(
                project_default_ae_camera(
                    ae_point,
                    camera_z=camera_ae[2],
                    zoom=zoom,
                    comp_width=width,
                    comp_height=height,
                )
            ),
        }
    return {
        "schema": S10_SCHEMA,
        "schema_version": S10_SCHEMA_VERSION,
        "basis": [list(row) for row in BLENDER_TO_AE_BASIS],
        "comp": {"width": width, "height": height, "pixel_aspect": FIXTURE["pixel_aspect"]},
        "fps": FIXTURE["fps"],
        "frame_start": FIXTURE["frame_start"],
        "frame_end": FIXTURE["frame_end"],
        "spatial_scale": scale,
        "camera": {
            "blender_location": list(camera["location"]),
            "blender_rotation_euler_xyz_degrees": list(camera["rotation_euler_xyz_degrees"]),
            "ae_position_candidate": list(camera_ae),
            "ae_point_of_interest_candidate": [width / 2.0, height / 2.0, 0.0],
            "lens_mm": camera["lens_mm"],
            "sensor_width_mm": camera["sensor_width_mm"],
            "horizontal_fov_radians": horizontal_fov_from_lens(
                lens_mm=camera["lens_mm"], sensor_width_mm=camera["sensor_width_mm"]
            ),
            "ae_zoom_candidate": zoom,
        },
        "points": points,
    }

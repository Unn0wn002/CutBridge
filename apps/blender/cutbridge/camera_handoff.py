from __future__ import annotations

from math import isfinite, tan
from typing import Iterable


CONTRACT_VERSION = 1
DEFAULT_PIXELS_PER_BLENDER_UNIT = 100.0
SUPPORTED_CAMERA_TYPE = "PERSP"
SQUARE_PIXEL_TOLERANCE = 1e-6
SHIFT_TOLERANCE = 1e-9


class HandoffContractError(ValueError):
    """Stable failure for S10 camera/null contract primitives."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _finite_number(value, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise HandoffContractError("HANDOFF_VALUE_INVALID", f"{label} must be numeric.") from exc
    if not isfinite(result):
        raise HandoffContractError("HANDOFF_VALUE_INVALID", f"{label} must be finite.")
    return result


def _vector3(value: Iterable[float], label: str) -> tuple[float, float, float]:
    try:
        items = tuple(value)
    except TypeError as exc:
        raise HandoffContractError("HANDOFF_VECTOR_INVALID", f"{label} must contain three numbers.") from exc
    if len(items) != 3:
        raise HandoffContractError("HANDOFF_VECTOR_INVALID", f"{label} must contain exactly three numbers.")
    return tuple(_finite_number(item, label) for item in items)  # type: ignore[return-value]


def blender_to_ae_direction(value: Iterable[float]) -> tuple[float, float, float]:
    """Map a Blender world-space direction into CutBridge AE composition axes.

    Contract basis:
      Blender +X -> AE +X (right)
      Blender +Y -> AE +Z (farther from viewer)
      Blender +Z -> AE -Y (up on screen)

    This is the proper rotation (x, y, z) -> (x, -z, y); it does not add the
    composition-center translation used for positions.
    """
    x, y, z = _vector3(value, "direction")
    return (x, -z, y)


def blender_to_ae_position(
    value: Iterable[float],
    *,
    width: float,
    height: float,
    pixels_per_blender_unit: float = DEFAULT_PIXELS_PER_BLENDER_UNIT,
) -> tuple[float, float, float]:
    """Map Blender world position to AE composition space.

    CutBridge deliberately maps Blender world origin to the composition center.
    Spatial scale is product-defined and explicit; it must never be inferred
    from scene names, camera distance, or other hidden heuristics.
    """
    x, y, z = _vector3(value, "position")
    width = _finite_number(width, "width")
    height = _finite_number(height, "height")
    scale = _finite_number(pixels_per_blender_unit, "pixels_per_blender_unit")
    if width <= 0 or height <= 0:
        raise HandoffContractError("HANDOFF_COMP_INVALID", "Composition width/height must be positive.")
    if scale <= 0:
        raise HandoffContractError("HANDOFF_SCALE_INVALID", "pixels_per_blender_unit must be positive.")
    return (width * 0.5 + x * scale, height * 0.5 - z * scale, y * scale)


def normalize_direction(value: Iterable[float]) -> tuple[float, float, float]:
    x, y, z = _vector3(value, "direction")
    length_sq = x * x + y * y + z * z
    if length_sq <= 0:
        raise HandoffContractError("HANDOFF_VECTOR_ZERO", "Direction vector must be non-zero.")
    length = length_sq ** 0.5
    return (x / length, y / length, z / length)


def point_along_direction(
    position: Iterable[float], direction: Iterable[float], distance: float
) -> tuple[float, float, float]:
    px, py, pz = _vector3(position, "position")
    dx, dy, dz = normalize_direction(direction)
    distance = _finite_number(distance, "distance")
    if distance <= 0:
        raise HandoffContractError("HANDOFF_DISTANCE_INVALID", "Direction distance must be positive.")
    return (px + dx * distance, py + dy * distance, pz + dz * distance)


def frame_to_ae_time(frame: int, *, frame_start: int, fps: float) -> float:
    """Map an exported Blender frame to AE composition time in seconds.

    The first exported Blender frame is AE time 0. This matches CutBridge's
    current composition duration contract: frame_count / fps.
    """
    if isinstance(frame, bool) or not isinstance(frame, int):
        raise HandoffContractError("HANDOFF_FRAME_INVALID", "frame must be an integer.")
    if isinstance(frame_start, bool) or not isinstance(frame_start, int):
        raise HandoffContractError("HANDOFF_FRAME_INVALID", "frame_start must be an integer.")
    fps = _finite_number(fps, "fps")
    if fps <= 0:
        raise HandoffContractError("HANDOFF_FPS_INVALID", "fps must be greater than zero.")
    if frame < frame_start:
        raise HandoffContractError("HANDOFF_FRAME_INVALID", "frame must not precede frame_start.")
    return (frame - frame_start) / fps


def ae_zoom_from_horizontal_fov(*, width: float, horizontal_fov_radians: float) -> float:
    """Return AE camera Zoom in pixels for a centered perspective camera.

    This formula is intentionally gated to the MVP constraints below. Native AE
    validation must confirm the final importer reconstruction before S10 ships.
    """
    width = _finite_number(width, "width")
    fov = _finite_number(horizontal_fov_radians, "horizontal_fov_radians")
    if width <= 0:
        raise HandoffContractError("HANDOFF_COMP_INVALID", "Composition width must be positive.")
    if not 0.0 < fov < 3.141592653589793:
        raise HandoffContractError("HANDOFF_FOV_INVALID", "Horizontal FOV must be between 0 and pi radians.")
    return width / (2.0 * tan(fov * 0.5))


def validate_mvp_camera_constraints(
    *,
    camera_type: str,
    pixel_aspect: float,
    shift_x: float = 0.0,
    shift_y: float = 0.0,
) -> None:
    """Fail closed on camera cases not yet proven safe for the S10 MVP."""
    if str(camera_type).upper() != SUPPORTED_CAMERA_TYPE:
        raise HandoffContractError(
            "HANDOFF_CAMERA_TYPE_UNSUPPORTED",
            "S10 MVP supports Blender perspective cameras only.",
        )
    pixel_aspect = _finite_number(pixel_aspect, "pixel_aspect")
    if abs(pixel_aspect - 1.0) > SQUARE_PIXEL_TOLERANCE:
        raise HandoffContractError(
            "HANDOFF_PIXEL_ASPECT_UNSUPPORTED",
            "S10 MVP camera handoff requires square pixels until native projection parity is proven.",
        )
    shift_x = _finite_number(shift_x, "shift_x")
    shift_y = _finite_number(shift_y, "shift_y")
    if abs(shift_x) > SHIFT_TOLERANCE or abs(shift_y) > SHIFT_TOLERANCE:
        raise HandoffContractError(
            "HANDOFF_CAMERA_SHIFT_UNSUPPORTED",
            "S10 MVP does not support shifted Blender camera sensors.",
        )

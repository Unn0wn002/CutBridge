from __future__ import annotations

from math import isfinite

import bpy
from mathutils import Vector

from .camera_handoff import (
    DEFAULT_PIXELS_PER_BLENDER_UNIT,
    HandoffContractError,
    ae_zoom_from_horizontal_fov,
    blender_to_ae_direction,
    blender_to_ae_position,
    frame_to_ae_time,
    validate_mvp_camera_constraints,
)

HANDOFF_SCHEMA = "cutbridge-handoff-3d"
HANDOFF_SCHEMA_VERSION = 1
MARKER_PROPERTY = "cutbridge_handoff_3d"
MAX_HANDOFF_FRAMES = 10_000
MAX_HANDOFF_NULLS = 64
MAX_HANDOFF_SAMPLES = 100_000
ORTHOGONAL_TOLERANCE = 1e-5
AXIS_LENGTH_EPSILON = 1e-9


def handoff_3d_enabled(settings) -> bool:
    return bool(getattr(settings, "handoff_3d_enabled", False))


def _clean_number(value: float) -> float:
    result = round(float(value), 9)
    return 0.0 if result == -0.0 else result


def _vec(value) -> list[float]:
    return [_clean_number(component) for component in value]


def _pixels_per_blender_unit(settings) -> float:
    raw = getattr(
        settings,
        "handoff_3d_pixels_per_blender_unit",
        DEFAULT_PIXELS_PER_BLENDER_UNIT,
    )
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise HandoffContractError(
            "HANDOFF_SCALE_INVALID",
            "3D handoff pixels-per-Blender-unit must be numeric.",
        ) from exc
    if not isfinite(value) or value <= 0:
        raise HandoffContractError(
            "HANDOFF_SCALE_INVALID",
            "3D handoff pixels-per-Blender-unit must be finite and greater than zero.",
        )
    return value


def _pixel_aspect(scene) -> float:
    x = float(getattr(scene.render, "pixel_aspect_x", 1.0) or 1.0)
    y = float(getattr(scene.render, "pixel_aspect_y", 1.0) or 1.0)
    if not isfinite(x) or not isfinite(y) or x <= 0 or y <= 0:
        raise HandoffContractError(
            "HANDOFF_PIXEL_ASPECT_UNSUPPORTED",
            "3D handoff requires a finite positive pixel aspect ratio.",
        )
    return x / y


def _marked_empties(scene) -> list:
    marked = [obj for obj in scene.objects if bool(obj.get(MARKER_PROPERTY, False))]
    unsupported = [obj.name for obj in marked if obj.type != "EMPTY"]
    if unsupported:
        raise HandoffContractError(
            "HANDOFF_MARKER_TYPE_UNSUPPORTED",
            "Only Blender Empty objects may use the CutBridge 3D handoff marker: "
            + ", ".join(sorted(unsupported)),
        )
    empties = sorted(marked, key=lambda obj: obj.name)
    if len(empties) > MAX_HANDOFF_NULLS:
        raise HandoffContractError(
            "HANDOFF_NULL_LIMIT",
            f"3D handoff supports at most {MAX_HANDOFF_NULLS} marked Empties per cut.",
        )
    return empties


def _validate_frame_budget(scene, null_count: int) -> int:
    frame_start = int(scene.frame_start)
    frame_end = int(scene.frame_end)
    frame_count = frame_end - frame_start + 1
    if frame_start < 0 or frame_end < frame_start:
        raise HandoffContractError(
            "HANDOFF_FRAME_RANGE_INVALID",
            "3D handoff requires the same non-negative, increasing export frame range as CutBridge packages.",
        )
    if frame_count > MAX_HANDOFF_FRAMES:
        raise HandoffContractError(
            "HANDOFF_FRAME_LIMIT",
            f"3D handoff supports at most {MAX_HANDOFF_FRAMES} baked frames per cut.",
        )
    total_samples = frame_count * (1 + null_count)
    if total_samples > MAX_HANDOFF_SAMPLES:
        raise HandoffContractError(
            "HANDOFF_SAMPLE_LIMIT",
            f"3D handoff would create {total_samples} samples; the safety limit is {MAX_HANDOFF_SAMPLES}.",
        )
    return frame_count


def _validate_setup(context):
    scene = context.scene
    settings = scene.cutbridge
    if not handoff_3d_enabled(settings):
        return None
    if scene.camera is None:
        raise HandoffContractError(
            "HANDOFF_CAMERA_MISSING",
            "3D handoff requires an active scene camera.",
        )

    camera_data = scene.camera.data
    validate_mvp_camera_constraints(
        camera_type=getattr(camera_data, "type", ""),
        pixel_aspect=_pixel_aspect(scene),
        shift_x=float(getattr(camera_data, "shift_x", 0.0)),
        shift_y=float(getattr(camera_data, "shift_y", 0.0)),
    )
    scale = _pixels_per_blender_unit(settings)
    empties = _marked_empties(scene)
    frame_count = _validate_frame_budget(scene, len(empties))
    fps = float(scene.render.fps) / float(scene.render.fps_base or 1.0)
    if not isfinite(fps) or fps <= 0:
        raise HandoffContractError(
            "HANDOFF_FPS_INVALID",
            "3D handoff requires a finite FPS greater than zero.",
        )
    return {
        "camera": scene.camera,
        "empties": empties,
        "frame_count": frame_count,
        "fps": fps,
        "scale": scale,
        "pixel_aspect": _pixel_aspect(scene),
        "width": int(scene.render.resolution_x),
        "height": int(scene.render.resolution_y),
    }


def handoff_3d_issues(context) -> list[dict]:
    settings = context.scene.cutbridge
    if not handoff_3d_enabled(settings):
        return []
    try:
        _validate_setup(context)
    except HandoffContractError as exc:
        return [
            {
                "level": "ERROR",
                "code": exc.code,
                "message": exc.message,
                "fix": "Disable 3D handoff or correct the unsupported camera/marker/export setting.",
            }
        ]
    return [
        {
            "level": "WARNING",
            "code": "HANDOFF_PRODUCER_ONLY",
            "message": "3D handoff producer data is enabled; the current After Effects importer does not create camera/null layers yet.",
            "fix": "Use this data for S10 validation only until native AE reconstruction is approved.",
        }
    ]


def _mapped_transform(matrix_world, *, width: int, height: int, scale: float) -> dict:
    basis_matrix = matrix_world.to_3x3()
    raw_axes = [
        basis_matrix @ Vector((1.0, 0.0, 0.0)),
        basis_matrix @ Vector((0.0, 1.0, 0.0)),
        basis_matrix @ Vector((0.0, 0.0, 1.0)),
    ]
    lengths = [axis.length for axis in raw_axes]
    if any(length <= AXIS_LENGTH_EPSILON for length in lengths):
        raise HandoffContractError(
            "HANDOFF_DEGENERATE_TRANSFORM",
            "3D handoff does not support zero-scale object transforms.",
        )

    axes = [axis / length for axis, length in zip(raw_axes, lengths)]
    if max(
        abs(axes[0].dot(axes[1])),
        abs(axes[0].dot(axes[2])),
        abs(axes[1].dot(axes[2])),
    ) > ORTHOGONAL_TOLERANCE:
        raise HandoffContractError(
            "HANDOFF_SHEAR_UNSUPPORTED",
            "3D handoff does not support evaluated world transforms containing shear.",
        )

    handedness = axes[0].cross(axes[1]).dot(axes[2])
    if handedness <= 0:
        raise HandoffContractError(
            "HANDOFF_REFLECTION_UNSUPPORTED",
            "3D handoff does not support reflected world transforms with negative handedness.",
        )

    origin = matrix_world.translation
    mapped_position = blender_to_ae_position(
        origin,
        width=width,
        height=height,
        pixels_per_blender_unit=scale,
    )
    mapped_axes = [blender_to_ae_direction(axis) for axis in axes]
    return {
        "position": _vec(mapped_position),
        "basis": {
            "x": _vec(mapped_axes[0]),
            "y": _vec(mapped_axes[1]),
            "z": _vec(mapped_axes[2]),
        },
        "scale": [_clean_number(length) for length in lengths],
    }


def _base_sample(obj_eval, *, frame: int, frame_start: int, fps: float, width: int, height: int, scale: float) -> dict:
    sample = {
        "frame": int(frame),
        "time": _clean_number(frame_to_ae_time(frame, frame_start=frame_start, fps=fps)),
    }
    sample.update(
        _mapped_transform(
            obj_eval.matrix_world,
            width=width,
            height=height,
            scale=scale,
        )
    )
    return sample


def _camera_sample(camera, depsgraph, *, frame: int, frame_start: int, fps: float, width: int, height: int, scale: float, pixel_aspect: float) -> dict:
    camera_eval = camera.evaluated_get(depsgraph)
    data = camera_eval.data
    validate_mvp_camera_constraints(
        camera_type=getattr(data, "type", ""),
        pixel_aspect=pixel_aspect,
        shift_x=float(getattr(data, "shift_x", 0.0)),
        shift_y=float(getattr(data, "shift_y", 0.0)),
    )
    sample = _base_sample(
        camera_eval,
        frame=frame,
        frame_start=frame_start,
        fps=fps,
        width=width,
        height=height,
        scale=scale,
    )
    fov = float(getattr(data, "angle_x"))
    zoom = ae_zoom_from_horizontal_fov(width=width, horizontal_fov_radians=fov)
    sample["forward"] = _vec([-value for value in sample["basis"]["z"]])
    sample["up"] = list(sample["basis"]["y"])
    sample["horizontal_fov_radians"] = _clean_number(fov)
    sample["ae_zoom"] = _clean_number(zoom)
    # Camera object scale is not an AE camera property. It is retained in the
    # generic transform sample for auditability, but the future importer must
    # reconstruct projection only from position/orientation/FOV/Zoom.
    return sample


def _null_sample(obj, depsgraph, *, frame: int, frame_start: int, fps: float, width: int, height: int, scale: float) -> dict:
    obj_eval = obj.evaluated_get(depsgraph)
    return _base_sample(
        obj_eval,
        frame=frame,
        frame_start=frame_start,
        fps=fps,
        width=width,
        height=height,
        scale=scale,
    )


def build_handoff_3d(context) -> dict | None:
    """Bake the opt-in S10B producer payload from evaluated Blender world state.

    This function only serializes data. It never creates After Effects layers,
    recreates Blender hierarchy, executes external code, or performs I/O.
    """
    setup = _validate_setup(context)
    if setup is None:
        return None

    scene = context.scene
    frame_start = int(scene.frame_start)
    frame_end = int(scene.frame_end)
    original_frame = int(scene.frame_current)
    original_subframe = float(getattr(scene, "frame_subframe", 0.0))
    camera_samples = []
    null_samples = {obj.name: [] for obj in setup["empties"]}

    try:
        for frame in range(frame_start, frame_end + 1):
            scene.frame_set(frame, subframe=0.0)
            depsgraph = context.evaluated_depsgraph_get()
            camera_samples.append(
                _camera_sample(
                    setup["camera"],
                    depsgraph,
                    frame=frame,
                    frame_start=frame_start,
                    fps=setup["fps"],
                    width=setup["width"],
                    height=setup["height"],
                    scale=setup["scale"],
                    pixel_aspect=setup["pixel_aspect"],
                )
            )
            for obj in setup["empties"]:
                null_samples[obj.name].append(
                    _null_sample(
                        obj,
                        depsgraph,
                        frame=frame,
                        frame_start=frame_start,
                        fps=setup["fps"],
                        width=setup["width"],
                        height=setup["height"],
                        scale=setup["scale"],
                    )
                )
    finally:
        scene.frame_set(original_frame, subframe=original_subframe)

    return {
        "schema": HANDOFF_SCHEMA,
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "space": {
            "coordinate_system": "after-effects-composition",
            "axis_map": "blender_xyz_to_ae_x_negz_y",
            "origin": "composition-center",
            "position_units": "pixels",
            "pixels_per_blender_unit": _clean_number(setup["scale"]),
        },
        "sampling": {
            "mode": "baked-per-frame",
            "frame_start": frame_start,
            "frame_end": frame_end,
            "frame_step": 1,
        },
        "camera": {
            "name": setup["camera"].name,
            "type": "PERSP",
            "samples": camera_samples,
        },
        "nulls": [
            {
                "name": obj.name,
                "source_type": "EMPTY",
                "samples": null_samples[obj.name],
            }
            for obj in setup["empties"]
        ],
    }

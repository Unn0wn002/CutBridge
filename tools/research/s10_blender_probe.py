from __future__ import annotations

import json
import math

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

from tools.research import s10_spatial_math as spatial


PROBE_SCENE_NAME = "__CUTBRIDGE_S10_PROBE_SCENE__"
PROBE_CAMERA_NAME = "__CUTBRIDGE_S10_PROBE_CAMERA__"


def _rounded(values, digits: int = 12) -> list[float]:
    return [round(float(value), digits) for value in values]


def build_probe_report() -> dict:
    """Create an isolated synthetic Blender scene and return projection evidence.

    The function does not use or modify the user's active scene. Every data-block
    allocated by the probe is removed in the finally block.
    """
    fixture = spatial.FIXTURE
    scene = bpy.data.scenes.new(PROBE_SCENE_NAME)
    camera_data = bpy.data.cameras.new(PROBE_CAMERA_NAME)
    camera = bpy.data.objects.new(PROBE_CAMERA_NAME, camera_data)
    scene.collection.objects.link(camera)

    try:
        width = int(fixture["comp_width"])
        height = int(fixture["comp_height"])
        scene.render.resolution_x = width
        scene.render.resolution_y = height
        scene.render.resolution_percentage = 100
        scene.render.pixel_aspect_x = 1.0
        scene.render.pixel_aspect_y = 1.0
        scene.render.fps = int(fixture["fps"])
        scene.render.fps_base = 1.0
        scene.frame_start = int(fixture["frame_start"])
        scene.frame_end = int(fixture["frame_end"])

        camera_data.type = "PERSP"
        camera_data.lens = float(fixture["camera"]["lens_mm"])
        camera_data.sensor_fit = "HORIZONTAL"
        camera_data.sensor_width = float(fixture["camera"]["sensor_width_mm"])
        camera.location = fixture["camera"]["location"]
        camera.rotation_mode = "XYZ"
        camera.rotation_euler = tuple(
            math.radians(value) for value in fixture["camera"]["rotation_euler_xyz_degrees"]
        )
        scene.camera = camera

        forward = camera.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
        up = camera.matrix_world.to_quaternion() @ Vector((0.0, 1.0, 0.0))
        right = camera.matrix_world.to_quaternion() @ Vector((1.0, 0.0, 0.0))

        expected = spatial.fixture_expected_report()
        points = {}
        for name, coordinates in fixture["points"].items():
            ndc = world_to_camera_view(scene, camera, Vector(coordinates))
            comp_px = (float(ndc.x) * width, (1.0 - float(ndc.y)) * height)
            points[name] = {
                "blender_world": list(coordinates),
                "blender_camera_view": _rounded((ndc.x, ndc.y, ndc.z)),
                "blender_comp_px": _rounded(comp_px),
                "candidate_ae_world": expected["points"][name]["ae_world_candidate"],
                "candidate_ae_comp_px": expected["points"][name]["expected_comp_px"],
                "projection_delta_px": _rounded(
                    (
                        comp_px[0] - expected["points"][name]["expected_comp_px"][0],
                        comp_px[1] - expected["points"][name]["expected_comp_px"][1],
                    )
                ),
            }

        return {
            "schema": spatial.S10_SCHEMA,
            "schema_version": spatial.S10_SCHEMA_VERSION,
            "host": "blender",
            "host_version": bpy.app.version_string,
            "fixture": "front_camera_50mm_1920x1080",
            "basis_candidate": [list(row) for row in spatial.BLENDER_TO_AE_BASIS],
            "comp": {
                "width": width,
                "height": height,
                "pixel_aspect": 1.0,
                "fps": float(scene.render.fps) / float(scene.render.fps_base),
            },
            "camera": {
                "type": camera_data.type,
                "position_world": _rounded(camera.matrix_world.translation),
                "right_world": _rounded(right),
                "up_world": _rounded(up),
                "forward_world": _rounded(forward),
                "lens_mm": float(camera_data.lens),
                "sensor_fit": camera_data.sensor_fit,
                "sensor_width_mm": float(camera_data.sensor_width),
                "angle_x_radians": float(camera_data.angle_x),
                "angle_y_radians": float(camera_data.angle_y),
                "candidate_ae_position": expected["camera"]["ae_position_candidate"],
                "candidate_ae_point_of_interest": expected["camera"]["ae_point_of_interest_candidate"],
                "candidate_ae_zoom": expected["camera"]["ae_zoom_candidate"],
            },
            "points": points,
        }
    finally:
        # Remove only data-blocks allocated by this probe. The user's active scene
        # and existing camera/object data are never selected or mutated.
        if camera.name in bpy.data.objects:
            bpy.data.objects.remove(camera, do_unlink=True)
        if camera_data.name in bpy.data.cameras:
            bpy.data.cameras.remove(camera_data, do_unlink=True)
        if scene.name in bpy.data.scenes:
            bpy.data.scenes.remove(scene, do_unlink=True)


def main() -> None:
    print(json.dumps(build_probe_report(), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

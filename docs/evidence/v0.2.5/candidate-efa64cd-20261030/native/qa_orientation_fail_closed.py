"""Native check that the efa64cd Blender add-on refuses camera roll and rotated Empties (scratch script, copied into the evidence folder).

Run with an isolated profile:
  blender --factory-startup -b --python qa_orientation_fail_closed.py -- <workdir>
For each case: a fresh factory scene with 3D handoff on, then Validate (operator report + handoff_3d_issues)
and Build. Expected: Build does not finish and no package folder is created.
"""
import json
import sys
from math import radians
from pathlib import Path

import addon_utils
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
work = Path(argv[0])
addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)
from bl_ext.user_default.cutbridge.handoff_3d import MARKER_PROPERTY, handoff_3d_issues  # noqa: E402

results = []


def run_case(name, setup):
    bpy.ops.wm.read_factory_settings(use_empty=False)
    addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, 3
    scene.render.resolution_x, scene.render.resolution_y = 480, 270
    out = work / f"orientation_{name}"
    s = scene.cutbridge
    s.project, s.episode, s.scene_id, s.cut, s.take, s.version = "QAPROJ", "EP01", "SC010", "C015", "T01", 1
    s.output_dir = str(out)
    s.handoff_3d_enabled = True
    s.handoff_3d_pixels_per_blender_unit = 100.0
    setup(scene)
    bpy.ops.wm.save_as_mainfile(filepath=str(work / f"orientation_{name}.blend"))
    bpy.context.view_layer.update()
    issues = [(i["level"], i["code"]) for i in handoff_3d_issues(bpy.context)]
    try:
        build = sorted(bpy.ops.cutbridge.build_package())
    except RuntimeError as exc:
        build = ["RuntimeError: " + str(exc).strip().splitlines()[-1]]
    created = sorted(p.name for p in out.iterdir()) if out.exists() else []
    results.append({"case": name, "handoff_issues": issues, "build": build, "package_dirs_created": created})
    print("QA|", name, issues, build, created, flush=True)


def rolled_camera(scene):
    cam = scene.camera
    cam.rotation_euler = (cam.rotation_euler.x, radians(10.0), cam.rotation_euler.z)


def rotated_empty(scene):
    empty = bpy.data.objects.new("QA_NULL", None)
    scene.collection.objects.link(empty)
    empty[MARKER_PROPERTY] = True
    empty.rotation_euler = (0.0, 0.0, radians(15.0))


def rotation_keyed_later(scene):
    empty = bpy.data.objects.new("QA_NULL", None)
    scene.collection.objects.link(empty)
    empty[MARKER_PROPERTY] = True
    empty.rotation_euler = (0.0, 0.0, 0.0)
    empty.keyframe_insert("rotation_euler", frame=1)
    empty.rotation_euler = (0.0, 0.0, radians(30.0))
    empty.keyframe_insert("rotation_euler", frame=3)
    scene.frame_set(1)


def level_control(scene):
    empty = bpy.data.objects.new("QA_NULL", None)
    scene.collection.objects.link(empty)
    empty[MARKER_PROPERTY] = True


for case_name, fn in (("level_control", level_control), ("rolled_camera", rolled_camera),
                      ("rotated_empty", rotated_empty), ("rotation_keyed_later", rotation_keyed_later)):
    run_case(case_name, fn)

(work / "orientation_results.json").write_text(json.dumps(results, indent=1), encoding="utf-8")

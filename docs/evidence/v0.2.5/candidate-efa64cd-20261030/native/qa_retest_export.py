"""Native Blender retest for rows P5/N4/N5/N6 (scratch script, copied into the evidence folder).

Run with an isolated profile:
  blender --factory-startup -b --python qa_retest_export.py -- <zip> <workdir> <version>
Builds one disposable cut with 3D handoff and a custom preset (BEAUTY required, LINE optional).
Compared with the first 2026-10-30 run, the camera now moves and turns, the Empty moves on two axes,
and Blender's own projection of the Empty into the frame is recorded per frame so After Effects
projection parity can be measured, not only key values.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index("--") + 1:]
zip_path, work, version = Path(argv[0]), Path(argv[1]), int(argv[2])
log = []


def say(*parts):
    line = " ".join(str(p) for p in parts)
    log.append(line)
    print("QA|" + line, flush=True)


say("blender", bpy.app.version_string, "hash", bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash, bytes) else bpy.app.build_hash)

# 1. Installed bytes versus the verified ZIP
ext_dir = Path(bpy.utils.user_resource("EXTENSIONS")) / "user_default" / "cutbridge"
mismatch, checked = [], 0
with zipfile.ZipFile(zip_path) as z:
    for info in z.infolist():
        if info.is_dir() or info.filename == "LICENSE":
            continue
        target = ext_dir / info.filename
        checked += 1
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(z.read(info)).hexdigest():
            mismatch.append(info.filename)
say("installed files compared", checked, "mismatched", mismatch)

import addon_utils
addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)
say("scene.cutbridge registered", hasattr(bpy.context.scene, "cutbridge"))

# 2. Custom preset: BEAUTY required, LINE optional
preset = {
    "schema": "cutbridge-studio-preset", "schema_version": 1, "id": "qa-optional-line", "name": "QA optional LINE",
    "naming": {"package": "{project}_{episode}_{scene}_{cut}_{take}_{version}", "sequence": "{cut}_{pass}_####", "ae_comp": "{cut}_COMP"},
    "folders": {"render": "render", "preview": "preview", "camera": "camera"},
    "passes": [{"name": "BEAUTY", "required": True}, {"name": "LINE", "required": False}],
    "output": {"image_format": "PNG"},
    "versioning": {"prefix": "V", "padding": 3},
}
preset_path = work / "qa_preset_optional_line.json"
preset_path.write_text(json.dumps(preset, indent=1), encoding="utf-8")

# 3. Disposable cut: moving, turning camera and one marked Empty moving on x and y
scene = bpy.context.scene
scene.render.fps = 24
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 480, 270, 100
scene.frame_start, scene.frame_end = 1, 3
scene.render.engine = "CYCLES"
scene.cycles.samples = 1
scene.cycles.device = "CPU"
scene.render.use_freestyle = True
bpy.context.view_layer.freestyle_settings.as_render_pass = True
cube = bpy.data.objects.get("Cube")
if cube is not None:
    cube.rotation_euler.z = version * 0.5
cam = scene.camera
base_loc, base_rot = cam.location.copy(), cam.rotation_euler.copy()
for frame, dx, drz in ((1, 0.0, 0.0), (3, 0.6, 0.06)):
    cam.location = (base_loc.x + dx, base_loc.y, base_loc.z)
    cam.rotation_euler = (base_rot.x, base_rot.y, base_rot.z + drz)
    cam.keyframe_insert("location", frame=frame)
    cam.keyframe_insert("rotation_euler", frame=frame)
empty = bpy.data.objects.new("QA_NULL", None)
scene.collection.objects.link(empty)
empty["cutbridge_handoff_3d"] = True
for frame, x, y in ((1, 0.0, 0.0), (3, 1.0, -0.5)):
    empty.location = (x, y, 0.5)
    empty.keyframe_insert("location", frame=frame)
s = scene.cutbridge
s.project, s.episode, s.scene_id, s.cut, s.take, s.version = "QAPROJ", "EP01", "SC010", "C014", "T01", version
s.output_dir = str(work / "cutbridge_exports")
s.language = "EN"
s.studio_preset_mode = "CUSTOM"
s.studio_preset_path = str(preset_path)
s.handoff_3d_enabled = True
s.handoff_3d_pixels_per_blender_unit = 100.0
blend = work / f"QA_retest_v{version:03d}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
say("saved", blend.name, "camera", cam.name, "type", cam.data.type, "lens", cam.data.lens, "sensor", cam.data.sensor_width, cam.data.sensor_fit)

# 4. Blender's own projection of the Empty, in pixels from the top-left of the frame
projection = []
for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.frame_set(frame)
    co = world_to_camera_view(scene, cam, empty.matrix_world.translation)
    projection.append({"frame": frame, "x_px": co.x * scene.render.resolution_x, "y_px": (1.0 - co.y) * scene.render.resolution_y, "depth": co.z})
    say("projection frame", frame, "x_px %.4f y_px %.4f depth %.4f" % (projection[-1]["x_px"], projection[-1]["y_px"], co.z))
(work / f"blender_projection_v{version:03d}.json").write_text(json.dumps(projection, indent=1), encoding="utf-8")
scene.frame_set(scene.frame_start)

# 5. Validate, build, render
say("validate ->", bpy.ops.cutbridge.validate())
say("build_package ->", bpy.ops.cutbridge.build_package(), "last_package_path", s.last_package_path)
pkg = Path(bpy.path.abspath(s.last_package_path)) if s.last_package_path else None
say("package dir exists", bool(pkg and pkg.is_dir()), pkg.name if pkg else None)
if pkg and pkg.is_dir():
    say("render ->", bpy.ops.render.render(animation=True))
    files = sorted(p.relative_to(pkg).as_posix() + ":" + str(p.stat().st_size) for p in pkg.rglob("*") if p.is_file())
    say("package files", len(files))
    for f in files:
        say("  file", f)
    manifest = pkg / "cutbridge.json"
    if manifest.is_file():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        say("manifest version", m.get("version"), "passes", [(p.get("name"), p.get("required")) for p in m.get("passes", [])])
        h = m.get("handoff_3d") or {}
        say("handoff_3d camera", (h.get("camera") or {}).get("name"), "nulls", [n.get("name") for n in h.get("nulls", [])])
        say("manifest sha256", hashlib.sha256(manifest.read_bytes()).hexdigest())
(work / f"qa_blender_log_v{version:03d}.txt").write_text("\n".join(log), encoding="utf-8")

"""Native Blender QA for rows P5/N4/N5 (scratch script, not part of the repository).

Run with an isolated profile:
  blender --factory-startup -b --python qa_native_rows_export.py -- <zip> <workdir> <version>
Builds one disposable cut with 3D handoff (camera + one marked Empty) and a custom preset that
declares BEAUTY required and LINE optional, validates it, builds the package and renders.
LINE is rendered (Freestyle as render pass); the host step then removes its frames so After Effects
meets a declared-but-unavailable optional pass.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import bpy

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

# 3. Disposable cut with camera + one marked Empty
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
empty = bpy.data.objects.new("QA_NULL", None)
scene.collection.objects.link(empty)
empty["cutbridge_handoff_3d"] = True
for frame, x in ((1, 0.0), (3, 1.0)):
    empty.location = (x, 0.0, 0.5)
    empty.keyframe_insert("location", frame=frame)
s = scene.cutbridge
s.project, s.episode, s.scene_id, s.cut, s.take, s.version = "QAPROJ", "EP01", "SC010", "C014", "T01", version
s.output_dir = str(work / "cutbridge_exports")
s.language = "EN"
s.studio_preset_mode = "CUSTOM"
s.studio_preset_path = str(preset_path)
s.handoff_3d_enabled = True
s.handoff_3d_pixels_per_blender_unit = 100.0
blend = work / f"QA_rows_v{version:03d}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
say("saved", blend.name, "camera", scene.camera.name if scene.camera else None, "camera type", scene.camera.data.type if scene.camera else None)

# 4. Validate, build, render
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

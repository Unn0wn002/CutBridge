"""S14B fixture S14B-FX01: build one CutBridge package (V001 reference, V002 or V003) from the start scene.

Run with an isolated Blender profile in which the verified candidate ZIP is installed:
  blender --factory-startup -b <start.blend> --python build_revision_package.py -- <zip> <preset.json> <outdir> <version>

Applies exactly the task-brief settings a participant is asked to enter in JP03, plus a visible content change
per version (V002: character body colour; V003: the prop also moves), then Validate Cut, Build Package and a
full render. The install check compares every ZIP entry except LICENSE with the installed files.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
zip_path, preset_path, out, version = Path(argv[0]), Path(argv[1]), Path(argv[2]), int(argv[3])
log = []


def say(*parts):
    line = " ".join(str(p) for p in parts)
    log.append(line)
    print("FX|" + line, flush=True)


say("blender", bpy.app.version_string, "start", Path(bpy.data.filepath).name)

ext_dir = Path(bpy.utils.user_resource("EXTENSIONS")) / "user_default" / "cutbridge"
mismatch, checked = [], 0
with zipfile.ZipFile(zip_path) as z:
    for info in z.infolist():
        if info.is_dir() or info.filename == "LICENSE":
            continue
        target = ext_dir / info.filename
        checked += 1
        if not target.is_file() or hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256(z.read(info)).digest():
            mismatch.append(info.filename)
say("installed files compared", checked, "mismatched", mismatch)
if mismatch:
    raise SystemExit("installed add-on does not match the candidate ZIP")

import addon_utils
addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)

scene = bpy.context.scene
# Task brief values (docs/evidence/v0.2.5/s14b-fixture-20261030/participant/task_brief_JA.md)
scene.camera = bpy.data.objects["CAM_MAIN"]
scene.render.fps = 24
scene.render.fps_base = 1.0
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 960, 540, 100
scene.frame_start, scene.frame_end = 1, 12

if version >= 2:
    bpy.data.materials["M_CHAR_BODY"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.75, 0.35, 1)
if version >= 3:
    bpy.data.objects["PROP_BOX"].location = (0.6, 1.6, 0.4)

s = scene.cutbridge
s.project, s.episode, s.scene_id, s.cut, s.take, s.version = "S14B", "EP01", "SC001", "C001", "T01", version
s.output_dir = str(out)
s.studio_preset_mode = "CUSTOM"
s.studio_preset_path = str(preset_path)

blend = out.parent / f"S14B_FX01_v{version:03d}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend), compress=False)
say("saved", blend.name)

say("validate ->", bpy.ops.cutbridge.validate())
say("build_package ->", bpy.ops.cutbridge.build_package())
pkg = Path(bpy.path.abspath(s.last_package_path)) if s.last_package_path else None
say("package", pkg.name if pkg else None, "exists", bool(pkg and pkg.is_dir()))
if not (pkg and pkg.is_dir()):
    raise SystemExit("no package")
say("render ->", bpy.ops.render.render(animation=True))
for p in sorted(pkg.rglob("*")):
    if p.is_file():
        say("  file", p.relative_to(pkg).as_posix(), p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
m = json.loads((pkg / "cutbridge.json").read_text(encoding="utf-8"))
say("manifest", m["package_name"], "version", m["version"], "fps", m["fps"], "res", m["resolution"]["width"], m["resolution"]["height"],
    "frames", m["frames"], "camera", m["camera"], "passes", [(p["name"], p.get("required")) for p in m["passes"]],
    "preset", m["studio_preset"]["id"], "handoff_3d" in m)
(out.parent / f"build_log_v{version:03d}.txt").write_text("\n".join(log) + "\n", encoding="utf-8")

"""Native Blender QA run (scratch script, not part of the repository).

Run with an isolated profile:  blender --factory-startup -b --python qa_blender_export.py -- <zip> <workdir> <version>
Builds one disposable cut, validates it, builds the package and renders the mapped outputs.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import bpy

zip_path, work, version = Path(sys.argv[sys.argv.index("--") + 1]), Path(sys.argv[sys.argv.index("--") + 2]), int(sys.argv[sys.argv.index("--") + 3])
log = []


def say(*parts):
    line = " ".join(str(p) for p in parts)
    log.append(line)
    print("QA|" + line, flush=True)


say("blender", bpy.app.version_string, "hash", bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash, bytes) else bpy.app.build_hash)

# 1. Installed bytes versus the verified ZIP -----------------------------------------------------
ext_dir = Path(bpy.utils.user_resource("EXTENSIONS")) / "user_default" / "cutbridge"
say("extension dir exists", ext_dir.is_dir())
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

# 2. Enabled and registered ------------------------------------------------------------------------
module = "bl_ext.user_default.cutbridge"
say("addon enabled at startup (factory-startup does not persist the CLI enable)", module in bpy.context.preferences.addons)
import addon_utils
say("enable call ->", addon_utils.enable(module, default_set=False, persistent=False) is not None)
say("addon enabled", module in bpy.context.preferences.addons or module in addon_utils.addons_fake_modules or hasattr(bpy.context.scene, "cutbridge"))
say("scene.cutbridge registered", hasattr(bpy.context.scene, "cutbridge"))
say("operators", hasattr(bpy.ops.cutbridge, "validate"), hasattr(bpy.ops.cutbridge, "build_package"))

# 3. Disposable cut ----------------------------------------------------------------------------------
scene = bpy.context.scene
scene.render.fps = 24
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 480, 270, 100
scene.frame_start, scene.frame_end = 1, 3
scene.render.engine = "BLENDER_WORKBENCH"
s = scene.cutbridge
s.project, s.episode, s.scene_id, s.cut, s.take, s.version = "QAPROJ", "EP01", "SC010", "C012", "T01", version
s.output_dir = str(work / "cutbridge_exports")
s.language = "EN"
cube = bpy.data.objects.get("Cube")
if cube is not None:
    cube.rotation_euler.z = version * 0.5  # makes each revision's frames differ
blend = work / "QA_cut.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
say("saved", blend.name, "camera", scene.camera.name if scene.camera else None)

# 4. Validate, build, render -------------------------------------------------------------------------
r = bpy.ops.cutbridge.validate()
say("validate ->", r)
r = bpy.ops.cutbridge.build_package()
say("build_package ->", r, "last_package_path", s.last_package_path)
pkg = Path(bpy.path.abspath(s.last_package_path)) if s.last_package_path else None
say("package dir exists", bool(pkg and pkg.is_dir()), pkg.name if pkg else None)
if pkg and pkg.is_dir():
    r = bpy.ops.render.render(animation=True)
    say("render ->", r)
    files = sorted(p.relative_to(pkg).as_posix() + ":" + str(p.stat().st_size) for p in pkg.rglob("*") if p.is_file())
    say("package files", len(files))
    for f in files:
        say("  file", f)
    manifest = pkg / "cutbridge.json"
    if manifest.is_file():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        say("manifest keys", sorted(m.keys()))
        say("manifest version", m.get("version"), "fps", m.get("fps") or m.get("frame_rate"), "range", m.get("frame_start"), m.get("frame_end"))
        say("manifest sha256", hashlib.sha256(manifest.read_bytes()).hexdigest())
(work / "qa_blender_log.txt").write_text("\n".join(log), encoding="utf-8")

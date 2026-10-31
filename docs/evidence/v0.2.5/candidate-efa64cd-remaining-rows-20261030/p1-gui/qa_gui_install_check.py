"""Check a CutBridge install made by a person through Blender's Install from Disk dialog (scratch script, copied into the evidence folder).

Run after the GUI session has closed, with the same isolated profile and WITHOUT --factory-startup, so the
saved preferences decide what is enabled:
  blender -b --python qa_gui_install_check.py -- <zip> <out.txt>
"""
import hashlib
import sys
import zipfile
from pathlib import Path

import addon_utils
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
zip_path, out = Path(argv[0]), Path(argv[1])
log = []


def say(*parts):
    line = " ".join(str(p) for p in parts)
    log.append(line)
    print("QA|" + line, flush=True)


say("blender", bpy.app.version_string)
say("user resources", bpy.utils.resource_path("USER"))
ext_dir = Path(bpy.utils.user_resource("EXTENSIONS")) / "user_default" / "cutbridge"
say("extension dir exists", ext_dir.is_dir(), ext_dir)
mismatch, checked, zip_names = [], 0, set()
with zipfile.ZipFile(zip_path) as z:
    for info in z.infolist():
        if info.is_dir():
            continue
        zip_names.add(info.filename)
        target = ext_dir / info.filename
        checked += 1
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(z.read(info)).hexdigest():
            mismatch.append(info.filename)
say("zip entries compared", checked, "mismatched", mismatch)
extra = sorted(p.relative_to(ext_dir).as_posix() for p in ext_dir.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.relative_to(ext_dir).as_posix() not in zip_names)
say("installed files not in zip (excluding __pycache__)", extra)
module = "bl_ext.user_default.cutbridge"
say("enabled in saved preferences", module in bpy.context.preferences.addons.keys())
default, loaded = addon_utils.check(module)
say("addon_utils.check (default, loaded)", default, loaded)
say("scene.cutbridge registered", hasattr(bpy.context.scene, "cutbridge"))
panels = sorted(c.bl_label for c in bpy.types.Panel.__subclasses__() if getattr(c, "bl_category", "") == "CutBridge" and getattr(c, "bl_space_type", "") == "VIEW_3D")
say("VIEW_3D panels in the CutBridge sidebar tab", panels)
out.write_text("\n".join(log) + "\n", encoding="utf-8")

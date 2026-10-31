"""S14B fixture S14B-FX02: check the shipped JP04 file from a copy of the bundle in a different folder.

Run with the isolated profile that holds the verified candidate:
  blender --factory-startup -b <bundle copy>/S14B_FX01_JP04.blend --python check_jp04_file.py
Expected: Validate Cut fails with CAMERA_MISSING only; after assigning CAM_MAIN it passes. The file is not saved.
"""
import bpy
import addon_utils

addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)
scene = bpy.context.scene
print("JP04|file", bpy.data.filepath, "camera", scene.camera, "language", scene.cutbridge.language, flush=True)
try:
    print("JP04|validate ->", bpy.ops.cutbridge.validate(), flush=True)
except RuntimeError as exc:
    print("JP04|validate raised:", str(exc).replace("\n", " | "), flush=True)
scene.camera = bpy.data.objects["CAM_MAIN"]
print("JP04|camera assigned", flush=True)
try:
    print("JP04|validate ->", bpy.ops.cutbridge.validate(), flush=True)
except RuntimeError as exc:
    print("JP04|validate raised:", str(exc).replace("\n", " | "), flush=True)

"""S14B fixture S14B-FX01: check the JP04 setup (active camera cleared) on the configured V001 scene.

Run with the isolated profile that holds the verified candidate:
  blender --factory-startup -b <S14B_FX01_v001.blend> --python check_jp04.py
Validate Cut runs with the UI language set to Japanese (the default), first with the camera cleared, then restored.
Its messages are Blender operator reports, which background Blender prints to the console. The .blend is not saved.
"""
import bpy
import addon_utils

addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)
scene = bpy.context.scene
scene.cutbridge.language = "JA"
camera = scene.camera
scene.camera = None
print("JP04|camera cleared", flush=True)
try:
    print("JP04|validate ->", bpy.ops.cutbridge.validate(), flush=True)
except RuntimeError as exc:
    print("JP04|validate raised:", str(exc).replace("\n", " | "), flush=True)
scene.camera = camera
print("JP04|camera restored", flush=True)
try:
    print("JP04|validate ->", bpy.ops.cutbridge.validate(), flush=True)
except RuntimeError as exc:
    print("JP04|validate raised:", str(exc).replace("\n", " | "), flush=True)

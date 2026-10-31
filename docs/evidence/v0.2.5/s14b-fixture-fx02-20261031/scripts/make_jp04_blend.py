"""S14B fixture S14B-FX02: the JP04 file for asynchronous sessions.

Run with an isolated Blender profile in which the verified candidate ZIP is installed:
  blender --factory-startup -b <S14B_FX01_start.blend> --python make_jp04_blend.py -- <out.blend>

Applies the task-brief values (as a participant would in JP03), then clears the active scene camera, so that Validate
Cut reports CAMERA_MISSING and nothing else. The output folder and the preset path are blend-relative ("//"), so the
file validates the same way wherever the participant extracts the bundle, as long as it stays next to
studio_preset_s14b_fx01.json. No package is built.
"""
import sys

import bpy
import addon_utils

out = sys.argv[sys.argv.index("--") + 1:][0]
addon_utils.enable("bl_ext.user_default.cutbridge", default_set=False, persistent=False)

scene = bpy.context.scene
scene.render.fps = 24
scene.render.fps_base = 1.0
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 960, 540, 100
scene.frame_start, scene.frame_end = 1, 12

s = scene.cutbridge
s.project, s.episode, s.scene_id, s.cut, s.take, s.version = "S14B", "EP01", "SC001", "C001", "T01", 1
s.output_dir = "//jp04_output"
s.studio_preset_mode = "CUSTOM"
s.studio_preset_path = "//studio_preset_s14b_fx01.json"
s.language = "JA"

scene.camera = None
bpy.ops.wm.save_as_mainfile(filepath=out, compress=False, relative_remap=False)
print("FX|saved", out, "camera", scene.camera, "output_dir", s.output_dir, "preset", s.studio_preset_path, flush=True)

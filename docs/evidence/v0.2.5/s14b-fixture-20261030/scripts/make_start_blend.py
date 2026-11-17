"""S14B fixture S14B-FX01: synthetic start scene (plain bpy, CutBridge not loaded).

Run:
  blender --factory-startup -b --python make_start_blend.py -- <out.blend>

The scene is original and synthetic: a floor, a walking "character" made of primitives, a prop, a light and
CAM_MAIN as the active camera. Render settings deliberately differ from the task brief (30 fps, 1920x1080,
frames 1-250) so that JP03 requires real configuration. Freestyle is enabled as a render pass so the
optional LINE pass renders. No CutBridge metadata is stored.
"""
import sys

import bpy

out = sys.argv[sys.argv.index("--") + 1:][0]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "S14B_FX01"


def material(name, rgba):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = rgba
    return mat


def add(op, name, mat, **kw):
    op(**kw)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


add(bpy.ops.mesh.primitive_plane_add, "FLOOR", material("M_FLOOR", (0.55, 0.6, 0.65, 1)), size=20)
body = add(bpy.ops.mesh.primitive_cylinder_add, "CHAR_BODY", material("M_CHAR_BODY", (0.9, 0.35, 0.25, 1)),
           radius=0.35, depth=1.2, location=(-2.5, 0, 0.6))
head = add(bpy.ops.mesh.primitive_uv_sphere_add, "CHAR_HEAD", material("M_CHAR_HEAD", (0.95, 0.8, 0.65, 1)),
           radius=0.3, location=(0, 0, 0.85))
head.parent = body
add(bpy.ops.mesh.primitive_cube_add, "PROP_BOX", material("M_PROP_BOX", (0.25, 0.45, 0.85, 1)),
    size=0.8, location=(1.8, 1.2, 0.4))

# Simple walk across the frame over frames 1-12
for frame, x in ((1, -2.5), (12, 2.0)):
    body.location.x = x
    body.keyframe_insert("location", index=0, frame=frame)

bpy.ops.object.light_add(type="SUN", location=(4, -4, 8))
bpy.context.active_object.name = "SUN_KEY"
bpy.context.active_object.data.energy = 3.0

bpy.ops.object.camera_add(location=(0, -9, 3.2), rotation=(1.29, 0, 0))
cam = bpy.context.active_object
cam.name = "CAM_MAIN"
cam.data.name = "CAM_MAIN"
scene.camera = cam

world = bpy.data.worlds.new("WORLD")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.8, 0.85, 0.9, 1)
scene.world = world

# Deliberately not the brief's values
scene.render.fps = 30
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 1920, 1080, 100
scene.frame_start, scene.frame_end = 1, 250

# Quick, CPU-only renders on a participant's machine
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 16
scene.cycles.use_denoising = False
scene.render.use_freestyle = True
freestyle = bpy.context.view_layer.freestyle_settings
freestyle.as_render_pass = True
# An empty factory scene's line set has no line style; without one the LINE pass renders blank
if not freestyle.linesets:
    freestyle.linesets.new("LINES")
for lineset in freestyle.linesets:
    if lineset.linestyle is None:
        lineset.linestyle = bpy.data.linestyles.new("LS_LINE")
        lineset.linestyle.thickness = 2.0

bpy.ops.wm.save_as_mainfile(filepath=out, compress=False)
print("FX|saved", out, "objects", sorted(o.name for o in bpy.data.objects), "camera", scene.camera.name,
      "fps", scene.render.fps, "res", scene.render.resolution_x, scene.render.resolution_y,
      "range", scene.frame_start, scene.frame_end, "blender", bpy.app.version_string, flush=True)

import bpy


class CUTBRIDGE_PT_MainPanel(bpy.types.Panel):
    bl_label = "CutBridge"
    bl_idname = "CUTBRIDGE_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CutBridge"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        s = scene.cutbridge

        box = layout.box()
        box.label(text="Project Setup")
        box.prop(s, "project")
        row = box.row(align=True)
        row.prop(s, "episode")
        row.prop(s, "scene_id")
        row = box.row(align=True)
        row.prop(s, "cut")
        row.prop(s, "take")
        row.prop(s, "version")

        box = layout.box()
        box.label(text="Scene Metadata")
        row = box.row(align=True)
        row.label(text=f"FPS: {scene.render.fps / (scene.render.fps_base or 1.0):g}")
        row.label(text=f"Frames: {scene.frame_start}-{scene.frame_end}")
        box.label(text=f"Resolution: {scene.render.resolution_x} × {scene.render.resolution_y}")
        box.label(text=f"Camera: {scene.camera.name if scene.camera else 'NOT SET'}")

        box = layout.box()
        box.label(text="Pass Package")
        row = box.row(align=True)
        row.prop(s, "pass_beauty")
        row.prop(s, "pass_line")
        row.prop(s, "pass_shadow")
        row = box.row(align=True)
        row.prop(s, "pass_depth")
        row.prop(s, "image_format")

        box = layout.box()
        box.label(text="Export")
        box.prop(s, "output_dir")
        row = box.row(align=True)
        row.operator("cutbridge.validate", icon="CHECKMARK")
        row.operator("cutbridge.build_package", icon="PACKAGE")
        if s.last_package_path:
            box.operator("cutbridge.open_package_folder", icon="FILE_FOLDER")
            box.label(text=s.last_package_path)

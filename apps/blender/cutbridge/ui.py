import bpy

from .environment import snapshot
from .update_ops import get_preferences


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

        env = snapshot(bpy)
        box = layout.box()
        box.label(text="Environment")
        box.label(text=f"CutBridge: {env['cutbridge_version']}")
        box.label(text=f"Blender: {env['blender_version']} — {env['compatibility_label']}")
        box.label(text=f"Platform: {env['platform']}")
        box.label(text=f"Python: {env['python_version']}")
        box.label(text=f"Online access: {'Enabled' if env['online_access'] else 'Disabled'}")

        preferences = get_preferences(context)
        update_box = layout.box()
        update_box.label(text="Updates")
        if preferences is None:
            update_box.label(text="CutBridge preferences unavailable", icon="ERROR")
            return

        update_box.label(text=f"Channel: {preferences.update_channel.title()}")
        if not preferences.update_index_url.strip():
            update_box.label(text="Update endpoint not configured")
            update_box.label(text="Configure it in Blender Preferences > Add-ons/Extensions")
        elif not env["online_access"]:
            update_box.label(text="Blender online access is disabled", icon="ERROR")

        row = update_box.row()
        row.enabled = bool(preferences.update_index_url.strip()) and env["online_access"]
        row.operator("cutbridge.check_for_updates", icon="FILE_REFRESH")

        if preferences.update_available:
            update_box.label(text=f"New version: {preferences.latest_version}", icon="INFO")
            if preferences.latest_release_url:
                update_box.operator("cutbridge.open_release_page", icon="URL")
        else:
            update_box.label(text=preferences.last_update_message or "Not checked")

        update_box.label(text="No forced updates; installation remains user-approved")

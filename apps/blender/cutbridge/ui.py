import bpy

from .core import validate_scene
from .diagnostics import diagnostic_parts
from .environment import snapshot
from .handoff_3d import handoff_3d_issues
from .localization import tr
from .package_safety import package_lifecycle_issues
from .preferences import RUNTIME_UPDATE_STATE
from .update_ops import get_preferences
from .version import DEFAULT_UPDATE_INDEX_URL


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
        language = s.language

        def help_button(container, topic):
            op = container.operator("cutbridge.context_help", text="", icon="QUESTION", emboss=False)
            op.topic = topic
            return op

        def labeled_prop(container, data, property_name, label_text, help_topic=None, enabled=True):
            # Labels and editable values use separate full-width rows so core
            # identifiers remain readable in a practical narrow N-panel.
            label_row = container.row(align=True)
            label_row.label(text=label_text)
            if help_topic:
                help_button(label_row, help_topic)
            value_row = container.row()
            value_row.enabled = enabled
            value_row.prop(data, property_name, text="")

        def inline_prop_help(container, data, property_name, label_text, topic, enabled=True):
            row = container.row(align=True)
            control = row.row(align=True)
            control.enabled = enabled
            control.prop(data, property_name, text=label_text)
            help_button(row, topic)

        def action_help(container, operator_id, text, icon, topic):
            row = container.row(align=True)
            row.operator(operator_id, text=text, icon=icon)
            help_button(row, topic)

        labeled_prop(layout, s, "language", tr(language, "language"))

        box = layout.box()
        box.label(text=tr(language, "project_setup"))
        labeled_prop(box, s, "project", tr(language, "project"))
        labeled_prop(box, s, "episode", tr(language, "episode"))
        labeled_prop(box, s, "scene_id", tr(language, "scene"))
        labeled_prop(box, s, "cut", tr(language, "cut"))
        labeled_prop(box, s, "take", tr(language, "take"))
        labeled_prop(box, s, "version", tr(language, "version"), "version")

        box = layout.box()
        box.label(text=tr(language, "scene_metadata"))
        row = box.row(align=True)
        row.label(text=tr(language, "fps", value=f"{scene.render.fps / (scene.render.fps_base or 1.0):g}"))
        row.label(text=tr(language, "frames", value=f"{scene.frame_start}-{scene.frame_end}"))
        box.label(text=tr(language, "resolution", value=f"{scene.render.resolution_x} × {scene.render.resolution_y}"))
        camera_name = scene.camera.name if scene.camera else tr(language, "camera_not_set")
        row = box.row(align=True)
        row.label(text=tr(language, "camera", value=camera_name))
        help_button(row, "camera")

        preset_box = layout.box()
        preset_box.label(text=tr(language, "studio_preset"))
        labeled_prop(preset_box, s, "studio_preset_mode", tr(language, "preset_mode"), "studio_preset")
        if s.studio_preset_mode == "CUSTOM":
            labeled_prop(preset_box, s, "studio_preset_path", tr(language, "preset_json"), "studio_preset")
        if s.studio_preset_mode == "MANUAL":
            preset_box.label(text=tr(language, "preset_manual_hint"), icon="INFO")
        else:
            preset_box.label(text=tr(language, "preset_managed_hint"), icon="LOCKED")

        box = layout.box()
        box.label(text=tr(language, "pass_package"))
        controls_enabled = s.studio_preset_mode == "MANUAL"
        inline_prop_help(box, s, "pass_beauty", tr(language, "beauty"), "beauty", controls_enabled)
        inline_prop_help(box, s, "pass_line", tr(language, "line"), "line", controls_enabled)
        inline_prop_help(box, s, "pass_shadow", tr(language, "shadow"), "shadow", controls_enabled)
        inline_prop_help(box, s, "pass_depth", tr(language, "depth"), "depth", controls_enabled)
        labeled_prop(
            box,
            s,
            "image_format",
            tr(language, "sequence_format"),
            "sequence_format",
            controls_enabled,
        )
        if s.studio_preset_mode == "MANUAL":
            inline_prop_help(
                box,
                s,
                "per_pass_formats_enabled",
                tr(language, "per_pass_formats"),
                "sequence_format",
                controls_enabled,
            )
            if s.per_pass_formats_enabled:
                for prop_name, pass_key in (
                    ("format_beauty", "beauty"),
                    ("format_line", "line"),
                    ("format_shadow", "shadow"),
                    ("format_depth", "depth"),
                ):
                    row = box.row()
                    row.enabled = controls_enabled and bool(getattr(s, "pass_" + pass_key))
                    row.prop(s, prop_name, text=tr(language, pass_key))
        if s.studio_preset_mode != "MANUAL":
            box.label(text=tr(language, "preset_controls_passes"))

        box = layout.box()
        box.label(text=tr(language, "export"))
        labeled_prop(box, s, "output_dir", tr(language, "package_output"), "output_path")
        action_help(box, "cutbridge.validate", tr(language, "validate_cut"), "CHECKMARK", "validate")
        action_help(box, "cutbridge.build_package", tr(language, "build_package"), "PACKAGE", "build")
        if s.last_package_path:
            box.operator(
                "cutbridge.open_package_folder",
                text=tr(language, "open_package_folder"),
                icon="FILE_FOLDER",
            )
            box.label(text=s.last_package_path)

        validation_box = layout.box()
        validation_box.label(text=tr(language, "validation_status"))
        # Panel draw must remain read-only. Line/Shadow socket probes create
        # temporary compositor datablocks, so they run only from the explicit
        # validation and package-build operators where mutation is controlled.
        issues = validate_scene(context)
        issues.extend(handoff_3d_issues(context))
        issues.extend(package_lifecycle_issues(context))
        errors = [item for item in issues if item["level"] == "ERROR"]
        warnings = [item for item in issues if item["level"] == "WARNING"]
        infos = [item for item in issues if item["level"] == "INFO"]

        if not issues:
            validation_box.label(text=tr(language, "ready_to_build"), icon="CHECKMARK")
        elif not errors and not warnings and infos:
            parts = diagnostic_parts(language, infos[0])
            validation_box.label(text=parts["title"], icon="CHECKMARK")
            validation_box.label(text=parts["what"])
            validation_box.label(text=parts["continue"])
            if parts["fix"]:
                validation_box.label(text=tr(language, "fix", value=parts["fix"]))
            validation_box.label(text=tr(language, "support_code", value=infos[0]["code"]))
        else:
            validation_box.label(
                text=tr(language, "validation_counts", errors=len(errors), warnings=len(warnings)),
                icon="ERROR" if errors else "INFO",
            )
            for item in issues[:3]:
                level = str(item.get("level", "INFO")).upper()
                icon = "ERROR" if level == "ERROR" else "INFO"
                parts = diagnostic_parts(language, item)
                issue_box = validation_box.box()
                issue_box.label(text=f"{level}: {parts['title']}", icon=icon)
                issue_box.label(text=tr(language, "diagnostic_what", value=parts["what"]))
                issue_box.label(text=tr(language, "diagnostic_why", value=parts["why"]))
                issue_box.label(text=tr(language, "diagnostic_continue", value=parts["continue"]))
                if parts["fix"]:
                    issue_box.label(text=tr(language, "fix", value=parts["fix"]))
                # Technical identifiers remain visible for support, but are no
                # longer the first wording a production user has to interpret.
                issue_box.label(text=tr(language, "support_code", value=item["code"]))
            if len(issues) > 3:
                validation_box.label(text=tr(language, "more_issues", count=len(issues) - 3))

        env = snapshot(bpy)
        box = layout.box()
        box.label(text=tr(language, "environment"))
        box.label(text=f"CutBridge: {env['cutbridge_version']}")
        box.label(text=f"Blender: {env['blender_version']} — {env['compatibility_label']}")
        box.label(text=tr(language, "platform", value=env["platform"]))
        box.label(text=tr(language, "python", value=env["python_version"]))
        online_label = tr(language, "enabled") if env["online_access"] else tr(language, "disabled")
        box.label(text=tr(language, "online_access", value=online_label))

        preferences = get_preferences(context)
        update_box = layout.box()
        update_box.label(text=tr(language, "updates"))
        if preferences is None:
            update_box.label(text=tr(language, "preferences_unavailable"), icon="ERROR")
            return

        update_box.label(text=tr(language, "channel", value=preferences.update_channel.title()))
        endpoint_ready = bool(DEFAULT_UPDATE_INDEX_URL.strip())
        if not endpoint_ready:
            update_box.label(text=tr(language, "update_endpoint_missing"))
        elif not env["online_access"]:
            update_box.label(text=tr(language, "online_access_disabled"), icon="ERROR")

        row = update_box.row()
        row.enabled = endpoint_ready and env["online_access"]
        row.operator("cutbridge.check_for_updates", text=tr(language, "check_updates"), icon="FILE_REFRESH")

        state = RUNTIME_UPDATE_STATE
        if state.update_available:
            update_box.label(text=tr(language, "new_version", value=state.latest_version), icon="INFO")
            if state.latest_release_url:
                update_box.operator(
                    "cutbridge.open_release_page",
                    text=tr(language, "open_release_page"),
                    icon="URL",
                )
        else:
            update_box.label(text=state.last_update_message or tr(language, "not_checked"))

        update_box.label(text=tr(language, "updates_user_approved"))

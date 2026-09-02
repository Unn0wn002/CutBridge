"""User-level CutBridge preferences and transient update state.

Only settings that genuinely need Blender persistence are RNA properties.
Release endpoint/status strings stay out of AddonPreferences so Blender RNA
registration cannot fail on updater transport metadata.
"""

import bpy
from bpy.props import BoolProperty, EnumProperty

from .version import DEFAULT_UPDATE_INDEX_URL


class _RuntimeUpdateState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.update_available = False
        self.latest_version = ""
        self.latest_release_url = ""
        self.last_update_message = "Not checked"
        self.last_update_check = ""


RUNTIME_UPDATE_STATE = _RuntimeUpdateState()


class CUTBRIDGE_AP_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    update_channel: EnumProperty(
        name="Update Channel",
        items=(
            ("stable", "Stable", "Production-oriented releases"),
            ("beta", "Beta", "Stable and beta releases"),
            ("development", "Development", "Stable, beta, and development releases"),
        ),
        default="stable",
    )
    check_updates_on_startup: BoolProperty(
        name="Check on Startup",
        description="Check for a compatible CutBridge release after Blender starts; never installs automatically",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "update_channel")
        layout.prop(self, "check_updates_on_startup")

        box = layout.box()
        box.label(text="Update policy")
        if DEFAULT_UPDATE_INDEX_URL:
            box.label(text="Release endpoint is managed by the CutBridge distribution channel.")
        else:
            box.label(text="Release endpoint is not configured in this development build.")
        box.label(text="CutBridge checks only; it never force-installs or replaces active code.")
        box.label(text="Installation/rollback must be user-approved through the distribution workflow.")

        state = RUNTIME_UPDATE_STATE
        if state.last_update_check:
            box.label(text=f"Last check: {state.last_update_check}")
        box.label(text=state.last_update_message or "Not checked")

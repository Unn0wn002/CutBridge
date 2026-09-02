"""User-level CutBridge preferences.

Update settings belong in Blender preferences rather than scene data because
release channels and network policy are workstation/user concerns.
"""

import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty

from .version import DEFAULT_UPDATE_INDEX_URL


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
    update_index_url: StringProperty(
        name="Update Index URL",
        description="Separately hosted CutBridge release index; the private source repository is not used as an update endpoint",
        subtype="URL",
        default=DEFAULT_UPDATE_INDEX_URL,
    )
    check_updates_on_startup: BoolProperty(
        name="Check on Startup",
        description="Check for a compatible CutBridge release after Blender starts; never installs automatically",
        default=True,
    )

    update_available: BoolProperty(default=False, options={"HIDDEN"})
    latest_version: StringProperty(default="", options={"HIDDEN"})
    latest_release_url: StringProperty(default="", options={"HIDDEN"})
    last_update_message: StringProperty(default="Not checked", options={"HIDDEN"})
    last_update_check: StringProperty(default="", options={"HIDDEN"})

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "update_channel")
        layout.prop(self, "update_index_url")
        layout.prop(self, "check_updates_on_startup")

        box = layout.box()
        box.label(text="Update policy")
        box.label(text="CutBridge checks only; it never force-installs or replaces active code.")
        box.label(text="Installation/rollback must be user-approved through the distribution workflow.")

        if self.last_update_check:
            box.label(text=f"Last check: {self.last_update_check}")
        box.label(text=self.last_update_message or "Not checked")

"""Blender operators and startup timer for update discovery."""

from __future__ import annotations

from datetime import datetime, timezone
import webbrowser

import bpy

from .environment import platform_id
from .updates import UpdateIndexError, fetch_update_index, select_latest_compatible
from .version import __version__


def get_preferences(context=None):
    context = context or bpy.context
    addons = getattr(context.preferences, "addons", {})
    addon = addons.get(__package__)
    return addon.preferences if addon else None


def _set_message(preferences, message: str):
    preferences.last_update_message = message
    preferences.last_update_check = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def perform_update_check(preferences) -> bool:
    """Check metadata and update preference state. Never installs anything."""
    preferences.update_available = False
    preferences.latest_version = ""
    preferences.latest_release_url = ""

    if not preferences.update_index_url.strip():
        _set_message(preferences, "Update endpoint not configured")
        return False

    if not bool(getattr(bpy.app, "online_access", False)):
        _set_message(preferences, "Blender online access is disabled")
        return False

    try:
        payload = fetch_update_index(preferences.update_index_url)
        release = select_latest_compatible(
            payload,
            current_version=__version__,
            blender_version=bpy.app.version,
            platform_name=platform_id(),
            selected_channel=preferences.update_channel,
        )
    except UpdateIndexError as exc:
        _set_message(preferences, f"Update check failed: {exc}")
        return False

    if release is None:
        _set_message(preferences, f"CutBridge {__version__} is up to date for this environment")
        return True

    preferences.update_available = True
    preferences.latest_version = release["version"]
    preferences.latest_release_url = release["release_page_url"]
    _set_message(preferences, f"CutBridge {release['version']} is available")
    return True


class CUTBRIDGE_OT_CheckForUpdates(bpy.types.Operator):
    bl_idname = "cutbridge.check_for_updates"
    bl_label = "Check for Updates"
    bl_description = "Check the configured CutBridge release index; no software is installed"

    def execute(self, context):
        preferences = get_preferences(context)
        if preferences is None:
            self.report({"ERROR"}, "CutBridge preferences are unavailable")
            return {"CANCELLED"}

        success = perform_update_check(preferences)
        if preferences.update_available:
            self.report({"INFO"}, preferences.last_update_message)
        elif success:
            self.report({"INFO"}, preferences.last_update_message)
        else:
            self.report({"WARNING"}, preferences.last_update_message)
        return {"FINISHED"}


class CUTBRIDGE_OT_OpenReleasePage(bpy.types.Operator):
    bl_idname = "cutbridge.open_release_page"
    bl_label = "Open Release Page"
    bl_description = "Open the compatible release page so the user can review and approve the update"

    def execute(self, context):
        preferences = get_preferences(context)
        if preferences is None or not preferences.latest_release_url:
            self.report({"WARNING"}, "No compatible release URL is available")
            return {"CANCELLED"}

        try:
            if hasattr(bpy.ops.wm, "url_open"):
                bpy.ops.wm.url_open(url=preferences.latest_release_url)
            else:
                webbrowser.open(preferences.latest_release_url)
        except Exception as exc:  # Browser integration is platform-dependent.
            self.report({"ERROR"}, f"Unable to open release page: {exc}")
            return {"CANCELLED"}
        return {"FINISHED"}


def _startup_update_check():
    preferences = get_preferences()
    if preferences and preferences.check_updates_on_startup and preferences.update_index_url.strip():
        perform_update_check(preferences)
    return None


def schedule_startup_update_check():
    if not bpy.app.timers.is_registered(_startup_update_check):
        bpy.app.timers.register(_startup_update_check, first_interval=4.0)


def cancel_startup_update_check():
    if bpy.app.timers.is_registered(_startup_update_check):
        bpy.app.timers.unregister(_startup_update_check)

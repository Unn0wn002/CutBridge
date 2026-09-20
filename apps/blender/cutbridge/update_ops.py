"""Blender operators and startup timer for update discovery."""

from __future__ import annotations

from datetime import datetime, timezone
import webbrowser

import bpy

from .environment import platform_id
from .preferences import RUNTIME_UPDATE_STATE
from .updates import UpdateIndexError, fetch_update_index, select_latest_compatible
from .version import DEFAULT_UPDATE_INDEX_URL, __version__


def get_preferences(context=None):
    context = context or bpy.context
    addons = getattr(context.preferences, "addons", {})
    addon = addons.get(__package__)
    return addon.preferences if addon else None


def _set_message(message: str):
    RUNTIME_UPDATE_STATE.last_update_message = message
    RUNTIME_UPDATE_STATE.last_update_check = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def perform_update_check(preferences) -> bool:
    """Check metadata and update transient state. Never installs anything."""
    state = RUNTIME_UPDATE_STATE
    state.update_available = False
    state.latest_version = ""
    state.latest_release_url = ""

    update_index_url = DEFAULT_UPDATE_INDEX_URL.strip()
    if not update_index_url:
        _set_message("Update endpoint not configured")
        return False

    if not bool(getattr(bpy.app, "online_access", False)):
        _set_message("Blender online access is disabled")
        return False

    try:
        payload = fetch_update_index(update_index_url)
        release = select_latest_compatible(
            payload,
            current_version=__version__,
            blender_version=bpy.app.version,
            platform_name=platform_id(),
            selected_channel=preferences.update_channel,
        )
    except UpdateIndexError as exc:
        _set_message(f"Update check failed: {exc}")
        return False

    if release is None:
        _set_message(f"CutBridge {__version__} is up to date for this environment")
        return True

    state.update_available = True
    state.latest_version = release["version"]
    state.latest_release_url = release["release_page_url"]
    _set_message(f"CutBridge {release['version']} is available")
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
        state = RUNTIME_UPDATE_STATE
        if state.update_available or success:
            self.report({"INFO"}, state.last_update_message)
        else:
            self.report({"WARNING"}, state.last_update_message)
        return {"FINISHED"}


class CUTBRIDGE_OT_OpenReleasePage(bpy.types.Operator):
    bl_idname = "cutbridge.open_release_page"
    bl_label = "Open Release Page"
    bl_description = "Open the compatible release page so the user can review and approve the update"

    def execute(self, context):
        release_url = RUNTIME_UPDATE_STATE.latest_release_url
        if not release_url:
            self.report({"WARNING"}, "No compatible release URL is available")
            return {"CANCELLED"}

        try:
            if hasattr(bpy.ops.wm, "url_open"):
                bpy.ops.wm.url_open(url=release_url)
            else:
                webbrowser.open(release_url)
        except Exception as exc:  # Browser integration is platform-dependent.
            self.report({"ERROR"}, f"Unable to open release page: {exc}")
            return {"CANCELLED"}
        return {"FINISHED"}


def _startup_update_check():
    preferences = get_preferences()
    if preferences and preferences.check_updates_on_startup and DEFAULT_UPDATE_INDEX_URL.strip():
        perform_update_check(preferences)
    return None


def schedule_startup_update_check():
    # Temporarily disabled while isolating Blender 5.2.1 Render Animation crash
    # reported in owner validation (#82). Manual update checks remain available.
    # A background bpy.app.timer touching bpy.context shortly after add-on
    # registration is not required for core CutBridge handoff functionality and
    # is being removed from the beta candidate until native render safety is
    # revalidated.
    return None


def cancel_startup_update_check():
    if bpy.app.timers.is_registered(_startup_update_check):
        bpy.app.timers.unregister(_startup_update_check)

from .version import BLENDER_VERSION_MIN, VERSION

bl_info = {
    "name": "CutBridge",
    "author": "CutBridge Student Project",
    "version": VERSION,
    "blender": BLENDER_VERSION_MIN,
    "location": "View3D > Sidebar > CutBridge",
    "description": "Build a deterministic anime cut package for Blender to After Effects handoff",
    "category": "Pipeline",
}

import bpy
from bpy.props import PointerProperty

from .properties import CUTBRIDGE_PG_Settings
from .operators import (
    CUTBRIDGE_OT_Validate,
    CUTBRIDGE_OT_BuildPackage,
    CUTBRIDGE_OT_OpenPackageFolder,
)
from .help_ops import CUTBRIDGE_OT_ContextHelp
from .preferences import CUTBRIDGE_AP_Preferences
from .update_ops import (
    CUTBRIDGE_OT_CheckForUpdates,
    CUTBRIDGE_OT_OpenReleasePage,
    cancel_startup_update_check,
    schedule_startup_update_check,
)
from .ui import CUTBRIDGE_PT_MainPanel

CLASSES = (
    CUTBRIDGE_PG_Settings,
    CUTBRIDGE_AP_Preferences,
    CUTBRIDGE_OT_Validate,
    CUTBRIDGE_OT_BuildPackage,
    CUTBRIDGE_OT_OpenPackageFolder,
    CUTBRIDGE_OT_ContextHelp,
    CUTBRIDGE_OT_CheckForUpdates,
    CUTBRIDGE_OT_OpenReleasePage,
    CUTBRIDGE_PT_MainPanel,
)


def _registered_class_for(cls):
    """Return a stale/current Blender class registration with this identifier."""
    lookup = getattr(bpy.types.Struct, "bl_rna_get_subclass_py", None)
    if lookup is None:
        return None
    try:
        return lookup(cls.__name__)
    except Exception:
        return None


def _safe_unregister_class(cls):
    """Unregister one CutBridge class without failing on partial prior loads."""
    existing = _registered_class_for(cls)
    target = existing or cls

    # Never unregister another add-on's class just because an identifier collides.
    module_name = getattr(target, "__module__", "")
    if existing is not None and existing is not cls and not module_name.startswith(__package__):
        return

    try:
        bpy.utils.unregister_class(target)
    except (RuntimeError, ValueError):
        pass


def _cleanup_partial_registration():
    """Recover from an interrupted/failed enable before attempting registration."""
    try:
        cancel_startup_update_check()
    except Exception:
        pass

    if hasattr(bpy.types.Scene, "cutbridge"):
        try:
            del bpy.types.Scene.cutbridge
        except Exception:
            pass

    for cls in reversed(CLASSES):
        _safe_unregister_class(cls)


def register():
    # A previous failed enable can leave the first few classes registered. Clean
    # those remnants so retrying the extension does not produce "already
    # registered as a subclass" errors.
    _cleanup_partial_registration()

    registered = []
    try:
        for cls in CLASSES:
            bpy.utils.register_class(cls)
            registered.append(cls)

        bpy.types.Scene.cutbridge = PointerProperty(type=CUTBRIDGE_PG_Settings)
        schedule_startup_update_check()
    except Exception:
        # Registration must be transactional: if any class/property fails, roll
        # back everything registered in this attempt before re-raising the root
        # error. This keeps Blender usable and allows an immediate retry.
        try:
            cancel_startup_update_check()
        except Exception:
            pass

        if hasattr(bpy.types.Scene, "cutbridge"):
            try:
                del bpy.types.Scene.cutbridge
            except Exception:
                pass

        for cls in reversed(registered):
            _safe_unregister_class(cls)
        raise


def unregister():
    _cleanup_partial_registration()


if __name__ == "__main__":
    register()

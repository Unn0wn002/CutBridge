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
    CUTBRIDGE_OT_CheckForUpdates,
    CUTBRIDGE_OT_OpenReleasePage,
    CUTBRIDGE_PT_MainPanel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cutbridge = PointerProperty(type=CUTBRIDGE_PG_Settings)
    schedule_startup_update_check()


def unregister():
    cancel_startup_update_check()
    if hasattr(bpy.types.Scene, "cutbridge"):
        del bpy.types.Scene.cutbridge
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

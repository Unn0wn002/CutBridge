bl_info = {
    "name": "CutBridge",
    "author": "CutBridge Student Project",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
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
from .ui import CUTBRIDGE_PT_MainPanel

CLASSES = (
    CUTBRIDGE_PG_Settings,
    CUTBRIDGE_OT_Validate,
    CUTBRIDGE_OT_BuildPackage,
    CUTBRIDGE_OT_OpenPackageFolder,
    CUTBRIDGE_PT_MainPanel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cutbridge = PointerProperty(type=CUTBRIDGE_PG_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "cutbridge"):
        del bpy.types.Scene.cutbridge
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

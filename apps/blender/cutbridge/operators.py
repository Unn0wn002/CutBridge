import os
import subprocess
import sys

import bpy

from .core import (
    absolute_output_dir,
    build_manifest,
    ensure_package_dirs,
    package_name,
    selected_passes,
    validate_scene,
    write_manifest,
)


def _open_folder(path: str):
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


class CUTBRIDGE_OT_Validate(bpy.types.Operator):
    bl_idname = "cutbridge.validate"
    bl_label = "Validate Cut"
    bl_description = "Check cut metadata and Blender scene settings"

    def execute(self, context):
        issues = validate_scene(context)
        errors = [i for i in issues if i["level"] == "ERROR"]
        warnings = [i for i in issues if i["level"] == "WARNING"]

        if errors:
            self.report({"ERROR"}, f"CutBridge: {len(errors)} error(s), {len(warnings)} warning(s). See console.")
        elif warnings:
            self.report({"WARNING"}, f"CutBridge: valid with {len(warnings)} warning(s). See console.")
        else:
            self.report({"INFO"}, "CutBridge: validation passed.")

        if issues:
            print("\n=== CutBridge Validation ===")
            for item in issues:
                print(f"[{item['level']}] {item['code']}: {item['message']} FIX: {item['fix']}")
            print("============================\n")

        return {"FINISHED"}


class CUTBRIDGE_OT_BuildPackage(bpy.types.Operator):
    bl_idname = "cutbridge.build_package"
    bl_label = "Build Package"
    bl_description = "Create deterministic cut folders and cutbridge.json manifest"

    def execute(self, context):
        issues = validate_scene(context)
        errors = [i for i in issues if i["level"] == "ERROR"]
        if errors:
            for item in errors[:3]:
                self.report({"ERROR"}, item["message"])
            return {"CANCELLED"}

        settings = context.scene.cutbridge
        root = absolute_output_dir(settings) / package_name(settings)
        ensure_package_dirs(root, selected_passes(settings))
        manifest = build_manifest(context, root)
        manifest_path = write_manifest(manifest, root)
        settings.last_package_path = str(root)

        self.report({"INFO"}, f"CutBridge package created: {manifest_path}")
        print(f"CutBridge package: {root}")
        return {"FINISHED"}


class CUTBRIDGE_OT_OpenPackageFolder(bpy.types.Operator):
    bl_idname = "cutbridge.open_package_folder"
    bl_label = "Open Package Folder"

    def execute(self, context):
        path = context.scene.cutbridge.last_package_path
        if not path or not os.path.isdir(path):
            self.report({"WARNING"}, "Build a package first.")
            return {"CANCELLED"}
        _open_folder(path)
        return {"FINISHED"}

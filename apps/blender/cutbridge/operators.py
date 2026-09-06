import os
import subprocess
import sys

import bpy

from .core import (
    absolute_output_dir,
    build_manifest,
    configure_render_outputs,
    ensure_package_dirs,
    package_name,
    selected_passes,
    validate_scene,
    write_manifest,
)
from .package_safety import (
    assert_package_integrity,
    format_issue,
    package_target_issues,
)


def _open_folder(path: str):
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def _all_validation_issues(context) -> list[dict]:
    issues = validate_scene(context)
    issues.extend(package_target_issues(context.scene.cutbridge))
    return issues


class CUTBRIDGE_OT_Validate(bpy.types.Operator):
    bl_idname = "cutbridge.validate"
    bl_label = "Validate Cut"
    bl_description = "Check cut metadata, scene settings, render mapping, and package target safety"

    def execute(self, context):
        issues = _all_validation_issues(context)
        errors = [i for i in issues if i["level"] == "ERROR"]
        warnings = [i for i in issues if i["level"] == "WARNING"]

        if errors:
            first = format_issue(errors[0])
            self.report({"ERROR"}, f"CutBridge: {len(errors)} error(s), {len(warnings)} warning(s). {first}")
        elif warnings:
            first = format_issue(warnings[0])
            self.report({"WARNING"}, f"CutBridge: valid with {len(warnings)} warning(s). {first}")
        else:
            self.report({"INFO"}, "CutBridge: validation passed. Package target is safe to build.")

        if issues:
            print("\n=== CutBridge Validation ===")
            for item in issues:
                print(f"[{item['level']}] {item['code']}: {format_issue(item)}")
            print("============================\n")

        return {"FINISHED"}


class CUTBRIDGE_OT_BuildPackage(bpy.types.Operator):
    bl_idname = "cutbridge.build_package"
    bl_label = "Build Package"
    bl_description = "Configure deterministic render outputs and create a new non-overwriting CutBridge package"

    def execute(self, context):
        issues = _all_validation_issues(context)
        errors = [i for i in issues if i["level"] == "ERROR"]
        if errors:
            for item in errors[:3]:
                self.report({"ERROR"}, format_issue(item))
            return {"CANCELLED"}

        settings = context.scene.cutbridge
        root = absolute_output_dir(settings) / package_name(settings)
        passes = selected_passes(settings)

        # Configure the scene before touching the package directory. If the
        # selected engine cannot expose a requested logical pass, Build Package
        # fails without leaving a misleading empty handoff package on disk.
        try:
            configure_render_outputs(context, root)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        try:
            ensure_package_dirs(root, passes)
            manifest = build_manifest(context, root)
            manifest_path = write_manifest(manifest, root)
            assert_package_integrity(root, manifest, passes)
        except (OSError, RuntimeError, ValueError) as exc:
            self.report({"ERROR"}, f"CutBridge package build failed: {exc}")
            return {"CANCELLED"}

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

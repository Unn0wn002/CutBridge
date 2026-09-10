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
from .localization import format_localized_issue, tr
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


def _language(context) -> str:
    return getattr(context.scene.cutbridge, "language", "EN")


class CUTBRIDGE_OT_Validate(bpy.types.Operator):
    bl_idname = "cutbridge.validate"
    bl_label = "Validate Cut"
    bl_description = "Check cut metadata, scene settings, render mapping, Studio Preset, and package target safety"

    def execute(self, context):
        language = _language(context)
        issues = _all_validation_issues(context)
        errors = [i for i in issues if i["level"] == "ERROR"]
        warnings = [i for i in issues if i["level"] == "WARNING"]

        if errors:
            first = format_localized_issue(language, errors[0])
            self.report(
                {"ERROR"},
                tr(language, "validation_failed", errors=len(errors), warnings=len(warnings), detail=first),
            )
        elif warnings:
            first = format_localized_issue(language, warnings[0])
            self.report(
                {"WARNING"},
                tr(language, "validation_warning", warnings=len(warnings), detail=first),
            )
        else:
            self.report({"INFO"}, tr(language, "validation_passed"))

        # Console output intentionally keeps the canonical English technical
        # details for support/debugging while the interactive UI is localized.
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
        language = _language(context)
        issues = _all_validation_issues(context)
        errors = [i for i in issues if i["level"] == "ERROR"]
        if errors:
            for item in errors[:3]:
                self.report({"ERROR"}, format_localized_issue(language, item))
            return {"CANCELLED"}

        settings = context.scene.cutbridge
        try:
            root = absolute_output_dir(settings) / package_name(settings)
            passes = selected_passes(settings)
        except (OSError, RuntimeError, ValueError) as exc:
            self.report({"ERROR"}, tr(language, "package_build_failed", detail=str(exc)))
            return {"CANCELLED"}

        # Configure the scene before touching the package directory. If the
        # selected engine cannot expose a requested logical pass, Build Package
        # fails without leaving a misleading empty handoff package on disk.
        try:
            configure_render_outputs(context, root)
        except (RuntimeError, ValueError) as exc:
            self.report({"ERROR"}, tr(language, "package_build_failed", detail=str(exc)))
            return {"CANCELLED"}

        try:
            manifest = build_manifest(context, root)
            ensure_package_dirs(root, passes, manifest.get("folders"))
            manifest_path = write_manifest(manifest, root)
            assert_package_integrity(root, manifest, passes)
        except (OSError, RuntimeError, ValueError) as exc:
            self.report({"ERROR"}, tr(language, "package_build_failed", detail=str(exc)))
            return {"CANCELLED"}

        settings.last_package_path = str(root)

        self.report({"INFO"}, tr(language, "package_created", path=manifest_path))
        print(f"CutBridge package: {root}")
        return {"FINISHED"}


class CUTBRIDGE_OT_OpenPackageFolder(bpy.types.Operator):
    bl_idname = "cutbridge.open_package_folder"
    bl_label = "Open Package Folder"

    def execute(self, context):
        language = _language(context)
        path = context.scene.cutbridge.last_package_path
        if not path or not os.path.isdir(path):
            self.report({"WARNING"}, tr(language, "build_first"))
            return {"CANCELLED"}
        _open_folder(path)
        return {"FINISHED"}

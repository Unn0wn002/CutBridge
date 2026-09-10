import os
import subprocess
import sys
from contextlib import nullcontext
from pathlib import Path

import bpy

from .core import (
    absolute_output_dir,
    active_preset,
    build_manifest,
    configure_render_outputs,
    effective_package_name,
    ensure_package_dirs,
    selected_passes,
    validate_scene,
    write_manifest,
)
from .handoff_3d import build_handoff_3d, handoff_3d_enabled, handoff_3d_issues
from .localization import format_localized_issue, tr
from .package_safety import (
    assert_package_integrity,
    format_issue,
    package_target_issues,
)
from .presets import use_preset_file_snapshot


def _open_folder(path: str):
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def _all_validation_issues(context) -> list[dict]:
    issues = validate_scene(context)
    issues.extend(handoff_3d_issues(context))
    issues.extend(package_target_issues(context.scene.cutbridge))
    return issues


def _language(context) -> str:
    return getattr(context.scene.cutbridge, "language", "EN")


class CUTBRIDGE_OT_Validate(bpy.types.Operator):
    bl_idname = "cutbridge.validate"
    bl_label = "Validate Cut"
    bl_description = "Check cut metadata, scene settings, render mapping, Studio Preset, optional 3D handoff, and package target safety"

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
            preset = active_preset(settings)
            snapshot_context = nullcontext(preset)
            if str(getattr(settings, "studio_preset_mode", "MANUAL")).upper() == "CUSTOM":
                raw_path = str(getattr(settings, "studio_preset_path", "") or "").strip()
                resolved_path = Path(bpy.path.abspath(raw_path)).expanduser().resolve()
                snapshot_context = use_preset_file_snapshot(resolved_path, preset)
        except (OSError, RuntimeError, ValueError) as exc:
            self.report({"ERROR"}, tr(language, "package_build_failed", detail=str(exc)))
            return {"CANCELLED"}

        try:
            with snapshot_context:
                # The custom preset snapshot stays fixed for package naming,
                # compositor mapping, manifest generation, and directory setup.
                root = absolute_output_dir(settings) / effective_package_name(settings)
                passes = selected_passes(settings)

                # S10B evaluates the opt-in 3D payload before changing compositor
                # state or touching the package directory. Any unsupported animated
                # transform therefore fails closed without leaving a partial package.
                handoff_payload = None
                if handoff_3d_enabled(settings):
                    handoff_payload = build_handoff_3d(context)

                # Configure the scene before touching the package directory. If
                # the selected engine cannot expose a requested logical pass,
                # Build Package fails without a misleading empty handoff package.
                configure_render_outputs(context, root)

                manifest = build_manifest(context, root)
                if handoff_payload is not None:
                    manifest["handoff_3d"] = handoff_payload
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

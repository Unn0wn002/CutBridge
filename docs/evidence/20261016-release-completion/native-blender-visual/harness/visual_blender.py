"""Prepare the actual CutBridge sidebar for trusted visual inspection in Sandbox.

No visual PASS is produced. Native screenshots and actual RNA/UI-region state are
retained for independent inspection. No installation dialog, button workflow,
render, update request, AE or S14B acceptance is claimed.
"""

import hashlib
import importlib
import json
import os
import re
import sys
import time
import traceback
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import bpy


OUT = Path(r"C:\Evidence\verification-output\native-blender-visual")
COMMAND = OUT / "phase.json"
REVIEW = Path(r"C:\Review\candidate.json")
ZIP = Path(os.environ.get("CUTBRIDGE_BLENDER_ZIP", r"C:\Inputs\CutBridge-Blender-v0.2.5.zip"))
EXTENSION = "bl_ext.cutbridge_candidate.cutbridge"
PHASES = {"EN", "JA", "NARROW_EN", "NARROW_JA", "NARROW_API_EN", "NARROW_API_JA",
          "HELP_CAMERA_EN", "HELP_CAMERA_JA", "CAPTURE", "QUIT"}
REPORT = {"status": "INITIALIZING", "candidate_sha": None, "pid": os.getpid(),
          "host": bpy.app.version_string, "host_build_hash": bpy.app.build_hash.decode("ascii", "replace"),
          "background": bpy.app.background, "visual_result": "NOT_EXECUTED — independent screenshot inspection required",
          "install_dialog": "NOT_EXECUTED", "direct_validate_build_buttons": "NOT_EXECUTED",
          "manual_update": "NOT_EXECUTED", "ae": "NOT_EXECUTED", "s14b": "NOT_EXECUTED",
          "phases": [], "notes": []}
STATE = {"area": None, "last_sequence": -1, "pending": None, "capture_due": None,
         "started": time.monotonic(), "quit_requested": False, "narrow_area": None}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_report():
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT["updated_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "ready.json").write_text(json.dumps(REPORT, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def window_area():
    windows = list(bpy.context.window_manager.windows)
    assert windows, "No native Blender window"
    window = windows[0]
    areas = list(window.screen.areas)
    if STATE["area"] is not None:
        chosen = next((area for area in areas if area.as_pointer() == STATE["area"]), None)
        if chosen is not None and chosen.type == "VIEW_3D":
            return window, chosen
    views = [area for area in areas if area.type == "VIEW_3D"]
    chosen = max(views or areas, key=lambda area: area.width * area.height)
    chosen.type = "VIEW_3D"
    STATE["area"] = chosen.as_pointer()
    return window, chosen


def ui_state():
    window, area = window_area()
    region = next((item for item in area.regions if item.type == "UI"), None)
    settings = bpy.context.scene.cutbridge
    return {"phase": REPORT.get("phase"), "language": settings.language,
            "identifiers": {name: getattr(settings, name) for name in ("project", "episode", "scene_id", "cut", "take", "version")},
            "area_type": area.type, "area_width": area.width, "area_height": area.height,
            "sidebar_shown": area.spaces.active.show_region_ui,
            "sidebar_width": region.width if region else None,
            "active_panel_category": getattr(region, "active_panel_category", None) if region else None,
            "handoff_3d_enabled": settings.handoff_3d_enabled,
            "narrow_target_met": bool(region and region.width > 0 and region.width <= 320),
            "scope": "Actual RNA and region measurements; readability/clipping/claims require image inspection"}


def show_sidebar():
    window, area = window_area()
    area.spaces.active.show_region_ui = True
    area.tag_redraw()
    region = next((item for item in area.regions if item.type == "UI"), None)
    if not region or region.width <= 1:
        return False
    try:
        # Categories populate after drawing; retry on later GUI timer ticks.
        region.active_panel_category = "CutBridge"
    except (AttributeError, TypeError, ValueError, RuntimeError) as exc:
        REPORT["last_category_selection_error"] = str(exc)
        return False
    area.tag_redraw()
    return region.active_panel_category == "CutBridge"


def narrow_area_api():
    window, area = window_area()
    if STATE["narrow_area"] is not None:
        narrow = next((item for item in window.screen.areas if item.as_pointer() == STATE["narrow_area"]), None)
        if narrow is not None:
            STATE["area"] = narrow.as_pointer()
            return
    target = 320
    if area.width > 650:
        region = next((item for item in area.regions if item.type == "WINDOW"), None)
        factor = max(0.1, min(0.45, target / area.width))
        with bpy.context.temp_override(window=window, area=area, region=region):
            result = bpy.ops.screen.area_split(direction="VERTICAL", factor=factor)
        assert result == {"FINISHED"}, f"Native area split did not finish: {result}"
        views = [item for item in window.screen.areas if item.type == "VIEW_3D"]
        narrow = min(views, key=lambda item: item.width)
    else:
        narrow = area
    STATE["area"] = STATE["narrow_area"] = narrow.as_pointer()
    REPORT["notes"].append("Narrow API phase uses an actual native VIEW_3D area split; inspect measured sidebar width and screenshot")


def capture(sequence, phase):
    window, area = window_area()
    state = ui_state()
    path = OUT / f"{sequence:03d}-{phase.lower()}.png"
    try:
        with bpy.context.temp_override(window=window, area=area):
            result = bpy.ops.screen.screenshot(filepath=str(path), check_existing=False, hide_props_region=False)
        assert result == {"FINISHED"} and path.is_file() and path.stat().st_size > 0, f"Native screenshot failed: {result}"
        record = {"sequence": sequence, "phase": phase, "utc": datetime.now(timezone.utc).isoformat(),
                  "state": state, "native_screenshot": {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)},
                  "visual_result": "NOT_EXECUTED — trusted observer must inspect this actual screenshot"}
    except Exception:
        record = {"sequence": sequence, "phase": phase, "state": state, "screenshot_error": traceback.format_exc(),
                  "visual_result": "INSUFFICIENT EVIDENCE — capture failed"}
    REPORT["phases"].append(record)
    REPORT["current_state"] = state
    REPORT["status"] = "READY_FOR_INDEPENDENT_INSPECTION"
    save_report()


def request_quit(reason):
    if STATE["quit_requested"]:
        return
    STATE["quit_requested"] = True
    REPORT["status"] = "NORMAL_QUIT_REQUESTED"
    REPORT["quit_reason"] = reason
    REPORT["actual_exit"] = "Launcher must retain actual process exit; request is not exit evidence"
    save_report()
    bpy.app.timers.register(quit_normally, first_interval=2.0)


def quit_normally():
    REPORT["quit_requested_utc"] = datetime.now(timezone.utc).isoformat()
    save_report()
    bpy.ops.wm.quit_blender()
    return None


def apply_phase(command):
    sequence, phase = command.get("sequence"), command.get("phase")
    assert type(sequence) is int and sequence >= 0 and phase in PHASES, "Invalid control command; expected integer sequence and whitelisted phase"
    STATE["last_sequence"] = sequence
    if phase == "QUIT":
        request_quit("trusted controller QUIT phase")
        return
    if phase != "CAPTURE":
        bpy.context.scene.cutbridge.language = "JA" if phase.endswith("JA") or phase == "JA" else "EN"
        if phase.startswith("NARROW_API_"):
            narrow_area_api()
        REPORT["phase"] = phase
    REPORT["status"] = "REDRAW_PENDING"
    STATE["pending"] = {"sequence": sequence, "phase": phase, "requested": time.monotonic(),
                        "help": phase.startswith("HELP_CAMERA_")}
    STATE["capture_due"] = None
    show_sidebar()
    save_report()


def tick():
    if STATE["quit_requested"]:
        return None
    try:
        if time.monotonic() - STATE["started"] >= REPORT["timeout_seconds"]:
            request_quit("visual observation timeout; no automatic visual PASS")
            return None
        if COMMAND.is_file():
            if COMMAND.stat().st_size > 4096:
                raise ValueError("Control file exceeds 4096 bytes")
            try:
                command = json.loads(COMMAND.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                return 0.5  # Trusted host may be atomically replacing its command.
            if type(command.get("sequence")) is int and command["sequence"] > STATE["last_sequence"]:
                apply_phase(command)
        pending = STATE["pending"]
        if pending:
            selected = show_sidebar()
            if not selected and time.monotonic() - pending["requested"] < 12:
                return 0.5
            if not selected:
                REPORT["notes"].append("API could not select CutBridge category; trusted observer may click native tab before CAPTURE")
            if STATE["capture_due"] is None:
                if pending["help"]:
                    window, area = window_area()
                    with bpy.context.temp_override(window=window, area=area):
                        popup_result = bpy.ops.cutbridge.context_help("INVOKE_DEFAULT", topic="camera")
                    REPORT["help_popup_operator_result"] = sorted(popup_result)
                STATE["capture_due"] = time.monotonic() + 2
            elif time.monotonic() >= STATE["capture_due"]:
                capture(pending["sequence"], pending["phase"])
                STATE["pending"] = STATE["capture_due"] = None
        return 0.5
    except Exception:
        REPORT["status"] = "INSUFFICIENT EVIDENCE"
        REPORT["error"] = traceback.format_exc()
        save_report()
        request_quit("visual harness error; inspect retained traceback")
        return None


def initialize():
    try:
        assert not bpy.app.background and sys.flags.optimize == 0, "Native GUI and enabled assertions required"
        assert REVIEW.is_file() and ZIP.is_file(), "Missing exact candidate identity or ZIP"
        review = json.loads(REVIEW.read_text(encoding="utf-8-sig"))
        candidate_sha = review.get("sha") or review.get("candidate_sha")
        assert isinstance(candidate_sha, str) and re.fullmatch(r"[a-f0-9]{40}", candidate_sha), review
        REPORT["candidate_sha"] = candidate_sha
        approved = Path(r"C:\Evidence\verification-output").resolve()
        paths = {name: os.environ.get(name) for name in ("PYTHONPYCACHEPREFIX", "TEMP", "TMP", "TMPDIR",
                                                        "BLENDER_USER_CONFIG", "BLENDER_USER_DATAFILES", "BLENDER_USER_EXTENSIONS")}
        for name, value in paths.items():
            assert value and Path(value).resolve().is_relative_to(approved), f"Unapproved writable {name}: {value!r}"
        REPORT["writable_environment_paths"] = paths
        assert EXTENSION in bpy.context.preferences.addons, "Exact official CLI-installed extension not enabled"
        cutbridge = importlib.import_module(EXTENSION)
        update_ops = importlib.import_module(EXTENSION + ".update_ops")
        installed = Path(cutbridge.__file__).parent
        installed_hashes = {}
        with zipfile.ZipFile(ZIP) as archive:
            assert archive.testzip() is None and len(archive.namelist()) == len(set(archive.namelist())), "Bad or duplicate ZIP entries"
            for name in archive.namelist():
                relative = PurePosixPath(name)
                assert not relative.is_absolute() and ".." not in relative.parts and "\\" not in name, f"Unsafe ZIP entry: {name}"
                if name.endswith("/"):
                    continue
                path = installed.joinpath(*relative.parts)
                expected = hashlib.sha256(archive.read(name)).hexdigest()
                assert path.is_file() and not path.is_symlink() and sha256(path) == expected, f"Installed bytes differ from exact ZIP: {name}"
                installed_hashes[name] = expected
        REPORT["inputs"] = {"candidate_json_sha256": sha256(REVIEW), "blender_zip_sha256": sha256(ZIP),
                            "harness_sha256": sha256(Path(__file__)), "installed_files": installed_hashes}
        assert not bpy.app.timers.is_registered(update_ops._startup_update_check), "Unexpected startup update timer"
        assert "handoff_3d_enabled" not in (installed / "ui.py").read_text(encoding="utf-8"), "Normal panel unexpectedly exposes advanced 3D opt-in"
        settings = bpy.context.scene.cutbridge
        settings.project, settings.episode, settings.scene_id = "Visual025", "EP01", "SC010"
        settings.cut, settings.take, settings.version = "C001", "T01", 1
        settings.output_dir = str(OUT / "packages")
        settings.last_package_path = ""
        settings.studio_preset_mode = "MANUAL"
        settings.pass_beauty = True
        settings.pass_line = settings.pass_shadow = settings.pass_depth = False
        settings.handoff_3d_enabled = False
        scene = bpy.context.scene
        scene.render.filepath = str(OUT / "tmp" / "main-render-")
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 320, 180, 100
        scene.render.fps, scene.render.fps_base = 24, 1.0
        scene.frame_start, scene.frame_end = 1, 3
        (OUT / "tmp").mkdir(parents=True, exist_ok=True)
        assert bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "visual-fixture.blend")) == {"FINISHED"}, "Could not save disposable visual fixture"
        REPORT["timeout_seconds"] = max(60, min(900, int(os.environ.get("CUTBRIDGE_VISUAL_TIMEOUT_SECONDS", "180"))))
        REPORT["advanced_3d_control"] = "Not exposed in source panel; opt-in disabled; independent screenshot inspection still required"
        REPORT["phase_control_file"] = str(COMMAND)
        REPORT["notes"].append("EN/JA use scene.cutbridge.language. NARROW phases measure actual width; manual resize may be required. NARROW_API optionally creates a real narrow VIEW_3D area.")
        apply_phase({"sequence": 0, "phase": "EN"})
        bpy.app.timers.register(tick, first_interval=0.5)
    except Exception:
        REPORT["status"] = "INSUFFICIENT EVIDENCE"
        REPORT["error"] = traceback.format_exc()
        save_report()
        request_quit("initialization failed")
    return None


save_report()
bpy.app.timers.register(initialize, first_interval=2.0)

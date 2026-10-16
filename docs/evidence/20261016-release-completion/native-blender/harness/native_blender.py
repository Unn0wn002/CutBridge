"""Prepared native Blender campaign; execute only in the approved offline Sandbox.

The launcher installs the exact ZIP through Blender's official extension manager,
sets isolated config/data/extensions/bytecode/temp paths, and retains policy/logs.
This script exercises native APIs/operators inside the real GUI event loop. It
does not inspect the UI, establish its own isolation, or execute After Effects.
"""

import hashlib
import importlib
import json
import math
import os
import re
import sys
import traceback
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import bpy
from mathutils import Vector


OUT = Path(r"C:\Evidence\verification-output\native-blender")
PACKAGES = OUT / "packages"
FIXTURES = OUT / "fixtures"
REVIEW = Path(r"C:\Review\candidate.json")
ZIP = Path(os.environ.get("CUTBRIDGE_BLENDER_ZIP", r"C:\Inputs\CutBridge-Blender-v0.2.5.zip"))
EXTENSION = "bl_ext.cutbridge_candidate.cutbridge"
FRAMES = (1, 2, 3)
EXPECTED_PASSES = {"BEAUTY": "PNG", "LINE": "PNG", "SHADOW": "PNG", "DEPTH": "OPEN_EXR"}
REPORT = {
    "candidate_sha": None,
    "host": bpy.app.version_string,
    "host_build_hash": bpy.app.build_hash.decode("ascii", "replace"),
    "host_binary": bpy.app.binary_path,
    "python": sys.version,
    "background": bpy.app.background,
    "method": "Native scripted API/operators invoked by the Blender GUI timer event loop",
    "isolation_evidence": "Launcher policy/runtime records required separately; script does not establish isolation",
    "gui_visual_inspection": "NOT_EXECUTED",
    "install_dialog_inspection": "NOT_EXECUTED",
    "direct_panel_button_clicks": "NOT_EXECUTED",
    "fresh_process_reopen": "NOT_EXECUTED; this script covers same-process open_mainfile only",
    "ae_execution": "NOT_EXECUTED",
    "overall_scope_result": "RUNNING",
    "stage": "prerequisites",
    "results": {},
    "packages": [],
    "inputs": {},
}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


def write_report():
    REPORT["report_time_utc"] = datetime.now(timezone.utc).isoformat()
    write_json("native-blender.json", REPORT)


def stage(name):
    REPORT["stage"] = name
    write_report()


def passed(name, evidence=None):
    REPORT["results"][name] = {"result": "PASS", "evidence": evidence}
    write_report()


def inventory(root):
    result = {}
    for path in sorted(Path(root).rglob("*")):
        assert not path.is_symlink(), f"Unexpected symlink in campaign output: {path}"
        if path.is_file():
            result[path.relative_to(root).as_posix()] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    return result


def finite_values(value, path="payload"):
    if isinstance(value, dict):
        for name, child in value.items():
            finite_values(child, f"{path}.{name}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            finite_values(child, f"{path}[{index}]")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        assert math.isfinite(value), f"Nonfinite value at {path}: {value!r}"


def number(value, label):
    assert type(value) in (int, float) and math.isfinite(value), f"{label}: expected finite number, got {value!r}"


def close(actual, expected, label, tolerance=1e-4):
    number(actual, label)
    assert math.isclose(actual, expected, rel_tol=1e-6, abs_tol=tolerance), f"{label}: expected {expected!r}, actual {actual!r}"


def vector_close(actual, expected, label):
    assert isinstance(actual, list) and len(actual) == 3, f"{label}: expected three-element list, actual {actual!r}"
    for index, value in enumerate(actual):
        close(value, expected[index], f"{label}[{index}]")


def mapped_direction(value):
    # Independent oracle: native evaluated matrix plus the documented axis map.
    return [float(value[0]), -float(value[2]), float(value[1])]


def host_sample(scene, obj, frame):
    scene.frame_set(frame, subframe=0.0)
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    matrix = evaluated.matrix_world.copy()
    axes = [matrix.to_3x3() @ Vector(axis) for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    lengths = [float(axis.length) for axis in axes]
    basis = {name: mapped_direction(axis / axis.length) for name, axis in zip(("x", "y", "z"), axes)}
    pos = matrix.translation
    return {
        "position": [160.0 + float(pos.x) * 100.0, 90.0 - float(pos.z) * 100.0, float(pos.y) * 100.0],
        "basis": basis,
        "scale": lengths,
        "evaluated_world_position": [float(value) for value in pos],
    }


def inspect_handoff(manifest, scene, camera, marker, version):
    payload = manifest.get("handoff_3d")
    assert isinstance(payload, dict), "handoff_3d must be an object, not just truthy"
    finite_values(payload)
    assert payload.get("schema") == "cutbridge-handoff-3d", payload
    assert type(payload.get("schema_version")) is int and payload["schema_version"] == 1, payload
    assert payload.get("space") == {
        "coordinate_system": "after-effects-composition", "axis_map": "blender_xyz_to_ae_x_negz_y",
        "origin": "composition-center", "position_units": "pixels", "pixels_per_blender_unit": 100.0,
    }, payload.get("space")
    assert payload.get("sampling") == {"mode": "baked-per-frame", "frame_start": 1, "frame_end": 3, "frame_step": 1}, payload.get("sampling")
    cam_data = payload.get("camera")
    nulls = payload.get("nulls")
    assert isinstance(cam_data, dict) and cam_data.get("name") == camera.name and cam_data.get("type") == "PERSP", cam_data
    assert isinstance(nulls, list) and len(nulls) == 1, f"Expected only one explicitly marked Empty: {nulls!r}"
    assert isinstance(nulls[0], dict) and nulls[0].get("name") == marker.name and nulls[0].get("source_type") == "EMPTY", nulls
    expected = {}
    original_frame, original_subframe = scene.frame_current, scene.frame_subframe
    try:
        for data, obj, kind in ((cam_data, camera, "camera"), (nulls[0], marker, "null")):
            samples = data.get("samples")
            assert isinstance(samples, list) and len(samples) == 3, f"{kind}: expected 3 samples, actual {samples!r}"
            expected[kind] = []
            for frame, sample in zip(FRAMES, samples):
                assert isinstance(sample, dict), f"{kind}: sample must be object"
                assert type(sample.get("frame")) is int and sample["frame"] == frame, f"{kind}: wrong frame {sample!r}"
                close(sample.get("time"), (frame - 1) / 24.0, f"{kind}.time", tolerance=1e-8)
                oracle = host_sample(scene, obj, frame)
                known_position = [7 + version * 0.1 + frame * 0.05, -7.0, 5.0] if kind == "camera" else [version * 0.25 + frame * 0.15, 0.0, frame * 0.05]
                vector_close(oracle["evaluated_world_position"], known_position, f"{kind}.known-fixture-position")
                vector_close(sample.get("position"), oracle["position"], f"{kind}.position")
                vector_close(sample.get("scale"), oracle["scale"], f"{kind}.scale")
                assert isinstance(sample.get("basis"), dict), f"{kind}: missing basis"
                for axis in ("x", "y", "z"):
                    vector_close(sample["basis"].get(axis), oracle["basis"][axis], f"{kind}.basis.{axis}")
                oracle.update(frame=frame, time=(frame - 1) / 24.0)
                if kind == "camera":
                    fov = float(camera.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.angle_x)
                    zoom = 320.0 / (2.0 * math.tan(fov / 2.0))
                    vector_close(sample.get("forward"), [-value for value in oracle["basis"]["z"]], "camera.forward")
                    vector_close(sample.get("up"), oracle["basis"]["y"], "camera.up")
                    close(sample.get("horizontal_fov_radians"), fov, "camera.horizontal_fov_radians")
                    close(sample.get("ae_zoom"), zoom, "camera.ae_zoom")
                    oracle.update(horizontal_fov_radians=fov, ae_zoom=zoom)
                expected[kind].append(oracle)
    finally:
        scene.frame_set(original_frame, subframe=original_subframe)
    record = {"version": version, "expected_from_native_evaluated_host": expected, "actual": payload,
              "scope": "Producer serialization only; does not establish AE roll/rotation/projection behavior"}
    write_json(f"handoff-V{version:03d}-comparison.json", record)
    return sha256(OUT / f"handoff-V{version:03d}-comparison.json")


def artist_state(tree):
    rgb = tree.nodes.get("ArtistRGB025")
    reroute = tree.nodes.get("ArtistReroute025")
    assert rgb is not None and reroute is not None, "Artist sentinel node disappeared"
    return {"tree": tree.name,
            "rgb": {"name": rgb.name, "label": rgb.label, "location": list(rgb.location), "mute": rgb.mute,
                    "value": list(rgb.outputs[0].default_value), "note": rgb.get("studio_note")},
            "reroute": {"name": reroute.name, "location": list(reroute.location)},
            "links": sorted((link.from_node.name, link.from_socket.name, link.to_node.name, link.to_socket.name)
                            for link in tree.links if not link.from_node.name.startswith("CUTBRIDGE_")
                            and not link.to_node.name.startswith("CUTBRIDGE_"))}


def mapping_state(scene, layer):
    tree = scene.compositing_node_group
    nodes = []
    for node in tree.nodes:
        item = {"name": node.name, "type": node.bl_idname, "label": node.label,
                "location": list(node.location), "mute": node.mute, "hide": node.hide}
        if hasattr(node, "file_output_items"):
            item.update(directory=node.directory, file_name=node.file_name, media_type=node.format.media_type,
                        items=[{"name": entry.name, "override_node_format": entry.override_node_format,
                                "file_format": entry.format.file_format, "media_type": entry.format.media_type}
                               for entry in node.file_output_items])
        nodes.append(item)
    return {"tree": tree.name, "nodes": sorted(nodes, key=lambda item: item["name"]),
            "links": sorted((link.from_node.name, link.from_socket.name, link.to_node.name, link.to_socket.name) for link in tree.links),
            "flags": {"use_compositing": scene.render.use_compositing, "render_use_freestyle": scene.render.use_freestyle,
                      "layer_use_freestyle": layer.use_freestyle, "use_pass_shadow": layer.use_pass_shadow,
                      "use_pass_z": layer.use_pass_z}, "render_filepath": scene.render.filepath,
            "artist": artist_state(tree)}


def inspect_render_outputs(root, manifest):
    assert {entry["name"]: entry["image_format"] for entry in manifest["passes"]} == EXPECTED_PASSES, manifest["passes"]
    expected_all = set()
    for entry in manifest["passes"]:
        folder = root / entry["path"]
        assert folder.resolve().is_relative_to(root.resolve()), f"Pass folder escapes package: {folder}"
        pattern = entry["sequence_pattern"]
        assert len(re.findall(r"#+", pattern)) == 1, f"Unexpected sequence pattern: {pattern}"
        expected_names = {re.sub(r"#+", lambda match: str(frame).zfill(len(match.group())), pattern) for frame in FRAMES}
        actual_names = {path.name for path in folder.iterdir() if path.is_file()}
        assert actual_names == expected_names, f"{entry['name']}: expected {expected_names!r}, actual {actual_names!r}"
        for name in sorted(expected_names):
            path = folder / name
            assert path.stat().st_size > 0, f"Empty render: {path}"
            with path.open("rb") as stream:
                header = stream.read(8)
            if entry["image_format"] == "PNG":
                assert header == b"\x89PNG\r\n\x1a\n", f"Not PNG bytes: {path}"
            else:
                assert header[:4] == b"\x76\x2f\x31\x01", f"Not OpenEXR bytes: {path}"
            expected_all.add(path.relative_to(root).as_posix())
    actual_all = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.suffix.lower() in (".png", ".exr")}
    assert actual_all == expected_all and len(actual_all) == 12, f"Expected exactly 12 four-pass outputs: {actual_all!r}"
    return sorted(expected_all)


def blocked_build():
    try:
        result = bpy.ops.cutbridge.build_package()
    except RuntimeError as exc:
        return {"result": "RuntimeError from cancelled operator", "message": str(exc)}
    assert result == {"CANCELLED"}, f"Unsafe Build unexpectedly returned {result!r}"
    return {"result": "CANCELLED"}


def quit_normally():
    REPORT["normal_quit_requested_utc"] = datetime.now(timezone.utc).isoformat()
    REPORT["normal_exit_observed"] = "Launcher must record actual exit code; request is not exit evidence"
    write_report()
    bpy.ops.wm.quit_blender()
    return None


def run():
    try:
        assert not bpy.app.background and sys.flags.optimize == 0, "Native GUI event loop and enabled assertions required"
        assert REVIEW.is_file() and ZIP.is_file(), f"Missing candidate identity or ZIP: {REVIEW}, {ZIP}"
        review = json.loads(REVIEW.read_text(encoding="utf-8-sig"))
        candidate_sha = review.get("sha") or review.get("candidate_sha")
        assert isinstance(candidate_sha, str) and re.fullmatch(r"[a-f0-9]{40}", candidate_sha), review
        REPORT["candidate_sha"] = candidate_sha
        approved_writable = Path(r"C:\Evidence\verification-output").resolve()
        paths = {name: os.environ.get(name) for name in ("PYTHONPYCACHEPREFIX", "TEMP", "TMP", "TMPDIR",
                                                        "BLENDER_USER_CONFIG", "BLENDER_USER_DATAFILES", "BLENDER_USER_EXTENSIONS")}
        for name, value in paths.items():
            assert value and Path(value).resolve().is_relative_to(approved_writable), f"{name} must target approved verification-output: {value!r}"
        REPORT["writable_environment_paths"] = paths
        REPORT["python_pycache_prefix"] = sys.pycache_prefix
        REPORT["inputs"] = {"candidate_json": {"path": str(REVIEW), "sha256": sha256(REVIEW)},
                            "blender_zip": {"path": str(ZIP), "sha256": sha256(ZIP)},
                            "harness": {"path": __file__, "sha256": sha256(Path(__file__))},
                            "host_binary_sha256": sha256(Path(bpy.app.binary_path))}
        assert EXTENSION in bpy.context.preferences.addons, f"Official extension installation/enablement unavailable: {EXTENSION}"
        cutbridge = importlib.import_module(EXTENSION)
        operators = importlib.import_module(EXTENSION + ".operators")
        core = importlib.import_module(EXTENSION + ".core")
        update_ops = importlib.import_module(EXTENSION + ".update_ops")
        installed = Path(cutbridge.__file__).parent
        installed_inputs = {}
        with zipfile.ZipFile(ZIP) as archive:
            assert archive.testzip() is None, "ZIP CRC failure"
            names = archive.namelist()
            assert len(names) == len(set(names)), "Duplicate ZIP paths"
            for name in names:
                relative = PurePosixPath(name)
                assert not relative.is_absolute() and ".." not in relative.parts and "\\" not in name, f"Unsafe ZIP entry {name!r}"
                if name.endswith("/"):
                    continue
                path = installed.joinpath(*relative.parts)
                assert path.is_file() and not path.is_symlink(), f"Installed file absent or linked: {path}"
                expected = hashlib.sha256(archive.read(name)).hexdigest()
                assert sha256(path) == expected, f"Installed bytes differ from exact ZIP: {name}"
                installed_inputs[name] = expected
        REPORT["inputs"]["installed_files"] = installed_inputs
        assert cutbridge.version.__version__ == "0.2.5", cutbridge.version.__version__
        assert hasattr(bpy.types.Scene, "cutbridge"), "Scene settings not registered"
        panel = importlib.import_module(EXTENSION + ".ui").CUTBRIDGE_PT_MainPanel
        assert "bl_rna" in panel.__dict__, "Panel RNA registration absent"
        assert not bpy.app.timers.is_registered(update_ops._startup_update_check), "Unexpected startup update timer"
        passed("exact_zip_install_enable_and_panel_registration", {"installed_root": str(installed), "version": "0.2.5", "scope": "CLI install/enable persistence and RNA, not install-dialog or visual UI inspection"})
        passed("startup_scheduler_disabled")

        stage("synthetic_fixture")
        PACKAGES.mkdir(parents=True, exist_ok=True)
        FIXTURES.mkdir(parents=True, exist_ok=True)
        (OUT / "main-render").mkdir(exist_ok=True)
        scene = bpy.context.scene
        assert hasattr(scene, "compositing_node_group"), "This campaign requires Blender's modern compositor API"
        scene.render.filepath = str(OUT / "main-render" / "frame-")
        scene.render.engine = "BLENDER_EEVEE"
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 320, 180, 100
        scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1.0
        scene.render.fps, scene.render.fps_base = 24, 1.0
        scene.frame_start, scene.frame_end = 1, 3
        if hasattr(scene.render, "compositor_device"):
            scene.render.compositor_device = "CPU"
        camera = scene.camera
        assert camera is not None, "Fresh default Blender fixture must contain a camera"
        camera.name = "Native025Camera"
        camera.data.type = "PERSP"
        camera.data.shift_x = camera.data.shift_y = 0.0
        camera.location = (7, -7, 5)
        camera.rotation_euler = (Vector((0, 0, 0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
        cube = bpy.data.objects.get("Cube")
        assert cube is not None, "Fresh default Blender fixture must contain Cube"
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
        marker = bpy.context.object
        marker.name = "Native025Null"
        marker["cutbridge_handoff_3d"] = True
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=(1, 2, 3))
        bpy.context.object.name = "Native025Unmarked"
        scene.render.use_freestyle = True
        layer = bpy.context.view_layer
        layer.use_freestyle = layer.freestyle_settings.as_render_pass = True
        layer.use_pass_shadow = layer.use_pass_z = True
        tree = bpy.data.node_groups.new("ArtistCompositor025", "CompositorNodeTree")
        rgb = tree.nodes.new("CompositorNodeRGB")
        rgb.name, rgb.label = "ArtistRGB025", "Artist node must survive"
        rgb.location = (-500, 400)
        rgb.outputs[0].default_value = (0.125, 0.25, 0.5, 1.0)
        rgb["studio_note"] = "Artist sentinel / preserved note"
        reroute = tree.nodes.new("NodeReroute")
        reroute.name, reroute.location = "ArtistReroute025", (-200, 400)
        tree.links.new(rgb.outputs[0], reroute.inputs[0])
        scene.compositing_node_group = tree
        artist_before = artist_state(tree)
        write_json("artist-before.json", artist_before)
        settings = scene.cutbridge
        settings.language = "EN"
        settings.project, settings.episode, settings.scene_id = "Native025", "EP01", "SC010"
        settings.cut, settings.take, settings.output_dir = "C001", "T01", str(PACKAGES)
        settings.studio_preset_mode = "MANUAL"
        settings.pass_beauty = settings.pass_line = settings.pass_shadow = settings.pass_depth = True
        settings.per_pass_formats_enabled = True
        settings.format_beauty = settings.format_line = settings.format_shadow = "PNG"
        settings.format_depth = "OPEN_EXR"
        settings.handoff_3d_enabled = True
        settings.handoff_3d_pixels_per_blender_unit = 100.0
        write_json("fixture-contract.json", {"frames": FRAMES, "fps": 24, "resolution": [320, 180], "passes": EXPECTED_PASSES,
                   "camera": camera.name, "marked_empty": marker.name, "unmarked_empty": "Native025Unmarked",
                   "scale": 100.0, "versions": [1, 2, 3], "source": "Synthetic scene generated by retained harness"})

        for version in (1, 2, 3):
            stage(f"V{version:03d}_build_render_and_safety")
            settings.version = version
            for frame in FRAMES:
                cube.location.x = version * 0.15 + frame * 0.1
                cube.keyframe_insert(data_path="location", frame=frame)
                marker.location = (version * 0.25 + frame * 0.15, 0.0, frame * 0.05)
                marker.scale = (1.0 + version * 0.1, 1.0 + frame * 0.05, 1.0)
                marker.rotation_euler = (0.0, 0.0, frame * 0.1)
                for data_path in ("location", "scale", "rotation_euler"):
                    marker.keyframe_insert(data_path=data_path, frame=frame)
                camera.location = (7 + version * 0.1 + frame * 0.05, -7, 5)
                camera.keyframe_insert(data_path="location", frame=frame)
            scene.frame_set(2, subframe=0.25)
            fixture = FIXTURES / f"fixture-V{version:03d}.blend"
            assert bpy.ops.wm.save_as_mainfile(filepath=str(fixture)) == {"FINISHED"}, "Fixture save failed"
            issues = operators._all_validation_issues(bpy.context, for_build=True)
            assert not [issue for issue in issues if issue["level"] == "ERROR"], issues
            warning = next(issue for issue in issues if issue["code"] == "HANDOFF_PRODUCER_ONLY")
            assert "Camera Position/Point of Interest/Zoom and Null Position/Scale only" in warning["message"], warning
            assert "Camera roll and Empty rotation are not reconstructed" in warning["fix"], warning
            assert "QC does not inspect these transforms" in warning["fix"], warning
            assert bpy.ops.cutbridge.validate() == {"FINISHED"}, "Validate operator failed"
            assert bpy.ops.cutbridge.build_package() == {"FINISHED"}, "Build operator failed"
            assert scene.frame_current == 2 and math.isclose(scene.frame_subframe, 0.25), "Build did not restore original frame/subframe"
            root = Path(settings.last_package_path)
            assert root.resolve().is_relative_to(PACKAGES.resolve()), f"Package escaped approved output: {root}"
            manifest = json.loads((root / "cutbridge.json").read_text(encoding="utf-8"))
            assert manifest["version"] == version and manifest["frames"] == {"start": 1, "end": 3, "count": 3}, manifest
            comparison_hash = inspect_handoff(manifest, scene, camera, marker, version)
            assert artist_state(tree) == artist_before, "Build changed artist nodes/links/values"
            assert bpy.ops.render.render(animation=True) == {"FINISHED"}, "Native animation render failed"
            rendered = inspect_render_outputs(root, manifest)
            assert artist_state(tree) == artist_before, "Render changed artist sentinel state"
            before = inventory(root)
            lifecycle = operators._all_validation_issues(bpy.context)
            assert any(issue["code"] == "PACKAGE_RENDER_READY" and issue["level"] == "INFO" for issue in lifecycle), lifecycle
            build_issues = operators._all_validation_issues(bpy.context, for_build=True)
            assert any(issue["code"] == "PACKAGE_EXISTS" and issue["level"] == "ERROR" for issue in build_issues), build_issues
            overwrite = blocked_build()
            assert inventory(root) == before, "Blocked overwrite changed package files"
            state_before = mapping_state(scene, layer)
            scene.frame_end = 4
            try:
                mismatch = operators._all_validation_issues(bpy.context)
                assert any(issue["code"] == "PACKAGE_STATE_MISMATCH" and issue["level"] == "ERROR" for issue in mismatch), mismatch
                mismatch_build = blocked_build()
                assert inventory(root) == before, "Contract mismatch changed existing package files"
                assert mapping_state(scene, layer) == state_before, "Blocked mismatch changed compositor/render flags"
            finally:
                scene.frame_end = 3
            recovery = operators._all_validation_issues(bpy.context)
            assert not [issue for issue in recovery if issue["level"] == "ERROR"], recovery
            assert artist_state(tree) == artist_before, "Blocked operations changed artist state"
            package_record = {"version": version, "root": str(root), "manifest_sha256": sha256(root / "cutbridge.json"),
                              "fixture_sha256": sha256(fixture), "handoff_comparison_sha256": comparison_hash,
                              "rendered": rendered, "files": before, "overwrite": overwrite, "mismatch_build": mismatch_build}
            REPORT["packages"].append(package_record)
            write_json(f"package-V{version:03d}-inventory.json", package_record)
            passed(f"V{version:03d}_native_build_render_handoff_and_safety", {"outputs": len(rendered), "manifest_sha256": package_record["manifest_sha256"]})

        stage("fault_injected_mapping_rollback")
        before = mapping_state(scene, layer)
        write_json("rollback-before.json", before)
        original_socket = core._find_output_socket
        core._find_output_socket = lambda node, pass_name: None if pass_name == "LINE" else original_socket(node, pass_name)
        failed = False
        try:
            core.configure_render_outputs(bpy.context, OUT / "failed-mapping")
        except RuntimeError as exc:
            assert "LINE mapping is unavailable" in str(exc), f"Unexpected injected failure: {exc}"
            REPORT["mapping_fault_message"] = str(exc)
            failed = True
        finally:
            core._find_output_socket = original_socket
        assert failed, "Injected missing LINE socket unexpectedly succeeded"
        after = mapping_state(scene, layer)
        write_json("rollback-after.json", after)
        assert after == before and scene.compositing_node_group is tree, "Rollback did not restore exact mapping/artist/render state"
        for package in REPORT["packages"]:
            assert inventory(Path(package["root"])) == package["files"], f"Rollback changed package V{package['version']:03d}"
        passed("native_fault_injection_mapping_rollback", {"injection": "Temporary in-memory missing LINE socket; original function restored in finally"})

        stage("locale_and_save_reopen")
        identity = (settings.project, settings.episode, settings.scene_id, settings.cut, settings.take, settings.version)
        settings.language = "JA"
        assert identity == (settings.project, settings.episode, settings.scene_id, settings.cut, settings.take, settings.version), "Locale changed cut identity"
        settings.language = "EN"
        assert identity == (settings.project, settings.episode, settings.scene_id, settings.cut, settings.take, settings.version), "Locale recovery changed identity"
        passed("locale_identity_preservation", {"scope": "RNA state only; visual JP/EN inspection NOT_EXECUTED"})
        scene.frame_set(1, subframe=0.0)
        reopen_fixture = FIXTURES / "reopen-V003.blend"
        assert bpy.ops.wm.save_as_mainfile(filepath=str(reopen_fixture)) == {"FINISHED"}, "Reopen fixture save failed"
        before_reopen = mapping_state(scene, layer)
        assert bpy.ops.wm.open_mainfile(filepath=str(reopen_fixture)) == {"FINISHED"}, "Same-process open_mainfile failed"
        scene, layer = bpy.context.scene, bpy.context.view_layer
        settings = scene.cutbridge
        assert settings.version == 3 and settings.language == "EN" and settings.output_dir == str(PACKAGES), "Saved settings changed after reopen"
        assert scene.frame_current == 1 and scene.camera.name == "Native025Camera", "Saved frame/camera changed after reopen"
        assert mapping_state(scene, layer) == before_reopen, "Saved compositor/artist/render state changed after reopen"
        assert not [issue for issue in operators._all_validation_issues(bpy.context) if issue["level"] == "ERROR"], "Reopened package lifecycle invalid"
        last_root = Path(settings.last_package_path)
        last_manifest = json.loads((last_root / "cutbridge.json").read_text(encoding="utf-8"))
        inspect_handoff(last_manifest, scene, scene.camera, bpy.data.objects["Native025Null"], 3)
        for package in REPORT["packages"]:
            assert inventory(Path(package["root"])) == package["files"], "Reopen changed package files"
        passed("same_process_save_and_reopen", {"fixture": str(reopen_fixture), "sha256": sha256(reopen_fixture), "fresh_process": "NOT_EXECUTED"})
        REPORT["fixture_files"] = inventory(FIXTURES)
        REPORT["fixture_contract_sha256"] = sha256(OUT / "fixture-contract.json")
        REPORT["overall_scope_result"] = "PASS"
        REPORT["scope_limitations"] = ["Scripted native scope only", "GUI visual/install-dialog/direct-button inspection NOT_EXECUTED",
                                       "Fresh-process reopen NOT_EXECUTED", "AE execution and S14B NOT_EXECUTED",
                                       "Launcher must independently validate isolation, input manifests and actual normal exit"]
    except AssertionError:
        REPORT["overall_scope_result"] = "INSUFFICIENT EVIDENCE" if REPORT["stage"] == "prerequisites" else "FAIL"
        REPORT["error"] = traceback.format_exc()
        REPORT["results"][REPORT["stage"]] = {"result": REPORT["overall_scope_result"], "error": REPORT["error"]}
    except Exception:
        REPORT["overall_scope_result"] = "INSUFFICIENT EVIDENCE"
        REPORT["error"] = traceback.format_exc()
        REPORT["classification_note"] = "Unexpected harness/host exception; inspect before attributing a candidate defect"
    finally:
        if FIXTURES.is_dir():
            REPORT["fixture_files"] = inventory(FIXTURES)
        write_report()
        bpy.app.timers.register(quit_normally, first_interval=2.0)
    return None


write_report()
bpy.app.timers.register(run, first_interval=2.0)

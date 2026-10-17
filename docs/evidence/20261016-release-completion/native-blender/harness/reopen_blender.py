"""Fresh-process persistence check; launcher proves sequential PIDs/exits/isolation.

Execute only in the same approved offline Sandbox, as a new Blender GUI process
after the initial process exits normally. This script does not import the initial
harness, repeat fixture generation, or claim visual UI/AE/S14B acceptance.
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


OUT = Path(r"C:\Evidence\verification-output\native-blender")
FIXTURE = OUT / "fixtures" / "reopen-V003.blend"
REVIEW = Path(r"C:\Review\candidate.json")
ZIP = Path(os.environ.get("CUTBRIDGE_BLENDER_ZIP", r"C:\Inputs\CutBridge-Blender-v0.2.5.zip"))
EXTENSION = "bl_ext.cutbridge_candidate.cutbridge"
REPORT = {"overall_scope_result": "RUNNING", "stage": "prerequisites", "pid": os.getpid(),
          "candidate_sha": None, "host": bpy.app.version_string,
          "host_build_hash": bpy.app.build_hash.decode("ascii", "replace"),
          "background": bpy.app.background, "method": "Separate GUI process opens exact prior saved native fixture",
          "fresh_process_provenance": "Launcher must retain previous normal exit, previous/new PIDs and current exit",
          "gui_visual_inspection": "NOT_EXECUTED", "ae_execution": "NOT_EXECUTED", "s14b": "NOT_EXECUTED"}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_report():
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT["report_time_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "reopen-blender.json").write_text(json.dumps(REPORT, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def canonical(value):
    return json.loads(json.dumps(value, allow_nan=False))


def artist_state(tree):
    rgb, reroute = tree.nodes.get("ArtistRGB025"), tree.nodes.get("ArtistReroute025")
    assert rgb is not None and reroute is not None, "Saved artist nodes missing"
    return {"tree": tree.name,
            "rgb": {"name": rgb.name, "label": rgb.label, "location": list(rgb.location), "mute": rgb.mute,
                    "value": list(rgb.outputs[0].default_value), "note": rgb.get("studio_note")},
            "reroute": {"name": reroute.name, "location": list(reroute.location)},
            "links": sorted((link.from_node.name, link.from_socket.name, link.to_node.name, link.to_socket.name)
                            for link in tree.links if not link.from_node.name.startswith("CUTBRIDGE_")
                            and not link.to_node.name.startswith("CUTBRIDGE_"))}


def mapping_state(scene, layer):
    tree, nodes = scene.compositing_node_group, []
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


def check_package_files(prior):
    for package in prior["packages"]:
        root = Path(package["root"])
        assert root.resolve().is_relative_to((OUT / "packages").resolve()), f"Package path outside approved output: {root}"
        current = {}
        for path in sorted(root.rglob("*")):
            assert not path.is_symlink(), f"Unexpected linked package file: {path}"
            if path.is_file():
                current[path.relative_to(root).as_posix()] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        assert current == package["files"], f"Saved package bytes/inventory changed: V{package['version']:03d}"


def quit_normally():
    REPORT["normal_quit_requested_utc"] = datetime.now(timezone.utc).isoformat()
    REPORT["normal_exit_observed"] = "Launcher must record actual exit; request alone is not exit evidence"
    write_report()
    bpy.ops.wm.quit_blender()
    return None


def run():
    try:
        assert not bpy.app.background and sys.flags.optimize == 0, "GUI event loop and enabled assertions required"
        prior_path = OUT / "native-blender.json"
        assert prior_path.is_file() and FIXTURE.is_file() and REVIEW.is_file() and ZIP.is_file(), "Required retained first-run inputs absent"
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        assert prior.get("overall_scope_result") == "PASS", "Initial scripted campaign did not pass; inspect that record before fresh-process reuse"
        review = json.loads(REVIEW.read_text(encoding="utf-8-sig"))
        candidate_sha = review.get("sha") or review.get("candidate_sha")
        assert isinstance(candidate_sha, str) and re.fullmatch(r"[a-f0-9]{40}", candidate_sha), review
        assert candidate_sha == prior["candidate_sha"], "Candidate identity changed between native processes"
        assert sha256(REVIEW) == prior["inputs"]["candidate_json"]["sha256"], "Candidate metadata bytes changed"
        assert sha256(ZIP) == prior["inputs"]["blender_zip"]["sha256"], "Candidate ZIP changed"
        assert sha256(FIXTURE) == prior["fixture_files"]["reopen-V003.blend"]["sha256"], "Exact saved fixture bytes changed"
        assert bpy.app.version_string == prior["host"] and REPORT["host_build_hash"] == prior["host_build_hash"], "Host/build changed between runs"
        assert sha256(Path(bpy.app.binary_path)) == prior["inputs"]["host_binary_sha256"], "Native executable changed"
        approved = Path(r"C:\Evidence\verification-output").resolve()
        paths = {name: os.environ.get(name) for name in ("PYTHONPYCACHEPREFIX", "TEMP", "TMP", "TMPDIR",
                                                        "BLENDER_USER_CONFIG", "BLENDER_USER_DATAFILES", "BLENDER_USER_EXTENSIONS")}
        for name, value in paths.items():
            assert value and Path(value).resolve().is_relative_to(approved), f"Unapproved {name}: {value!r}"
        assert EXTENSION in bpy.context.preferences.addons, "Candidate was not persistently enabled before reopen"
        cutbridge = importlib.import_module(EXTENSION)
        update_ops = importlib.import_module(EXTENSION + ".update_ops")
        operators = importlib.import_module(EXTENSION + ".operators")
        installed = Path(cutbridge.__file__).parent
        installed_hashes = {}
        with zipfile.ZipFile(ZIP) as archive:
            assert archive.testzip() is None, "Candidate ZIP CRC failed"
            names = archive.namelist()
            assert len(names) == len(set(names)), "Duplicate candidate ZIP paths"
            for name in names:
                relative = PurePosixPath(name)
                assert not relative.is_absolute() and ".." not in relative.parts and "\\" not in name, f"Unsafe ZIP path: {name}"
                if name.endswith("/"):
                    continue
                path = installed.joinpath(*relative.parts)
                assert path.is_file() and not path.is_symlink(), f"Missing/linked installed file: {name}"
                expected_hash = hashlib.sha256(archive.read(name)).hexdigest()
                assert sha256(path) == expected_hash, f"Installed candidate bytes changed: {name}"
                installed_hashes[name] = expected_hash
        assert installed_hashes == prior["inputs"]["installed_files"], "Installed source inventory/hash changed"
        assert cutbridge.version.__version__ == "0.2.5", "Unexpected enabled candidate product version"
        assert not bpy.app.timers.is_registered(update_ops._startup_update_check), "Startup timer registered in new process"
        REPORT.update(candidate_sha=candidate_sha, writable_environment_paths=paths,
                      inputs={"prior_report_sha256": sha256(prior_path), "candidate_json_sha256": sha256(REVIEW),
                              "zip_sha256": sha256(ZIP), "fixture_sha256": sha256(FIXTURE),
                              "harness_sha256": sha256(Path(__file__)), "installed_files": installed_hashes})
        REPORT["stage"] = "fresh_process_open_and_inspect"
        write_report()
        assert bpy.ops.wm.open_mainfile(filepath=str(FIXTURE)) == {"FINISHED"}, "Could not open exact saved fixture"
        scene, layer = bpy.context.scene, bpy.context.view_layer
        settings = scene.cutbridge
        assert settings.version == 3 and settings.language == "EN", "Saved version/locale changed"
        assert settings.output_dir == str(OUT / "packages"), "Saved output directory changed"
        assert settings.handoff_3d_enabled and settings.handoff_3d_pixels_per_blender_unit == 100.0, "Saved handoff settings changed"
        assert scene.frame_current == 1 and math.isclose(scene.frame_subframe, 0.0), "Saved frame/subframe changed"
        assert scene.camera.name == "Native025Camera", "Saved active camera changed"
        assert bpy.data.objects["Native025Null"].get("cutbridge_handoff_3d") is True, "Saved explicit Empty marker changed"
        assert not bpy.data.objects["Native025Unmarked"].get("cutbridge_handoff_3d", False), "Unmarked Empty was adopted"
        expected_artist = json.loads((OUT / "artist-before.json").read_text(encoding="utf-8"))
        assert canonical(artist_state(scene.compositing_node_group)) == expected_artist, "Fresh-process artist sentinel/links/values changed"
        expected_mapping = json.loads((OUT / "rollback-after.json").read_text(encoding="utf-8"))
        assert canonical(mapping_state(scene, layer)) == expected_mapping, "Fresh-process compositor mapping/render flags changed"
        issues = operators._all_validation_issues(bpy.context)
        assert not [issue for issue in issues if issue["level"] == "ERROR"], issues
        assert any(issue["code"] == "PACKAGE_RENDER_READY" and issue["level"] == "INFO" for issue in issues), issues
        assert not bpy.app.timers.is_registered(update_ops._startup_update_check), "Startup timer registered after fixture load"
        last_root = Path(settings.last_package_path)
        manifest = json.loads((last_root / "cutbridge.json").read_text(encoding="utf-8"))
        assert type(manifest["version"]) is int and manifest["version"] == 3 and manifest["version_label"] == "V003", "Saved manifest revision identity changed"
        assert manifest["cutbridge_version"] == "0.2.5", "Saved manifest product version changed"
        assert manifest["handoff_3d"]["camera"]["name"] == scene.camera.name, "Saved camera manifest binding changed"
        assert manifest["handoff_3d"]["camera"]["type"] == "PERSP", "Unexpected serialized camera type"
        nulls = manifest["handoff_3d"]["nulls"]
        assert len(nulls) == 1 and nulls[0]["name"] == "Native025Null" and nulls[0]["source_type"] == "EMPTY", "Saved marked Empty binding changed"
        check_package_files(prior)
        assert sha256(FIXTURE) == prior["fixture_files"]["reopen-V003.blend"]["sha256"], "Inspection mutated saved fixture"
        REPORT["overall_scope_result"] = "PASS"
        REPORT["checks"] = ["Exact candidate metadata/ZIP/installed bytes and host build unchanged", "Persistently enabled extension and startup timer absent",
                            "Fresh process opened exact saved V003 fixture", "Artist/compositor/render state equals retained prior state",
                            "Saved version/locale/handoff/ownership manifest binding intact", "V001-V003 package inventory/bytes unchanged",
                            "Native package lifecycle reports render-ready"]
    except AssertionError:
        REPORT["overall_scope_result"] = "INSUFFICIENT EVIDENCE" if REPORT["stage"] == "prerequisites" else "FAIL"
        REPORT["error"] = traceback.format_exc()
    except Exception:
        REPORT["overall_scope_result"] = "INSUFFICIENT EVIDENCE"
        REPORT["error"] = traceback.format_exc()
        REPORT["classification_note"] = "Unexpected harness/host exception; inspect before attributing candidate defect"
    finally:
        write_report()
        bpy.app.timers.register(quit_normally, first_interval=2.0)
    return None


write_report()
bpy.app.timers.register(run, first_interval=2.0)

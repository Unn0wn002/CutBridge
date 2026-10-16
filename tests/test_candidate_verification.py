"""Verifier integrity regressions; no Docker, network, credentials or real Git."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import stat
import zipfile
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("candidate_verification", ROOT / "tools/candidate_verification.py")
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def git_tree(*entries):
    return b"".join(f"{mode} {kind} {oid}\t{name}".encode() + b"\0" for mode, kind, oid, name in entries)


@pytest.mark.parametrize("name", [
    "/absolute", "../outside", "a/../outside", "a//b", r"a\b", "C:escape", ".git/config",
    "a/.GIT/config", "verification-output/x", "Verification-Input/x", "NUL.txt", "a/aux",
    "trailing.", "trailing ", "control\nfile",
])
def test_unsafe_or_reserved_git_paths_are_rejected(name):
    with pytest.raises(verifier.IntegrityError):
        verifier.safe_path(name)


@pytest.mark.parametrize("mode,kind", [("120000", "blob"), ("160000", "commit"), ("040000", "tree")])
def test_git_symlink_submodule_or_unknown_type_is_rejected(monkeypatch, mode, kind):
    monkeypatch.setattr(verifier, "git", lambda *args: git_tree((mode, kind, "a" * 40, "unsafe")))
    with pytest.raises(verifier.IntegrityError, match="type/mode"):
        verifier.tree_entries(ROOT, "f" * 40)


def test_case_colliding_parent_directories_are_rejected(monkeypatch):
    tree = git_tree(("100644", "blob", "a" * 40, "A/one"), ("100644", "blob", "b" * 40, "a/two"))
    monkeypatch.setattr(verifier, "git", lambda *args: tree)
    with pytest.raises(verifier.IntegrityError, match="case-colliding"):
        verifier.tree_entries(ROOT, "f" * 40)


@pytest.mark.parametrize("paths", [("same", "same"), ("directory/file", "directory"), ("file", "file/nested")])
def test_duplicate_or_conflicting_git_inventory_is_invalid(monkeypatch, paths):
    monkeypatch.setattr(verifier, "git", lambda *args: git_tree(
        *[("100644", "blob", "a" * 40, name) for name in paths]))
    with pytest.raises(verifier.IntegrityError, match="duplicate|conflicting"):
        verifier.tree_entries(ROOT, "f" * 40)


def test_exact_blobs_keep_export_ignored_and_unsubstituted_bytes(tmp_path, monkeypatch):
    blobs = {
        ".gitattributes": b"hidden export-ignore\nsubstituted export-subst\n",
        "hidden": b"must not disappear\n",
        "substituted": b"$Format:%H$\r\nbinary:\x00\xff",
    }
    objects = {hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(): data for data in blobs.values()}
    tree = git_tree(*[("100644", "blob", oid, name) for name, data in blobs.items()
                      for oid, value in objects.items() if value == data])
    calls = []

    def fake_git(repo, *args):
        calls.append(args)
        return tree if args[0] == "ls-tree" else objects[args[-1]]

    monkeypatch.setattr(verifier, "git", fake_git)
    if os.name != "posix":
        # Windows chmod cannot establish Linux mode invariants; bytes still tested.
        monkeypatch.setattr(verifier, "verify_snapshot", lambda *args: None)
    snapshot = tmp_path / "snapshot"
    try:
        inventory = verifier.prepare_snapshot(ROOT, "f" * 40, snapshot)
        assert {item["path"] for item in inventory} == set(blobs)
        assert all((snapshot / name).read_bytes() == data for name, data in blobs.items())
        assert not any("archive" in command for command in calls)
    finally:
        for name in blobs:
            path = snapshot / name
            if path.exists():
                path.chmod(0o666)
        snapshot.chmod(0o777)


def test_corrupt_blob_object_is_not_accepted(tmp_path, monkeypatch):
    monkeypatch.setattr(verifier, "git", lambda repo, *args:
                        git_tree(("100644", "blob", "a" * 40, "file")) if args[0] == "ls-tree" else b"corrupt")
    with pytest.raises(verifier.IntegrityError, match="blob hash"):
        verifier.prepare_snapshot(ROOT, "f" * 40, tmp_path / "snapshot")


def test_non_utf8_git_path_encoding_is_integrity_failure(monkeypatch):
    monkeypatch.setattr(verifier, "git", lambda *args:
                        b"100644 blob " + b"a" * 40 + b"\tbad-\xff\0")
    with pytest.raises(verifier.IntegrityError, match="encoding"):
        verifier.tree_entries(ROOT, "f" * 40)


def test_inventory_includes_cache_names_outside_designated_output(tmp_path):
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__/unexpected.pyc").write_bytes(b"unexpected generated input")
    (tmp_path / "verification-output").mkdir()
    (tmp_path / "verification-output/allowed").write_bytes(b"writable")
    inventory = verifier.regular_inventory(tmp_path, allow_root_output=True)
    assert [item["path"] for item in inventory] == ["__pycache__", "__pycache__/unexpected.pyc"]


def test_inventory_uses_complete_nofollow_stat_not_partial_direntry_metadata(tmp_path, monkeypatch):
    (tmp_path / "ordinary").write_bytes(b"regular file with one link")
    real_scandir = verifier.os.scandir

    def partial_scandir(directory):
        with real_scandir(directory) as entries:
            return [SimpleNamespace(
                path=entry.path, name=entry.name,
                stat=lambda **kwargs: pytest.fail("DirEntry metadata can omit Windows link count"))
                for entry in entries]

    monkeypatch.setattr(verifier.os, "scandir", partial_scandir)
    inventory = verifier.regular_inventory(tmp_path)
    assert len(inventory) == 1
    assert inventory[0]["path"] == "ordinary"
    assert inventory[0]["sha256"] == verifier.digest(b"regular file with one link")


@pytest.mark.skipif(os.name != "posix", reason="snapshot modes require the Linux verifier host")
def test_snapshot_verification_rejects_missing_extra_and_mode_changes(tmp_path):
    path = tmp_path / "source"
    path.write_bytes(b"source")
    path.chmod(0o444)
    expected = [{"path": "source", "mode": "100644", "size": 6, "sha256": verifier.digest(b"source")}]
    verifier.verify_snapshot(tmp_path, expected)
    path.chmod(0o644)
    with pytest.raises(verifier.IntegrityError):
        verifier.verify_snapshot(tmp_path, expected)
    path.chmod(0o444)
    (tmp_path / "unexpected").write_bytes(b"x")
    with pytest.raises(verifier.IntegrityError):
        verifier.verify_snapshot(tmp_path, expected)
    (tmp_path / "unexpected").unlink()
    path.unlink()
    with pytest.raises(verifier.IntegrityError):
        verifier.verify_snapshot(tmp_path, expected)


def package_pair(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (first / "artifact").write_bytes(b"same")
    (second / "artifact").write_bytes(b"same")
    return first, second


@pytest.mark.parametrize("change", ["extra", "missing", "bytes", "empty-directory"])
def test_complete_repeated_inventory_detects_both_sides(tmp_path, change):
    first, second = package_pair(tmp_path)
    verifier.compare_packages(first, second)
    if change == "extra":
        (second / "second-only").write_bytes(b"never silently ignore this")
    elif change == "missing":
        (second / "artifact").unlink()
    elif change == "bytes":
        (second / "artifact").write_bytes(b"diff")
    else:
        (second / "extra-empty-directory").mkdir()
    with pytest.raises(verifier.CandidateFailure):
        verifier.compare_packages(first, second)


def make_symlink(source, target):
    try:
        source.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable in this host sandbox")


def test_source_and_output_inventory_do_not_follow_symlinks(tmp_path):
    outside, directory = tmp_path / "owner-file", tmp_path / "inventory"
    outside.write_bytes(b"must never read through a candidate link")
    directory.mkdir()
    make_symlink(directory / "link", outside)
    with pytest.raises(verifier.IntegrityError, match="symlink"):
        verifier.regular_inventory(directory)


def test_hardlinks_are_rejected_before_staging(tmp_path):
    output, evidence = tmp_path / "output", tmp_path / "evidence"
    (output / "dist-ci").mkdir(parents=True)
    evidence.mkdir()
    target = tmp_path / "outside"
    target.write_bytes(b"outside")
    try:
        os.link(target, output / "dist-ci/linked")
    except OSError:
        pytest.skip("hardlinks unavailable")
    with pytest.raises(verifier.IntegrityError, match="hardlink"):
        verifier.stage_outputs(output, evidence)
    assert not (evidence / "candidate-output").exists()


@pytest.mark.skipif(os.name != "posix", reason="FIFO regression requires POSIX")
def test_fifo_is_rejected_without_blocking(tmp_path):
    os.mkfifo(tmp_path / "fifo")
    with pytest.raises(verifier.IntegrityError, match="special"):
        verifier.regular_inventory(tmp_path)


def test_pytest_report_root_symlink_is_not_uploaded(tmp_path):
    output, evidence = tmp_path / "output", tmp_path / "evidence"
    output.mkdir()
    evidence.mkdir()
    owner_file = tmp_path / "owner"
    owner_file.write_bytes(b"private")
    make_symlink(output / "pytest.xml", owner_file)
    with pytest.raises(verifier.IntegrityError, match="symlink"):
        verifier.stage_outputs(output, evidence)
    assert list(evidence.iterdir()) == []


def test_only_fixed_regular_output_roots_are_copied_to_host_stage(tmp_path):
    output, evidence = tmp_path / "output", tmp_path / "evidence"
    (output / "dist-ci").mkdir(parents=True)
    (output / "home").mkdir()
    evidence.mkdir()
    (output / "dist-ci/package.zip").write_bytes(b"zip")
    (output / "home/not-an-artifact").write_bytes(b"do not upload")
    (output / "verdict.txt").write_text("forged PASS")
    staged = verifier.stage_outputs(output, evidence)
    assert [entry["path"] for entry in staged] == ["dist-ci/package.zip"]
    assert (evidence / "candidate-output/dist-ci/package.zip").read_bytes() == b"zip"
    assert not (evidence / "verdict.txt").exists()
    (evidence / "candidate-output/dist-ci/package.zip").chmod(0o666)


def isolation():
    mounts = [("/snapshot", "/candidate", False), ("/out", "/candidate/verification-output", True),
              ("/inputs", "/verification-input", False), ("/runner", "/orchestration", False)]
    info = {
        "HostConfig": {"NetworkMode": "none", "ReadonlyRootfs": True, "CapDrop": ["ALL"],
                       "SecurityOpt": ["no-new-privileges"], "Privileged": False, "PidMode": "",
                       "IpcMode": "private", "PidsLimit": 512, "Memory": 6 * 1024**3, "NanoCpus": 2 * 10**9},
        "Config": {"User": "1000:1000", "WorkingDir": "/candidate", "Env": ["PATH=/usr/local/bin:/usr/bin", "HOME=/candidate/verification-output/home"]},
        "Mounts": [{"Source": source, "Destination": target, "RW": writable} for source, target, writable in mounts],
    }
    return info, mounts


@pytest.mark.parametrize("change", ["network", "source-write", "extra-mount", "credential", "root-user", "privileged", "host-pid", "engine-socket"])
def test_isolation_inspection_rejects_boundary_weakening(change):
    info, mounts = isolation()
    verifier.validate_isolation(info, mounts)
    if change == "network":
        info["HostConfig"]["NetworkMode"] = "bridge"
    elif change == "source-write":
        info["Mounts"][0]["RW"] = True
    elif change == "extra-mount":
        info["Mounts"].append({"Source": "/owner", "Destination": "/owner", "RW": False})
    elif change == "credential":
        info["Config"]["Env"].append("GH_TOKEN=never-expose")
    elif change == "root-user":
        info["Config"]["User"] = "0:0"
    elif change == "privileged":
        info["HostConfig"]["Privileged"] = True
    elif change == "host-pid":
        info["HostConfig"]["PidMode"] = "host"
    else:
        info["Mounts"][0]["Source"] = "/var/run/docker.sock"
    with pytest.raises(verifier.IntegrityError):
        verifier.validate_isolation(info, mounts)


def execution_state(**changes):
    return {"Status": "exited", "OOMKilled": False, "Error": "", "ExitCode": 0, "StartedAt": "2026-10-16T00:00:00Z", **changes}


@pytest.mark.parametrize("changes,attach,timeout", [
    ({"OOMKilled": True, "ExitCode": 137}, 137, False),
    ({"Error": "daemon startup failure", "ExitCode": 125}, 125, False),
    ({"Status": "created", "StartedAt": "0001-01-01T00:00:00Z"}, 125, False),
    ({}, 1, False), ({}, 0, True),
])
def test_infrastructure_failure_is_insufficient_not_candidate_fail(changes, attach, timeout):
    assert verifier.classify_execution(execution_state(**changes), attach, timeout) == "INSUFFICIENT EVIDENCE"


@pytest.mark.parametrize("code", [1, 2, 125, 126, 127])
def test_real_candidate_exit_is_fail_when_container_started_and_attach_agrees(code):
    assert verifier.classify_execution(execution_state(ExitCode=code), code) == "FAIL"


def test_success_is_limited_to_completed_execution():
    assert verifier.classify_execution(execution_state(), 0) == "PASS"


def test_trusted_preflight_probe_failure_is_invalid_before_candidate_execution():
    assert verifier.classify_preflight(execution_state(ExitCode=1), 1) == "INVALID"
    assert verifier.classify_preflight(execution_state(), 0) == "PASS"
    assert verifier.classify_preflight(execution_state(Error="shell could not start", ExitCode=127), 127) == "INSUFFICIENT EVIDENCE"
    assert verifier.classify_preflight(execution_state(), 0, True) == "INSUFFICIENT EVIDENCE"


def test_workflow_trust_selection_and_upload_paths_are_outside_candidate_control():
    workflow = (ROOT / ".github/workflows/candidate-verification.yml").read_text()
    assert "  push:" not in workflow and "  pull_request:" not in workflow
    assert "  workflow_dispatch:" in workflow
    assert '[[ "$WORKFLOW_SHA" == "$TRUSTED_SHA" ]]' in workflow
    assert '[[ "$CANDIDATE_SHA" != "$TRUSTED_SHA" ]]' in workflow
    assert "ref: $" + "{{ inputs.trusted_orchestration_sha }}" in workflow
    assert "path: $" + "{{ runner.temp }}/cutbridge-verification/evidence/" in workflow
    assert "cutbridge-snapshot/verification-output" not in workflow


def test_canonical_commands_are_kept_in_reviewed_orchestration():
    script = (ROOT / "tools/candidate_checks.sh").read_text()
    assert "python -m compileall -q apps tools tests" in script
    assert "python -m pytest -q -p no:cacheprovider" in script
    assert "python tests/test_blender_runtime_52.py" in script
    assert script.count("python tools/build_release.py") == 2
    assert "/verification-input/production-release-index.json" in script


def test_packaged_checksum_inventory_cannot_omit_an_artifact(tmp_path):
    version = "0.2.5"
    (tmp_path / f"CutBridge-Blender-v{version}.zip").write_bytes(b"blender")
    (tmp_path / f"CutBridge-AfterEffects-v{version}.zip").write_bytes(b"AE")
    (tmp_path / "SHA256SUMS.txt").write_text(
        verifier.digest(b"blender") + f"  CutBridge-Blender-v{version}.zip\n")
    (tmp_path / "release-metadata.json").write_text("{}")
    with pytest.raises(verifier.CandidateFailure, match="incomplete"):
        verifier.validate_packages(tmp_path, version)


def write_zip(path, entries):
    with zipfile.ZipFile(path, "w") as archive:
        for name, data, mode in entries:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, data)


@pytest.mark.parametrize("mode", [stat.S_IFLNK | 0o777, stat.S_IFIFO | 0o644, stat.S_IFREG | 0o777])
def test_zip_member_links_specials_and_unexpected_modes_are_rejected(tmp_path, mode):
    archive = tmp_path / "candidate.zip"
    write_zip(archive, [("member", b"outside", mode)])
    with pytest.raises(verifier.CandidateFailure, match="canonical regular"):
        verifier.validate_archive(archive)


def valid_packages(directory):
    version = "0.2.5"
    directory.mkdir()
    blender = directory / "CutBridge-Blender-v0.2.5.zip"
    ae = directory / "CutBridge-AfterEffects-v0.2.5.zip"
    write_zip(blender, [("blender_manifest.toml", b'version = "0.2.5"', stat.S_IFREG | 0o644)])
    write_zip(ae, [(name, (b"See /blob/v0.2.5/docs/RELEASE_READINESS.md" if name == "INSTALL.md" else b"runtime"), stat.S_IFREG | 0o644)
                   for name in ("CutBridge.jsx", "revision_manager.js", "qc_plus.js", "localization.js", "INSTALL.md", "LICENSE")])
    hashes = {path.name: verifier.digest(path.read_bytes()) for path in (blender, ae)}
    (directory / "SHA256SUMS.txt").write_text("".join(f"{value}  {name}\n" for name, value in sorted(hashes.items())))
    (directory / "release-metadata.json").write_text(json.dumps({
        "version": version, "tag": "v" + version,
        "artifacts": {"blender": {"filename": blender.name, "sha256": hashes[blender.name]},
                      "after_effects": {"filename": ae.name, "sha256": hashes[ae.name]}}}))
    return version


def test_valid_package_inventory_checksums_metadata_and_install_are_verified(tmp_path):
    directory = tmp_path / "packages"
    version = valid_packages(directory)
    verifier.validate_packages(directory, version)
    metadata_path = directory / "release-metadata.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["artifacts"]["after_effects"]["sha256"] = "0" * 64
    metadata_path.write_text(json.dumps(metadata))
    with pytest.raises(verifier.CandidateFailure, match="metadata artifact"):
        verifier.validate_packages(directory, version)


def test_extra_repeated_package_output_cannot_satisfy_four_artifact_contract(tmp_path):
    directory = tmp_path / "packages"
    version = valid_packages(directory)
    (directory / "unreviewed-extra").write_bytes(b"extra")
    with pytest.raises(verifier.CandidateFailure, match="exactly four"):
        verifier.validate_packages(directory, version)


@pytest.mark.parametrize("same_candidate,wrong_checkout", [(True, False), (False, True)])
def test_orchestration_rejects_candidate_trust_and_wrong_checkout_before_any_execution(tmp_path, monkeypatch, same_candidate, wrong_checkout):
    trusted = "a" * 40
    candidate = trusted if same_candidate else "b" * 40
    root = tmp_path / "attempt"
    monkeypatch.setattr(sys, "argv", ["candidate_verification.py", "--trusted-sha", trusted,
        "--candidate-sha", candidate, "--develop-sha", "c" * 40, "--root", str(root)])
    git_calls = []

    def fake_git(repo, *args):
        git_calls.append(args)
        assert args == ("rev-parse", "HEAD")  # No candidate inspection/execution.
        return ("d" * 40 + "\n").encode()

    monkeypatch.setattr(verifier, "git", fake_git)
    monkeypatch.setattr(verifier.subprocess, "run", lambda *args, **kwargs: pytest.fail("untrusted orchestration must not execute commands"))
    assert verifier.main() == 1
    result = json.loads((root / "evidence/verification.json").read_text())
    assert result["verdict"] == "INVALID"
    assert result["commands"] == []
    assert len(git_calls) == int(wrong_checkout)

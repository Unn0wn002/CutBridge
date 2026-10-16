#!/usr/bin/env python3
"""Pinned Actions orchestration wrapping the existing CONTRIBUTING commands.

Execute only from a separately reviewed orchestration SHA, never a candidate ref.
The operator supplies that independent trust decision; equality is only a guard
against dispatching the wrong revision. PASS covers automated scope only.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tarfile
import time
import tomllib
import urllib.request
import zipfile

INDEX_URL = "https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json"
MAX_FILES, MAX_BYTES, MAX_FILE_BYTES = 20000, 512 * 1024**2, 256 * 1024**2
SHA = re.compile(r"[a-f0-9]{40}\Z")
DOCKERFILE = """FROM node:22-bookworm-slim AS node
FROM python:3.13-bookworm
COPY --from=node /usr/local/bin/node /usr/local/bin/node
RUN apt-get update && apt-get install -y --no-install-recommends \\
 libgl1 libegl1 libxrender1 libxi6 libxfixes3 libxkbcommon0 \\
 libsm6 libice6 libwayland-client0 && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir pytest jsonschema bpy==5.2.1
RUN python -I -c 'import bpy, pytest, jsonschema; assert bpy.app.version == (5, 2, 1)'
RUN node --version && python --version && python -m pip freeze
"""


class IntegrityError(ValueError):
    """Inputs/outputs violate verification integrity assumptions."""


class CandidateFailure(ValueError):
    """Checks executed correctly but candidate behavior/output is incorrect."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def safe_path(name):
    """Reject traversal, Git internals, reserved mount paths and OS aliases."""
    if not name or "\\" in name or ":" in name or any(ord(c) < 32 or ord(c) == 127 for c in name):
        raise IntegrityError(f"unsafe path: {name!r}")
    parts = name.split("/")
    devices = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
    if any(p in ("", ".", "..") or p.casefold() == ".git" or p.endswith((" ", "."))
           or p.split(".")[0].casefold() in devices for p in parts):
        raise IntegrityError(f"unsafe path: {name!r}")
    if parts[0].casefold() in {"verification-output", "verification-input"}:
        raise IntegrityError(f"reserved path: {name!r}")
    return name


def git(repo, *args):
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"}
    return subprocess.check_output(["git", "-c", "core.hooksPath=" + os.devnull, *args], cwd=repo, env=env)


def tree_entries(repo, sha):
    entries, aliases, file_paths = [], {}, set()
    for raw in git(repo, "ls-tree", "-rz", "--full-tree", sha).split(b"\0"):
        if not raw:
            continue
        header, raw_name = raw.split(b"\t", 1)
        try:
            mode, kind, oid = header.decode("ascii").split()
            name = safe_path(raw_name.decode("utf-8", errors="strict"))
        except UnicodeError as error:
            raise IntegrityError("unsupported Git path/header encoding") from error
        if mode not in ("100644", "100755") or kind != "blob":
            raise IntegrityError(f"unsupported Git type/mode for {name}: {mode} {kind}")
        parts = name.split("/")
        if name in file_paths or name in aliases or any("/".join(parts[:i]) in file_paths for i in range(1, len(parts))):
            raise IntegrityError(f"duplicate or file/directory-conflicting Git path: {name}")
        file_paths.add(name)
        for i in range(1, len(parts) + 1):
            prefix = "/".join(parts[:i])
            alias = prefix.casefold()
            if alias in aliases and aliases[alias] != prefix:
                raise IntegrityError(f"case-colliding Git path: {name}")
            aliases[alias] = prefix
        entries.append({"path": name, "mode": mode, "oid": oid})
    if not entries or len(entries) > MAX_FILES:
        raise IntegrityError("empty or oversized source inventory")
    return sorted(entries, key=lambda entry: entry["path"])


def prepare_snapshot(repo, sha, destination):
    """Exact blobs; export-ignore/export-subst and checkout filters never apply."""
    destination.mkdir(mode=0o700)
    inventory, total = tree_entries(repo, sha), 0
    for entry in inventory:
        data = git(repo, "cat-file", "blob", entry["oid"])
        total += len(data)
        if len(data) > MAX_FILE_BYTES or total > MAX_BYTES:
            raise IntegrityError("snapshot size limit exceeded")
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if oid != entry["oid"]:
            raise IntegrityError(f"Git blob hash mismatch: {entry['path']}")
        path = destination / entry["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)
        path.chmod(0o555 if entry["mode"] == "100755" else 0o444)
        entry.update(size=len(data), sha256=digest(data))
    (destination / "verification-output").mkdir()
    for current, dirs, _ in os.walk(destination, topdown=False):
        for name in dirs:
            (Path(current) / name).chmod(0o555)
    destination.chmod(0o555)
    verify_snapshot(destination, inventory)
    return inventory


def regular_inventory(root, *, allow_root_output=False):
    """Include empty dirs/modes; reject links and special files without following."""
    if root.is_symlink() or not root.is_dir():
        raise IntegrityError(f"not a real directory: {root}")
    result, total, pending = [], 0, [root]
    while pending:
        for entry in sorted(os.scandir(pending.pop()), key=lambda item: item.name):
            relative = Path(entry.path).relative_to(root).as_posix()
            # Windows DirEntry.stat may omit inode/device/link-count metadata
            # (reporting zero links for an ordinary file). Obtain complete
            # no-follow metadata for hardlink rejection and open identity checks.
            info = os.stat(entry.path, follow_symlinks=False)
            if allow_root_output and relative == "verification-output":
                if not stat.S_ISDIR(info.st_mode):
                    raise IntegrityError("designated output is not a directory")
                continue
            safe_path(relative)
            if stat.S_ISDIR(info.st_mode):
                result.append({"path": relative, "type": "directory", "mode": stat.S_IMODE(info.st_mode)})
                pending.append(Path(entry.path))
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                total += info.st_size
                if info.st_size > MAX_FILE_BYTES or total > MAX_BYTES:
                    raise IntegrityError("inventory size limit exceeded")
                flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
                with os.fdopen(os.open(entry.path, flags), "rb") as stream:
                    opened = os.fstat(stream.fileno())
                    if (opened.st_ino, opened.st_dev, opened.st_mode, opened.st_nlink, opened.st_size) != (info.st_ino, info.st_dev, info.st_mode, info.st_nlink, info.st_size):
                        raise IntegrityError(f"file changed while opening: {relative}")
                    data = stream.read(MAX_FILE_BYTES + 1)
                if len(data) != info.st_size:
                    raise IntegrityError(f"file changed while reading: {relative}")
                result.append({"path": relative, "type": "file", "mode": stat.S_IMODE(info.st_mode),
                               "size": len(data), "sha256": digest(data)})
            else:
                raise IntegrityError(f"symlink, hardlink, or special file: {relative}")
            if len(result) > MAX_FILES:
                raise IntegrityError("inventory entry limit exceeded")
    return sorted(result, key=lambda item: item["path"])


def verify_snapshot(root, expected):
    actual, wanted, dirs = regular_inventory(root, allow_root_output=True), [], set()
    for entry in expected:
        wanted.append({"path": entry["path"], "type": "file", "mode": 0o555 if entry["mode"] == "100755" else 0o444,
                       "size": entry["size"], "sha256": entry["sha256"]})
        parts = entry["path"].split("/")
        dirs.update("/".join(parts[:i]) for i in range(1, len(parts)))
    wanted.extend({"path": name, "type": "directory", "mode": 0o555} for name in dirs)
    if actual != sorted(wanted, key=lambda item: item["path"]):
        raise IntegrityError("snapshot paths/types/modes/bytes differ from exact Git inputs")
    return actual


def compare_packages(first, second):
    left, right = regular_inventory(first), regular_inventory(second)
    if left != right:
        raise CandidateFailure("repeated package inventories/types/modes/bytes differ")
    return left


def validate_archive(path):
    """Reject archive links/unsafe names before reading any member contents."""
    with zipfile.ZipFile(path) as archive:
        names, aliases, total = set(), {}, 0
        entries = archive.infolist()
        if not entries or len(entries) > MAX_FILES:
            raise CandidateFailure("empty or oversized archive inventory")
        for entry in entries:
            safe_path(entry.filename)
            if entry.filename in names:
                raise CandidateFailure("duplicate archive member")
            parts = entry.filename.split("/")
            if entry.filename in aliases or any("/".join(parts[:i]) in names for i in range(1, len(parts))):
                raise CandidateFailure("archive file/directory path conflict")
            for i in range(1, len(parts) + 1):
                prefix = "/".join(parts[:i])
                alias = prefix.casefold()
                if alias in aliases and aliases[alias] != prefix:
                    raise CandidateFailure("archive paths collide on a supported case-insensitive filesystem")
                aliases[alias] = prefix
            names.add(entry.filename)
            mode = entry.external_attr >> 16
            if entry.create_system != 3 or mode != stat.S_IFREG | 0o644:
                raise CandidateFailure("archive member is not a canonical regular file (links forbidden)")
            if entry.date_time != (1980, 1, 1, 0, 0, 0) or entry.flag_bits & 1:
                raise CandidateFailure("noncanonical timestamp or encrypted archive member")
            total += entry.file_size
            if entry.file_size > MAX_FILE_BYTES or total > MAX_BYTES:
                raise CandidateFailure("archive uncompressed size limit exceeded")
        if archive.testzip() is not None:
            raise CandidateFailure("archive member CRC mismatch")


def validate_packages(root, version):
    names = {f"CutBridge-Blender-v{version}.zip", f"CutBridge-AfterEffects-v{version}.zip", "SHA256SUMS.txt", "release-metadata.json"}
    if {item["path"] for item in regular_inventory(root)} != names:
        raise CandidateFailure("package directory must contain exactly four release artifacts")
    zips, checksums = names - {"SHA256SUMS.txt", "release-metadata.json"}, {}
    for line in (root / "SHA256SUMS.txt").read_text().splitlines():
        match = re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
        if not match or match[2] not in zips or match[2] in checksums:
            raise CandidateFailure("invalid, duplicate, or unexpected checksum entry")
        checksums[match[2]] = match[1]
    if set(checksums) != zips or any(digest((root / name).read_bytes()) != value for name, value in checksums.items()):
        raise CandidateFailure("incomplete or incorrect package checksums")
    for name in zips:
        validate_archive(root / name)
    metadata = json.loads((root / "release-metadata.json").read_text())
    if not isinstance(metadata, dict) or not isinstance(metadata.get("artifacts"), dict):
        raise CandidateFailure("release metadata must contain an artifact object")
    if metadata.get("version") != version or metadata.get("tag") != "v" + version:
        raise CandidateFailure("release metadata identity mismatch")
    for key, name in (("blender", f"CutBridge-Blender-v{version}.zip"), ("after_effects", f"CutBridge-AfterEffects-v{version}.zip")):
        if metadata.get("artifacts", {}).get(key) != {"filename": name, "sha256": checksums[name]}:
            raise CandidateFailure("release metadata artifact hash/name mismatch")
    with zipfile.ZipFile(root / f"CutBridge-AfterEffects-v{version}.zip") as archive:
        expected = {"CutBridge.jsx", "revision_manager.js", "qc_plus.js", "localization.js", "INSTALL.md", "LICENSE"}
        if len(archive.namelist()) != len(expected) or set(archive.namelist()) != expected:
            raise CandidateFailure("After Effects ZIP has missing/duplicate/unexpected entries")
        info = archive.getinfo("INSTALL.md")
        if info.file_size > 1024 * 1024:
            raise CandidateFailure("oversized packaged installation instructions")
        install = archive.read(info).decode("utf-8")
        if any(word in install.lower() for word in ("development build", "unpublished")) or "RELEASE_TAG" in install or f"/blob/v{version}/docs/RELEASE_READINESS.md" not in install:
            raise CandidateFailure("packaged INSTALL.md has stale wording or unpinned readiness link")


def validate_isolation(info, mounts):
    host, config = info["HostConfig"], info["Config"]
    actual = {(m["Source"], m["Destination"], m["RW"]) for m in info["Mounts"]}
    if (host["NetworkMode"] != "none" or host["ReadonlyRootfs"] is not True
            or config["User"] != "1000:1000" or host["CapDrop"] != ["ALL"]
            or "no-new-privileges" not in host["SecurityOpt"] or host["Privileged"]
            or host.get("PidMode") or host.get("IpcMode") == "host"
            or len(info["Mounts"]) != len(mounts) or actual != set(mounts)
            or host["PidsLimit"] != 512 or host["Memory"] != 6 * 1024**3
            or host["NanoCpus"] != 2 * 10**9 or host.get("Devices") or host.get("DeviceRequests")
            or config["WorkingDir"] != "/candidate"):
        raise IntegrityError("container settings differ from reviewed isolation boundary")
    allowed = {"PATH", "LANG", "GPG_KEY", "PYTHON_VERSION", "PYTHON_SHA256",
               "PYTHON_PIP_VERSION", "PYTHON_SETUPTOOLS_VERSION", "PYTHON_GET_PIP_URL", "PYTHON_GET_PIP_SHA256",
               "HOME", "PYTHONPYCACHEPREFIX", "TEMP", "TMP", "TMPDIR", "CUTBRIDGE_VERSION", "PYTEST_DISABLE_PLUGIN_AUTOLOAD"}
    if any(item.split("=", 1)[0] not in allowed for item in config["Env"]):
        raise IntegrityError("unexpected container environment; possible credential exposure")


def classify_execution(state, attach_exit, timed_out=False):
    if (timed_out or state.get("OOMKilled") or state.get("Error") or state.get("Status") != "exited"
            or not state.get("StartedAt", "").startswith("20") or attach_exit != state["ExitCode"]):
        return "INSUFFICIENT EVIDENCE"
    return "PASS" if state["ExitCode"] == 0 else "FAIL"


def classify_preflight(state, attach_exit, timed_out=False):
    # Only the reviewed Python -I probe executes here, never candidate commands.
    result = classify_execution(state, attach_exit, timed_out)
    return "INVALID" if result == "FAIL" else result


def stage_outputs(output, evidence):
    """Read only after all candidate processes are removed; copy checked files."""
    staged = []
    for name in ("pytest.xml", "dist-ci", "dist-repeat", "distribution-preview"):
        source = output / name
        if not os.path.lexists(source):
            continue
        if source.is_symlink():
            raise IntegrityError(f"symlink output root: {name}")
        if name == "pytest.xml":
            info = source.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > MAX_FILE_BYTES:
                raise IntegrityError("unsafe pytest report")
            entries = [{"path": name, "type": "file", "size": info.st_size, "sha256": digest(source.read_bytes())}]
        else:
            entries = regular_inventory(source)
        for entry in entries:
            if entry["type"] != "file":
                continue
            relative = name if name == "pytest.xml" else name + "/" + entry["path"]
            destination = evidence / "candidate-output" / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            data = (output / relative).read_bytes()
            if len(data) != entry["size"] or digest(data) != entry["sha256"]:
                raise IntegrityError(f"output changed during staging: {relative}")
            with destination.open("xb") as stream:
                stream.write(data)
            destination.chmod(0o444)
            staged.append({**entry, "path": relative})
    return staged


def manifest_bytes(inventory):
    return "".join(f"{entry['sha256']}  {entry['path']}\n" for entry in inventory if entry.get("type", "file") == "file").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("trusted-sha", "candidate-sha", "develop-sha", "root"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    repo, root = Path.cwd(), Path(args.root).absolute()
    root.mkdir(mode=0o700)  # Never reuse an attempt.
    evidence = root / "evidence"
    evidence.mkdir(mode=0o700)
    verdict, reason, container, removed = "INSUFFICIENT EVIDENCE", "preparation incomplete", None, False
    records = {"candidate_sha": args.candidate_sha, "trusted_orchestration_sha": args.trusted_sha,
               "develop_sha": args.develop_sha, "scope": "canonical automated checks only; no native-host or release authorization claim",
               "started_at_unix": int(time.time()), "commands": []}

    def command(argv, log_name, timeout=900):
        records["commands"].append(argv)
        with (evidence / log_name).open("wb") as log:
            result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
        if result.returncode:
            raise RuntimeError(f"infrastructure command failed ({result.returncode}); see {log_name}")

    try:
        if not all(SHA.fullmatch(value) for value in (args.trusted_sha, args.candidate_sha, args.develop_sha)) or args.trusted_sha == args.candidate_sha:
            raise IntegrityError("invalid trust/candidate/base pins")
        if git(repo, "rev-parse", "HEAD").decode().strip() != args.trusted_sha:
            raise IntegrityError("orchestration checkout does not equal independent trust pin")
        command(["git", "-c", "core.hooksPath=" + os.devnull, "fetch", "--no-tags", "origin", args.candidate_sha, args.develop_sha], "fetch.log")
        for value in (args.candidate_sha, args.develop_sha):
            if git(repo, "cat-file", "-t", value) != b"commit\n":
                raise IntegrityError("pin does not identify a commit")
        bases = git(repo, "merge-base", "--all", args.develop_sha, args.candidate_sha).decode().splitlines()
        if len(bases) != 1:
            raise RuntimeError("candidate/develop require one unambiguous merge-base")
        records["merge_base_sha"] = bases[0]
        review = git(repo, "diff", "--binary", "--full-index", "--no-ext-diff", "--no-textconv", bases[0], args.candidate_sha, "--")
        (evidence / "candidate.diff").write_bytes(review)
        snapshot, output = root / "snapshot", root / "output"
        inventory = prepare_snapshot(repo, args.candidate_sha, snapshot)
        (evidence / "git-inventory.json").write_bytes(json_bytes(inventory))
        before = verify_snapshot(snapshot, inventory)
        (evidence / "manifest-before.sha256").write_bytes(manifest_bytes(before))
        (evidence / "inventory-before.json").write_bytes(json_bytes(before))
        with tarfile.open(evidence / "source-inputs.tar", "w") as archive:
            for entry in inventory:
                archive.add(snapshot / entry["path"], arcname=entry["path"], recursive=False)
        inputs = root / "inputs"
        inputs.mkdir(mode=0o755)
        with urllib.request.urlopen(INDEX_URL, timeout=30) as response:
            index = response.read(5 * 1024**2 + 1)
            if len(index) > 5 * 1024**2:
                raise RuntimeError("production index size limit exceeded")
            records["production_index_url"] = response.geturl()
        (inputs / "production-release-index.json").write_bytes(index)
        (evidence / "production-release-index.json").write_bytes(index)
        records["production_index_sha256"] = digest(index)
        records["snapshot_id"] = digest(json_bytes(inventory) + review + index + json_bytes({k: records[k] for k in ("candidate_sha", "develop_sha", "merge_base_sha")}))
        manifest_path = snapshot / "apps/blender/cutbridge/blender_manifest.toml"
        if not manifest_path.is_file():
            raise CandidateFailure("candidate Blender manifest is missing")
        version = tomllib.loads(manifest_path.read_text()).get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise CandidateFailure("candidate version is not stable semver")
        preparation = root / "image-preparation"
        preparation.mkdir()
        (preparation / "Dockerfile").write_text(DOCKERFILE)
        (evidence / "Dockerfile").write_text(DOCKERFILE)
        image = "cutbridge-verifier:" + args.trusted_sha
        command(["docker", "build", "--pull", "-t", image, str(preparation)], "dependency-preparation.log")
        command(["docker", "image", "inspect", image], "image.json")
        image_id = json.loads((evidence / "image.json").read_text())[0]["Id"]
        records["image_id"] = image_id
        output.mkdir(mode=0o755)
        for name in ("pycache", "tmp", "home"):
            (output / name).mkdir(mode=0o755)
        command(["sudo", "chown", "-R", "1000:1000", str(output)], "output-ownership.log")
        runner = root / "orchestration"
        runner.mkdir(mode=0o755)
        # Read the immutable trusted object, never a candidate or dirty worktree.
        script = git(repo, "cat-file", "blob", args.trusted_sha + ":tools/candidate_checks.sh")
        (runner / "checks.sh").write_bytes(script)
        (runner / "checks.sh").chmod(0o444)
        (evidence / "checks.sh").write_bytes(script)
        records["trusted_checks_sha256"] = digest(script)
        combined_before = ([{**item, "path": "candidate/" + item["path"]} for item in before]
                           + [{**item, "path": "verification-input/" + item["path"]} for item in regular_inventory(inputs)]
                           + [{**item, "path": "orchestration/" + item["path"]} for item in regular_inventory(runner)])
        (evidence / "manifest-before.sha256").write_bytes(manifest_bytes(combined_before))
        (evidence / "inventory-before.json").write_bytes(json_bytes(combined_before))
        mounts = [(str(snapshot), "/candidate", False), (str(output), "/candidate/verification-output", True),
                  (str(inputs), "/verification-input", False), (str(runner), "/orchestration", False)]
        create = ["docker", "create", "--network", "none", "--read-only", "--user", "1000:1000", "--cap-drop", "ALL",
                  "--security-opt", "no-new-privileges", "--pids-limit", "512", "--memory", "6g", "--cpus", "2", "--workdir", "/candidate"]
        for source, target, writable in mounts:
            create += ["--mount", f"type=bind,src={source},dst={target}" + ("" if writable else ",readonly")]
        for key, value in {"HOME": "/candidate/verification-output/home", "PYTHONPYCACHEPREFIX": "/candidate/verification-output/pycache",
                           "TEMP": "/candidate/verification-output/tmp", "TMP": "/candidate/verification-output/tmp", "TMPDIR": "/candidate/verification-output/tmp",
                           "CUTBRIDGE_VERSION": version, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}.items():
            create += ["--env", key + "=" + value]
        create += [image_id, "bash", "/orchestration/checks.sh", "--preflight"]
        command(create, "preflight-create.log")
        container = (evidence / "preflight-create.log").read_text().strip()
        if not re.fullmatch(r"[a-f0-9]{64}", container):
            raise RuntimeError("Docker preflight create returned no unique container ID")
        command(["docker", "inspect", container], "preflight-isolation.json")
        validate_isolation(json.loads((evidence / "preflight-isolation.json").read_text())[0], mounts)
        preflight_timeout = False
        records["commands"].append(["docker", "start", "--attach", container])
        try:
            with (evidence / "preflight.log").open("wb") as log:
                probe_exit = subprocess.run(["docker", "start", "--attach", container], stdout=log, stderr=subprocess.STDOUT, timeout=60).returncode
        except subprocess.TimeoutExpired:
            preflight_timeout, probe_exit = True, None
        command(["docker", "inspect", container], "preflight-after.json")
        probe_state = json.loads((evidence / "preflight-after.json").read_text())[0]["State"]
        preflight_verdict = classify_preflight(probe_state, probe_exit, preflight_timeout)
        command(["docker", "rm", "--force", container], "preflight-remove.log")
        removed = True
        if preflight_verdict == "INVALID":
            raise IntegrityError("trusted isolation probe failed; see preflight.log")
        if preflight_verdict != "PASS":
            raise RuntimeError("trusted preflight unavailable; see preflight-after.json")
        records["preflight_verdict"] = "PASS"
        create[-1] = "--checks"
        command(create, "container-create.log")
        container = (evidence / "container-create.log").read_text().strip()
        removed = False
        if not re.fullmatch(r"[a-f0-9]{64}", container):
            raise RuntimeError("Docker create returned no unique container ID")
        command(["docker", "inspect", container], "isolation-before.json")
        validate_isolation(json.loads((evidence / "isolation-before.json").read_text())[0], mounts)
        timed_out = False
        records["commands"].append(["docker", "start", "--attach", container])
        try:
            with (evidence / "checks.log").open("wb") as log:
                attach = subprocess.run(["docker", "start", "--attach", container], stdout=log, stderr=subprocess.STDOUT, timeout=900).returncode
        except subprocess.TimeoutExpired:
            timed_out, attach = True, None
        command(["docker", "inspect", container], "isolation-after.json")
        state = json.loads((evidence / "isolation-after.json").read_text())[0]["State"]
        verdict = classify_execution(state, attach, timed_out)
        reason = "canonical checks completed" if verdict == "PASS" else ("candidate command failed; see checks.log" if verdict == "FAIL" else "execution/attachment unavailable, timed out, or OOM; see isolation-after.json")
        command(["docker", "rm", "--force", container], "container-remove.log")
        removed = True
        # Preserve the observed after inventory even if an integrity comparison fails.
        after = regular_inventory(snapshot, allow_root_output=True)
        combined_after = ([{**item, "path": "candidate/" + item["path"]} for item in after]
                          + [{**item, "path": "verification-input/" + item["path"]} for item in regular_inventory(inputs)]
                          + [{**item, "path": "orchestration/" + item["path"]} for item in regular_inventory(runner)])
        (evidence / "manifest-after.sha256").write_bytes(manifest_bytes(combined_after))
        (evidence / "inventory-after.json").write_bytes(json_bytes(combined_after))
        verify_snapshot(snapshot, inventory)
        if combined_before != combined_after:
            raise IntegrityError("candidate/verification/orchestration inputs changed during execution")
        records["integrity_comparison"] = "identical exact paths/types/modes/bytes"
        if verdict == "PASS":
            if not (output / "dist-ci").exists() or not (output / "dist-repeat").exists():
                raise CandidateFailure("completed build did not create both required package directories")
            repeated = compare_packages(output / "dist-ci", output / "dist-repeat")
            (evidence / "repeated-package-inventory.json").write_bytes(json_bytes(repeated))
            validate_packages(output / "dist-ci", version)
        staged = stage_outputs(output, evidence)
        (evidence / "staged-output-inventory.json").write_bytes(json_bytes(staged))
    except IntegrityError as error:
        verdict, reason = "INVALID", str(error)
    except (CandidateFailure, zipfile.BadZipFile, UnicodeError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        verdict, reason = "FAIL", str(error)
    except Exception as error:
        verdict, reason = "INSUFFICIENT EVIDENCE", f"{type(error).__name__}: {error}"
    finally:
        if container and not removed:
            try:
                command(["docker", "rm", "--force", container], "container-cleanup.log", timeout=30)
            except Exception as error:
                verdict, reason = "INSUFFICIENT EVIDENCE", f"container cleanup failed: {error}; do not read/upload candidate outputs"
        records.update(verdict=verdict, reason=reason, finished_at_unix=int(time.time()))
        (evidence / "verification.json").write_bytes(json_bytes(records))
        (evidence / "verdict.txt").write_text(verdict + "\n")
        (evidence / "evidence.sha256").write_bytes(manifest_bytes(regular_inventory(evidence)))
        print(verdict + ": " + reason)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

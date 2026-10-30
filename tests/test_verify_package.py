"""Package-to-source verification must not depend on zlib or checkout line endings."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
TAG = "v" + next(
    line.split('"')[1] for line in (ROOT / "apps/blender/cutbridge/blender_manifest.toml").read_text(encoding="utf-8").splitlines()
    if line.startswith("version")
)


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _lf_snapshot(destination: Path) -> Path:
    """Copy build inputs with LF endings, as a clean ``git archive`` would."""
    sources = [ROOT / "LICENSE", ROOT / "tools/build_release.py"]
    sources += [p for p in (ROOT / "apps/after-effects").iterdir() if p.is_file()]
    sources += [
        p for p in (ROOT / "apps/blender/cutbridge").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pyo", ".zip"}
    ]
    for source in sources:
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes().replace(b"\r\n", b"\n"))
    return destination


@pytest.fixture(scope="module")
def candidate(tmp_path_factory):
    base = tmp_path_factory.mktemp("verify-package")
    source = _lf_snapshot(base / "source")
    builder = _module("test_snapshot_builder", source / "tools/build_release.py")
    builder.build(tag=TAG, output_dir=base / "candidate")
    return {
        "source": source,
        "dir": base / "candidate",
        "blender": base / "candidate" / f"CutBridge-Blender-{TAG}.zip",
        "after_effects": base / "candidate" / f"CutBridge-AfterEffects-{TAG}.zip",
    }


@pytest.fixture(scope="module")
def verifier():
    return _module("verify_package_under_test", ROOT / "tools/verify_package.py")


def _rewrite(src: Path, dst: Path, *, compression=zipfile.ZIP_DEFLATED, edit=None, drop=None, extra=None):
    with zipfile.ZipFile(src) as old, zipfile.ZipFile(dst, "w", compression=compression) as new:
        for info in old.infolist():
            if info.filename == drop:
                continue
            data = old.read(info)
            if edit and info.filename == edit[0]:
                data = edit[1](data)
            new.writestr(info.filename, data, compress_type=compression)
        if extra:
            new.writestr(extra[0], extra[1])


def _verify(verifier, candidate, tmp_path, blender, ae):
    return verifier.verify(candidate["source"], TAG, {"blender": blender, "after_effects": ae}, tmp_path)


def test_unmodified_candidate_matches_source_snapshot(verifier, candidate, tmp_path):
    report = _verify(verifier, candidate, tmp_path, candidate["blender"], candidate["after_effects"])
    assert report["ok"] is True
    for result in report["artifacts"].values():
        assert result["content_identical"] and result["zip_bytes_identical_to_rebuild"]
        assert result["zip_sha256"] == result["rebuilt_sha256_this_toolchain"]


def test_recompressed_zip_still_matches_by_content(verifier, candidate, tmp_path):
    """A different zlib/compression level changes ZIP bytes but not package identity."""
    stored_ae = tmp_path / candidate["after_effects"].name
    stored_bl = tmp_path / candidate["blender"].name
    _rewrite(candidate["after_effects"], stored_ae, compression=zipfile.ZIP_STORED)
    _rewrite(candidate["blender"], stored_bl, compression=zipfile.ZIP_STORED)
    report = _verify(verifier, candidate, tmp_path / "work", stored_bl, stored_ae)
    assert report["ok"] is True
    assert all(not r["zip_bytes_identical_to_rebuild"] for r in report["artifacts"].values())
    assert all(r["content_identical"] for r in report["artifacts"].values())


def test_changed_entry_is_reported(verifier, candidate, tmp_path):
    tampered = tmp_path / candidate["after_effects"].name
    _rewrite(candidate["after_effects"], tampered, edit=("qc_plus.js", lambda data: data + b"\n// tampered\n"))
    report = _verify(verifier, candidate, tmp_path / "work", candidate["blender"], tampered)
    ae = report["artifacts"]["after_effects"]
    assert report["ok"] is False and ae["ok"] is False
    assert ae["changed_entries"] == ["qc_plus.js"]
    assert report["artifacts"]["blender"]["ok"] is True


def test_missing_and_unexpected_entries_are_reported(verifier, candidate, tmp_path):
    altered = tmp_path / candidate["blender"].name
    _rewrite(candidate["blender"], altered, drop="LICENSE", extra=("payload.pyc", b"x"))
    report = _verify(verifier, candidate, tmp_path / "work", altered, candidate["after_effects"])
    blender = report["artifacts"]["blender"]
    assert blender["ok"] is False
    assert blender["missing_entries"] == ["LICENSE"]
    assert blender["unexpected_entries"] == ["payload.pyc"]


def test_unsafe_entry_names_and_wrong_filename_fail(verifier, candidate, tmp_path):
    evil = tmp_path / candidate["after_effects"].name
    _rewrite(candidate["after_effects"], evil, extra=("../escape.txt", b"x"))
    unsafe = _verify(verifier, candidate, tmp_path / "work1", candidate["blender"], evil)
    assert unsafe["artifacts"]["after_effects"]["unsafe_entry_names"] == ["../escape.txt"]
    assert unsafe["ok"] is False

    renamed = tmp_path / "CutBridge-AfterEffects-v9.9.9.zip"
    shutil.copyfile(candidate["after_effects"], renamed)
    wrong_name = _verify(verifier, candidate, tmp_path / "work2", candidate["blender"], renamed)
    assert wrong_name["artifacts"]["after_effects"]["content_identical"] is True
    assert wrong_name["artifacts"]["after_effects"]["ok"] is False


def test_source_change_after_packaging_is_detected(verifier, candidate, tmp_path):
    """A candidate built from different source must not verify against the named snapshot."""
    other = _lf_snapshot(tmp_path / "other-source")
    target = other / "apps/after-effects/localization.js"
    target.write_bytes(target.read_bytes() + b"\n// drift\n")
    drifted = _module("drifted_builder", other / "tools/build_release.py")
    drifted.build(tag=TAG, output_dir=tmp_path / "drifted")
    report = _verify(
        verifier, candidate, tmp_path / "work",
        tmp_path / "drifted" / candidate["blender"].name,
        tmp_path / "drifted" / candidate["after_effects"].name,
    )
    assert report["ok"] is False
    assert report["artifacts"]["after_effects"]["changed_entries"] == ["localization.js"]
    assert report["artifacts"]["blender"]["ok"] is True

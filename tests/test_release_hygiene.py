"""Release safety regressions runnable without Blender or third-party packages."""

import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class ReleaseHygieneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        shutil.copytree(ROOT / "apps", self.root / "apps")
        if (ROOT / "LICENSE").exists():
            shutil.copy2(ROOT / "LICENSE", self.root / "LICENSE")
        spec = importlib.util.spec_from_file_location("release_hygiene", ROOT / "tools/build_release.py")
        self.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.builder)
        self.builder.ROOT = self.root
        self.builder.BLENDER_ROOT = self.root / "apps/blender/cutbridge"
        self.builder.AE_SCRIPT = self.root / "apps/after-effects/CutBridge.jsx"
        self.builder.AE_REVISION = self.root / "apps/after-effects/revision_manager.js"
        self.builder.AE_INSTALL = self.root / "apps/after-effects/INSTALL.md"
        self.output = Path(self.temp.name) / "dist"

    def test_identical_sources_produce_identical_artifacts(self):
        self.builder.build("v0.2.3", self.output)
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        for path in self.root.rglob("*"):
            if path.is_file():
                os.utime(path, (946684800, 946684800))
                path.chmod(0o600)
        self.builder.build("v0.2.3", self.output)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})

    def test_unrelated_output_is_never_deleted(self):
        self.output.mkdir()
        marker = self.output / "unrelated.txt"
        marker.write_text("preserve me", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.builder.build("v0.2.3", self.output)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve me")
        self.assertEqual(list(self.output.iterdir()), [marker])

    def test_source_directory_cannot_be_used_as_output(self):
        before = self.builder.AE_SCRIPT.read_bytes()
        with self.assertRaises(ValueError):
            self.builder.build("v0.2.3", self.builder.AE_SCRIPT.parent)
        self.assertEqual(self.builder.AE_SCRIPT.read_bytes(), before)

    def test_both_packages_include_declared_license(self):
        self.builder.build("v0.2.3", self.output)
        for archive_path in self.output.glob("*.zip"):
            with self.subTest(archive=archive_path.name), zipfile.ZipFile(archive_path) as archive:
                self.assertIn("LICENSE", archive.namelist())
                self.assertEqual(archive.read("LICENSE"), (ROOT / "LICENSE").read_bytes())

    def test_tag_mismatch_preserves_output(self):
        self.builder.build("v0.2.3", self.output)
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        with self.assertRaises(ValueError):
            self.builder.build("v9.9.9", self.output)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})

    def test_version_constant_mismatch_is_rejected(self):
        source = self.builder.BLENDER_ROOT / "version.py"
        source.write_text(source.read_text().replace("VERSION = (0, 2, 3)", "VERSION = (0, 2, 2)"))
        with self.assertRaises(ValueError):
            self.builder.build("v0.2.3", self.output)
        self.assertFalse(self.output.exists())

    def test_ae_version_mismatch_is_rejected_before_output(self):
        source = self.builder.AE_SCRIPT
        source.write_text(source.read_text(encoding="utf-8").replace(
            'var PRODUCT_VERSION = "0.2.3";', 'var PRODUCT_VERSION = "0.2.2";'), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "PRODUCT_VERSION"):
            self.builder.build("v0.2.3", self.output)
        self.assertFalse(self.output.exists())

    def test_artifact_symlink_cannot_overwrite_another_file(self):
        self.output.mkdir()
        victim = Path(self.temp.name) / "preserve.txt"
        victim.write_text("preserve me")
        (self.output / "CutBridge-Blender-v0.2.3.zip").symlink_to(victim)
        with self.assertRaises(ValueError):
            self.builder.build("v0.2.3", self.output)
        self.assertEqual(victim.read_text(), "preserve me")

    def test_rc_build_uses_beta_prerelease_metadata(self):
        metadata = self.builder.build("v0.2.3-rc.1", self.output)
        self.assertEqual(metadata["version"], "0.2.3-rc.1")
        self.assertEqual(metadata["product_version"], "0.2.3")
        self.assertEqual(metadata["channel"], "beta")
        self.assertIs(metadata["prerelease"], True)
        self.assertTrue((self.output / "CutBridge-Blender-v0.2.3-rc.1.zip").is_file())
        self.assertTrue((self.output / "CutBridge-AfterEffects-v0.2.3-rc.1.zip").is_file())

    def test_development_build_uses_development_channel(self):
        metadata = self.builder.build("v0.2.3-dev.1", self.output)
        self.assertEqual(metadata["version"], "0.2.3-dev.1")
        self.assertEqual(metadata["channel"], "development")
        self.assertIs(metadata["prerelease"], True)

    def test_release_workflow_publishes_verification_assets(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        marker = "- name: Publish GitHub Release"
        self.assertIn(marker, workflow)
        publish_step = workflow.split(marker, 1)[1]
        self.assertIn("dist/SHA256SUMS.txt", publish_step)
        self.assertIn("dist/release-metadata.json", publish_step)


if __name__ == "__main__":
    unittest.main()

"""Run S6 contract regressions in the complete pytest suite as well as CI."""
from pathlib import Path
import shutil
import subprocess


def test_revision_contract():
    node = shutil.which("node")
    assert node, "Node is required for S6 revision contract tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests/ae_s6_revision_checks.cjs")], cwd=root, check=True)


def test_native_revision_lifecycle_preserves_retired_footage_provenance():
    """Retired CutBridge footage must not become an unmanaged S5 collision."""
    root = Path(__file__).resolve().parents[1]
    source = (root / "apps/after-effects/CutBridge.jsx").read_text(encoding="utf-8")

    assert 'setItemComment(item.oldSource, item.oldComment);' in source
    assert 'setItemComment(item.oldSource, "");' not in source
    assert 'setItemComment(item.replacement, CutBridgeContract.managedTag("footage", newManifest, passName));' in source


def test_revision_confirmation_fails_closed_when_host_dialog_is_unavailable():
    root = Path(__file__).resolve().parents[1]
    source = (root / "apps/after-effects/CutBridge.jsx").read_text(encoding="utf-8")

    assert 'if (typeof confirm !== "function") throw new Error("After Effects confirmation UI is unavailable; revision was not applied.");' in source
    assert 'if (!confirm(message)) return;' in source

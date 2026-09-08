"""Release publication authorization and channel regressions."""

from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_release import parse_release_tag  # noqa: E402
from validate_release_authorization import validate_authorization  # noqa: E402


def _workflow_uses_are_pinned(workflow: str) -> bool:
    uses = re.findall(r"^\s*- uses: ([^\s#]+)", workflow, flags=re.MULTILINE)
    return bool(uses) and all(re.fullmatch(r"[^@\s]+@[0-9a-f]{40}", item) for item in uses)


def test_release_tag_channels_are_explicit():
    stable = parse_release_tag("v0.2.3")
    assert stable == {
        "tag": "v0.2.3",
        "base_version": "0.2.3",
        "release_version": "0.2.3",
        "channel": "stable",
        "prerelease": False,
    }

    rc = parse_release_tag("v0.2.3-rc.1")
    assert rc["base_version"] == "0.2.3"
    assert rc["release_version"] == "0.2.3-rc.1"
    assert rc["channel"] == "beta"
    assert rc["prerelease"] is True

    beta = parse_release_tag("v0.2.3-beta.2")
    assert beta["channel"] == "beta"
    assert beta["prerelease"] is True

    development = parse_release_tag("v0.2.3-dev.3")
    assert development["channel"] == "development"
    assert development["prerelease"] is True


@pytest.mark.parametrize(
    "tag",
    [
        "0.2.3",
        "v0.2",
        "v0.2.3-rc",
        "v0.2.3-rc.0",
        "v0.2.3-preview.1",
        "v0.2.3+build.1",
    ],
)
def test_unsupported_release_tag_forms_fail_closed(tag):
    with pytest.raises(ValueError):
        parse_release_tag(tag)


def test_release_authorization_requires_current_main_and_exact_metadata():
    approval = {
        "approved": True,
        "tag": "v0.2.3-rc.1",
        "channel": "beta",
        "prerelease": True,
    }
    release = validate_authorization(
        approval=approval,
        tag="v0.2.3-rc.1",
        release_sha="abc123",
        main_sha="abc123",
    )
    assert release["channel"] == "beta"
    assert release["prerelease"] is True

    with pytest.raises(ValueError, match="current main"):
        validate_authorization(
            approval=approval,
            tag="v0.2.3-rc.1",
            release_sha="feature-sha",
            main_sha="main-sha",
        )


@pytest.mark.parametrize(
    "override, message",
    [
        ({"approved": False}, "not approved"),
        ({"tag": "v0.2.3"}, "Authorization tag"),
        ({"channel": "stable"}, "Authorization channel"),
        ({"prerelease": False}, "prerelease flag"),
    ],
)
def test_release_authorization_rejects_mismatched_approval(override, message):
    approval = {
        "approved": True,
        "tag": "v0.2.3-rc.1",
        "channel": "beta",
        "prerelease": True,
    }
    approval.update(override)
    with pytest.raises(ValueError, match=message):
        validate_authorization(
            approval=approval,
            tag="v0.2.3-rc.1",
            release_sha="same-sha",
            main_sha="same-sha",
        )


def test_release_workflow_separates_read_only_packaging_from_write_publication():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

    assert "permissions:\n  contents: read" in workflow
    assert "package:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: read" in workflow
    assert "publish:\n    needs: package\n    runs-on: ubuntu-latest\n    permissions:\n      contents: write" in workflow
    assert workflow.count("validate_release_authorization.py") == 2
    assert "actions/upload-artifact@" in workflow
    assert "actions/download-artifact@" in workflow
    assert "Revalidate downloaded release bundle" in workflow
    assert "fail_on_unmatched_files: true" in workflow
    assert workflow.index("Upload validated release bundle") < workflow.index("\n  publish:")
    assert workflow.index("\n  publish:") < workflow.index("uses: softprops/action-gh-release@")


def test_release_workflow_pins_actions_and_does_not_persist_git_credentials():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

    assert _workflow_uses_are_pinned(workflow)
    assert "@v4" not in workflow and "@v5" not in workflow and "@v2" not in workflow
    assert workflow.count("persist-credentials: false") == 2
    assert "concurrency:\n  group: release-${{ github.ref }}\n  cancel-in-progress: false" in workflow


def test_ci_workflow_is_read_only_and_pins_actions():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "permissions:\n  contents: read" in workflow
    assert _workflow_uses_are_pinned(workflow)
    assert "@v4" not in workflow and "@v5" not in workflow
    assert workflow.count("persist-credentials: false") == 2

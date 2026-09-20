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


def test_release_workflow_uses_validate_clean_package_and_write_only_publish_jobs():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

    assert "permissions:\n  contents: read" in workflow
    assert "validate:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: read" in workflow
    assert "package:\n    needs: validate\n    runs-on: ubuntu-latest\n    permissions:\n      contents: read" in workflow
    assert "publish:\n    needs: package\n    runs-on: ubuntu-latest\n    permissions:\n      contents: write" in workflow
    assert workflow.count("validate_release_authorization.py") == 3

    validate_start = workflow.index("\n  validate:")
    package_start = workflow.index("\n  package:")
    publish_start = workflow.index("\n  publish:")
    validate_section = workflow[validate_start:package_start]
    package_section = workflow[package_start:publish_start]
    publish_section = workflow[publish_start:]

    assert "Install test dependencies" in validate_section
    assert "pip install" in validate_section
    assert "Build versioned packages" not in validate_section
    assert "pip install" not in package_section
    assert "Build versioned packages on clean runner" in package_section
    assert "Upload validated release bundle" in package_section
    assert "pip install" not in publish_section
    assert "Download validated release bundle" in publish_section
    assert "Revalidate downloaded release bundle" in publish_section
    assert "uses: softprops/action-gh-release@" in publish_section
    assert "fail_on_unmatched_files: true" in publish_section


def test_release_publish_revalidates_exact_metadata_identity():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

    for token in [
        "EXPECTED_RELEASE_VERSION",
        "EXPECTED_PRODUCT_VERSION",
        'metadata.get("version")',
        'metadata.get("product_version")',
        'CutBridge-Blender-{tag}.zip',
        'CutBridge-AfterEffects-{tag}.zip',
    ]:
        assert token in workflow


def test_release_workflow_pins_actions_and_does_not_persist_git_credentials():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

    assert _workflow_uses_are_pinned(workflow)
    assert "@v4" not in workflow and "@v5" not in workflow and "@v2" not in workflow
    assert workflow.count("persist-credentials: false") == 3
    assert workflow.count("fetch-depth: 0") == 3
    assert "git fetch origin main" not in workflow
    assert workflow.count("refs/remotes/origin/main^{commit}") == 3
    assert "concurrency:\n  group: release-${{ github.ref }}\n  cancel-in-progress: false" in workflow


def test_ci_workflow_is_read_only_and_pins_actions():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "permissions:\n  contents: read" in workflow
    assert _workflow_uses_are_pinned(workflow)
    assert "@v4" not in workflow and "@v5" not in workflow
    assert workflow.count("persist-credentials: false") == 2


def test_codeowners_covers_release_sensitive_controls():
    codeowners = (ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")

    assert "* @Unn0wn002" in codeowners
    for required in [
        "/.github/workflows/ @Unn0wn002",
        "/release-authorization.json @Unn0wn002",
        "/tools/validate_release_authorization.py @Unn0wn002",
        "/tools/build_release.py @Unn0wn002",
        "/docs/RELEASE_CHECKLIST.md @Unn0wn002",
        "/docs/RELEASE_READINESS.md @Unn0wn002",
    ]:
        assert required in codeowners

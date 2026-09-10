import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "s14" / "validate_evidence.py"
TEMPLATE_PATH = ROOT / "tools" / "s14" / "evidence-template.json"

spec = importlib.util.spec_from_file_location("s14_validate_evidence", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def template():
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def participant(number: int, candidate_sha: str):
    tasks = []
    for task in template()["task_catalog"]:
        tasks.append(
            {
                "id": task["id"],
                "status": "PASS" if task["id"] != "JP12" else "NOT_APPLICABLE",
                "evidence": [f"evidence/jp-u{number:02d}-{task['id'].lower()}.md"],
                "observed_behavior": "Participant completed the assigned task under the recorded protocol.",
                "participant_statement": None,
                "moderator_intervention": None,
                "unassisted": True,
            }
        )
    return {
        "participant_id": f"JP-U{number:02d}",
        "representative": True,
        "role_category": "animation-compositing",
        "experience_band": "intermediate-production",
        "executed": True,
        "candidate_sha": candidate_sha,
        "tasks": tasks,
    }


def pass_record():
    record = template()
    sha = "a" * 40
    record["overall_state"] = "PASS"
    record["candidate"] = {
        "source_sha": sha,
        "product_version": "0.2.3",
        "blender_artifact": {"filename": "CutBridge-Blender-v0.2.3-s14.zip", "sha256": "b" * 64},
        "after_effects_artifact": {"filename": "CutBridge-AfterEffects-v0.2.3-s14.zip", "sha256": "c" * 64},
        "fixture": {"id": "cutbridge-s14-synthetic-v1", "provenance": "synthetic-original", "sha256": "d" * 64},
        "blender_host": {"version": "5.2.1 LTS", "os": "Windows 11"},
        "after_effects_host": {"version": "2026 26.3x87", "os": "Windows 11"},
    }
    record["participants"] = [participant(1, sha), participant(2, sha), participant(3, sha)]
    record["summary"] = {
        "claim_scope": "Japanese target-user tasks JP01-JP11 on the recorded v0.2.3 candidate; JP12 excluded from normal release-facing scope.",
        "statement": "All required recorded S14 tasks passed under the documented conditions.",
        "limitations": ["Internal minimum cohort; not statistical population evidence."],
    }
    return record


def test_committed_template_is_valid_and_not_executed():
    record = template()
    assert record["overall_state"] == "NOT_EXECUTED"
    assert record["participants"] == []
    assert validator.validate(record) == []


def test_not_executed_cannot_contain_participant_evidence():
    record = template()
    record["participants"] = [participant(1, "a" * 40)]
    errors = validator.validate(record)
    assert any("NOT_EXECUTED requires participants to be empty" in error for error in errors)


def test_pass_requires_three_distinct_representative_participants():
    record = pass_record()
    record["participants"] = record["participants"][:2]
    errors = validator.validate(record)
    assert any("at least 3 distinct representative participants" in error for error in errors)

    record = pass_record()
    record["participants"][1]["participant_id"] = record["participants"][0]["participant_id"]
    errors = validator.validate(record)
    assert any("duplicate participant_id" in error for error in errors)

    record = pass_record()
    record["participants"][0]["representative"] = False
    errors = validator.validate(record)
    assert any("representative must be true" in error for error in errors)


def test_pass_requires_all_core_tasks_for_every_participant():
    record = pass_record()
    record["participants"][1]["tasks"][3]["status"] = "FAIL"
    errors = validator.validate(record)
    assert any("JP04=PASS" in error for error in errors)


def test_optional_jp12_may_be_not_applicable_but_core_tasks_may_not():
    record = pass_record()
    assert validator.validate(record) == []

    record["participants"][0]["tasks"][0]["status"] = "NOT_APPLICABLE"
    errors = validator.validate(record)
    assert any("JP01 is required and cannot be NOT_APPLICABLE" in error for error in errors)


def test_executed_task_requires_evidence_and_observed_behavior():
    record = pass_record()
    record["participants"][0]["tasks"][0]["evidence"] = []
    errors = validator.validate(record)
    assert any("requires at least one evidence reference" in error for error in errors)

    record = pass_record()
    record["participants"][0]["tasks"][0]["observed_behavior"] = ""
    errors = validator.validate(record)
    assert any("requires observed_behavior" in error for error in errors)


def test_moderator_assistance_cannot_be_labeled_unassisted_pass():
    record = pass_record()
    task = record["participants"][0]["tasks"][0]
    task["moderator_intervention"] = "Moderator gave step-by-step navigation help."
    task["unassisted"] = True
    errors = validator.validate(record)
    assert any("cannot be unassisted PASS" in error for error in errors)


def test_pass_rejects_open_blocker_or_major_finding():
    for severity in ("BLOCKER", "MAJOR"):
        record = pass_record()
        record["findings"] = [
            {
                "id": f"F-{severity}",
                "severity": severity,
                "status": "OPEN",
                "task_ids": ["JP04"],
                "description": "Material unresolved usability or safety finding.",
                "evidence": ["evidence/finding.md"],
            }
        ]
        errors = validator.validate(record)
        assert any("unresolved BLOCKER or MAJOR" in error for error in errors)


def test_fail_repair_required_needs_real_failure_signal():
    record = template()
    record["overall_state"] = "FAIL_REPAIR_REQUIRED"
    record["participants"] = [participant(1, "a" * 40)]
    errors = validator.validate(record)
    assert any("requires a failed/blocked task or open BLOCKER/MAJOR" in error for error in errors)

    record = template()
    record["overall_state"] = "FAIL_REPAIR_REQUIRED"
    p = participant(1, "a" * 40)
    p["tasks"][4]["status"] = "BLOCKED"
    record["participants"] = [p]
    assert validator.validate(record) == []


def test_pass_requires_candidate_hashes_hosts_fixture_and_summary():
    record = pass_record()
    assert validator.validate(record) == []

    variants = []
    missing_hash = copy.deepcopy(record)
    missing_hash["candidate"]["blender_artifact"]["sha256"] = None
    variants.append(missing_hash)

    bad_fixture = copy.deepcopy(record)
    bad_fixture["candidate"]["fixture"]["provenance"] = "third-party-unknown"
    variants.append(bad_fixture)

    missing_summary = copy.deepcopy(record)
    missing_summary["summary"]["statement"] = None
    variants.append(missing_summary)

    for invalid in variants:
        assert validator.validate(invalid)


def test_participant_identifying_fields_are_rejected():
    record = pass_record()
    record["participants"][0]["email"] = "user@example.test"
    errors = validator.validate(record)
    assert any("forbidden identifying fields" in error for error in errors)


def test_pass_requires_all_participants_on_final_candidate():
    record = pass_record()
    record["participants"][2]["candidate_sha"] = "e" * 40
    errors = validator.validate(record)
    assert any("must match final PASS candidate.source_sha" in error for error in errors)

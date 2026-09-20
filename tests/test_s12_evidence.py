import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "s12" / "validate_evidence.py"
TEMPLATE_PATH = ROOT / "tools" / "s12" / "evidence-template.json"

spec = importlib.util.spec_from_file_location("s12_validate_evidence", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def template():
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def make_pass_record():
    record = template()
    record["overall_state"] = "PASS"
    record["candidate"]["blender_artifact"] = {
        "filename": "CutBridge-Blender-v0.2.3-s12.zip",
        "sha256": "a" * 64,
    }
    record["candidate"]["after_effects_artifact"] = {
        "filename": "CutBridge-AfterEffects-v0.2.3-s12.zip",
        "sha256": "b" * 64,
    }
    record["environment"]["blender"] = {
        "executed": True,
        "version": "5.2.1 LTS",
        "os": "Windows 11",
    }
    record["environment"]["after_effects"] = {
        "executed": True,
        "version": "2026 Build 87",
        "os": "Windows 11",
    }
    record["fixture"]["sha256"] = "c" * 64
    for gate in record["gates"]:
        gate["status"] = "PASS"
        gate["evidence"] = [f"evidence/{gate['id'].lower()}.txt"]
    return record


def test_template_is_valid_but_explicitly_not_executed():
    record = template()
    assert record["overall_state"] == "NOT_EXECUTED"
    assert validator.validate(record) == []


def test_not_executed_cannot_hide_attempted_gate():
    record = template()
    record["gates"][0]["status"] = "PASS"
    record["gates"][0]["evidence"] = ["evidence/install.txt"]
    errors = validator.validate(record)
    assert errors
    assert "NOT_EXECUTED requires every gate" in errors[0]


def test_pass_requires_real_hosts_and_all_gates():
    record = template()
    record["overall_state"] = "PASS"
    errors = validator.validate(record)
    assert errors
    assert "PASS requires real Blender and After Effects execution" in errors[0]


def test_pass_requires_artifact_and_fixture_checksums():
    record = make_pass_record()
    record["candidate"]["blender_artifact"]["sha256"] = None
    errors = validator.validate(record)
    assert errors
    assert "candidate.blender_artifact.sha256" in errors[0]


def test_pass_requires_evidence_for_every_gate():
    record = make_pass_record()
    record["gates"][3]["evidence"] = []
    errors = validator.validate(record)
    assert errors
    assert "must contain at least one real evidence reference" in errors[0]


def test_complete_pass_record_is_structurally_valid():
    record = make_pass_record()
    assert validator.validate(record) == []


def test_fail_repair_required_needs_a_real_failed_gate():
    record = template()
    record["overall_state"] = "FAIL_REPAIR_REQUIRED"
    errors = validator.validate(record)
    assert errors
    assert "requires at least one failed gate" in errors[0]

    record = template()
    record["overall_state"] = "FAIL_REPAIR_REQUIRED"
    record["environment"]["blender"]["executed"] = True
    record["gates"][0]["status"] = "FAIL"
    record["gates"][0]["evidence"] = ["evidence/install-failure.txt"]
    assert validator.validate(record) == []


def test_gate_set_is_exact_and_duplicate_ids_fail():
    record = template()
    record["gates"] = copy.deepcopy(record["gates"][:-1])
    errors = validator.validate(record)
    assert errors
    assert "missing required gates" in errors[0]

    record = template()
    record["gates"].append(copy.deepcopy(record["gates"][0]))
    errors = validator.validate(record)
    assert errors
    assert "duplicate gate id" in errors[0]

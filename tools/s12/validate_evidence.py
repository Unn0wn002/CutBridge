#!/usr/bin/env python3
"""Validate CutBridge S12 real-host evidence without inferring native success.

This validator checks record completeness and internal consistency only. It never
executes Blender or After Effects, and a successful validator run is not itself
native-host evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cutbridge-s12-e2e-evidence"
SCHEMA_VERSION = 1
OVERALL_STATES = {"NOT_EXECUTED", "IN_PROGRESS", "PASS", "FAIL_REPAIR_REQUIRED"}
GATE_STATES = {"NOT_EXECUTED", "PASS", "FAIL"}
REQUIRED_GATES = (
    "B_INSTALL",
    "B_VALIDATE_MANUAL",
    "B_STUDIO_PRESET",
    "B_HANDOFF_3D",
    "B_BUILD_V001",
    "B_RENDER_REAL",
    "B_BUILD_V002_V003",
    "AE_LOAD_RUNTIME",
    "AE_BUILD_V001",
    "AE_QC_V001",
    "AE_S10C_CAMERA_NULL",
    "AE_REVISION_V002",
    "AE_REVISION_V003",
    "AE_ARTIST_STATE_PRESERVATION",
    "AE_SAVE_CLOSE_REOPEN",
    "PATH_UNICODE",
    "EVIDENCE_ARCHIVE",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class EvidenceError(ValueError):
    pass


def _obj(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvidenceError(f"{path} must be an object")
    return value


def _list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise EvidenceError(f"{path} must be an array")
    return value


def _nonempty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{path} must be a non-empty string")
    return value.strip()


def _sha256(value: Any, path: str) -> str:
    value = _nonempty_string(value, path).lower()
    if not SHA256_RE.fullmatch(value):
        raise EvidenceError(f"{path} must be a lowercase 64-character SHA-256")
    return value


def _evidence_refs(value: Any, path: str, *, required: bool) -> list[str]:
    refs = _list(value, path)
    cleaned: list[str] = []
    for index, item in enumerate(refs):
        cleaned.append(_nonempty_string(item, f"{path}[{index}]"))
    if required and not cleaned:
        raise EvidenceError(f"{path} must contain at least one real evidence reference")
    return cleaned


def validate(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    try:
        if record.get("schema") != SCHEMA:
            raise EvidenceError(f"schema must be {SCHEMA!r}")
        if record.get("schema_version") != SCHEMA_VERSION:
            raise EvidenceError(f"schema_version must be {SCHEMA_VERSION}")

        overall = record.get("overall_state")
        if overall not in OVERALL_STATES:
            raise EvidenceError(f"overall_state must be one of {sorted(OVERALL_STATES)}")

        candidate = _obj(record.get("candidate"), "candidate")
        develop_sha = _nonempty_string(candidate.get("develop_sha"), "candidate.develop_sha").lower()
        if not COMMIT_RE.fullmatch(develop_sha):
            raise EvidenceError("candidate.develop_sha must be a lowercase 40-character commit SHA")

        blender_artifact = _obj(candidate.get("blender_artifact"), "candidate.blender_artifact")
        ae_artifact = _obj(candidate.get("after_effects_artifact"), "candidate.after_effects_artifact")

        environment = _obj(record.get("environment"), "environment")
        blender_env = _obj(environment.get("blender"), "environment.blender")
        ae_env = _obj(environment.get("after_effects"), "environment.after_effects")
        for name, env in (("blender", blender_env), ("after_effects", ae_env)):
            if not isinstance(env.get("executed"), bool):
                raise EvidenceError(f"environment.{name}.executed must be boolean")

        fixture = _obj(record.get("fixture"), "fixture")
        _nonempty_string(fixture.get("id"), "fixture.id")
        source_type = _nonempty_string(fixture.get("source_type"), "fixture.source_type")
        if source_type not in {"synthetic-original", "user-owned-original"}:
            raise EvidenceError("fixture.source_type must be synthetic-original or user-owned-original")
        _nonempty_string(fixture.get("provenance"), "fixture.provenance")

        gates = _list(record.get("gates"), "gates")
        by_id: dict[str, dict[str, Any]] = {}
        for index, raw_gate in enumerate(gates):
            gate = _obj(raw_gate, f"gates[{index}]")
            gate_id = _nonempty_string(gate.get("id"), f"gates[{index}].id")
            if gate_id in by_id:
                raise EvidenceError(f"duplicate gate id: {gate_id}")
            if gate_id not in REQUIRED_GATES:
                raise EvidenceError(f"unknown gate id: {gate_id}")
            status = gate.get("status")
            if status not in GATE_STATES:
                raise EvidenceError(f"gate {gate_id} status must be one of {sorted(GATE_STATES)}")
            _evidence_refs(gate.get("evidence"), f"gate {gate_id}.evidence", required=status in {"PASS", "FAIL"})
            by_id[gate_id] = gate

        missing = [gate_id for gate_id in REQUIRED_GATES if gate_id not in by_id]
        if missing:
            raise EvidenceError("missing required gates: " + ", ".join(missing))
        if len(by_id) != len(REQUIRED_GATES):
            raise EvidenceError("gate set must exactly match the required S12 gate set")

        statuses = [by_id[gate_id]["status"] for gate_id in REQUIRED_GATES]

        if overall == "NOT_EXECUTED":
            if blender_env["executed"] or ae_env["executed"]:
                raise EvidenceError("NOT_EXECUTED requires both real hosts executed=false")
            if any(status != "NOT_EXECUTED" for status in statuses):
                raise EvidenceError("NOT_EXECUTED requires every gate to remain NOT_EXECUTED")

        elif overall == "IN_PROGRESS":
            if all(status == "NOT_EXECUTED" for status in statuses):
                raise EvidenceError("IN_PROGRESS requires at least one attempted gate")
            if all(status == "PASS" for status in statuses):
                raise EvidenceError("IN_PROGRESS is inconsistent when every required gate is PASS")

        elif overall == "FAIL_REPAIR_REQUIRED":
            if "FAIL" not in statuses:
                raise EvidenceError("FAIL_REPAIR_REQUIRED requires at least one failed gate")

        elif overall == "PASS":
            if not blender_env["executed"] or not ae_env["executed"]:
                raise EvidenceError("PASS requires real Blender and After Effects execution")
            if any(status != "PASS" for status in statuses):
                raise EvidenceError("PASS requires every required gate to be PASS")

            _nonempty_string(blender_env.get("version"), "environment.blender.version")
            _nonempty_string(blender_env.get("os"), "environment.blender.os")
            _nonempty_string(ae_env.get("version"), "environment.after_effects.version")
            _nonempty_string(ae_env.get("os"), "environment.after_effects.os")

            _nonempty_string(blender_artifact.get("filename"), "candidate.blender_artifact.filename")
            _sha256(blender_artifact.get("sha256"), "candidate.blender_artifact.sha256")
            _nonempty_string(ae_artifact.get("filename"), "candidate.after_effects_artifact.filename")
            _sha256(ae_artifact.get("sha256"), "candidate.after_effects_artifact.sha256")
            _sha256(fixture.get("sha256"), "fixture.sha256")

            # Evidence refs are checked per gate above. Requiring every PASS gate
            # to have at least one reference prevents an empty all-green record.

    except EvidenceError as exc:
        errors.append(str(exc))

    return errors


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"could not read evidence JSON: {exc}") from exc
    return _obj(data, "root")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args(argv)

    try:
        record = load(args.evidence)
    except EvidenceError as exc:
        print(f"S12 evidence INVALID: {exc}", file=sys.stderr)
        return 2

    errors = validate(record)
    if errors:
        for error in errors:
            print(f"S12 evidence INVALID: {error}", file=sys.stderr)
        return 1

    print(f"S12 evidence VALID: state={record['overall_state']}")
    if record["overall_state"] != "PASS":
        print("Native S12 PASS has not been established by this record.")
    else:
        print("Record is structurally eligible for S12 PASS; review referenced native evidence manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

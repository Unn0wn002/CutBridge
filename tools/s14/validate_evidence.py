#!/usr/bin/env python3
"""Fail-closed structural validator for CutBridge S14 target-user evidence."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_TASKS = tuple(f"JP{i:02d}" for i in range(1, 13))
REQUIRED_TASKS = set(EXPECTED_TASKS[:11])
OVERALL_STATES = {"NOT_EXECUTED", "IN_PROGRESS", "FAIL_REPAIR_REQUIRED", "PASS"}
TASK_STATES = {"NOT_RUN", "PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE"}
SEVERITIES = {"BLOCKER", "MAJOR", "MINOR", "NOTE"}
FINDING_STATES = {"OPEN", "RESOLVED"}
EXPERIENCE_BANDS = {"beginner-production", "intermediate-production", "advanced-production"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PARTICIPANT_KEYS = {
    "name",
    "full_name",
    "email",
    "phone",
    "employer",
    "studio",
    "company",
    "account_id",
    "github_username",
}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_hash(value: Any, regex: re.Pattern[str]) -> bool:
    return isinstance(value, str) and bool(regex.fullmatch(value))


def _participant_task_map(participant: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tasks = participant.get("tasks")
    if not isinstance(tasks, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for item in tasks:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result[item["id"]] = item
    return result


def validate(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["root must be an object"]

    if record.get("schema") != "cutbridge-s14-target-user-evidence":
        errors.append("schema must be cutbridge-s14-target-user-evidence")
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if record.get("protocol_version") != 1:
        errors.append("protocol_version must be 1")

    state = record.get("overall_state")
    if state not in OVERALL_STATES:
        errors.append(f"overall_state must be one of {sorted(OVERALL_STATES)}")

    minimum = record.get("minimum_participants")
    if minimum != 3:
        errors.append("minimum_participants must remain 3 for protocol version 1")

    catalog = record.get("task_catalog")
    if not isinstance(catalog, list):
        errors.append("task_catalog must be a list")
    else:
        ids = [item.get("id") for item in catalog if isinstance(item, dict)]
        if ids != list(EXPECTED_TASKS):
            errors.append("task_catalog must contain JP01..JP12 exactly once and in order")
        for item in catalog:
            if not isinstance(item, dict):
                continue
            task_id = item.get("id")
            expected_required = task_id in REQUIRED_TASKS
            if item.get("required") is not expected_required:
                errors.append(f"{task_id}.required must be {expected_required}")

    participants = record.get("participants")
    if not isinstance(participants, list):
        errors.append("participants must be a list")
        participants = []

    participant_ids: set[str] = set()
    executed_count = 0
    any_failed_task = False

    for index, participant in enumerate(participants):
        prefix = f"participants[{index}]"
        if not isinstance(participant, dict):
            errors.append(f"{prefix} must be an object")
            continue

        forbidden = sorted(FORBIDDEN_PARTICIPANT_KEYS.intersection(participant))
        if forbidden:
            errors.append(f"{prefix} contains forbidden identifying fields: {', '.join(forbidden)}")

        participant_id = participant.get("participant_id")
        if not _is_nonempty_string(participant_id):
            errors.append(f"{prefix}.participant_id is required")
        elif participant_id in participant_ids:
            errors.append(f"duplicate participant_id: {participant_id}")
        else:
            participant_ids.add(participant_id)

        if participant.get("representative") is not True:
            errors.append(f"{prefix}.representative must be true for S14 evidence")
        if participant.get("experience_band") not in EXPERIENCE_BANDS:
            errors.append(f"{prefix}.experience_band is invalid")
        if not _is_nonempty_string(participant.get("role_category")):
            errors.append(f"{prefix}.role_category is required")
        if participant.get("executed") is not True:
            errors.append(f"{prefix}.executed must be true when participant is recorded")
        else:
            executed_count += 1

        candidate_sha = participant.get("candidate_sha")
        if not _check_hash(candidate_sha, SHA_RE):
            errors.append(f"{prefix}.candidate_sha must be a lowercase 40-character commit SHA")

        task_map = _participant_task_map(participant)
        if set(task_map) != set(EXPECTED_TASKS):
            errors.append(f"{prefix}.tasks must contain JP01..JP12 exactly once")

        for task_id in EXPECTED_TASKS:
            task = task_map.get(task_id)
            if not task:
                continue
            task_state = task.get("status")
            if task_state not in TASK_STATES:
                errors.append(f"{prefix}.{task_id}.status is invalid")
                continue
            if task_id in REQUIRED_TASKS and task_state == "NOT_APPLICABLE":
                errors.append(f"{prefix}.{task_id} is required and cannot be NOT_APPLICABLE")
            if task_state in {"FAIL", "BLOCKED"}:
                any_failed_task = True
            if task_state != "NOT_RUN":
                evidence = task.get("evidence")
                if not isinstance(evidence, list) or not any(_is_nonempty_string(item) for item in evidence):
                    errors.append(f"{prefix}.{task_id} executed result requires at least one evidence reference")
                if not _is_nonempty_string(task.get("observed_behavior")):
                    errors.append(f"{prefix}.{task_id} executed result requires observed_behavior")
            if task.get("moderator_intervention") and task_state == "PASS" and task.get("unassisted") is True:
                errors.append(f"{prefix}.{task_id} cannot be unassisted PASS when moderator_intervention is recorded")

    findings = record.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []

    finding_ids: set[str] = set()
    unresolved_material = False
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{prefix} must be an object")
            continue
        finding_id = finding.get("id")
        if not _is_nonempty_string(finding_id):
            errors.append(f"{prefix}.id is required")
        elif finding_id in finding_ids:
            errors.append(f"duplicate finding id: {finding_id}")
        else:
            finding_ids.add(finding_id)
        severity = finding.get("severity")
        finding_state = finding.get("status")
        if severity not in SEVERITIES:
            errors.append(f"{prefix}.severity is invalid")
        if finding_state not in FINDING_STATES:
            errors.append(f"{prefix}.status is invalid")
        if severity in {"BLOCKER", "MAJOR"} and finding_state == "OPEN":
            unresolved_material = True
        task_ids = finding.get("task_ids")
        if not isinstance(task_ids, list) or not task_ids or any(task_id not in EXPECTED_TASKS for task_id in task_ids):
            errors.append(f"{prefix}.task_ids must reference one or more JP01..JP12 tasks")
        evidence = finding.get("evidence")
        if not isinstance(evidence, list) or not any(_is_nonempty_string(item) for item in evidence):
            errors.append(f"{prefix}.evidence requires at least one reference")
        if not _is_nonempty_string(finding.get("description")):
            errors.append(f"{prefix}.description is required")

    candidate = record.get("candidate")
    candidate_sha = None
    if not isinstance(candidate, dict):
        errors.append("candidate must be an object")
    else:
        candidate_sha = candidate.get("source_sha")

    if state == "NOT_EXECUTED":
        if participants:
            errors.append("NOT_EXECUTED requires participants to be empty")
        if findings:
            errors.append("NOT_EXECUTED requires findings to be empty")

    if state in {"IN_PROGRESS", "FAIL_REPAIR_REQUIRED", "PASS"} and executed_count == 0:
        errors.append(f"{state} requires at least one executed participant")

    if state == "FAIL_REPAIR_REQUIRED" and not (any_failed_task or unresolved_material):
        errors.append("FAIL_REPAIR_REQUIRED requires a failed/blocked task or open BLOCKER/MAJOR finding")

    if state == "PASS":
        if len(participants) < 3:
            errors.append("PASS requires at least 3 distinct representative participants")
        if not _check_hash(candidate_sha, SHA_RE):
            errors.append("PASS requires candidate.source_sha as a lowercase 40-character commit SHA")
        if isinstance(candidate, dict):
            for key in ("blender_artifact", "after_effects_artifact"):
                artifact = candidate.get(key)
                if not isinstance(artifact, dict) or not _is_nonempty_string(artifact.get("filename")):
                    errors.append(f"PASS requires candidate.{key}.filename")
                if not isinstance(artifact, dict) or not _check_hash(artifact.get("sha256"), SHA256_RE):
                    errors.append(f"PASS requires candidate.{key}.sha256")
            fixture = candidate.get("fixture")
            if not isinstance(fixture, dict):
                errors.append("PASS requires candidate.fixture")
            else:
                if not _is_nonempty_string(fixture.get("id")):
                    errors.append("PASS requires candidate.fixture.id")
                if fixture.get("provenance") not in {"synthetic-original", "user-owned-original"}:
                    errors.append("PASS requires authorized candidate.fixture.provenance")
                if not _check_hash(fixture.get("sha256"), SHA256_RE):
                    errors.append("PASS requires candidate.fixture.sha256")
            for host_key in ("blender_host", "after_effects_host"):
                host = candidate.get(host_key)
                if not isinstance(host, dict) or not _is_nonempty_string(host.get("version")) or not _is_nonempty_string(host.get("os")):
                    errors.append(f"PASS requires candidate.{host_key}.version and os")

        for index, participant in enumerate(participants):
            prefix = f"participants[{index}]"
            if isinstance(candidate_sha, str) and participant.get("candidate_sha") != candidate_sha:
                errors.append(f"{prefix}.candidate_sha must match final PASS candidate.source_sha")
            task_map = _participant_task_map(participant)
            for task_id in REQUIRED_TASKS:
                if task_map.get(task_id, {}).get("status") != "PASS":
                    errors.append(f"PASS requires {prefix}.{task_id}=PASS")
            if task_map.get("JP12", {}).get("status") not in {"PASS", "NOT_APPLICABLE"}:
                errors.append(f"PASS requires {prefix}.JP12 to be PASS or NOT_APPLICABLE")

        if unresolved_material:
            errors.append("PASS cannot contain unresolved BLOCKER or MAJOR findings")

        summary = record.get("summary")
        if not isinstance(summary, dict) or not _is_nonempty_string(summary.get("claim_scope")):
            errors.append("PASS requires summary.claim_scope")
        if not isinstance(summary, dict) or not _is_nonempty_string(summary.get("statement")):
            errors.append("PASS requires summary.statement")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_evidence.py <s14-evidence.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"S14 evidence INVALID: cannot read JSON: {exc}", file=sys.stderr)
        return 1

    errors = validate(record)
    if errors:
        print("S14 evidence INVALID:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    state = record.get("overall_state")
    print(f"S14 evidence VALID: state={state}")
    if state != "PASS":
        print("Japanese target-user PASS has not been established by this record.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

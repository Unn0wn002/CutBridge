# S12 Evidence Tools

These files support the **real-host** S12 Blender → package → After Effects campaign.

They do not run Blender or After Effects and cannot establish native PASS by themselves.

## Files

- `evidence-template.json` — starts in `NOT_EXECUTED` state.
- `validate_evidence.py` — checks evidence-record structure and fail-closed state consistency.
- `../../docs/S12_E2E_VALIDATION.md` — complete real-host execution runbook.

## Start a campaign record

From the repository root in PowerShell:

```powershell
Copy-Item tools\s12\evidence-template.json .\s12-evidence.json
python tools\s12\validate_evidence.py .\s12-evidence.json
```

Expected initial output:

```text
S12 evidence VALID: state=NOT_EXECUTED
Native S12 PASS has not been established by this record.
```

Before testing, replace `candidate.develop_sha` with the exact frozen candidate SHA if it differs from the preparation baseline.

## During native testing

After executing a real gate:

- change its status from `NOT_EXECUTED` to `PASS` or `FAIL`;
- add at least one real evidence reference;
- set overall state to `IN_PROGRESS` while required gates remain incomplete;
- if a required gate fails, use `FAIL_REPAIR_REQUIRED`;
- record artifact hashes, host versions/OS, and fixture hash as soon as they are known.

Validate after edits:

```powershell
python tools\s12\validate_evidence.py .\s12-evidence.json
```

## PASS semantics

The validator rejects `PASS` unless:

- Blender and After Effects are both marked actually executed;
- every required gate is PASS;
- every PASS gate has evidence references;
- both candidate artifacts have filenames and SHA-256 hashes;
- the fixture has a SHA-256 hash;
- both host version/OS records are populated.

A structurally valid PASS record produces:

```text
Record is structurally eligible for S12 PASS; review referenced native evidence manually.
```

Manual evidence review is still required. The script does not inspect screenshots, launch desktop applications, or attest that a tester performed the recorded actions.

## Do not commit fake PASS evidence

Tests construct synthetic PASS records in memory only to verify validator rules. Do not add a repository `example-pass-evidence.json` that could later be mistaken for native validation evidence.

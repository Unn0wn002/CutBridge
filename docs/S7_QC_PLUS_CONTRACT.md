# S7 QC+ Contract

Status: implementation contract for `feature/session-7-qc-plus`.

Base: green S6 integration commit `5d309f51d75b357974d17c94090792d27dea6163`.
Tracking issue: #33.

## Objective

S7 upgrades CutBridge QC from a flat human-readable check list into a deterministic diagnostic system that is more actionable for production artists and future localization, while preserving S5/S6 fail-closed ownership and revision behavior.

S7 must not silently repair, adopt, rename, retag, migrate, or guess ownership/source state.

## Diagnostic record

Each QC finding should be representable by the following conceptual fields:

- `severity`: `PASS`, `WARNING`, or `ERROR`.
- `code`: stable machine-testable identifier, e.g. `SEQ_MISSING_REQUIRED_FRAMES`.
- `scope`: package, manifest, pass, sequence, revision, comp, footage, layer, or project.
- `subject`: human-readable target such as pass name or comp name.
- `message`: concise condition summary.
- `remediation`: safe next action; mandatory for warnings and errors.

The initial UI may remain a text alert, but formatting and ordering must derive from deterministic records rather than ad-hoc concatenation.

## Severity policy

### PASS

Use when an explicitly checked invariant is satisfied. PASS findings never imply native AE behavior that was not actually inspected.

### WARNING

Use when the package/work can remain usable but intervention or awareness is required, including optional-pass absence, unexpected extra matching frames, and policy changes that require confirmation rather than automatic mutation.

### ERROR

Use when CutBridge cannot safely trust or operate on the inspected state, including invalid manifests, missing required frames, incompatible comp geometry/timing, ambiguous managed ownership, stale/foreign managed tags, missing required managed objects, or unsupported revision structure.

## Stable diagnostic categories

### Package / manifest

- `MANIFEST_SCHEMA_OK`
- `MANIFEST_CONTRACT_ERROR`
- `PACKAGE_IDENTITY_OK`
- `PACKAGE_VERSION_OK`
- `PASS_DEFINITION_ERROR`
- `LAYER_ORDER_ERROR`
- `PATH_SAFETY_ERROR`
- `PATTERN_SAFETY_ERROR`

### Sequence

- `SEQ_COMPLETE`
- `SEQ_FOLDER_MISSING_REQUIRED`
- `SEQ_FOLDER_MISSING_OPTIONAL`
- `SEQ_MISSING_REQUIRED_FRAMES`
- `SEQ_MISSING_OPTIONAL_FRAMES`
- `SEQ_UNEXPECTED_MATCHES`

### Managed AE state

- `ROOT_OWNERSHIP_AMBIGUOUS`
- `MANAGED_FOLDER_MISSING`
- `MANAGED_FOLDER_AMBIGUOUS`
- `COMP_MISSING`
- `COMP_OWNERSHIP_ERROR`
- `COMP_SPEC_OK`
- `COMP_SPEC_DRIFT`
- `FOOTAGE_OK`
- `FOOTAGE_MISSING_REQUIRED`
- `FOOTAGE_MISSING_OPTIONAL`
- `FOOTAGE_OWNERSHIP_ERROR`
- `LAYER_OK`
- `LAYER_MISSING_REQUIRED`
- `LAYER_MISSING_OPTIONAL`
- `LAYER_OWNERSHIP_ERROR`
- `STALE_MANAGED_TAG`

### Revision

- `REVISION_IDENTITY_OK`
- `REVISION_NEWER_AVAILABLE`
- `REVISION_INCOMPATIBLE`
- `REVISION_POLICY_WARNING`

Revision discovery must remain fail closed and must not scan/adopt ambiguous project state merely to produce a more attractive QC result.

## Deterministic output order

Recommended order:

1. manifest/contract;
2. package identity/version;
3. global FPS/frame-count/resolution summary;
4. passes in manifest order;
5. sequence findings for each pass;
6. managed footage/layer findings for each pass;
7. managed comp/project findings;
8. revision findings when safely available;
9. summary counts.

Repeated QC on unchanged state must produce the same ordered findings.

## Remediation rules

Warnings and errors must contain safe next actions. Examples:

- missing required frames → re-render the missing frame range into the expected pass folder, then rerun QC;
- optional pass missing → render or remove the optional pass deliberately in the source package; do not create placeholder footage;
- comp spec drift → restore the intended FPS/duration/resolution/pixel aspect or rebuild/migrate deliberately; do not auto-resize artist work;
- stale/foreign managed tag → inspect and deliberately restore/remove the stale managed object; CutBridge must not adopt it automatically;
- ownership ambiguity → resolve duplicates manually before Build/Revision/QC continues;
- incompatible revision → rebuild/migrate deliberately rather than source-only replacement.

Remediation text must not claim an automatic fix exists unless such a fix is separately designed, tested, and explicitly invoked by the user.

## Regression requirements

S7 tests must cover at minimum:

- stable severity/code formatting;
- deterministic ordering;
- required vs optional sequence severity;
- missing-frame remediation;
- unexpected-match warning;
- comp FPS/duration/resolution/pixel-aspect drift diagnostics;
- stale/foreign managed-layer diagnostics;
- missing required footage/layer diagnostics;
- ownership ambiguity remains fail closed;
- revision incompatibility/warning classification does not bypass S6 gates;
- no automatic mutation from QC;
- existing S5/S6 tests remain green.

## Native-host boundary

Headless/Node tests may validate formatting, classification, ordering, and host-shaped adapter logic. They are not evidence that After Effects GUI behavior executed successfully.

Any native AE S7 claim must be recorded separately with exact source/package identity and real After Effects evidence.

## Merge gate

Before S7 merges:

1. dedicated S7 tests pass;
2. existing S5/S6 tests pass;
3. release authorization remains fail closed;
4. authoritative CI is green;
5. solo-maintainer adversarial review finds no unresolved merge blocker;
6. if native AE behavior materially changes, execute and record the relevant real-host validation;
7. merge to `develop` and require green post-merge CI before S8 begins.

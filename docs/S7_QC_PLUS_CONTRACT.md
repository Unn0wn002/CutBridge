# S7 QC+ Contract

Status: **implementation in progress** on `feature/session-7-qc-plus`.

Base: green S6 integration commit `5d309f51d75b357974d17c94090792d27dea6163`.
Tracking issue: #33. Draft PR: #35.

## Objective

S7 upgrades CutBridge QC from a flat human-readable checklist into a deterministic diagnostic system that is more actionable for production artists and future localization, while preserving S5/S6 fail-closed ownership and revision behavior.

S7 must not silently repair, adopt, rename, retag, migrate, or guess ownership/source state.

## Implemented foundation

The first S7 implementation slice is committed and CI-tested:

- `apps/after-effects/qc_plus.js` provides the pure, host-independent diagnostic engine.
- Diagnostics use stable `CBQ-*` identifiers.
- Every WARNING/ERROR requires remediation text.
- Diagnostic output is deterministically sorted and rendered.
- Sequence required/optional severity is implemented.
- Comp-drift and revision compatibility records are implemented.
- The diagnostic engine is explicitly non-mutating.
- `tests/ae_s7_qc_plus_checks.cjs` and `tests/test_ae_s7.py` provide dedicated regressions.
- Fast CI runs the S7 pytest wrapper, direct Node checks, and syntax validation.
- The deterministic AE release package now requires and contains `qc_plus.js`.

Native panel wiring into `CutBridge.jsx` is still in progress. Do not claim S7 native AE execution merely because the diagnostic engine and host-independent regressions pass.

## Diagnostic record

Each finding uses:

- `severity`: `PASS`, `WARNING`, or `ERROR`.
- `code`: stable machine-testable identifier in the `CBQ-*` namespace.
- `scope`: package, manifest, sequence, footage, layer, comp, revision, or host.
- `subject`: optional human-readable target such as pass/revision name.
- `message`: concise condition summary.
- `detail`: optional deterministic supporting detail.
- `remediation`: safe next action; mandatory for WARNING and ERROR.

The initial UI may remain a text alert, but formatting and ordering must derive from deterministic records rather than ad-hoc concatenation.

## Severity policy

### PASS
Use when an explicitly checked invariant is satisfied. PASS findings never imply native AE behavior that was not actually inspected.

### WARNING
Use when the package/work can remain usable but intervention or awareness is required, including optional-pass absence, unexpected extra matching frames, and policy changes that require confirmation rather than automatic mutation.

### ERROR
Use when CutBridge cannot safely trust or operate on the inspected state, including invalid manifests, missing required frames, incompatible comp geometry/timing, ambiguous managed ownership, stale/foreign managed tags, missing required managed objects, or unsupported revision structure.

## Stable diagnostic identifiers

Implemented identifiers currently include:

### Sequence
- `CBQ-SEQ-COMPLETE`
- `CBQ-SEQ-REQUIRED-FOLDER-MISSING`
- `CBQ-SEQ-OPTIONAL-FOLDER-MISSING`
- `CBQ-SEQ-REQUIRED-FRAMES-MISSING`
- `CBQ-SEQ-OPTIONAL-FRAMES-MISSING`
- `CBQ-SEQ-UNEXPECTED-MATCHES`

### Managed comp
- `CBQ-COMP-SPEC-OK`
- `CBQ-COMP-DRIFT-RESOLUTION`
- `CBQ-COMP-DRIFT-PIXEL-ASPECT`
- `CBQ-COMP-DRIFT-FRAME-RATE`
- `CBQ-COMP-DRIFT-DURATION`

### Revision
- `CBQ-REV-SAFE`
- `CBQ-REV-POLICY-WARNING`
- `CBQ-REV-INCOMPATIBLE`
- `CBQ-REV-NOT-ASSESSED`

Additional host/ownership/package codes will be added as existing `runQC()` checks migrate into QC+ records. Existing identifiers must not be casually renamed once consumed by tests or future localization.

## Deterministic output order

The engine sorts by severity (`ERROR`, `WARNING`, `PASS`), stable scope rank, diagnostic code, subject, then message. Repeated QC on unchanged observations must produce the same rendered report regardless of insertion order.

## Remediation rules

Warnings and errors must contain safe next actions. Missing required frames should direct the artist to restore/re-render frames and rerun QC. Optional-pass absence should remain optional. Comp drift must never auto-resize artist work. Stale/foreign tags and ambiguous ownership must require deliberate manual resolution. Incompatible revisions must use rebuild/migration rather than source-only replacement.

## Regression requirements

- [x] stable severity/code formatting.
- [x] deterministic ordering.
- [x] required vs optional sequence severity.
- [x] missing-frame remediation.
- [x] unexpected-match warning.
- [x] comp FPS/duration/resolution/pixel-aspect diagnostic generation.
- [x] revision incompatibility/warning classification without bypassing S6 policy.
- [x] no automatic mutation from QC engine.
- [x] existing S5/S6 complete suite remains green after the first implementation slice.
- [ ] stale/foreign managed-layer diagnostics wired from real inspectable AE state.
- [ ] missing required footage/layer diagnostics wired from real inspectable AE state.
- [ ] ownership ambiguity mapped to stable QC+ records while remaining fail closed.
- [ ] native `CutBridge.jsx` QC output rendered from QC+ records.
- [ ] release/install boundary revalidated after native panel wiring.

## Native-host boundary

Headless/Node tests may validate formatting, classification, ordering, packaging, and host-shaped adapter logic. They are not evidence that After Effects GUI behavior executed successfully.

Any native AE S7 claim must be recorded separately with exact source/package identity and real After Effects evidence when native host behavior materially changes.

## Merge gate

Before S7 merges:

1. dedicated S7 tests pass;
2. existing S5/S6 tests pass;
3. release authorization remains fail closed;
4. authoritative CI is green;
5. native `CutBridge.jsx` uses the QC+ engine for the S7 diagnostic path;
6. solo-maintainer adversarial review finds no unresolved merge blocker;
7. if native AE behavior materially changes, execute and record the relevant real-host validation;
8. merge to `develop` and require green post-merge CI before S8 begins.

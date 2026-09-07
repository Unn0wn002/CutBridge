# S5 Independent Review — Merge Blocked

Date: 2026-09-07

Status: **CONTINUE SESSION 2 — S5 NOT SAFE TO MERGE**

PR #14 remains open and unmerged. S6 has not started.

This review was run against the local S5 PR snapshot and the ownership/cache repair under review. The existing 31-group S5 harness still passes; the findings below come from an additional adversarial host-adapter harness and are merge blockers because they can mutate or misreport managed After Effects state.

## Findings

### S5-R1 — Managed comp moved out of its folder can be duplicated

Reproduction:

1. Build a valid package.
2. Move the tagged CutBridge comp out of `01_COMP`.
3. Reload the script and build again.

Observed: `ensureManagedComp()` searches for the tag only inside the expected comp folder. It creates a second comp in `01_COMP` before the later layer ownership check notices the moved tagged layer. The build then fails, but the newly created duplicate comp remains.

Required correction: scan live project items for the package-scoped comp tag before creating anything. A single tagged comp in the wrong folder must fail closed without creating a replacement; duplicate tags must also fail closed.

### S5-R2 — Duplicate managed comp tags are silently accepted

Reproduction:

1. Build a valid package.
2. Add a second comp carrying the same CutBridge comp tag.
3. Build both before and after script reload.

Observed: the first tagged comp is reused and the duplicate is ignored. The build reports `reused safely`.

Required correction: count all live matching tags and reject duplicate ownership before any import or layer mutation.

### S5-R3 — QC loses comp metadata validation after script reload

Reproduction:

1. Build a valid package.
2. Change the managed comp frame rate from 24 to 30.
3. Run QC; then reload the script and run QC again.

Observed: same-session QC reports the frame-rate mismatch. After reload, `state.comp` is empty and QC reports `PASS` without checking the managed comp.

Required correction: QC must rediscover the live tagged comp and validate folder ownership and metadata on every run. Session state may cache an observation but cannot be the only source of truth.

### S5-R4 — Skipped optional passes can still be treated as verified during ordering

Reproduction:

1. Build a package containing required `BEAUTY` and optional `LINE` passes.
2. Invalidate the existing `LINE` layer source and remove the optional pass folder.
3. Reload and build again.

Observed: preflight skips `LINE`, but `orderManagedLayers()` iterates all manifest pass names and finds the old tagged `LINE` layer without revalidating its source. The stale layer remains eligible for movement and the build reports `reused safely` with only an optional-pass warning.

Required correction: order only passes successfully verified in the current build. Skipped optional layers must not be reused or reordered; they must remain untouched or produce an explicit stale-managed-layer diagnostic.

### S5-R5 — Reserved prototype key is rejected as a false duplicate

Reproduction: use a valid single pass named `constructor` and set `ae.layer_order` to `['constructor']`.

Observed: manifest validation reports both a duplicate render pass and duplicate layer-order entry even though each appears once. The validator uses ordinary object maps for membership tracking.

Required correction: use null-prototype maps or explicit own-property checks for pass/order membership. Add regression coverage for valid names such as `constructor`, `toString`, and `__proto__` according to the parser's safety policy.

## Validation evidence

- **PASS:** `node tests/ae_s5_checks.cjs` — 31 existing S5 groups.
- **PASS:** adversarial harness reproduces all findings above without claiming native After Effects execution.
- **BLOCKED:** local pytest command — `pytest` is unavailable in this runtime. The prior exact-head CI handoff reported authoritative CI green for the implementation head, but that green result does not cover these adversarial findings.
- **MANUAL NOT EXECUTED:** native After Effects GUI, real AE project persistence/undo behavior, Blender GUI, Blender→AE end-to-end, revision preservation, Japanese-user validation, and production/studio validation.

## Integration decision

Do not merge PR #14. Keep S5 open, repair the findings in a bounded follow-up on the same PR, rerun the full authoritative CI on the final head, and repeat independent review before integration. Do not begin S6.

## Follow-up repair prepared

The bounded repair is now implemented locally on the same S5 scope. It adds live package-scoped comp discovery with duplicate/moved/name/type rejection, reload-safe QC comp discovery, current-build verified-pass ordering, and prototype-safe manifest membership keys. Focused coverage now reports 36 S5 host-adapter groups, plus the existing rollback and ordering scripts.

The repair has not yet been pushed to PR #14 or independently re-reviewed. Exact-head CI, fresh review, merge, and post-merge `develop` CI remain outstanding.

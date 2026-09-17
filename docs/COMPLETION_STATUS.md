# CutBridge Completion Status

## Current state — 17 September 2026

CutBridge v0.2.3 remains **UNRELEASED / NOT RELEASE READY**.

The current product/runtime source immediately before this documentation reconciliation is `develop` commit `caaede1c296b9087ffee1b57a0907620b3495ffb`. Its tree is `fff813588579c16da0ad2353e5256ea63368b6b6`, which contains the natively owner-tested Blender repairs for Issues #82 and #83. This documentation update does not change runtime behavior.

Current repository boundaries:

- `main`: `7a34ebdcb297ced7e275c4c58382f765deee0ed9`;
- promotion PR #74: OPEN / unmerged / mergeable, but deliberately blocked by release gates;
- `release-authorization.json`: `approved: false`;
- GitHub Release publication: not authorized;
- repository governance Issue #18: OPEN publication blocker;
- S14 Issue #71: OPEN; real representative Japanese target-user execution is still pending;
- Issue #80: OPEN post-v0.2.3 design task for per-pass output formats, not a v0.2.3 release blocker.

## Current verified engineering state

### Integrated foundation — S1 through S13

The previously completed S1-S13 engineering foundation remains integrated for its documented scope:

- deterministic Blender/After Effects packaging and release hygiene;
- transactional Beauty / Line / Shadow / Depth Blender output mapping;
- package safety, same-version overwrite protection, UTF-8/Japanese-safe metadata;
- strict After Effects package/manifest/path/frame/pass validation;
- managed AE Build/reload/repeated-build ownership safety;
- compatible non-destructive V001 -> V002 -> V003 revision workflow;
- QC+ diagnostics;
- Japanese-first UI with deterministic English fallback;
- Studio Presets;
- optional bounded Camera/3D Null handoff;
- native AE Camera/Null reconstruction and revision repair;
- QA, documentation, release-authorization and deterministic-packaging controls.

Historical S12/S13 native evidence remains SHA-bound to the commits recorded in `docs/S12_S13_EVIDENCE_SUMMARY.md` and must not be reattributed to later commits without explicit retesting.

### Beta.2 repair chain

The historical frozen candidate `candidate/v0.2.3-beta.2` is fixed at:

`7fd7c34f16e43d328fbf88e63b534d1f04507cbd`

That candidate was useful for beta/internal validation, but material Blender-side findings were discovered after it was frozen. Therefore beta.2 is no longer the correct candidate identity for further current candidate-level testing.

#### Issue #82 — Blender Render Animation crash

**CONFIRMED FIXED for the tested environment.**

Owner/local Windows testing isolated a CutBridge/Blender interaction in which the N-panel continuously ran Line/Shadow compositor socket preflight during panel redraw. The probe created and removed temporary compositor datablocks while interactive Render Animation could be starting after View Layer pass changes.

Repair:

- remove Line/Shadow compositor preflight from continuous panel draw;
- keep both preflights in explicit `Validate Cut` and `Build Package` operations.

Native owner verification on Windows 11 + Blender 5.2.1 LTS passed:

- normal CutBridge N-panel visible;
- V005 `Validate Cut -> Build Package -> interactive Render Animation`;
- 24/24 frames for Beauty, Line, Shadow, Depth;
- all tested pass-combination cases;
- save/close/reopen persistence;
- V006 fresh revision Build + immediate Render Animation;
- explicit invalid Line/Shadow fail-closed checks;
- panel non-mutation check.

Blender 4.2 and 4.5 were **not** natively verified for this repair and must remain UNVERIFIED.

#### Issue #83 — post-build PACKAGE_EXISTS guidance

**CONFIRMED FIXED for the tested environment.**

The previous general Validation Status / `Validate Cut` flow incorrectly reused the strict Build Package overwrite error after a valid package already contained render payload. The repair now separates action-specific build protection from package lifecycle state:

- matching existing payload package -> `PACKAGE_RENDER_READY` INFO; continue Render Animation;
- deliberate same-Version Build Package -> `PACKAGE_EXISTS` ERROR; refuse overwrite;
- existing payload + changed cut/render contract -> `PACKAGE_STATE_MISMATCH` ERROR; fail closed.

Native owner verification on Windows 11 + Blender 5.2.1 LTS passed:

- exact owner-test artifact checksum match;
- clean V007 Validate/Build;
- 24/24 frames across Beauty, Line, Shadow, Depth;
- `PACKAGE_RENDER_READY` after payload exists;
- same-version rebuild refusal with manifest/render data preserved;
- frame-range mismatch detection and recovery;
- continued render with normal panel visible, with no Issue #82 regression;
- V007 -> V008 independent revision workflow;
- English and Japanese lifecycle diagnostics;
- data preservation across blocked build attempts.

Issues #82 and #83 are closed on GitHub as completed. This is owner/internal engineering evidence, not S14B customer/representative Japanese-user evidence.

## Latest authoritative automated evidence

Exact-head CI on pre-documentation `develop` commit `caaede1c296b9087ffee1b57a0907620b3495ffb` passed both push and PR workflows.

Recorded results include:

- static validation: **133 passed + 2 subtests**;
- deterministic v0.2.3 package/checksum simulation: PASS;
- S6/S7/S8/S10C/S13 regression checks: PASS;
- ExtendScript syntax checks: PASS;
- Blender 5.2.1 RNA registration lifecycle: PASS;
- complete Blender/runtime pytest suite: **289 passed, 72 warnings + 2 subtests**.

Known automated warning debt includes Blender `Scene.use_nodes` deprecation ahead of Blender 6.0 and GitHub Actions runtime deprecation messages from pinned upstream actions. These are not recorded as current v0.2.3 functional blockers, but remain technical debt.

## Evidence boundaries

### S12 structured evidence traceability

The repository still does **not** contain a final committed structured `s12-evidence.json` PASS record.

The issue/PR/native S12/S13 evidence is real and retained, but the missing structured record remains an evidence-traceability gap. Do not fabricate historical hashes, paths, timestamps, or a retroactive PASS JSON. If an authentic original record exists externally, recover and validate that exact record; otherwise preserve the limitation explicitly.

### S14 target-user validation

S14A protocol preparation exists, but S14B real representative Japanese-speaking target-user execution is not complete. Owner testing must not be represented as S14B PASS, customer validation, representative Japanese-user evidence, or proof of broad Japanese production usability.

Any broad Japanese production-usability claim therefore remains blocked unless real S14B evidence is completed or the intended release-facing claim is explicitly narrowed through a reviewed decision.

## Candidate identity after beta.2

Because Issues #82 and #83 required material product-source changes after frozen beta.2, the next current candidate must use a new identity.

**Required next freeze:** `candidate/v0.2.3-beta.3` from an exact green `develop` commit after release-readiness documentation reconciliation.

The beta.3 freeze must record:

- exact source commit;
- exact artifact names and SHA-256 hashes;
- authoritative CI at the frozen source;
- which native evidence carries forward unchanged and which tests were rerun;
- owner/internal regression result for the exact beta.3 candidate.

Do not mutate the historical beta.2 identity.

## Release blockers / gates

The remaining path to an RC/stable release is:

1. **Reconcile current release-readiness documentation** to the post-#82/#83 source state.
2. **Freeze exact beta.3 candidate** from a green develop head.
3. **Run bounded owner/internal regression on exact beta.3** and record the candidate identity/evidence.
4. **Resolve S12 structured-evidence traceability truthfully** without fabrication.
5. **Complete S14B real Japanese target-user validation** for broad target-user usability claims, or explicitly narrow those claims through a reviewed decision.
6. **Resolve repository governance Issue #18.** Current private-repository branch/tag protection capability remains insufficient; do not make the repository public merely to satisfy the checklist.
7. **Freeze/review PR #74 at the exact approved candidate head** and require authoritative CI there.
8. **Merge develop -> main only after the above gates are satisfied.**
9. **Verify authoritative CI on the exact promoted main commit.**
10. **Explicitly authorize one exact current-main/tag/channel/prerelease tuple** only after prerequisites pass.
11. **Publish and independently verify downloaded artifacts/checksums/content.**
12. **Verify the production update/distribution path separately.**

Until these gates are satisfied, `release-authorization.json` must remain fail-closed and no stable/RC publication is authorized.

## Non-blocking post-v0.2.3 work

Issue #80 remains intentionally outside the v0.2.3 release scope. Per-pass output formats require coordinated manifest/preset/Blender/AE compatibility work and must not be half-implemented into the current release candidate.

## Recommended immediate phase

**Beta.3 candidate freeze and exact-candidate owner regression.**

After that, continue release preparation only within the explicit evidence/governance boundaries above.
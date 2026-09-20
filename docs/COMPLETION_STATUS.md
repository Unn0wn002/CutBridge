# CutBridge Completion Status

## Current state — 20 September 2026

CutBridge v0.2.3 remains **UNRELEASED / NOT RELEASE READY**. The Japanese release-facing claim for v0.2.3 is now deliberately narrowed; S14B representative-user validation remains NOT_EXECUTED and is not claimed as complete.

- **Integrated product/validation sessions:** S1–S13.
- Historical S13 runtime integration baseline: `0a86d9a0605e1dd9714ef35a547693de76f714f4`.
- Historical final native-tested S13F source: `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`.

The current product/runtime source immediately before this documentation reconciliation is `develop` commit `caaede1c296b9087ffee1b57a0907620b3495ffb`. Its tree is `fff813588579c16da0ad2353e5256ea63368b6b6`, which contains the natively owner-tested Blender repairs for Issues #82 and #83. This documentation update does not change runtime behavior.

Current repository boundaries:

- `main`: `7a34ebdcb297ced7e275c4c58382f765deee0ed9`;
- promotion PR #74: OPEN / unmerged / mergeable, but deliberately blocked by release gates;
- `release-authorization.json`: `approved: false`;
- GitHub Release publication: not authorized;
- repository governance Issue #18: OPEN publication blocker;
- S14 Issue #71: representative Japanese target-user execution remains NOT_EXECUTED; v0.2.3 claim scope is narrowed so no representative-user usability claim is made;
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

**RESOLVED as a traceability decision for v0.2.3; historical structured artifact remains unavailable.**

A 20 September 2026 audit of the retained repository/GitHub evidence found no authentic final committed `s12-evidence.json` PASS artifact. The historical Issue #58 / Issue #60 / PR #68 / CI chain supports the bounded SHA-bound native S12/S13 result, but it does not establish every field required to reconstruct the missing structured JSON.

The project therefore takes the fail-closed non-fabrication path: no historical hashes, fixture hash, per-gate evidence paths, timestamps, or PASS JSON will be invented. The missing JSON remains an explicit provenance limitation. Future S12 campaigns must create and validate the structured record contemporaneously using the existing template and validator.

### S14 target-user validation / claim-scope decision

S14A protocol preparation exists. S14B real representative Japanese-speaking target-user execution remains **NOT_EXECUTED**.

For v0.2.3, the release-facing claim has been explicitly narrowed:

- Japanese-first UI and deterministic English fallback may be described as implemented behavior;
- engineering/native Japanese/English workflow evidence may be described only for its recorded tested scope;
- beta.3 owner/internal testing remains owner/internal engineering evidence only;
- no representative Japanese-user validation, customer validation, broad Japanese production-usability, ease-of-use, statistical usability, or S14B PASS claim may be made.

This resolves the v0.2.3 S14 **release-claim gate** without inventing participant evidence. The S14 protocol remains available for a future broader claim.

## Candidate identity and beta.3 result

The historical frozen beta.3 owner-test candidate is:

`candidate/v0.2.3-beta.3` at `00d2e51a6266d140d499e48b45557eb084568d9f`.

Recorded deterministic artifacts:

- Blender `CutBridge-Blender-v0.2.3-beta.3.zip` — SHA-256 `d665f5a20de7cbdd054a181c74b42c2d8bc68ce5e754592dc63d3d098b0c173c`;
- After Effects `CutBridge-AfterEffects-v0.2.3-beta.3.zip` — SHA-256 `85be3e40ed07dfa2db71007dbdb5266cd968a970737af43bb64a7a4d64b9c98a`.

The bounded beta.3 owner/internal regression passed for the recorded Windows 11 Home Single Language 25H2 / Blender 5.2.1 / After Effects 2026 v26.3 scope, including the Issue #82 render-crash regression, Issue #83 package lifecycle behavior, AE repeated Build, V003 QC, compatible revision/artist-state reporting, and persistence.

Later `develop` commits through `c8721ece179a3dd9afe0e9676477239872574b8e` are documentation/test reconciliation and do not retroactively change the SHA-bound beta.3 candidate identity.

## Release blockers / gates

The remaining path to an RC/stable release is:

1. **Reconcile current release-readiness documentation** to the post-#82/#83 source state.
2. **Freeze exact beta.3 candidate** from a green develop head.
3. **Run bounded owner/internal regression on exact beta.3** and record the candidate identity/evidence.
4. **S12 structured-evidence traceability decision: COMPLETE** through the documented non-fabrication path; the historical JSON remains unavailable and must not be recreated.
5. **v0.2.3 S14 claim-scope decision: COMPLETE through narrowing.** S14B remains NOT_EXECUTED; no representative Japanese-user usability claim is permitted for v0.2.3.
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

**Repository governance Issue #18, then exact promotion-head review/CI.**

The beta.3 freeze, bounded owner/internal regression, S12 traceability decision, and v0.2.3 S14 claim-scope decision are complete for their recorded scopes. S14B remains NOT_EXECUTED and may be pursued later only if broader Japanese target-user usability claims are desired.
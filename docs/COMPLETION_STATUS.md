# CutBridge Completion Status

## Current state — 23 September 2026

CutBridge v0.2.3 is released, published, independently verified, and mirrored to the separate production distribution. v0.2.4 is **PROMOTED / EXACT STABLE TUPLE AUTHORIZED / NOT TAGGED OR PUBLISHED**. S14B representative-user validation remains NOT_EXECUTED and is not claimed as complete.

- **Integrated product/validation sessions:** S1–S13.
- Historical S13 runtime integration baseline: `0a86d9a0605e1dd9714ef35a547693de76f714f4`.
- Historical final native-tested S13F source: `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`.

Stable tag `v0.2.3` remains immutable at `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f`. The verified v0.2.4 line was promoted through PR #97; promotion merge commit `30ea64c10617858a55fa9c32ef5f8ac18922964a` became protected `main` before this release-authorization branch.

Current repository boundaries:

- repository visibility: public;
- protected `develop`: `56bcfe186339c18f319989d46e392155c80cc9b3` after promotion-readiness reconciliation;
- protected `main` promotion merge baseline before authorization merge: `30ea64c10617858a55fa9c32ef5f8ac18922964a`;
- frozen runtime candidate `candidate/v0.2.4-beta.1`: `ef5911a83270a4ce8121741ada2d2726fa09ec29`;
- stable tag `v0.2.3`: exact protected-main SHA above;
- v0.2.3 GitHub Release: published, non-prerelease, four verified assets;
- production distribution commit: `635c1384af2649d4ce49705cce41f98826a861cc`;
- production notification index: `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- production Blender repository: `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`;
- four active governance rulesets protect `main`, `develop`, release-tag mutation, and no-bypass release-tag eligibility;
- `release-authorization.json` on this authorization branch: `approved: true`, tag `v0.2.4`, channel `stable`, `prerelease: false`;
- no v0.2.4 tag, GitHub Release, or production distribution entry exists;
- automatic startup update scheduling remains disabled following Issue #82;
- S14 Issue #71: representative Japanese target-user execution remains NOT_EXECUTED; v0.2.3 claim scope is narrowed so no representative-user usability claim is made;
- Issue #80: COMPLETED for v0.2.4; PR #93 per-pass output formats passed native Blender/After Effects acceptance (10/10 criteria), merged to protected `develop`, and post-merge CI passed;
- `candidate/v0.2.4-beta.1`: frozen and deterministic at `ef5911a83270a4ce8121741ada2d2726fa09ec29`; bounded exact-candidate native Blender/After Effects regression is recorded PASS for the tested scope, including the focused Issue #82 clean-exit rerun.

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

### v0.2.4 beta.1 exact-candidate native regression

The frozen candidate `candidate/v0.2.4-beta.1` resolves to `ef5911a83270a4ce8121741ada2d2726fa09ec29`, matching protected `develop` at the recorded gate.

Recorded exact-candidate evidence includes:

- exact Blender candidate ZIP SHA-256 `3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2`;
- exact After Effects candidate ZIP SHA-256 `e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b`;
- bounded Windows native Blender 5.2.1 + After Effects 2026 candidate campaign PASS for the tested scope;
- focused Issue #82 rerun PASS: 3-frame mixed-format interactive Render Animation with the normal N-panel active, 12 expected non-zero outputs, no new crash dump, responsive Blender host, no external force-kill, and actual process exit code `0`.

The focused rerun used Blender's own normal quit operator. It establishes clean technical shutdown, not evidence that a user literally clicked the menu item. Blender 4.2/4.5 and S14B remain unverified by this campaign.

## Latest authoritative automated evidence

Authoritative promotion evidence is green: exact promotion-head PR CI `35511056270` attempt 2 passed on `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50`, and post-promotion `main` CI `35513361337` passed on `049081f0fe3d3e74d77db807910c2e0fff56fe73`.

Recorded results include:

Current exact-head v0.2.4 frozen-candidate evidence on `ef5911a83270a4ce8121741ada2d2726fa09ec29`:
- static validation: **147 passed + 2 subtests**;
- deterministic v0.2.4 package/checksum simulation: PASS;
- S6/S7/S8/S10C/S13 regression checks: PASS;
- ExtendScript syntax checks: PASS;
- Blender 5.2.1 RNA registration lifecycle: PASS;
- complete Blender/runtime pytest suite: **307 passed, 72 warnings + 2 subtests**;
- authoritative post-merge/candidate push CI run `35797413040`: PASS for `static-validation` and `blender-52-rna-runtime`;
- deterministic candidate packaging reproduced identical Blender ZIP SHA-256 `3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2` and After Effects ZIP SHA-256 `e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b`.

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

Later documentation/governance commits through promotion head `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50` do not retroactively change the SHA-bound beta.3 candidate identity.

## Release and development gates

The v0.2.3 governance, exact authorization, guarded publication, downloaded-asset verification, and separate production-distribution verification gates are complete. Released v0.2.3 remains immutable.

The v0.2.4 release boundary remains fail-closed:

1. released `main` ancestry reconciliation is complete through merged PR #92;
2. PR #93 per-pass output formats and Issue #80 native acceptance are complete and integrated;
3. PR #94 release-tag eligibility push-trigger repair is complete and integrated;
4. exact release authorization is now prepared for `v0.2.4` / `stable` / non-prerelease and must be merged through protected `main` before eligibility can pass;
5. keep automatic startup update scheduling disabled and preserve the Issue #82 panel-readonly regression;
6. exact v0.2.4 candidate freeze is complete at `ef5911a83270a4ce8121741ada2d2726fa09ec29`;
7. bounded combined native Blender/After Effects release-candidate regression is complete for the recorded tested scope, including the focused Issue #82 clean-exit rerun;
8. protected `develop` → `main` promotion and post-promotion CI are complete;
9. require exact-current-main `release-tag-eligibility` PASS after this authorization is merged;
10. do not create the v0.2.4 tag, GitHub Release, or production distribution entry before that eligibility gate and the later explicit publication step.

## Non-blocking post-v0.2.3 work

Issue #80 was intentionally outside the v0.2.3 release scope and is now completed for v0.2.4. The coordinated manifest/preset/Blender/AE per-pass implementation was integrated through PR #93 with native acceptance evidence and green post-merge CI.

## Recommended immediate phase

Complete this exact release-authorization PR with green exact-head CI. If merged to protected `main`, require the main-push `release-tag-eligibility` check to PASS on that exact new main SHA. Stop before tag creation and GitHub Release publication pending the separate publication gate. S14B remains NOT_EXECUTED and is only required if broader Japanese target-user usability claims are desired.

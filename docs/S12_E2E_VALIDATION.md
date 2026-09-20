# CutBridge S12 — Release-Target End-to-End Validation

Status: **PASS AFTER S13F REPAIR CHAIN / CLOSED**

S12 validated the real desktop workflow:

`Blender artifact → real Blender GUI → CutBridge package + real sequences → exact After Effects runtime → Build / QC / Revision / save-reopen → recorded evidence`

This document now serves as the completed S12 campaign record and retained rerun procedure. Passing CI, unit tests, host-shaped tests, or `tools/s12/validate_evidence.py` alone does **not** establish native S12 PASS.

## 1. Final outcome

The original S12 campaign on Windows 11 + Blender 5.2.1 LTS + Adobe After Effects 2026 `26.3x87` exposed real defects and therefore ended in `FAIL_REPAIR_REQUIRED` rather than weakening the gate.

After the S13 repair sequence, exact native-tested commit:

`9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`

passed the repaired real-AE V001→V002→V003 revision path with:

- V001 Build/QC baseline PASS;
- V001→V002 PASS;
- V002→V003 PASS;
- Camera Position / Point of Interest / Zoom refreshed correctly;
- 3D Null Position / Scale refreshed correctly;
- version-scoped Camera/Null ownership migrated correctly;
- QC+ clean on the tested path;
- artist state preserved for the tested scope;
- zero duplicate managed Camera/Null layers;
- V003 save → fully close AE → reopen → reload CutBridge persistence PASS.

The exact tested commit was then pushed to GitHub, passed exact-head CI, passed PR #68 CI, was merged intact to `develop`, and passed post-merge CI at:

`0a86d9a0605e1dd9714ef35a547693de76f714f4`

Issue #58 was reconciled to PASS and closed. Issue #60 was also closed after S13F integration.

## 2. Campaign chronology

### Initial S12 campaign

Environment:

- Windows 11;
- Blender 5.2.1 LTS;
- Adobe After Effects 2026 `26.3x87` / Build 87.

The first campaign passed 15/17 gates but found a material version-scoped Camera/3D Null revision defect. V001→V002 left managed 3D ownership stale, causing QC+ `CBQ-HOST-STALE-MANAGED-TAG`; V002→V003 then correctly failed closed.

### S13 repair 1 — ownership and baked-data migration

PR #61 added:

- Camera/Null baked-sample refresh;
- exact version-scoped ownership migration;
- `state.layers` synchronization;
- 3D topology guards;
- rollback participation.

A subsequent real AE retest exposed another native issue rather than clearing the campaign prematurely.

### S13 repair 2 — Camera Point of Interest host behavior

Real AE rejected one Camera Point-of-Interest property access path with:

`After Effects error: internal verification failure, sorry! {no current context}`

The repair sequence removed unsafe access patterns, moved to verified Transform property-index access, and added a host-shaped regression that became mandatory in canonical CI.

### S13F — native keyframe overwrite repair

The final native blocker was repeated key removal / per-key mutation in the AE revision path. S13F changed the strategy to:

- verify sample topology and existing key times before mutation;
- fail closed on topology drift;
- avoid repeated `removeKey()` mutation;
- perform one native `setValuesAtTimes()` operation per animated property.

Exact native-tested source:

`9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`

This source passed the full real AE V001→V002→V003 chain and persistence test before integration.

## 3. SHA-bound integration evidence

The S13F native result is SHA-bound. The exact tested commit was not recreated under a different SHA.

Repository integration chain:

- native-tested commit: `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`;
- exact-head push CI: run `34503571091` — PASS;
- exact-head PR: #68;
- independent PR CI: run `34503805612` — PASS;
- merge commit on `develop`: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- post-merge CI: run `34504009878` — PASS.

The tested commit was merged intact without amend, rebase, squash, or cherry-pick.

## 4. Latest post-merge automated evidence

On `develop` `0a86d9a...`:

- static suite: 132 passed + 2 subtests;
- deterministic release-package simulation/checksums: PASS;
- S6 revision regressions: PASS;
- S7 QC+ regressions: PASS;
- S8 localization regressions: PASS;
- S10C reconstruction checks: 8/8 PASS;
- S13 3D revision native-host-shaped regression: PASS;
- ExtendScript syntax: PASS;
- Blender 5.2.1 RNA lifecycle: PASS;
- complete Blender/runtime suite: 245 passed + 2 subtests.

These automated results confirm integration stability but do not replace the native evidence above.

## 5. Evidence-traceability resolution

The current repository retains:

- `tools/s12/README.md`;
- `tools/s12/evidence-template.json`;
- `tools/s12/validate_evidence.py`.

A final committed structured `s12-evidence.json` PASS record is **not present in the retained repository evidence**.

On 20 September 2026 the project re-audited the surviving S12/S13 repository and GitHub record. The historical native result remains supported for its recorded SHA-bound scope, but the evidence set does not establish all values required to reconstruct a valid historical PASS JSON, including the complete authentic artifact/fixture hashes and per-gate evidence references.

The v0.2.3 decision is therefore:

1. do **not** manufacture a retroactive PASS record;
2. retain Issue #58, Issue #60, PR #68 and the exact-head/integration CI chain as the historical source;
3. classify the structured JSON as historically unavailable / not truthfully reconstructable from retained evidence;
4. keep that absence as an explicit provenance limitation rather than an unresolved request to invent data;
5. require future S12 campaigns to create and validate their structured record contemporaneously.

This resolves the traceability decision gate without pretending the missing artifact exists.

See `S12_S13_EVIDENCE_SUMMARY.md`.

## 6. Retained rerun rules

A future release candidate that changes behavior covered by S12/S13 invalidates candidate-specific evidence for the affected scope. Rerun the relevant real-host gates on the exact new candidate.

Before a future native rerun, freeze and record:

- exact candidate SHA;
- Blender ZIP filename + SHA-256;
- After Effects ZIP filename + SHA-256;
- Blender version + OS;
- After Effects version + OS;
- fixture identifier/provenance + SHA-256.

Do not infer native success from CI alone.

## 7. Fixture provenance rules

Use only:

- `synthetic-original` — created specifically for CutBridge validation; or
- `user-owned-original` — an original asset the tester owns and is authorized to use.

Do not use leaked or unauthorized studio production files.

A representative fixture should include:

- one supported perspective camera;
- render-visible geometry;
- stable lighting/materials;
- explicitly marked Blender Empties for 3D handoff;
- animation sufficient to exercise revision behavior;
- deterministic frame range/FPS;
- Japanese/Unicode metadata or path coverage where release claims require it.

## 8. V001→V002→V003 rerun design

For future compatible-revision testing:

### V001

Create a baseline with fixed resolution, FPS, frame range, required pass set, render content, and supported optional 3D handoff.

### V002

Change compatible content such as animation, rendered appearance, Camera motion, or Empty motion while preserving compatibility-critical package geometry.

### V003

Apply another compatible content revision so chained version migration is exercised rather than only one update.

Required assertions include:

- expected footage/source version;
- managed Camera/Null ownership version;
- baked Camera/Null values;
- QC state;
- preserved artist state;
- zero duplicate managed 3D layers;
- save/close/reopen persistence.

## 9. Release boundary

**S12 PASS is not release authorization.**

v0.2.3 remains unreleased because the following are still incomplete:

- repository-level governance issue #18;
- deliberate `develop` → `main` promotion;
- authoritative CI on exact promoted `main`;
- Japanese target-user evidence appropriate to broad production claims;
- exact release authorization tuple;
- publication and independent downloaded-asset verification;
- production update/distribution verification.

`release-authorization.json` must remain `approved: false` until those prerequisites are complete.

## 10. Historical verdict states

The S12 evidence tooling retains four states for future campaigns:

- `NOT_EXECUTED`;
- `IN_PROGRESS`;
- `PASS`;
- `FAIL_REPAIR_REQUIRED`.

For this completed campaign, the project tracking verdict is **PASS after the S13F repair chain**, with the structured evidence-record limitation documented above.
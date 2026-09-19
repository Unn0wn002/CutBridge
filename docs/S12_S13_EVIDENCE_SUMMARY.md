# CutBridge S12/S13 Evidence Summary

Status: **S12 PASS / S13 PASS / v0.2.3 STILL UNRELEASED**

Scope note: those PASS statements are limited to the recorded SHA-bound S12/S13 evidence described below; they are not a claim that later source commits inherited new native evidence automatically.

This file consolidates the verifiable repository and issue evidence for the historical S12 release-target campaign and S13 repair chain. It is an evidence index, not a substitute for an authentic structured native-evidence artifact, and it must not be used to reattribute historical native results to later source commits.

## Historical S12/S13 integration state

- S13 runtime integration baseline: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- final native-tested S13F source: `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`;
- exact-head push CI: `34503571091` — PASS;
- PR #68 exact-head CI: `34503805612` — PASS;
- PR #68 merge commit: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- post-merge CI: `34504009878` — PASS;
- S12 issue #58: closed as completed after reconciliation to PASS;
- S13 issue #60: closed as completed after S13F integration.

These are historical SHA-bound records. Current `develop` has moved beyond these commits through later documentation, beta repair and owner-testing work.

## Native host evidence

The final repaired S12/S13 path was tested in:

- Adobe After Effects 2026 `26.3x87` / Build 87;
- Windows 11.

The recorded native result for exact commit `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95` includes:

- V001 baseline Build/QC success;
- V001 -> V002 revision success;
- V002 -> V003 revision success;
- Camera Position refresh;
- Camera Point of Interest refresh;
- Camera Zoom refresh;
- 3D Null Position refresh;
- 3D Null Scale refresh;
- correct version-scoped Camera/Null ownership migration;
- QC+ PASS on the repaired path;
- artist-state preservation for the tested scope;
- zero duplicate managed Camera/Null layers;
- save/fully-close/reopen/reload persistence PASS.

## Repair chain

### S13A — 3D revision ownership/data migration

The first S12 campaign exposed stale Camera/Null ownership and baked-data state during compatible revision. The repair added version-scoped ownership migration, data refresh, topology checks, state synchronization, and rollback participation.

### S13B/S13D — Camera Point-of-Interest native access

Real AE exposed an internal verification failure in one CameraLayer Point-of-Interest access path. Follow-up work removed unsafe access forms and converged on verified Transform property-index access.

### S13C — CI coverage

The investigation found the S13 native-host-shaped regression was not part of canonical CI. That regression was added as a mandatory `static-validation` step.

### S13F — native keyframe overwrite repair

Real AE exposed another host-level failure around repeated key removal/per-key mutation. The final repair validates existing key topology/times and applies animated values using bulk `setValuesAtTimes()` writes instead of repeated destructive key recreation.

The exact native-tested repair source is `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`.

## SHA-bound integration rule

The S12/S13 native result is valid because the exact tested S13F commit was subsequently pushed and merged intact. Repository history records that it was not amended, rebased, squashed, cherry-picked, or recreated under a different SHA before integration.

That exact-source rule must be preserved for future native validation. Later source changes may rely on historical evidence only for unaffected behavior; they do not inherit a new exact native-test identity automatically.

## Historical automated integration evidence

Post-merge CI on `0a86d9a0605e1dd9714ef35a547693de76f714f4` recorded:

- static suite: 132 passed + 2 subtests;
- deterministic v0.2.3 package/checksum simulation: PASS;
- S6 revision checks: PASS;
- S7 QC+ checks: PASS;
- S8 localization checks: PASS;
- S10C reconstruction checks: 8/8 PASS;
- S13 3D revision native-host-shaped regression: PASS;
- ExtendScript syntax: PASS;
- Blender 5.2.1 RNA lifecycle: PASS;
- complete Blender/runtime pytest suite: 245 passed + 2 subtests.

For current automated evidence, use the current CI and `docs/COMPLETION_STATUS.md` rather than treating these historical counts as latest state.

## Structured evidence-record resolution

Repository and historical GitHub evidence were re-audited on 20 September 2026. No authentic final committed `s12-evidence.json` PASS artifact is available in the repository history/evidence set inspected for this release.

The surviving historical evidence is sufficient to retain the bounded S12/S13 native result, but it is not sufficient to reconstruct the missing structured artifact without inventing fields that the schema requires. In particular, a retroactive PASS JSON would require authentic artifact SHA-256 values, the fixture SHA-256, and per-gate evidence references. Those values are not established by the surviving record and must not be guessed or back-filled from later beta artifacts.

Therefore the traceability decision is final for v0.2.3:

- the historical S12/S13 result remains **PASS for its recorded SHA-bound tested scope** based on Issue #58, Issue #60, PR #68 and the exact-head/post-merge CI chain;
- the structured `s12-evidence.json` artifact is classified **historically unavailable / not reconstructable without fabrication**;
- no retroactive PASS JSON will be created;
- `tools/s12/evidence-template.json` and `validate_evidence.py` remain the required fail-closed mechanism for future campaigns;
- the missing historical JSON is retained as an explicit provenance limitation, not an open request to manufacture or recover data that is no longer evidenced.

This resolves the **decision/traceability gate** for v0.2.3 by choosing the documented non-fabrication path. It does not convert the missing artifact into evidence, does not broaden the native-test claim, and does not authorize release.

## Current release context — 20 September 2026

After the historical S12/S13 chain, frozen beta.2 exposed additional Blender-side findings during owner/internal testing. Issues #82 and #83 were repaired and natively owner-verified on Windows 11 + Blender 5.2.1 LTS, then closed. Those later Blender repairs do not alter the historical S12/S13 AE evidence described above, but they do mean the old beta.2 candidate is no longer the correct current candidate identity.

The frozen `candidate/v0.2.3-beta.3` identity and bounded owner/internal regression are complete for their recorded scope. The S12 structured-evidence traceability decision above is also complete: no retroactive PASS JSON will be fabricated.

Current release blockers/gates include:

1. complete S14B real Japanese target-user validation for broad target-user usability claims, or explicitly narrow the intended claim through review;
2. repository-level governance Issue #18;
3. exact promotion-head and promoted-main CI;
4. explicit exact release authorization;
5. publication plus independent downloaded-asset verification;
6. production update/distribution verification.

Current release state remains **NOT RELEASE READY**.
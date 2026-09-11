# CutBridge S12/S13 Evidence Summary

Status: **S12 PASS / S13 PASS / v0.2.3 STILL UNRELEASED**

This file consolidates the currently verifiable repository and issue evidence for the S12 release-target campaign and S13 repair chain. It is an evidence index, not a substitute for an authentic structured native-evidence artifact.

## Final integrated state

- latest integrated `develop`: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- final native-tested S13F source: `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`;
- exact-head push CI: `34503571091` — PASS;
- PR #68 exact-head CI: `34503805612` — PASS;
- PR #68 merge commit: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- post-merge `develop` CI: `34504009878` — PASS;
- S12 issue #58: closed as completed after reconciliation to PASS;
- S13 issue #60: closed as completed after S13F integration;
- release authorization: `approved: false`;
- GitHub Releases: none.

## Native host evidence

The final repaired path was tested in:

- Adobe After Effects 2026 `26.3x87` / Build 87;
- Windows 11.

The recorded native result for exact commit `9c99ae23...` includes:

- V001 baseline Build/QC success;
- V001→V002 revision success;
- V002→V003 revision success;
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

This exact repair source is `9c99ae23...`.

## SHA-bound integration rule

The native result is valid because the exact tested commit was subsequently pushed and merged intact. Repository history records that it was not amended, rebased, squashed, cherry-picked, or recreated under a different SHA before integration.

That exact-source rule should be preserved for future native validation.

## Latest automated integration evidence

Post-merge CI on `0a86d9a...` records:

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

## Structured evidence-record limitation

The current repository tree does not contain a final committed `s12-evidence.json` PASS record. The repository contains the S12 evidence template and validator, but not a final structured PASS artifact.

Therefore:

- do not claim that a final structured JSON record was committed when it was not;
- do not generate fake historical checksums or evidence paths;
- if the authentic original record exists outside the repository, recover that exact record and validate it;
- otherwise preserve this limitation explicitly in release-readiness documentation.

The absence of the structured file is an **evidence-traceability gap**, not proof that the recorded native run did not happen.

## Release implications

S12/S13 completion removes the previously active product/native revision blocker for the tested scope. It does **not** make v0.2.3 publishable.

Remaining release blockers include:

1. repository-level governance issue #18;
2. branch/tag protection unavailable under the current private-repository plan/configuration;
3. deliberate `develop` → `main` reconciliation;
4. exact promoted-main CI;
5. Japanese target-user validation appropriate to intended claims;
6. exact release authorization;
7. publication and independent downloaded-asset verification;
8. production update/distribution verification.

Current release state remains **NOT RELEASE READY**.
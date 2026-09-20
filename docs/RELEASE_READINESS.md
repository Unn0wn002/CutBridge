# CutBridge v0.2.3 Release Readiness

Status: **UNRELEASED / PUBLICATION BLOCKED**

This is the canonical release-readiness checklist for CutBridge v0.2.3. Green product CI and successful native validation are necessary, but neither is release authorization.

## Current repository boundary

Current integrated `develop` after the S12 traceability reconciliation:

`c8721ece179a3dd9afe0e9676477239872574b8e`

Current release state:

- product version: `0.2.3`;
- S1–S13 product/validation work: integrated or completed as documented below;
- S12 release-target real-host path: PASS after S13F repair chain;
- S13 native repair: PASS / integrated;
- beta.3 owner/internal regression: PASS for the recorded Windows 11 / Blender 5.2.1 / After Effects 2026 v26.3 scope;
- S12 structured-evidence traceability decision: resolved through the documented non-fabrication path;
- v0.2.3 Japanese release-facing claim scope: narrowed; S14B representative-user execution remains NOT_EXECUTED and is not claimed as PASS;
- `release-authorization.json`: `approved: false`;
- GitHub Releases: none;
- repository-level release governance issue #18: OPEN;
- `main` remains unchanged and promotion PR #74 remains open/unmerged;
- next blocking phase: repository governance issue #18, followed by exact promotion-head validation.

Do not edit this checklist to imply publication is allowed while #18 is unresolved or release authorization remains unapproved.

## 1. Product / contract integration

- [x] S1–S9 integrated on `develop`.
- [x] S10A camera/null coordinate, timing, FOV/Zoom contract integrated.
- [x] S10B optional/versioned Blender `handoff_3d` producer integrated.
- [x] S10C managed After Effects Camera/3D Null reconstruction integrated.
- [x] S10C bounded native projection-parity gate passed.
- [x] S11 QA / Docs / Release Engineering integrated.
- [x] S12 release-target campaign executed and reconciled to PASS after repairs.
- [x] S13 real-host Camera/Null revision defects repaired and integrated.
- [x] Historical manifests without `handoff_3d` remain valid.
- [x] Artist-owned object collision handling remains fail-closed.

## 2. Automated QA baseline

Latest authoritative post-merge CI on exact `develop` `c8721ece...` is PASS:

- [x] Python/static contract suite exists and is authoritative.
- [x] Blender 5.2.1 RNA lifecycle gate exists.
- [x] complete Blender/runtime package suite exists.
- [x] deterministic release simulation exists.
- [x] release-authorization regression tests exist.
- [x] release hygiene/checksum/package-content tests exist.
- [x] S6 revision regression suites exist.
- [x] S7 QC+ regression suites exist.
- [x] S8 localization regression suites exist.
- [x] S10C reconstruction regression suite exists.
- [x] S13 3D revision native-host-shaped regression is wired into canonical CI.
- [x] latest static suite: 132 passed + 2 subtests.
- [x] latest complete Blender/runtime suite: 245 passed + 2 subtests.
- [ ] final release-candidate CI PASS on an explicitly frozen `develop` release-candidate SHA.
- [ ] promoted `main` candidate CI PASS on the exact promoted SHA.

The latest green integration SHA is not automatically the release candidate; freezing/promoting is a separate deliberate step.

## 3. Native evidence already recorded

- [x] Blender 5.2.1 LTS S8 Japanese/English narrow-panel + Validate/Build gate.
- [x] Native After Effects S6 revision campaign.
- [x] Native After Effects S7 QC+ campaign after repaired findings.
- [x] After Effects 2026 Build 87 S8 localization/fallback gate.
- [x] After Effects 2026 Build 87 S10C managed Camera/3D Null reconstruction gate.
- [x] S10C maximum recorded 2D projection error `0.00018066 px` against `<= 0.05 px` tolerance.
- [x] S10C repeated Build produced zero duplicate managed Camera/Null layers.
- [x] S10C unmanaged Camera/Null collisions failed closed.
- [x] S13F native-tested commit `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95` passed the repaired AE V001→V002→V003 path.
- [x] S13F native run verified Camera Position/POI/Zoom and Null Position/Scale refresh.
- [x] S13F native run verified QC+, artist-state preservation, zero duplicate managed 3D layers, and save/close/reopen persistence.
- [x] the exact native-tested S13F commit was merged intact through PR #68 and post-merge CI passed on `0a86d9a...`.

These are bounded evidence statements. They do not certify every target host/OS combination.

## 4. S12 release-target end-to-end evidence

Status: **PASS AFTER S13F REPAIR CHAIN / STRUCTURED-EVIDENCE TRACEABILITY DECISION RESOLVED**.

The initial S12 campaign correctly produced `FAIL_REPAIR_REQUIRED` after real-host defects were found. The acceptance criteria were not weakened. S13 then repaired the native findings, culminating in exact candidate `9c99ae23...`, which passed the previously failing real-AE V001→V002→V003 path and persistence checks. Issue #58 was reconciled to PASS and closed after exact-head push CI, PR CI, merge, and post-merge CI all passed.

Completed native behavior includes:

- [x] release-target Blender/AE campaign was actually executed;
- [x] V001 baseline Build/QC behavior established;
- [x] compatible V001→V002 revision path passes after repairs;
- [x] compatible V002→V003 revision path passes after repairs;
- [x] Camera/Null ownership migrates correctly;
- [x] Camera Position/POI/Zoom refreshes correctly;
- [x] Null Position/Scale refreshes correctly;
- [x] QC+ remains clean on the repaired path;
- [x] artist effects/masks/opacity/manual state are preserved for the tested scope;
- [x] no duplicate managed Camera/Null layers are created;
- [x] save → close → reopen persistence passes for the tested scope.

Evidence-traceability resolution:

- [x] confirmed that a final committed structured `s12-evidence.json` PASS record is not present in the retained repository evidence;
- [x] audited the surviving Issue #58 / Issue #60 / PR #68 / CI evidence and preserved the historical SHA-bound native result without reattributing it to later commits;
- [x] determined that the missing PASS JSON cannot be reconstructed truthfully because required historical artifact hashes, fixture hash and per-gate evidence references are not all established by the surviving record;
- [x] selected the fail-closed non-fabrication path: no retroactive PASS JSON will be created;
- [x] retained the missing JSON as an explicit historical provenance limitation and kept the S12 template/validator requirement for future campaigns.

This closes the S12 **traceability decision gate** for v0.2.3. It does not assert that the missing structured artifact existed, does not broaden S12 native evidence, and does not authorize release.

See `S12_S13_EVIDENCE_SUMMARY.md`.

## 5. Japanese target-user evidence / v0.2.3 claim scope — S14

S14A protocol preparation is complete. S14B representative Japanese-speaking target-user execution remains **NOT_EXECUTED**.

For v0.2.3, the release-facing claim has been deliberately narrowed rather than treating missing participant evidence as a PASS:

- [x] Japanese-first UI with deterministic English fallback may be described as an implemented product characteristic;
- [x] documented engineering/native Japanese/English UI and workflow checks may be described only for their recorded tested environments;
- [x] beta.3 owner/internal workflow validation may be described only as owner/internal engineering evidence for the tested scope;
- [x] no claim will state or imply representative Japanese-user validation, customer validation, proven ease of use, broad Japanese production usability, statistical usability evidence, or S14B PASS;
- [x] S14B remains available as a future protocol and becomes required before introducing broader Japanese target-user usability claims.

This **claim-scope narrowing resolves the v0.2.3 S14 release-claim gate**. It does not create target-user evidence and does not change the S14 evidence template from `NOT_EXECUTED`.

See `S14_JP_USER_VALIDATION.md`.

## 6. Repository governance — BLOCKED BY #18

Required before RC/stable publication:

- [ ] protect `main` against accidental/direct changes outside the intended release path;
- [ ] protect `develop` against accidental/direct changes outside the intended integration path;
- [ ] require authoritative CI for protected integration/promotion;
- [ ] restrict creation/update/deletion of `v*` release tags to the intended release path or equivalent;
- [ ] protect against historical-workflow publication that bypasses current release safeguards;
- [ ] record repository-admin settings evidence;
- [ ] validate unauthorized and stale-tag negative cases;
- [ ] keep issue #18 OPEN until these controls are actually available and tested.

Current private-repository plan/configuration does not expose the required GitHub ruleset capability. Do **not** make the repository public merely to satisfy this checklist. Workflow-local authorization is defense-in-depth, not a replacement for repository governance.

## 7. Freeze release candidate on `develop`

Only after required native/product/evidence scope is complete:

- [x] beta.3 was frozen at `00d2e51a6266d140d499e48b45557eb084568d9f` and owner/internal regression passed for the recorded scope;
- [ ] choose the exact final promotion head after documentation/governance prerequisites are satisfied;
- [ ] record complete candidate diff and test evidence;
- [ ] require authoritative candidate CI PASS;
- [ ] stop feature changes on that candidate;
- [ ] if the candidate changes, invalidate candidate-specific evidence and repeat affected gates.

The historical beta.3 runtime candidate remains SHA-bound to `00d2e51a...`. Current `develop` includes later documentation/test reconciliation and is not automatically authorized for promotion or release.

## 8. Deliberate `develop` → `main` promotion

`main` and `develop` are materially diverged. **Do not perform a blind merge.**

The current release architecture on `develop` is also stronger than the older workflow on `main`; promotion must preserve the hardened validation/package/publish separation and release-authorization checks.

Before promotion:

- [ ] compare current `main...candidate` file-by-file;
- [ ] identify the five `main`-side commits/changes that are absent from `develop` and determine which release-lock behavior must be deliberately preserved;
- [ ] preserve the hardened `develop` release workflow rather than reverting to the older `main` workflow;
- [ ] produce an explicit promotion tree/commit whose contents are explainable;
- [ ] verify the promoted `main` tree matches intended candidate contents plus deliberately preserved release controls;
- [ ] require authoritative CI PASS on the exact promoted `main` SHA;
- [ ] keep release authorization false throughout promotion validation.

## 9. Release authorization

Authorization is one exact tuple, not a reusable global switch.

Before changing `release-authorization.json`:

- [ ] governance section complete;
- [x] evidence scope is complete for the **narrowed** v0.2.3 Japanese release-facing claim; S14B remains NOT_EXECUTED and no broad representative-user claim is permitted;
- [ ] exact promoted `main` SHA has green authoritative CI;
- [ ] choose exact release tag;
- [ ] derive intended channel and prerelease state;
- [ ] update authorization for that exact tag/channel/prerelease tuple only;
- [ ] validate the authorization change itself;
- [ ] do not authorize a stale or non-main candidate.

Supported tag forms:

- stable: `vX.Y.Z`;
- RC/beta: `vX.Y.Z-rc.N` or `vX.Y.Z-beta.N`;
- development validation: `vX.Y.Z-dev.N`.

## 10. Publication

Only after sections 1–9 are satisfied:

- [ ] create the exact authorized tag on current `main`;
- [ ] require Release workflow validation PASS;
- [ ] require clean-runner package build PASS;
- [ ] require checksum verification PASS;
- [ ] require release metadata/tag/channel/prerelease validation PASS;
- [ ] publish the GitHub Release only through the intended workflow;
- [ ] verify expected assets are present.

Never create a tag merely to test whether the workflow blocks it while repository governance is incomplete.

## 11. Independent published-asset verification

After a real authorized publication:

- [ ] download `CutBridge-Blender-<tag>.zip`;
- [ ] download `CutBridge-AfterEffects-<tag>.zip`;
- [ ] download `SHA256SUMS.txt` and `release-metadata.json`;
- [ ] recompute SHA-256 independently;
- [ ] verify checksums and archive contents;
- [ ] verify Blender archive contains expected extension files + `LICENSE`;
- [ ] verify AE archive contains `CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, `localization.js`, `INSTALL.md`, and `LICENSE`;
- [ ] verify metadata tag/version/channel/prerelease/artifact filenames;
- [ ] record verification evidence.

## 12. Production update/distribution verification

GitHub Release publication alone is not a functioning production update channel.

- [ ] deploy approved artifacts to a distribution endpoint separate from the private source repository;
- [ ] generate/deploy the production Blender extension repository index as applicable;
- [ ] deploy the CutBridge release-notification index;
- [ ] validate schema and HTTPS reachability;
- [ ] verify Stable/Beta/Development filtering behavior as claimed;
- [ ] verify Blender online-access-off behavior performs no request;
- [ ] verify notification-only behavior does not self-install or replace active code;
- [ ] verify rollback/previous-stable availability policy.

## 13. Final release decision

Use one of these states:

- **NOT RELEASE READY** — one or more required gates remain incomplete.
- **RC ELIGIBLE** — release-target validation and governance are complete, but stable-specific acceptance is not yet complete.
- **STABLE ELIGIBLE** — every stable-release gate is complete and evidence is recorded.
- **PUBLISHED / VERIFIED** — authorized publication completed and downloaded assets/update distribution were independently verified.

### Current verdict

**NOT RELEASE READY.**

S12/S13 product/native blockers are resolved for their tested scope, the S12 structured-evidence traceability decision is resolved through the documented non-fabrication path, and the v0.2.3 Japanese release-facing claim is narrowed so S14B is not represented as completed or required for that narrow claim. Repository governance #18, deliberate promotion to `main`, exact release authorization, publication, and distribution verification remain incomplete.

## Related documents

- `S12_E2E_VALIDATION.md`
- `S12_S13_EVIDENCE_SUMMARY.md`
- `UPDATE_ARCHITECTURE.md`
- `COMPATIBILITY.md`
- `TEST_PLAN.md`
- `COMPLETION_STATUS.md`
- `ROADMAP.md`
- `TECHNICAL_DEBT.md`
- `QUICK_START.md`
- `QUICK_START_JA.md`
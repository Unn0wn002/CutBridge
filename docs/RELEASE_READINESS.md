# CutBridge v0.2.3 Release Readiness

Status: **UNRELEASED / PUBLICATION BLOCKED**

This is the canonical release-readiness checklist for CutBridge v0.2.3. It separates evidence that is already complete from work that must still happen before an RC or stable publication claim.

Green product CI is necessary but is **not** release authorization.

## Current repository boundary

At S11 start:

- `main`: conservative release-locked baseline;
- `develop`: active validated integration branch;
- product version: `0.2.3`;
- `release-authorization.json`: `approved: false`;
- release tags: none;
- GitHub Releases: none;
- repository-level release governance issue #18: OPEN.

Do not edit this checklist to imply publication is allowed while #18 is unresolved and release authorization remains unapproved.

## 1. Product / contract integration

- [x] S1–S9 integrated on `develop`.
- [x] S10A camera/null coordinate, timing, FOV/Zoom contract integrated.
- [x] S10B optional/versioned Blender `handoff_3d` producer integrated.
- [x] S10C managed After Effects camera/3D Null reconstruction integrated.
- [x] S10C bounded native projection parity gate passed.
- [x] Historical manifests without `handoff_3d` remain valid.
- [x] Artist-owned object collision handling remains fail-closed.

## 2. Automated QA baseline

Authoritative CI must keep both jobs green on the exact candidate:

- [x] Python/static contract suite exists and is authoritative.
- [x] Blender 5.2.1 RNA lifecycle gate exists.
- [x] complete Blender/runtime package suite exists.
- [x] deterministic release simulation exists.
- [x] release authorization regression tests exist.
- [x] release hygiene/checksum/package-content tests exist.
- [x] S6 revision regression suites exist.
- [x] S7 QC+ regression suites exist.
- [x] S8 localization regression suites exist.
- [x] S10C reconstruction regression suite exists.
- [ ] final release-candidate CI PASS on the exact frozen `develop` SHA.
- [ ] promoted `main` candidate CI PASS on the exact promoted SHA.

## 3. Native evidence already recorded

- [x] Blender 5.2.1 LTS S8 Japanese/English narrow-panel + Validate/Build gate.
- [x] Native After Effects S6 revision campaign.
- [x] Native After Effects S7 QC+ campaign after repaired findings.
- [x] After Effects 2026 Build 87 S8 localization/fallback gate.
- [x] After Effects 2026 Build 87 S10C managed camera/3D Null reconstruction gate.
- [x] S10C maximum recorded 2D projection error `0.00018066 px` against `<= 0.05 px` tolerance.
- [x] S10C repeated Build produced zero duplicate managed camera/null layers.
- [x] S10C unmanaged camera/null collisions failed closed.

These are bounded evidence statements. They do not certify every target host/OS combination.

## 4. S12 release-target end-to-end evidence — REQUIRED

Do not check these from headless tests alone.

- [ ] install the exact candidate Blender artifact in the release-target Blender GUI build;
- [ ] create/validate a representative cut;
- [ ] exercise Manual and any release-claimed Studio Preset workflow;
- [ ] generate a real package from the exact candidate artifact;
- [ ] produce representative real render sequences;
- [ ] load the exact candidate AE runtime files in the release-target AE host;
- [ ] Build + QC the real package;
- [ ] exercise V001→V002→V003 compatible revision behavior;
- [ ] verify artist effects/masks/transforms/parenting/timing/layer order and unrelated objects are preserved where claimed;
- [ ] save, close, reopen, reload CutBridge, and repeat relevant Build/QC checks;
- [ ] exercise the release-claimed S10C camera/Null handoff using candidate artifacts;
- [ ] record OS/path/Unicode behavior appropriate to the release claim;
- [ ] record exact host versions, artifact checksums, fixture identity, screenshots/logs, and outcome.

## 5. Japanese target-user evidence — REQUIRED FOR TARGET-USER CLAIMS

S14 prepares this gate.

- [ ] define Japanese user task script and acceptance criteria;
- [ ] test with actual target users if making production-usability claims;
- [ ] record task completion, error/rework observations, terminology feedback, and material blockers;
- [ ] do not fabricate participants or measurements.

A Japanese-first UI implementation is not equivalent to Japanese target-user validation.

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

Workflow-local authorization is defense-in-depth, not a replacement for this section.

## 7. Freeze release candidate on `develop`

Only after product scope and required real-host gates are complete:

- [ ] choose one exact `develop` SHA as the release candidate;
- [ ] record complete candidate diff and test evidence;
- [ ] require authoritative candidate CI PASS;
- [ ] stop feature changes on that candidate;
- [ ] if the candidate changes, invalidate the previous release-candidate evidence and repeat the required gates.

## 8. Deliberate `develop` → `main` promotion

`main` and `develop` are materially diverged. Do **not** perform a blind merge.

- [ ] compare current `main...candidate` file-by-file;
- [ ] identify required `main`-only release-lock/history changes;
- [ ] produce an explicit promotion tree/commit whose contents are explainable;
- [ ] preserve release safeguards;
- [ ] verify the promoted `main` tree matches the intended candidate contents plus deliberately preserved release controls;
- [ ] require authoritative CI PASS on the exact promoted `main` SHA.

## 9. Release authorization

Authorization is one exact tuple, not a reusable global switch.

Before changing `release-authorization.json`:

- [ ] governance section complete;
- [ ] release-target validation complete;
- [ ] exact promoted `main` SHA has green authoritative CI;
- [ ] choose exact release tag;
- [ ] derive intended channel and prerelease state;
- [ ] update authorization for that exact tag/channel/prerelease tuple only;
- [ ] validate the authorization change itself;
- [ ] do not authorize a stale or non-main candidate.

Supported tag forms:

- stable: `vX.Y.Z`
- RC/beta: `vX.Y.Z-rc.N` or `vX.Y.Z-beta.N`
- development validation: `vX.Y.Z-dev.N`

## 10. Publication

Only after sections 1–9 are satisfied:

- [ ] create the exact authorized tag on current `main`;
- [ ] require Release workflow validation PASS;
- [ ] require clean-runner package build PASS;
- [ ] require checksum verification PASS;
- [ ] require release metadata/tag/channel/prerelease validation PASS;
- [ ] publish the GitHub Release only through the intended workflow;
- [ ] verify expected assets are present.

Never create a tag merely to see whether the release workflow blocks it when repository governance is still incomplete.

## 11. Independent published-asset verification

After a real authorized publication:

- [ ] download `CutBridge-Blender-<tag>.zip` from the published Release;
- [ ] download `CutBridge-AfterEffects-<tag>.zip`;
- [ ] download `SHA256SUMS.txt`;
- [ ] download `release-metadata.json`;
- [ ] recompute SHA-256 independently from the downloaded assets;
- [ ] verify checksums match;
- [ ] inspect archive contents;
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

Current v0.2.3 state during S11: **NOT RELEASE READY** because #18 governance, S12 end-to-end release-target validation, later target-user evidence where claimed, deliberate promotion, authorization, publication, and distribution verification remain incomplete.

## Related documents

- [UPDATE_ARCHITECTURE.md](UPDATE_ARCHITECTURE.md)
- [COMPATIBILITY.md](COMPATIBILITY.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [COMPLETION_STATUS.md](COMPLETION_STATUS.md)
- [ROADMAP.md](ROADMAP.md)
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)
- [QUICK_START.md](QUICK_START.md)
- [QUICK_START_JA.md](QUICK_START_JA.md)

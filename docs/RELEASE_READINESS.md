# CutBridge Release Readiness

Status: **v0.2.3 PUBLISHED / VERIFIED; v0.2.4 UNRELEASED / NOT AUTHORIZED**

This is the canonical release-readiness record. It preserves useful v0.2.3 pre-release evidence while distinguishing it from the current v0.2.4 development boundary. Green product CI and successful native validation are necessary, but neither is release authorization.

## Current repository boundary

Current protected branch and release state — 23 September 2026:

- protected `main`: `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f`;
- stable tag `v0.2.3`: the same exact SHA as `main`;
- protected `develop`: `ef5911a83270a4ce8121741ada2d2726fa09ec29`; this is also the frozen `candidate/v0.2.4-beta.1` source SHA;
- PR #92 updater/distribution/version baseline: merged into protected `develop`;
- PR #93 backward-compatible per-pass output formats: merged; Issue #80 native acceptance completed 10/10 and exact post-merge CI passed;
- PR #94 release-tag eligibility main-push trigger fix: merged; exact post-merge CI run `35756924486` passed both required jobs;
- PR #95 integration-sweep documentation reconciliation: merged; post-merge push CI run `35797413040` passed both required jobs;
- frozen candidate `candidate/v0.2.4-beta.1`: exact SHA `ef5911a83270a4ce8121741ada2d2726fa09ec29`; deterministic Blender ZIP SHA-256 `3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2`; deterministic After Effects ZIP SHA-256 `e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b`.

Stable v0.2.3 state:

- product version: `0.2.3`;
- release: published, non-draft, non-prerelease, and immutable;
- published artifacts and `release-metadata.json`: independently downloaded and verified;
- production D1 distribution: deployed separately in `Unn0wn002/cutbridge-distribution` at commit `635c1384af2649d4ce49705cce41f98826a861cc`;
- notification index: `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- Blender repository: `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`;
- S1–S13 product/validation work: integrated or completed as documented below;
- S12 release-target real-host path: PASS after S13F repair chain;
- S13 native repair: PASS / integrated;
- beta.3 owner/internal regression: PASS for the recorded Windows 11 / Blender 5.2.1 / After Effects 2026 v26.3 scope;
- S12 structured-evidence traceability decision: resolved through the documented non-fabrication path;
- v0.2.3 Japanese release-facing claim scope: narrowed; S14B representative-user execution remains NOT_EXECUTED and is not claimed as PASS;
- repository visibility: public;
- active governance rulesets: `Protect main`, `Protect develop`, `Protect release tags`, and `Require release tag eligibility`;
- repository-governance Issue #18: **OPEN**; its latest live evidence records completed v0.2.3 authorization, publication, independent asset verification, and production D1 deployment.

Active v0.2.4 remains fail-closed: `release-authorization.json` is unapproved, no v0.2.4 tag/GitHub Release/distribution entry exists, automatic startup update scheduling remains disabled, and S14B remains `NOT_EXECUTED`. The exact beta.1 candidate has completed the bounded native release-candidate gate for the recorded Windows 11 / Blender 5.2.1 / After Effects 2026 scope; this evidence does not authorize promotion or publication.

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

Historical v0.2.3 promotion evidence is PASS: pre-promotion PR CI `35511056270` attempt 2 on exact `develop` head `501f9bd6...`, and post-promotion `main` CI `35513361337` on `049081f0...`:

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
- [x] latest exact-head static suite on frozen candidate / protected `develop` `ef5911a83270a4ce8121741ada2d2726fa09ec29`: 147 passed + 2 subtests.
- [x] latest exact-head complete Blender/runtime suite: 307 passed, 72 warnings + 2 subtests.
- [x] exact-head release simulation built both v0.2.4 ZIPs and verified `SHA256SUMS.txt`.
- [x] exact-head Blender 5.2.1 RNA register/unregister/re-register lifecycle step passed.
- [x] exact-head post-merge/candidate push CI run `35797413040` passed `static-validation` and `blender-52-rna-runtime`.
- [x] final promotion-head CI PASS on explicitly frozen `develop` SHA `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50`.
- [x] promoted `main` candidate CI PASS on exact promoted SHA `049081f0fe3d3e74d77db807910c2e0fff56fe73`.

Those promotion checks established the pre-release baseline. The later v0.2.3 authorization, publication, asset verification, and production D1 deployment are now complete; every future release must repeat the applicable gates on its own exact candidate.

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

### v0.2.4 beta.1 exact-candidate native gate

The frozen v0.2.4 beta.1 candidate is `candidate/v0.2.4-beta.1` at `ef5911a83270a4ce8121741ada2d2726fa09ec29`, identical to protected `develop` at the recorded gate.

- [x] deterministic Blender candidate ZIP SHA-256: `3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2`;
- [x] deterministic After Effects candidate ZIP SHA-256: `e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b`;
- [x] bounded local Windows native candidate campaign recorded PASS for Blender 5.2.1 LTS and After Effects 2026 26.3x87 Build 87 for the tested scope, including exact-artifact installation, package/per-pass behavior, Issue #83 safety, updater safety, AE Build/QC+/revision/artist-state/persistence and negative-manifest handling;
- [x] focused Issue #82 exact-candidate rerun on Blender 5.2.1 LTS completed a 3-frame mixed-format interactive Render Animation with the normal CutBridge N-panel active, produced 12 non-zero expected outputs, generated no new crash dump, remained responsive, used Blender's normal quit operator without external force termination, and exited with process code `0`;
- [x] the prior forced-termination evidence ambiguity is cleared for this candidate.

This native evidence is bounded to the recorded hosts. It does not validate Blender 4.2/4.5, does not constitute S14B representative-user validation, and does not authorize promotion, tagging, or publication.

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

## 6. Repository governance — v0.2.3 COMPLETE / Issue #18 OPEN

Required governance configuration is now present:

- [x] `main` protected by active ruleset `Protect main` (ID 23728298);
- [x] `develop` protected by active ruleset `Protect develop` (ID 23728435);
- [x] authoritative checks `static-validation` and `blender-52-rna-runtime` required for protected branch updates;
- [x] release-tag creation/update/deletion restricted by `Protect release tags` (ID 23728606);
- [x] matching `v*.*.*` tags independently require no-bypass status check `release-tag-eligibility` through ruleset `Require release tag eligibility` (ID 23728953);
- [x] `.github/CODEOWNERS` covers release-sensitive controls as defense-in-depth;
- [x] exact-main/tag/channel/prerelease authorization validation remains fail-closed;
- [x] controlled unauthorized-current-main and stale/historical tag attempts were rejected by `GH013`;
- [x] explicitly authorized exact-current-main eligibility passed for v0.2.3;
- [x] v0.2.3 tag creation and workflow publication completed under the configured controls;
- [x] published assets, metadata, and production D1 distribution were independently verified.

Historical pre-release checkpoint — 20 September 2026:

- repository is public;
- `main` and `develop` report `protected: true`;
- all four governance rulesets above are ACTIVE;
- PR #74 promotion to protected `main` completed successfully;
- promoted-main CI `35513361337` passed both required jobs;
- v0.2.3 had not yet been authorized, tagged, or published at that checkpoint.

Current state — 22 September 2026: Issue #18 remains open as the live governance/release evidence log. Its latest evidence records v0.2.3 as published and independently verified with production D1 deployed. Active v0.2.4 development has restored authorization to fail-closed.

## 7. Historical v0.2.3 candidate freeze on `develop`

Promotion candidate record:

- [x] historical beta.3 runtime candidate remains SHA-bound to `00d2e51a6266d140d499e48b45557eb084568d9f` with owner/internal regression PASS for the recorded scope;
- [x] final promotion head frozen at `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50`;
- [x] candidate diff/test/governance evidence recorded in PR #74 and Issue #18;
- [x] fresh authoritative PR CI `35511056270` attempt 2 PASS on the exact promotion head;
- [x] feature changes stopped for the promotion operation.

The frozen promotion head included later documentation/governance reconciliation beyond the historical beta.3 runtime SHA. That distinction remains explicit.

## 8. Historical v0.2.3 `develop` → `main` promotion

**COMPLETE / VERIFIED.**

- [x] prior `main`-only history was reconciled without changing the validated product tree;
- [x] hardened validation/package/publish separation and fail-closed release authorization were preserved;
- [x] PR #74 promoted exact `develop` head `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50`;
- [x] protected `main` merge commit is `049081f0fe3d3e74d77db807910c2e0fff56fe73`;
- [x] compare shows `main` one merge commit ahead of `develop` with zero file differences;
- [x] post-promotion CI `35513361337` PASS on exact promoted `main`;
- [x] release authorization remained false throughout promotion.

Promotion completion does not authorize tagging or publication.

## 9. Release authorization

Authorization is one exact tuple, not a reusable global switch.

For v0.2.3:

- [x] governance enforcement-path validation completed under Issue #18;
- [x] evidence scope is complete for the **narrowed** v0.2.3 Japanese release-facing claim; S14B remains NOT_EXECUTED and no broad representative-user claim is permitted;
- [x] exact current `main` SHA `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f` was authorized for `v0.2.3` / stable / non-prerelease;
- [x] the authorization change and eligibility check passed before tag creation.

For active v0.2.4 development, `release-authorization.json` is restored to `approved: false` with null tag/channel/prerelease. No v0.2.4 authorization has occurred.

Supported tag forms:

- stable: `vX.Y.Z`;
- RC/beta: `vX.Y.Z-rc.N` or `vX.Y.Z-beta.N`;
- development validation: `vX.Y.Z-dev.N`.

## 10. Publication

v0.2.3 publication completed after sections 1–9 were satisfied:

- [x] exact authorized tag created on current `main`;
- [x] GitHub Release published as non-draft and non-prerelease;
- [x] checksums and release metadata independently validated;
- [x] expected four assets verified present.

The exact internal Release workflow job record is not asserted here; the published output was independently downloaded and verified.

Future releases must repeat these requirements on their own exact candidate. Never create a tag merely to test whether the workflow blocks it while repository governance is incomplete.

## 11. Independent published-asset verification

Independent v0.2.3 verification:

- [x] downloaded both ZIPs, `SHA256SUMS.txt`, and `release-metadata.json`;
- [x] recomputed SHA-256 independently;
- [x] Blender ZIP: `d665f5a20de7cbdd054a181c74b42c2d8bc68ce5e754592dc63d3d098b0c173c`;
- [x] After Effects ZIP: `85be3e40ed07dfa2db71007dbdb5266cd968a970737af43bb64a7a4d64b9c98a`;
- [x] verified checksums, metadata identity, archive integrity, required contents, and licenses;
- [x] recorded the verification evidence in Issue #18.

## 12. Production update/distribution verification

GitHub Release publication alone is not a functioning production update channel.

- [x] deployed approved v0.2.3 artifacts separately in `Unn0wn002/cutbridge-distribution`;
- [x] deployment commit: `635c1384af2649d4ce49705cce41f98826a861cc`;
- [x] Blender repository generated with Blender 5.2.1 official tooling and deployed at `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`;
- [x] notification index deployed at `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- [x] HTTPS delivery, schemas, production downloads, checksums, Blender sync/discovery/install, and versioned retention policy verified;
- [x] v0.2.3 left immutable; future stable versions must be additive so earlier stable artifacts remain available for rollback.

The v0.2.4 manual checker uses the verified notification index. Automatic startup update scheduling remains disabled. No v0.2.4 distribution entry exists.

## 13. Final release decision

Use one of these states:

- **NOT RELEASE READY** — one or more required gates remain incomplete.
- **RC ELIGIBLE** — release-target validation and governance are complete, but stable-specific acceptance is not yet complete.
- **STABLE ELIGIBLE** — every stable-release gate is complete and evidence is recorded.
- **PUBLISHED / VERIFIED** — authorized publication completed and downloaded assets/update distribution were independently verified.

### Current verdict

**v0.2.3 PUBLISHED / VERIFIED.**

Stable v0.2.3 is released and immutable at `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f`; its GitHub Release, artifacts, metadata, and separate production D1 distribution are verified. Active v0.2.4 is **CANDIDATE VALIDATED / NOT AUTHORIZED**: PR #92, PR #93, PR #94, and PR #95 are integrated with green exact-head CI; Issue #80 is completed; `candidate/v0.2.4-beta.1` is frozen at `ef5911a83270a4ce8121741ada2d2726fa09ec29`; deterministic candidate packaging and the bounded native Blender/After Effects candidate campaign are recorded PASS for the tested scope; the focused Issue #82 clean-exit rerun is PASS; authorization remains fail-closed; startup scheduling remains disabled; S14B remains `NOT_EXECUTED`; and no v0.2.4 tag, Release, or distribution entry exists. The next gate is promotion-readiness reconciliation plus exact-head CI, followed by a deliberate protected `develop` → `main` promotion PR.

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

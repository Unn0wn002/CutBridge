# CutBridge Release Readiness

**Non-VM preparation: NOT_INSTALLED / NOT_ACCEPTED.** Fixture transfer is verified at a111c61 (all 53 harness/fixture inputs). The owner approved [Sandboxie-Plus 1.18.8 laptop preparation](NON_VM_NATIVE_CONFIGURATION_2026-10-22.md#approved-preparation-and-laptop-handoff) on 22 October. Preparation approval covers the named facility and separate test identity; installation and effective controls are not yet observed. Continue in laptop Codex; this desktop session cannot control that laptop. Native controls and AE provenance remain unaccepted. No VM investigation, candidate execution or release occurred.

## Laptop fixture receipt — 22 October 2026

**Fixture transfer verified and staged; native verdict remains INSUFFICIENT EVIDENCE / HOLD RELEASE.** The laptop ZIP matches SHA-256 `d355a28913c12e7f65f9a8ddd126b62e1381c7ebdf92b36a2ef208ffb37f94b4`. All 39 fixture sizes/hashes match in fresh archive extraction, the owner's extracted folder and the operator packet. Added 39 files with zero conflicts/overwrites; all 24 prior packet files remain unchanged. The packet now has **63/73 exact historical entries**, including **53/53 harness/fixture inputs**; 10 historical root/review metadata entries remain explicitly accounted for, without relabeling old environment receipts.

[Actual laptop receipt, inventories and next prerequisite](evidence/20261022-pr114-laptop-fixture-transfer/README.md). Transport is complete. Next operator action: supply the actual non-VM execution configuration and control evidence for acceptance (owner-file/credential denial, network denial, read-only inputs, confined writable profiles/outputs and watchdog). AE vendor provenance remains separately unresolved. No CutBridge candidate code/test, application launch or VM investigation occurred during transfer. Frozen runtime/packages, release authorization false and production v0.2.3 remain unchanged. Earlier missing-fixture statements below describe preserved checkpoints.

## Laptop direct-host checkpoint — 22 October 2026

**INSUFFICIENT EVIDENCE / HOLD RELEASE.** Direct blank startup completed on laptop AYAKUMI_NOZOMI_: Blender **5.2.3 LTS / e13b728c6880**, RTX 3050 Ti / OpenGL 4.6 NVIDIA 617.42, PID 5608, normal exit 0; AE **26.5.0 Build 89**, empty workspace, no compatibility conflicts, CUDA selected, PID 4176, normal exit 0. Both installed application-tree inventories are unchanged. AE's core DLL still reports **HashMismatch**, cause unknown. No CutBridge/probe/native campaign was executed.

[The laptop evidence and exact next prerequisite](evidence/20261022-pr114-laptop-direct/README.md) supersede earlier environment actions: the owner requires direct applications and **no further Hyper-V, VMware or Sandbox creation, launch or troubleshooting**. The missing non-VM boundary is enforced separation from owner credentials/HOME/private files, effective network denial, immutable read-only inputs and confined output/temp/profile/cache writes. Temporary profile redirection alone is insufficient. Accepted AE vendor provenance also remains unresolved. No machine security/licensing settings were changed.

The original artifact is now on the laptop: outer SHA-256 and all 48 evidence sums, bootstrap, four repeated assets and recorded input inventories verify. Exact AE/Blender ZIP hashes remain frozen to source `5aa2da24fc8be41626ee84178c7fdce05d02eebc`. Fourteen retained harness/config files recovered exactly. The desktop has now verified and packaged all **39 missing fixture files** (three manifests, 36 renders) without regeneration; [the exact transfer ZIP and owner copy step](evidence/20261022-pr114-desktop-fixture-transfer/README.md) are ready. Laptop delivery and all 39 laptop-side checks remain unobserved. The partial packet has 24/73 exact historical handoff entries. No fixture regeneration, new product rerun or runtime change occurred. All open current-package native/release gates remain unexecuted; release authorization is false, v0.2.4 immutable/held, production v0.2.3.

## Prior desktop checkpoints (preserved)

**Current environment verdict: INSUFFICIENT EVIDENCE.** VMware Tools is now **ok/current** (legacy integer 13344), SVGA WDDM **9.17.11.0003 build 25171296** is loaded, and vendor logs confirm a guest restart after installation. The owner’s one post-Tools launch reaches **Blender 5.2.2 — Platform Unsupported**, reporting VMware SVGA3D / OpenGL 4.3 Core / Mesa 24.1.0. This changed rejection supersedes the missing-driver hypothesis; its exact failing capability remains undetermined. [The actual post-Tools record](evidence/20261021-pr114-guest-provisioning/vmware-post-tools-r11/OPERATOR_ACTION.md) preserves both failures. The owner reports a second laptop with Blender/AE and requested [the laptop continuation prompt](LAPTOP_NATIVE_HANDOFF_2026-10-22.md). Its actual versions, blank startup and isolation remain unverified. No current candidate native/release gate passed or CutBridge defect observed; frozen bytes, ancestry, prior evidence and artist work remain preserved.

Current setup checkpoint: Quick Create is open; Windows-image suitability remains unestablished, and the official current Windows ISO download request was blocked by Chrome. [The retained gallery/download record](evidence/20261021-pr114-guest-provisioning/quick-create-r3/OPERATOR_ACTION.md) names the one immediate manual selection needed and distinguishes metadata/URL availability from licensed guest availability. No native or release gate is newly passed; candidate bytes and earlier evidence remain unchanged.

Latest virtualization checkpoint: selected local Hyper-V host has no listed VMs; the normal signed Quick Create launcher is waiting at protected Windows elevation consent. [Exact action and evidence](evidence/20261021-pr114-guest-provisioning/quick-create-r2/OPERATOR_ACTION.md) replace the earlier host-selection request. No native or release gate is passed by this setup observation; no failed Sandbox attempt was repeated.

Latest setup result: **INSUFFICIENT EVIDENCE**. A fresh Sandbox provisioning attempt crashed before a usable guest (`0x80370106`), and Hyper-V Manager is elevated above the UI helper. [The setup record](evidence/20261021-pr114-guest-provisioning/OPERATOR_ACTION.md) preserves the exact error, official staged installers and immediate host-node selection needed from the operator. No current native case, screenshot or release gate is newly passed; existing candidate bytes and completed checks remain unchanged.

Continuation: package retrieval is complete. [PC verification](evidence/20261021-pr114-native-continuation/PC_PACKAGE_RECEIPT.json) binds both ZIP hashes and raw-source AE files; [the handoff](evidence/20261021-pr114-native-continuation/OPERATOR_HANDOFF.md) records remaining native cases. The original ChatGPT JSON was inaccessible; its user-supplied summary is retained without claiming original bytes. A fresh transfer runner recomputed the exact outer archive hash and inspected ZIPs/repeats; the PC verified all 11 transferred files. No native execution or qualified screenshot was produced. **HOLD / INSUFFICIENT EVIDENCE** continues because no suitable isolated, normally provisioned AE guest was established. AI administrative review and deferred representative-user research are not additional blockers.

[AI code/evidence review completed](AI_RELEASE_REVIEW_2026-10-21.md) for source `5aa2da24fc8be41626ee84178c7fdce05d02eebc`: CI **396 passed + 2 subtests**, reviewed isolated canonical checks PASS, package download verification recorded, release decision **HOLD / INSUFFICIENT EVIDENCE**. Administrative AI review does not replace missing native acceptance. No protected promotion, authorization or publication is performed.

Target: **Sunday, 25 October 2026 (Asia/Jakarta)**, confirmed by the owner. This supersedes the earlier 22 October working target. Scope is frozen; feature development stops at a qualified published release, with critical defects only afterward. See [the bounded release policy](FREE_RELEASE_2026-10-25.md).

The current branch `fix/free-release-20261021` retains all PR #113 commits and adds the dockable-first installation/compact ScriptUI/in-panel Build-QC patch. Earlier AE runtime/package hashes and frozen-runtime statements below describe historical candidates; they do not qualify this changed AE runtime. Historical 396-test/18-suite and Blender evidence remain bound to their exact recorded inputs.

The owner authorizes a separately documented AI code/evidence review instead of owner-controlled administrative human review for this release. This does not waive native acceptance or enforced GitHub approvals. S14B remains NOT_EXECUTED; unsupported channels and broad compatibility/commercial claims remain excluded.

Current native verdict: **INSUFFICIENT EVIDENCE**. Blank owner-session AE/Blender workspaces initialize, but the 19 October provisioned Sandbox is no longer present and the installed AE core DLL still reports HashMismatch. No current candidate code has been loaded into the owner session. The required isolated native campaign and qualified-build screenshots remain unexecuted. Release authorization remains false; v0.2.4 is immutable/held, production remains v0.2.3.

## Historical records (retain original identities and decisions)


Validation closeout — **17 October 2026: INSUFFICIENT EVIDENCE**. Frozen engineering SHA `639374ce5f1b5f0d36847258d052c36ab21dd208` retains completed **396 tests + 2 subtests**, RNA, 18 AE Node suites, syntax and repeat packaging. Runtime/package bytes are unchanged. The timeboxed follow-up did not establish native startup; no new candidate code was loaded. Independent release review and demonstrated-scope acceptance are **NOT_RECEIVED**. Use the [current checkpoint](COMPLETION_STATUS.md), [operator handoff](NATIVE_VALIDATION_HANDOFF.md) and [review packet](INDEPENDENT_RELEASE_REVIEW_PACKET.md). Authorization is false, production unchanged and S14B NOT_EXECUTED.

The 16 October paragraphs below preserve their named baselines; their 395/390 counts are not final-639 results.

Current readiness — **16 October 2026: INSUFFICIENT EVIDENCE** for submission and public release. The working submission target is **22 October 2026**; the official deadline remains unconfirmed. The [submission/demo checklist](SUBMISSION_DEMO_CHECKLIST.md) separates a reproducible review packet from protected release/publication/distribution actions.

Current exact tested code SHA `a44792099b3b5f5b7a2f69a41061268fe59586b3` passed [independently trusted Linux verification 38910000382](https://github.com/Unn0wn002/CutBridge/actions/runs/38910000382): **395 passed + 2 subtests**, no skips, official `bpy 5.2.1`, 18 AE Node suites, syntax, complete repeated-package comparison, safe upload and input integrity. Fixed bootstrap `8d1ecef5e2abb8c0b27f7951eb5a3eb75773afcc` uses trusted orchestration `a6ee2445f81906c024fd5b9e1689faac017f198a`; the [retained record](evidence/20261016-release-completion/trusted-linux/passed-r2/verification.json) closes that gate without protected workflow registration. [Ordinary exact-code CI 38909885640](https://github.com/Unn0wn002/CutBridge/actions/runs/38909885640) also passed **395 tests + 2 subtests**. Earlier Windows **390 passed, 2 skipped + 2 subtests** remain bound to `5293cd46a819debfe8ecf41f740c4e94806dd89c`.

Native Blender **5.2.2**, build `d13f752e3b9c`, passed its recorded scripted V001–V003/36-output preservation, negative/rollback and fresh-process reopen scope, with both actual exits **0**, using the demonstrated equivalent Blender ZIP. **Current AE acceptance and Blender visual checks: BLOCKED / INSUFFICIENT EVIDENCE** because the host processes failed initialization before candidate checks. Applicable visual installation/UI/manual-update checks, explicit scope acceptance and independent release review remain incomplete. S14B remains NOT_EXECUTED. See [current preparation](RELEASE_PREPARATION_v0.2.5.md#current-candidate-verification--16-october-2026) for hashes, retained assessments and local `dist/release-candidate-20261016/` packet instructions.

Each toolchain's full four-asset repeat builds are byte-identical. Windows/Linux ZIP bytes match; their metadata/checksum files have CRLF/LF byte differences with equivalent JSON/checksum entries. The local primary packet uses the exact Linux metadata/checksum bytes. These results do not authorize publication or create the unexecuted native/manual evidence.

Historical AE 26.5x89 observations informed cached-object repairs. The Blender `fef1023` and AE `049c095` campaign records do not retain the required isolation policy, offline-adapter state, complete mount/credential boundary and all temporary-path settings. Their native release gates therefore remain **INSUFFICIENT EVIDENCE**, even where historical reports call observed behavior PASS. Network restoration after a run does not establish network isolation during it. The Blender handoff assertion checked presence rather than Camera/Empty channel correctness. Repeat the applicable native checks on exact current package hashes inside a documented isolation boundary; do not reuse these records as complete gate evidence.

The historical checked boxes below describe their named candidates and scope. They do not mark current v0.2.5 native, review, installation or release gates complete. The current evidence above supersedes only its executed or explicitly equivalent scope; the older `fef1023`/`049c095` observations do not become valid release evidence retroactively. Authorization stays false.

Preparation update — 3 October 2026: see [the v0.2.5 preparation record](RELEASE_PREPARATION_v0.2.5.md) for the independent v0.2.4 download audit, confirmed distribution hold, isolated candidate verification, and remaining native/publication/delivery gates.

Status: **v0.2.4 PUBLISHED / VERIFIED ON GITHUB; PRODUCTION DISTRIBUTION HELD; v0.2.5 DEVELOPMENT / NOT AUTHORIZED**

This is the canonical release-readiness record. It preserves historical v0.2.3/v0.2.4 evidence while distinguishing the published-but-not-distributed v0.2.4 state from the current v0.2.5 development boundary. Green product CI and successful native validation are necessary, but neither alone authorizes a future publication; the exact release tuple and current-main eligibility gate remain separate controls.

## Current repository boundary

Current protected branch and release state — 23 September 2026:

- stable tag `v0.2.3`: immutable at `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f`;
- stable tag `v0.2.4` and protected `main`: exact SHA `a393e409d19445c4090460b7e7b4716779161fa4`;
- GitHub Release v0.2.4: published, non-draft, non-prerelease, latest; Release workflow `35843821702` completed SUCCESS;
- v0.2.5 development baseline: reconciles the published v0.2.4 main history with PR #100 / Issue #99 source remediation and restores fail-closed authorization;
- frozen runtime candidate `candidate/v0.2.4-beta.1`: `ef5911a83270a4ce8121741ada2d2726fa09ec29`;
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
- repository-governance Issue #18: **CLOSED / COMPLETED** after the authorized exact-current-main v0.2.4 tag path, Release workflow publication, and independent asset verification passed.

v0.2.4 publication is complete on GitHub and its tag/assets remain immutable. Independent verification found the AE package documentation defect tracked in Issue #99, so production distribution intentionally remains on v0.2.3. The v0.2.5 development baseline carries the source fix and restores `release-authorization.json` to `approved: false` with null tag/channel/prerelease. Automatic startup update scheduling remains disabled and S14B remains `NOT_EXECUTED`.

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

## 6. Repository governance — COMPLETE / Issue #18 CLOSED

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

Current state — 23 September 2026: Issue #18 is closed as completed after the positive authorized v0.2.4 exact-current-main tag/publication path and independent asset verification passed. The separate Issue #99 package-documentation defect does not invalidate governance enforcement and remains the reason production distribution is held.

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

For v0.2.4, the exact `v0.2.4` / stable / non-prerelease authorization was consumed by the published release at `a393e409d19445c4090460b7e7b4716779161fa4`. For active v0.2.5 development, `release-authorization.json` is restored to `approved: false` with null tag/channel/prerelease. No v0.2.5 authorization has occurred.

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

The manual checker uses the verified notification index. Automatic startup update scheduling remains disabled. No v0.2.4 distribution entry exists because Issue #99 triggered a deliberate distribution hold; production continues to advertise only v0.2.3 until a corrected post-v0.2.4 release is published and verified.

## 13. Final release decision

Use one of these states:

- **NOT RELEASE READY** — one or more required gates remain incomplete.
- **RC ELIGIBLE** — release-target validation and governance are complete, but stable-specific acceptance is not yet complete.
- **STABLE ELIGIBLE** — every stable-release gate is complete and evidence is recorded.
- **PUBLISHED / VERIFIED** — authorized publication completed and downloaded assets/update distribution were independently verified.

### Current verdict

**v0.2.4 PUBLISHED / VERIFIED ON GITHUB; PRODUCTION DISTRIBUTION HELD. v0.2.5 DEVELOPMENT / NOT AUTHORIZED.**

Stable GitHub release v0.2.4 is immutable at `a393e409d19445c4090460b7e7b4716779161fa4`; deterministic candidate/native evidence and independent published-asset verification are recorded PASS for the tested scope. Production distribution intentionally remains on v0.2.3 because Issue #99 found stale release-state wording in the immutable v0.2.4 AE `INSTALL.md`. The v0.2.5 development baseline carries the source remediation, bumps product identity to 0.2.5, keeps startup scheduling disabled, preserves S14B as `NOT_EXECUTED`, and restores release authorization to fail-closed. PR #104 integrated the Blender/action follow-ups and PR #105 integrated the remaining user-facing documentation corrections; exact-head and post-merge CI passed for both. The changed `core.py` legacy `Scene.use_nodes` state-capture/restore path has now passed the focused `tests/blender_legacy_compositor_probe.py` on Blender 4.2.23 and 4.5.14; this does not establish broader workflow compatibility in those versions. Before freezing an exact v0.2.5 candidate, complete the applicable full native Blender 5.2 workflow and verify the exact packaged After Effects guide/runtime. Release authorization remains false until exact-candidate CI, deterministic package checks, required native evidence, and deliberate owner authorization are complete.

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

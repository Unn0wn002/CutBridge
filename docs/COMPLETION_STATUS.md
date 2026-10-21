# CutBridge Completion Status

## Active bounded free release — 21 October 2026

Latest setup observation: `AYAKUMI_NOZOMI` is selected and its GUI inventory is empty. One launch of the verified Microsoft Hyper-V Quick Create executable reached Windows elevation consent; no consent was accepted by the agent. [The immediate handoff](evidence/20261021-pr114-guest-provisioning/quick-create-r2/OPERATOR_ACTION.md) is that exact prompt, replacing the earlier node-selection request. Runtime/packages and completed evidence remain frozen; native verdict remains **INSUFFICIENT EVIDENCE**.

Provisioning attempted: fresh Sandbox CLI 0.8.107.0 start failed with `0x80370106` before a usable guest; detailed Hyper-V logs require elevation. Official Blender 5.2.2 and Creative Cloud installers were downloaded and vendor signatures verified, with no execution. The supported Hyper-V Manager interface is open at a higher integrity level; [the precise operator handoff](evidence/20261021-pr114-guest-provisioning/OPERATOR_ACTION.md) is local host-node selection to reveal the available VM list/access message. No retry, host repair, security/licensing change or reboot occurred. Native verdict remains **INSUFFICIENT EVIDENCE**, separate from any observed CutBridge defect; frozen package/runtime/automation/review results are preserved.

Native continuation: **INSUFFICIENT EVIDENCE — environment unavailable, no observed CutBridge defect.** Both exact candidate ZIPs are now on the PC and independently hash-verified there through authenticated read-only Actions transport. The [current receipt and operator handoff](evidence/20261021-pr114-native-continuation/OPERATOR_HANDOFF.md) retain scope, source bindings and exact environment observations. The missing original attachment is not claimed as retrieved; its user-reported inspection is recorded separately. Current-package native cases and screenshots remain NOT_EXECUTED. No implementation change or new candidate execution occurred; release remains held solely for the required native qualification and subsequent protected release gates.

Exact tested source: **`5aa2da24fc8be41626ee84178c7fdce05d02eebc`**, [draft PR #114](https://github.com/Unn0wn002/CutBridge/pull/114). [Push CI](https://github.com/Unn0wn002/CutBridge/actions/runs/39575594812), [PR CI](https://github.com/Unn0wn002/CutBridge/actions/runs/39575602151), and [reviewed isolated verification](https://github.com/Unn0wn002/CutBridge/actions/runs/39575739610) succeeded; CI reports **396 tests + 2 subtests**. See the [separate AI review](AI_RELEASE_REVIEW_2026-10-21.md) for exact bindings, first-run failures, verified package hashes, retained scope and unresolved native gates. Later documentation commits do not replace this tested source identity.

Target: **Sunday, 25 October 2026 (Asia/Jakarta)**, confirmed by the owner. This supersedes the earlier 22 October working target. Scope is frozen; feature development stops at a qualified published release, with critical defects only afterward. See [the bounded release policy](FREE_RELEASE_2026-10-25.md).

The current branch `fix/free-release-20261021` retains all PR #113 commits and adds the dockable-first installation/compact ScriptUI/in-panel Build-QC patch. Earlier AE runtime/package hashes and frozen-runtime statements below describe historical candidates; they do not qualify this changed AE runtime. Historical 396-test/18-suite and Blender evidence remain bound to their exact recorded inputs.

The owner authorizes a separately documented AI code/evidence review instead of owner-controlled administrative human review for this release. This does not waive native acceptance or enforced GitHub approvals. S14B remains NOT_EXECUTED; unsupported channels and broad compatibility/commercial claims remain excluded.

Current native verdict: **INSUFFICIENT EVIDENCE**. Blank owner-session AE/Blender workspaces initialize, but the 19 October provisioned Sandbox is no longer present and the installed AE core DLL still reports HashMismatch. No current candidate code has been loaded into the owner session. The required isolated native campaign and qualified-build screenshots remain unexecuted. Release authorization remains false; v0.2.4 is immutable/held, production remains v0.2.3.

## Historical records (retain original identities and decisions)


## Source-replacement rollback preparation — 17 October 2026

**Verdict: INSUFFICIENT EVIDENCE. Native status: PREPARED_NOT_EXECUTED.** Branch `fix/current-release-completion-20261016` continues checkpoint `5a4f43b6b0f4c11e97221a3e800d39c4244fe4fa`. Frozen engineering/runtime baseline remains `639374ce5f1b5f0d36847258d052c36ab21dd208`; its completed 396 tests + 2 subtests and bounded native Blender evidence remain separately SHA-bound.

No reviewed source-swap failure supplement was found. [The new phase](../tests/native_ae/source_replacement_rollback.jsx) extends the retained CB native harness using the disposable V003 campaign project. It observes one successful real replacement, passes null through the real adapter on the second swap and requires an actual native exception. It retains snapshots, staged IDs/paths, exception and cleanup evidence, restores instrumentation in `finally`, compares original sources/metadata/caches/artist state, then reloads the actual panel and runs Build/QC. Existing AE host-shaped mocks cover the phase and adversarial no-throw/early-failure/no-op/retained-ID cases.

Exact preparation SHA **`85b8eb06617c1f195385c1b96ce9452882b63b8e`** passed [trusted isolated run 39012397226](https://github.com/Unn0wn002/CutBridge/actions/runs/39012397226): **396 tests + 2 subtests**, no skips, RNA `bpy 5.2.1`, 18 AE Node suites including the extended mock, syntax and complete four-asset repeated packaging. [Retained checks](evidence/20261017-source-replacement-rollback/checks.log) and [the binding record](evidence/20261017-source-replacement-rollback/preparation.json) identify commands, snapshot, image, host and artifact hashes. The downloaded ZIP SHA-256 is `39a9ec8f6029feee1d381a3d54201d58e3165b0fff29bcc00ece9a76b9962cef`; all 48 inner checksums plus the bootstrap-context checksum were verified. Before/after exact input inventories match, actual container exit is 0, and all four generated assets equal the frozen packet byte-for-byte. [Ordinary exact-head CI](https://github.com/Unn0wn002/CutBridge/actions/runs/39012366909) also succeeded. This is automated preparation evidence, separate from the preserved 639374c baseline and all native results.

The first preparation attempt at `62a0352` failed because a mock assertion diagnostic serialized circular AE-shaped objects. Its full failed-run archive/logs and unchanged input inventory are retained separately; `85b8eb0` fixes the diagnostic and uses a fresh immutable snapshot. No candidate-controlled command ran in the owner environment.

[The existing handoff](NATIVE_VALIDATION_HANDOFF.md#prepared-source-replacement-rollback-supplement) records the exact `AfterFX.exe -m -r C:\NativeAEInput\source_replacement_rollback.jsx` invocation, output files and proof requirements. The local operator bundle contains the exact reviewed supplement (`332dfcf34551caabd741e4cc6b31216d36a11899e7af1aae1ac30148ad97e54d`) and separate preparation metadata. Packaged runtime, release ZIPs, authorization and production remain unchanged. No startup retry, security/licensing change or acceptance occurred. Next action: an approved native operator executes this supplemental phase after the retained campaign and returns concrete evidence. Submission readiness remains insufficient; public-release gates remain separate, authorization false, production v0.2.3 and S14B NOT_EXECUTED.

## Validation closeout — 17 October 2026

**Verdict: INSUFFICIENT EVIDENCE.** Branch `fix/current-release-completion-20261016` retains frozen engineering SHA `639374ce5f1b5f0d36847258d052c36ab21dd208`; this follow-up changes documentation/evidence only. Its **396 tests + 2 subtests**, RNA, 18 AE Node suites, syntax and repeat packaging remain complete and SHA-bound. [The original final receipt](evidence/20261017-validation-closeout/BASELINE_639374c_VERIFICATION.json) is retained unchanged. Earlier 395/392/390 counts below remain historical. Runtime/package bytes are frozen; native Blender evidence retains only its recorded equivalent-package scope.

The 60-minute startup diagnosis window began `2026-10-16T15:55:38Z` and expired at `16:55:38Z` during an interrupted turn. On resumption at `2026-10-17T00:47:41Z`, no new startup attempt was launched. The pending Blender-only control produced no guest isolation/process/availability files; the Sandbox desktop alone did not establish native startup. Its **7,511 before/after input records were identical**. No claim is made that the VM stopped at the deadline. The existing control was subsequently closed, with no candidate code mapped or loaded.

Independent preparation found AE's active `AfterFXLib.dll` Authenticode **HashMismatch** and an incomplete full-tree inventory after an unreadable backup-file path. AE was excluded from the fresh control. These facts, prior `0xc0e90002`, the separate historical Application Control block, and absent control output do **not** establish a common root cause. No installation, execution policy, security setting or authorization was changed. [The retained assessment](evidence/20261017-validation-closeout/assessment.json) separates these gaps from product failures and accepted automation.

The packet README's four garbled arrows and one range dash are repaired. Original bytes and the original **63-entry** checksum catalog were preserved and verified before amendment; the immutable final-639 receipt and all four release assets are unchanged. The local packet includes a hash-inventoried, data-only `operator-handoff/` bundle: exact AE runtime, existing harnesses, real Blender V001–V003 inputs, 639 review metadata and unfilled acceptance forms. Configuration changes are explicit; data staging is not native installation or execution evidence.

[One operator handoff](NATIVE_VALIDATION_HANDOFF.md) specifies environment requirements, commands, expected outputs, native coverage gaps, manual EN/JA/installation/dockable/update checks and evidence to return. [The review packet](INDEPENDENT_RELEASE_REVIEW_PACKET.md) and [scope form](validation/scope-acceptance.json) are prepared. Independent release review, environment acceptance and demonstrated-scope acceptance are all **NOT_RECEIVED**; no reviewer was contacted and no approval is claimed.

Next action: an operator supplies an independently approved native environment with clean, readable vendor inputs and working orchestration; prove blank and no-candidate probe startup first, then execute the retained exact-package native/manual procedures and return named, SHA-bound scope/evidence decisions. Submission readiness remains insufficient. Public-release promotion, exact-tuple authorization, publication/download verification and distribution remain separate authorized gates. Authorization stays false, production stays v0.2.3, and S14B stays **NOT_EXECUTED**. Working target: **22 October 2026**; official deadline unconfirmed.

## Recorded engineering checkpoint — 16 October 2026

Current verdict — **INSUFFICIENT EVIDENCE**. Independently trusted Linux verification and the bounded equivalent-package native Blender campaign passed for the scope below. Native AE and visual checks could not execute in the current host environment; manual-update checks, scope acceptance and independent release review remain incomplete. Submission readiness and public-release readiness remain separate. Release authorization stays false; production distribution stays on v0.2.3.

## Current checkpoint — 16 October 2026

Working target: **22 October 2026**. The official submission deadline remains unconfirmed.

- Integration branch: `fix/current-release-completion-20261016`.
- Exact tested code SHA: `a44792099b3b5f5b7a2f69a41061268fe59586b3`. Documentation/evidence closeout commits must retain this tested identity and demonstrate any permitted equivalence rather than reassigning results to an untested head.
- Final command-record fix: `fa388b7` copies arguments before a reused Docker command list changes; a main-path regression checks distinct retained preflight/check invocations. Independently reviewed corrected tools are pinned to `571f4cdb1c992124bdb35e3d089de1de1535b254`. Final committed branch-head CI and trusted verification are recorded separately in the draft PR and local packet's `FINAL_HEAD_VERIFICATION.json`; the 395-test baseline count above is not automatically reassigned.
- Changes: captured-ID cleanup after failed import and invalid-native-handle regression coverage; narrowed Camera Position/Point of Interest/Zoom and Null Position/Scale claims; exact snapshot/inventory, trusted orchestration, safe staging, repeated-package and verification-result safeguards; safe retention of malformed/nondeterministic package evidence on failure and corrected temporary-fixture permissions; installation/limitations and submission/demo checklist.
- Independently trusted Linux verification: [run 38910000382](https://github.com/Unn0wn002/CutBridge/actions/runs/38910000382) **PASS**, **395 passed + 2 subtests**, no skips, official `bpy 5.2.1`, all **18 AE Node suites**, syntax checks, complete four-asset repeated-build comparison, input integrity and safe upload. Fixed push bootstrap `8d1ecef5e2abb8c0b27f7951eb5a3eb75773afcc` uses trusted orchestration `a6ee2445f81906c024fd5b9e1689faac017f198a` independently of candidate refs. [Retained evidence](evidence/20261016-release-completion/trusted-linux/passed-r2/verification.json) closes this Linux gate without protected default-branch workflow registration.
- Ordinary exact-code Linux CI: [run 38909885640](https://github.com/Unn0wn002/CutBridge/actions/runs/38909885640) **SUCCESS**, **395 passed + 2 subtests**.
- Earlier automated evidence remains bound to `5293cd46a819debfe8ecf41f740c4e94806dd89c`: offline/read-only Windows Sandbox **390 passed, 2 skipped + 2 subtests**, `bpy 5.2.1`, 18 AE Node suites and identical four-asset builds; [ordinary Linux run 38875347991](https://github.com/Unn0wn002/CutBridge/actions/runs/38875347991) **392 passed + 2 subtests**, no skips. Those Windows counts are not reassigned to the later tested SHA.
- Native Blender **5.2.2**, build `d13f752e3b9c`: bounded scripted GUI-event-loop campaign passed V001→V002→V003, **36** mixed-format four-pass outputs, value-level Camera/marked Empty serialization checks, artist/compositor preservation, overwrite/contract-mismatch rejection, injected mapping rollback and fresh-process reopen. Both actual Blender process exits were **0**. Apps, LICENSE and builder bytes are unchanged from `c234d1f42d7cdff10170289c0cbd35b4a007d8c6` through the tested SHA; both ZIP hashes match between the Windows `5293` and Linux `a447` builds. Reuse is limited to that equivalent-ZIP scope. Visual panel/install-dialog/button-click and manual-update checks remain unexecuted.
- Native AE: **BLOCKED / INSUFFICIENT EVIDENCE**. The corrected harness did not execute; actual AE startup exited `0xc0e90002` with both vGPU Enable and Disable. A fresh Windows preflight also recorded an `rpds` DLL blocked by Application Control; causation is not established and no policy changes were made. Zero current candidate native assertions are accepted. See [the retained assessment](evidence/20261016-release-completion/native-ae/assessment.json).
- Blender visual attempt: the official validator process exited `0xc0e90002` before candidate execution. Current visual/manual panel and installation acceptance remain **UNEXECUTED**; this is host/infrastructure evidence, not a candidate failure.

| Current unpublished artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe` |
| After Effects ZIP | `427a36ba8638e88940b18f9daa34537c7e41ad939f3b81fddb50a3812d691268` |

The actual downloaded trusted-run artifact ZIP has SHA-256 `53e9783c81da36c66eb5b9d3782244806d1b3023b1213eebd21fc354956d0e79`; **48 inner evidence checksums** were independently verified. Each toolchain's complete four-asset repeat builds are byte-identical. Across Windows/Linux, the two ZIPs match, while `release-metadata.json` and `SHA256SUMS.txt` have CRLF/LF byte differences with equivalent JSON/checksum entries. The primary local packet uses the exact Linux `a447` metadata/checksum bytes; Windows originals remain historical inputs.

The local, unpublished review packet is `dist/release-candidate-20261016/`; start with its `README.md`, compare both ZIPs against its `SHA256SUMS.txt` and `release-metadata.json`, then use `EVIDENCE_BINDING.json` and `DEMO_CHECKLIST.md`. Generated packet files remain outside Git.

Submission blockers: obtain an approved native environment that initializes AE and Blender's visual path, execute the corrected exact-package AE/visual checks, finish manual-update checks, record explicit demonstrated-scope acceptance and obtain independent exact-candidate release review. The trusted Linux gate is complete; optional manual workflow-dispatch registration on the default branch is not required for the recorded fixed-push-bootstrap run. S14B remains **NOT_EXECUTED** and no representative Japanese-user usability claim is made.

Next action: use an independently approved offline, credential-free native environment in which the hosts initialize, then run the retained corrected AE harness and visual checks against the exact ZIPs and rendered Blender packages. Retain host/build, actual process/reopen results and integrity evidence; do not weaken isolation or infer native success from Node/CI. Complete manual-update/scope acceptance and independent release review. Protected promotion, exact release authorization, publication, published-download verification and production distribution require their separate explicit authorization and gates.

The historical records below are preserved. The `fef1023` and `049c095` native campaigns lack retained isolation-policy evidence and remain INSUFFICIENT EVIDENCE for release gates; their original observed PASS statements are not current acceptance. The fresh Blender campaign above supersedes only the matching scripted Blender scope.

## Historical checkpoint — 4 October 2026

The revised v0.2.5 candidate passed 313 tests + 2 subtests and a partial scripted native Blender 5.2.2 campaign. It corrects stale Camera/3D Null handoff wording. Native AE 26.5x89 execution now covers the recorded positive/revision/optional-content/persistence scope; remaining installation, negative/preservation sign-off, review and delivery gates are still pending; see the linked preparation record for exact SHA-bound evidence.

Release preparation update — 3 October 2026: the independent v0.2.4 artifact audit confirms the Issue #99 distribution hold. v0.2.5 preparation and remaining exact-candidate gates are recorded in [RELEASE_PREPARATION_v0.2.5.md](RELEASE_PREPARATION_v0.2.5.md). Production, release authorization, and published artifacts are unchanged.

CutBridge v0.2.4 is **PUBLISHED / VERIFIED ON GITHUB** at exact main/tag SHA `a393e409d19445c4090460b7e7b4716779161fa4`. Production distribution remains intentionally on v0.2.3 because Issue #99 found stale pre-publication wording in the immutable v0.2.4 AE package. v0.2.5 is the **UNRELEASED / NOT AUTHORIZED** patch-development baseline carrying the source fix. S14B representative-user validation remains NOT_EXECUTED and is not claimed as complete.

- **Integrated product/validation sessions:** S1–S13.
- Historical S13 runtime integration baseline: `0a86d9a0605e1dd9714ef35a547693de76f714f4`.
- Historical final native-tested S13F source: `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`.

Stable tag `v0.2.3` remains immutable at `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f`. Stable tag `v0.2.4` and protected `main` resolve to `a393e409d19445c4090460b7e7b4716779161fa4`; Release workflow `35843821702` published the verified GitHub release. The v0.2.5 baseline deliberately reconciles that release history with PR #100 / Issue #99 source remediation.

Current repository boundaries:

- repository visibility: public;
- protected `main` / stable tag `v0.2.4`: `a393e409d19445c4090460b7e7b4716779161fa4`;
- v0.2.4 GitHub Release: published, non-prerelease, latest; Release run `35843821702` SUCCESS;
- frozen runtime candidate `candidate/v0.2.4-beta.1`: `ef5911a83270a4ce8121741ada2d2726fa09ec29`;
- v0.2.5 development line: product identity 0.2.5, Issue #99 source fix included, release authorization fail-closed;
- stable tag `v0.2.3`: immutable historical release;
- production distribution commit: `635c1384af2649d4ce49705cce41f98826a861cc`;
- production notification index: `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- production Blender repository: `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`;
- four active governance rulesets protect `main`, `develop`, release-tag mutation, and no-bypass release-tag eligibility;
- `release-authorization.json` for active v0.2.5 development: `approved: false` with null tag/channel/prerelease;
- v0.2.4 tag/GitHub Release exist and are immutable; no v0.2.4 production distribution entry exists because Issue #99 triggered a distribution hold;
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

Focused Windows host probes on Blender 4.2.23 LTS (build hash `d0cbe84903e8`) and Blender 4.5.14 LTS (build hash `62c1db4208e8`) passed the legacy `Scene.use_nodes` compositor state-capture/restore path at develop commit `84a6f26bac593831eb75bf81c1b65212c12b59d8`. The reproducible probe is `tests/blender_legacy_compositor_probe.py`. This evidence covers that narrow state path only; broader Blender 4.2/4.5 workflow behavior remains UNVERIFIED.

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

## Historical authoritative automated evidence — v0.2.4

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

The v0.2.4 GitHub release path is complete:

1. exact v0.2.4 candidate freeze and bounded native validation completed;
2. protected promotion, exact stable authorization, and current-main release-tag eligibility completed;
3. tag `v0.2.4` was created only on exact authorized main `a393e409d19445c4090460b7e7b4716779161fa4`;
4. Release workflow `35843821702` completed SUCCESS and published the stable GitHub Release;
5. independent asset verification passed for both ZIPs, checksums, metadata, archive integrity, version identity, and licenses;
6. Issue #99 records a user-facing packaged AE documentation defect; published v0.2.4 remains immutable;
7. production distribution therefore remains on v0.2.3 rather than mirroring v0.2.4.

The v0.2.5 development boundary is fail-closed:

1. reconcile published v0.2.4 main ancestry with the PR #100 Issue #99 source fix;
2. use product version 0.2.5 across Blender/After Effects packaging identity;
3. keep `release-authorization.json` unapproved;
4. keep automatic startup update scheduling disabled;
5. exact-head and post-merge CI passed for the reconciled baseline through PR #104 and follow-up PR #105;
6. do not authorize/tag/publish v0.2.5 or update production distribution without later explicit gates.

## Non-blocking post-v0.2.3 work

Issue #80 was intentionally outside the v0.2.3 release scope and is now completed for v0.2.4. The coordinated manifest/preset/Blender/AE per-pass implementation was integrated through PR #93 with native acceptance evidence and green post-merge CI.

## Recommended immediate phase

Use the 16 October checkpoint above as the active plan: the independently trusted Linux gate is complete. Resolve native-host initialization through an approved environment, then finish exact-package AE/visual/manual-update checks, explicit scope acceptance and independent release review. The scripted Blender 5.2.2 result does not certify the full 4.2/4.5 workflow; historical focused legacy `Scene.use_nodes` probes retain only their recorded scope. Keep release authorization false and production distribution on v0.2.3 until the separately authorized release/delivery gates are complete. S14B remains NOT_EXECUTED and becomes required only before broader representative Japanese-user usability claims.

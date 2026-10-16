# CutBridge v0.2.5 release preparation

Status: **PREPARING / NOT AUTHORIZED**. Production remains on v0.2.3. Do not mirror the immutable v0.2.4 packages: their AE installation guide has the confirmed Issue #99 documentation defect.

Current assessment — **16 October 2026: INSUFFICIENT EVIDENCE** for submission and public release. The working target is **22 October 2026**; the official submission deadline remains unconfirmed. Use [the submission/demo checklist](SUBMISSION_DEMO_CHECKLIST.md) to prepare the exact-candidate review packet and remaining native checks. S14B stays NOT_EXECUTED and broader representative-user claims remain excluded.

## Current candidate verification — 16 October 2026

Integration branch: `fix/current-release-completion-20261016`. Exact tested code SHA: **`5293cd46a819debfe8ecf41f740c4e94806dd89c`**. Keep later documentation/evidence commits distinct from this tested identity. Changes address verifier trust/inventory/staging/evidence weaknesses, failed-import captured-ID cleanup and invalid-native-handle regressions, and the actual Camera/Null reconstruction/QC claim boundary.

| Verification scope | Recorded result |
| --- | --- |
| Offline read-only Windows Sandbox automated run | **390 passed, 2 skipped + 2 subtests**; official `bpy 5.2.1`; **18 AE Node suites**; repeated builds produced identical complete four-asset outputs. The two skips remain recorded. |
| Ordinary Linux CI on exact code SHA | [38875347991](https://github.com/Unn0wn002/CutBridge/actions/runs/38875347991) **SUCCESS**, **392 passed + 2 subtests**, no skips. This does not replace the pending independently trusted Linux verifier run. |
| Native Blender 5.2.2, build `d13f752e3b9c` | Bounded scripted GUI-event-loop scope passed: V001→V002→V003, **36** mixed PNG/OpenEXR pass outputs, value-level Camera/marked Empty metadata checks, artist/compositor preservation, overwrite and mismatch rejection, injected rollback, save/reopen and fresh-process persistence. Both actual process exits were **0**. Visual/manual installation/UI/update acceptance is excluded. |
| Current native AE campaign | **PENDING — running; no current native AE PASS is recorded here.** Replace this placeholder only with actual SHA/hash/host/scope-bound results. |

| Current unpublished artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe` |
| After Effects ZIP | `427a36ba8638e88940b18f9daa34537c7e41ad939f3b81fddb50a3812d691268` |

Exact Blender ZIP bytes match between `c234d1f42d7cdff10170289c0cbd35b4a007d8c6` and `5293cd46a819debfe8ecf41f740c4e94806dd89c`. That demonstrated artifact equivalence permits only the recorded unchanged-package native Blender scope to accompany the tested code SHA. It does not transfer unrelated host/UI coverage or native AE acceptance. Retain the equivalence comparison, native fixture/harness/package hashes, actual host build and process exits with the evidence bundle.

Remaining submission gates are the current AE result, independent exact-candidate/verifier review, authorized default-branch registration and execution of the trusted Linux workflow, applicable visual install/panel/manual-update checks and explicit scope acceptance. Preserve generated packages/checksums/metadata outside Git and retain the reviewable demo packet. Public release additionally requires protected promotion, explicit exact release authorization, guarded publication, downloaded-asset verification and separate distribution approval. No current result changes the v0.2.3 production boundary or S14B NOT_EXECUTED status.

## Historical preparation records

The [historical installed AE 26.5x89 campaign](evidence/v0.2.5/049c095-native-ae/README.md) records observations at `049c095258f9fc2dd89cbf8f1d7b2b3114d80296`: ZIP Build/QC, V001→V002→V003, inspected artist state, Camera/Null samples, status-change confirmation, optional-content warnings and same-process reopen. These observations informed fixes, but the retained record does not establish the required Sandbox configuration, disabled network state, complete read-only mounts/credential boundary and all temporary-path settings. The same provenance gap applies to the Blender `fef1023` campaign. Their release-gate verdict is **INSUFFICIENT EVIDENCE**; preserve historical reports without promoting observed PASS statements into current native acceptance. Restoring network after a run does not prove it was disabled during candidate execution. Current code changes require fresh exact-candidate tests.

Historical exact-commit CI at `049c095`: [isolated 37180451235](https://github.com/Unn0wn002/CutBridge/actions/runs/37180451235), [normal CI 37180451191](https://github.com/Unn0wn002/CutBridge/actions/runs/37180451191) report **313 tests + 2 subtests**, Blender RNA 5.2.1, syntax, repeated packaging, input integrity and unpublished distribution-preview checks. An 18-suite AE Node run was also reported. These remain historical results subject to the current verifier review; green CI is not complete readiness. Historical unpublished hashes, not current candidate identity:

| Candidate artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48` |
| AE ZIP | `ae9bfb9c2aa36c6764b324ac74ef85cc5022071b04bb7b7695e64a3651f70366` |

## Candidate identity

- Preparation base: protected `develop` at `8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`.
- Published v0.2.4: immutable tag/main SHA `a393e409d19445c4090460b7e7b4716779161fa4`; release workflow [35843821702](https://github.com/Unn0wn002/CutBridge/actions/runs/35843821702).
- v0.2.5 already includes the Issue #99 source fix, packaged-guide regression checks, version synchronization, modern compositor state-capture repair, and refreshed action pins. Native preparation also corrects stale Blender handoff warning/tooltip/help text; schemas, hidden control defaults, and diagnostic identifiers remain unchanged.
- Existing exact-base CI: [36528627741](https://github.com/Unn0wn002/CutBridge/actions/runs/36528627741). Native evidence from earlier candidates remains historical; it is not reassigned to v0.2.5.
- Release authorization stays `approved: false`, with null tag/channel/prerelease. Startup update scheduling stays disabled. S14B remains `NOT_EXECUTED`.

## Independent v0.2.4 audit — 3 October 2026

Both published ZIPs and metadata were downloaded independently. ZIP integrity, source-version identity, required runtime files, GPL license bytes against the release commit, and hashes were recorded as passing. The earlier installed Blender 5.2.2 CLI package-validator claim lacks the retained exact input/command log needed for independent verification and remains unsubstantiated. These archive observations do not establish a GUI workflow or AE native success.

| Artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2` |
| After Effects ZIP | `e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b` |
| SHA256SUMS.txt | `8fb929650292105effaf39bbcb26427dc056a6cf64f435dd65e65a53083c24ac` |
| release-metadata.json | `6266daa58d12071d64b64e8f21777eb88e9a1f0577277c4650880295325dc0ee` |

The AE `INSTALL.md` still calls v0.2.4 a development package and says its evidence does not authorize publication. This confirms [Issue #99](https://github.com/Unn0wn002/CutBridge/issues/99). [PR #100](https://github.com/Unn0wn002/CutBridge/pull/100) fixed source documentation; [PR #101](https://github.com/Unn0wn002/CutBridge/pull/101) carried it into the v0.2.5 development line. The existing published v0.2.4 files are not modified.

Production notification and Blender indexes were rechecked: they advertise only v0.2.3 at distribution commit `635c1384af2649d4ce49705cce41f98826a861cc`. A local v0.2.4 mirror was prepared before discovering the hold, but was not committed, pushed, or deployed. It must not be used for publication.

## Isolated candidate verification

The existing `Isolated candidate verification` workflow is the automated entry point; [CONTRIBUTING.md](CONTRIBUTING.md) remains the command contract. Its orchestration must be trusted independently of candidate-controlled refs before execution. Record the immutable orchestrator SHA, candidate SHA and true merge-base, dependency-image identity, no-network settings, read-only source, explicit writable output/temp locations and absence of owner credentials. An authenticated environment may prepare and inspect inputs but must not execute candidate commands.

Verify exact path inventory, modes and bytes against the recorded Git candidate, including archive-attribute effects; reject unexpected symlinks and unsafe paths. Retain the candidate/base diff, all verification inputs and production-index input, manifests, logs and classifications. Stage uploads with trusted path/type checks so candidate output cannot inject links or unrelated host files. Compare the complete output inventories and every file from both package builds, including ZIPs, checksums and metadata. Infrastructure or dependency failures are INSUFFICIENT EVIDENCE; integrity violations are INVALID; only correctly isolated executable checks exposing a candidate defect are FAIL.

It runs full pytest, Blender 5.2.1 RNA lifecycle, Python compilation, existing AE Node suites and syntax checks, then invokes the canonical release builder twice. Candidate artifacts must match byte-for-byte. Artifacts are retained for 30 days; download and preserve the evidence bundle in durable release storage before expiry.

The workflow also retains an unpublished distribution preview: manifest-derived Blender index, notification index, versioned candidate files, and release page. It snapshots the live production notification index before offline execution, preserves its existing entries, and verifies v0.2.3 update selection and no downgrade against the staged candidate entry. The preview is partial and must never replace the production tree or bypass published-download verification.

### Recorded automated candidate evidence

Historical runtime candidate `604714d93627a870326a75564eba0af46e5ee957`: [isolated run 37137778152](https://github.com/Unn0wn002/CutBridge/actions/runs/37137778152) and [normal CI 37137778139](https://github.com/Unn0wn002/CutBridge/actions/runs/37137778139) passed **313 tests + 2 subtests**, RNA lifecycle, AE suites/syntax, identical repeated packaging, unchanged input manifests, and offline distribution-preview checks. [Durable logs and manifests](evidence/v0.2.5/604714d/checks.log) bind those results to the corrected handoff wording. That candidate Blender ZIP hash is `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48`; that candidate AE ZIP is `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e`.

Earlier candidate `0c1938aeca7815393cdcd131bb9c3cb1a3215bca`: [isolated run 37135550749](https://github.com/Unn0wn002/CutBridge/actions/runs/37135550749) and [normal CI 37135550709](https://github.com/Unn0wn002/CutBridge/actions/runs/37135550709) reported success with the hashes below. Earlier prose also claimed independent Blender CLI ZIP validation and agreement with the official server generator; exact retained inputs and command logs do not substantiate those independent-tool claims. Repeat and retain them before relying on them for delivery readiness. The recorded AE guide inspection is limited to its source/tag and release-neutral wording.

The [structured preparation record](RELEASE_PREPARATION_v0.2.5.json) records candidate/image identities, hashes, scope, and missing release gates. [Durable automated logs and source manifests](evidence/v0.2.5/0c1938a/checks.log) retain the isolated result in the repository; the archived diff and production-index input match their snapshot manifest hashes. This is automated evidence, not a native S12 PASS record.

Candidate `4f2688625980c4cb0905ee498d42c50ed0069ac6`, [isolated run 37135012123](https://github.com/Unn0wn002/CutBridge/actions/runs/37135012123): **PASS** for the isolated automated scope. Full suite: **312 tests + 2 subtests**, Blender 5.2.1 RNA lifecycle, AE Node/syntax checks, and deterministic repeated packaging passed. Source manifests are identical. [Normal CI 37135012125](https://github.com/Unn0wn002/CutBridge/actions/runs/37135012125) passed both required jobs on the same head. Subsequent preparation changes affect only orchestration/evidence/docs; retain their fresh CI separately from this SHA-bound result.

| Historical 4f268862 / 0c1938a / 3f323e1 candidate artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `b221a759208cfd81e22218db20709f0341a4dc931ab7f0c623f74e6bc87986f6` |
| After Effects ZIP | `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e` |

These are unpublished historical candidate hashes. Earlier native Blender records exposed the stale warning corrected in 604714d, but are now marked **INVALID**: default main-render files escaped the approved output directory. They are preserved as historical records and must not be reused as valid PASS evidence. The fresh bounded-output evidence below supersedes them. Native AE gates, protected promotion, release authorization, publication, and deployed delivery remain pending. Overall release-readiness verdict: **INSUFFICIENT EVIDENCE** until the remaining gates are satisfied.

Candidate packages are verification artifacts, not published releases. Green isolated checks and normal CI do not authorize tagging or replace native-host evidence.

### Revised native Blender evidence — 4 October 2026

The [bounded-output fef1023 campaign](evidence/v0.2.5/fef1023-native-ui/README.md) records Blender **5.2.2 LTS** observations including V001/V002/V003 and 36 mixed PNG/OpenEXR outputs, wording/screenshots, preservation, overwrite refusal, extension enablement, injected mapping rollback and exit code 0. It is **INSUFFICIENT EVIDENCE** for the native release gate because the retained execution policy/mount/offline/credential records are incomplete and `TMPDIR` was not set. Matching manifests alone do not establish sandbox isolation. The Camera/Empty assertion checks that `handoff_3d` is present; it does not validate actual camera/marked-Empty channel values and cannot support the earlier producer-PASS claim. Retain these observations, and repeat the applicable checks with complete boundary records and value-level assertions.

## Historical remaining-gate list — 4 October 2026

This preserved list describes the earlier preparation checkpoint. Use the current candidate section above for completed scope and active blockers; do not repeat or close a gate solely from this historical list.

Earlier [extension/rollback evidence at 0e02c76](evidence/v0.2.5/0e02c76-native-extension/README.md) remains INVALID because of unbounded main-render output. The later fef1023 observations do not close the gate because of the provenance gaps above. No current native PASS is established by those campaigns.

The [AE availability retry with signed runtime dependencies](evidence/v0.2.5/ae-runtime-probe/README.md) timed out after 90 seconds without executing its version script. Input integrity and isolation passed, but no candidate AE runtime was executed. The cause remains undetermined. This historical availability limitation is superseded by the installed AE 26.5x89 campaign above; its remaining S12 coverage gaps are explicitly recorded.

A further [software-graphics visual AE probe](evidence/v0.2.5/ae-software-graphics-probe/README.md) observed Mocha/plugin, missing-class, and invalid-type startup warnings. The version script still did not execute before the 180-second limit. These are host-initialization observations, not evidence of a CutBridge defect or a conclusive root cause.

1. Review and integrate this preparation through protected `develop` after exact-head CI. Record the immutable candidate SHA and package hashes from the isolated verification bundle before native testing; rebuild only if source or toolchain changes.
2. Repeat applicable Blender native checks under a retained, verified isolation configuration: exact-ZIP GUI installation/panel, real render, value-level camera/marked-Empty metadata inspection, fault-injected rollback/artist-node preservation, package safety, manual update behavior and normal clean exit. Existing 4.2/4.5 focused probes remain limited to their recorded scope and do not establish current full workflows.
3. Repeat exact-candidate AE installation, Build/QC, V001→V002→V003, supported status change, optional-content, preservation and native negative/rollback checks under that documented boundary. Inspect supported Camera/Null channels separately from QC. Include fresh-process project reopen and normal exit. Historical observations are comparison inputs only; do not manufacture representative-user results.
4. Promote the tested candidate through the existing protected-branch process. Explicitly authorize only the exact current-main `v0.2.5` / `stable` / non-prerelease tuple after all required evidence is complete. Require release-tag eligibility before creating the tag.
5. Independently download and verify the published v0.2.5 ZIPs, checksums, metadata, versions, licenses, AE sidecars, and corrected guide before distribution. Any failure keeps distribution held.
6. Add verified v0.2.5 files and its release page to the separate distribution repository; preserve v0.2.3. Add a stable notification entry and generate the Blender repository index with official Blender tooling. Do not add v0.2.4 as an intermediate advertised release.
7. After deployment, verify public hashes, both indexes, repository sync/install, manual v0.2.3→v0.2.5 update selection, no downgrade, and unchanged startup scheduling. Record the distribution commit and delivery results before resolving Issue #99.

Use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and [S12_E2E_VALIDATION.md](S12_E2E_VALIDATION.md) for the existing host/evidence procedures. Preparation completion is distinct from release and production-delivery completion.

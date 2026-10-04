# CutBridge v0.2.5 release preparation

Status: **PREPARING / NOT AUTHORIZED**. Production remains on v0.2.3. Do not mirror the immutable v0.2.4 packages: their AE installation guide has the confirmed Issue #99 documentation defect.

The [latest installed AE 26.5x89 campaign](evidence/v0.2.5/049c095-native-ae/README.md) verifies candidate `049c095258f9fc2dd89cbf8f1d7b2b3114d80296`: exact downloaded ZIP Build/QC, V001→V002→V003, inspected artist state, Camera/Null samples, status-change confirmation, optional-content warnings and same-process project reopen passed. Native tests exposed two cached-object defects, repaired with regressions: 3D revision migration now uses the executing adapter's live state, removed-footage cleanup checks captured item IDs, and ownership membership checks reject deleted native handles with `isValid()`. Historical failing campaigns remain preserved. Overall release readiness remains **INSUFFICIENT EVIDENCE**; the recorded scope does not complete installation, exhaustive preservation/negative sign-off, independent review or representative Japanese artist validation.

Latest exact-commit CI: [isolated 37180451235](https://github.com/Unn0wn002/CutBridge/actions/runs/37180451235), [normal CI 37180451191](https://github.com/Unn0wn002/CutBridge/actions/runs/37180451191). **313 tests + 2 subtests**, Blender RNA 5.2.1, syntax, repeated identical packaging, input integrity and unpublished distribution-preview checks passed. All 18 AE Node suites also passed separately in the offline Sandbox. Current unpublished hashes:

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

Both published ZIPs and metadata were downloaded independently. ZIP integrity, source-version identity, required runtime files, GPL license bytes against the release commit, and hashes pass. The downloaded Blender ZIP also passes the installed Blender 5.2.2 CLI package validator. These checks establish package validity; they do not establish a GUI workflow or AE native success.

| Artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2` |
| After Effects ZIP | `e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b` |
| SHA256SUMS.txt | `8fb929650292105effaf39bbcb26427dc056a6cf64f435dd65e65a53083c24ac` |
| release-metadata.json | `6266daa58d12071d64b64e8f21777eb88e9a1f0577277c4650880295325dc0ee` |

The AE `INSTALL.md` still calls v0.2.4 a development package and says its evidence does not authorize publication. This confirms [Issue #99](https://github.com/Unn0wn002/CutBridge/issues/99). [PR #100](https://github.com/Unn0wn002/CutBridge/pull/100) fixed source documentation; [PR #101](https://github.com/Unn0wn002/CutBridge/pull/101) carried it into the v0.2.5 development line. The existing published v0.2.4 files are not modified.

Production notification and Blender indexes were rechecked: they advertise only v0.2.3 at distribution commit `635c1384af2649d4ce49705cce41f98826a861cc`. A local v0.2.4 mirror was prepared before discovering the hold, but was not committed, pushed, or deployed. It must not be used for publication.

## Isolated candidate verification

The `Isolated candidate verification` workflow runs the existing project checks on a `git archive` snapshot without `.git` or owner credentials. Dependencies are prepared before candidate execution. The container has no network, a read-only root filesystem and source mount, an unprivileged user, dropped capabilities, and only the designated verification-output mount writable. The run records image identity, container settings, candidate SHA, source manifests before/after, logs, pytest results, and its verdict.

It runs full pytest, Blender 5.2.1 RNA lifecycle, Python compilation, existing AE Node suites and syntax checks, then invokes the canonical release builder twice. Candidate artifacts must match byte-for-byte. Artifacts are retained for 30 days; download and preserve the evidence bundle in durable release storage before expiry.

The workflow also retains an unpublished distribution preview: manifest-derived Blender index, notification index, versioned candidate files, and release page. It snapshots the live production notification index before offline execution, preserves its existing entries, and verifies v0.2.3 update selection and no downgrade against the staged candidate entry. The preview is partial and must never replace the production tree or bypass published-download verification.

### Recorded automated candidate evidence

Historical runtime candidate `604714d93627a870326a75564eba0af46e5ee957`: [isolated run 37137778152](https://github.com/Unn0wn002/CutBridge/actions/runs/37137778152) and [normal CI 37137778139](https://github.com/Unn0wn002/CutBridge/actions/runs/37137778139) passed **313 tests + 2 subtests**, RNA lifecycle, AE suites/syntax, identical repeated packaging, unchanged input manifests, and offline distribution-preview checks. [Durable logs and manifests](evidence/v0.2.5/604714d/checks.log) bind those results to the corrected handoff wording. That candidate Blender ZIP hash is `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48`; that candidate AE ZIP is `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e`.

Earlier candidate `0c1938aeca7815393cdcd131bb9c3cb1a3215bca`: [isolated run 37135550749](https://github.com/Unn0wn002/CutBridge/actions/runs/37135550749) and [normal CI 37135550709](https://github.com/Unn0wn002/CutBridge/actions/runs/37135550709) passed. Its staged Blender entry independently matched the installed Blender 5.2.2 official generator. Its package hashes matched the historical table below. The installed Blender CLI accepted that ZIP, and the downloaded AE guide was release-neutral with its readiness link pinned to `v0.2.5`.

The [structured preparation record](RELEASE_PREPARATION_v0.2.5.json) records candidate/image identities, hashes, scope, and missing release gates. [Durable automated logs and source manifests](evidence/v0.2.5/0c1938a/checks.log) retain the isolated result in the repository; the archived diff and production-index input match their snapshot manifest hashes. This is automated evidence, not a native S12 PASS record.

Candidate `4f2688625980c4cb0905ee498d42c50ed0069ac6`, [isolated run 37135012123](https://github.com/Unn0wn002/CutBridge/actions/runs/37135012123): **PASS** for the isolated automated scope. Full suite: **312 tests + 2 subtests**, Blender 5.2.1 RNA lifecycle, AE Node/syntax checks, and deterministic repeated packaging passed. Source manifests are identical. [Normal CI 37135012125](https://github.com/Unn0wn002/CutBridge/actions/runs/37135012125) passed both required jobs on the same head. Subsequent preparation changes affect only orchestration/evidence/docs; retain their fresh CI separately from this SHA-bound result.

| Historical 4f268862 / 0c1938a / 3f323e1 candidate artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `b221a759208cfd81e22218db20709f0341a4dc931ab7f0c623f74e6bc87986f6` |
| After Effects ZIP | `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e` |

These are unpublished historical candidate hashes. Earlier native Blender records exposed the stale warning corrected in 604714d, but are now marked **INVALID**: default main-render files escaped the approved output directory. They are preserved as historical records and must not be reused as valid PASS evidence. The fresh bounded-output evidence below supersedes them. Native AE gates, protected promotion, release authorization, publication, and deployed delivery remain pending. Overall release-readiness verdict: **INSUFFICIENT EVIDENCE** until the remaining gates are satisfied.

Candidate packages are verification artifacts, not published releases. Green isolated checks and normal CI do not authorize tagging or replace native-host evidence.

### Revised native Blender evidence — 4 October 2026

The [fresh bounded-output fef1023 campaign](evidence/v0.2.5/fef1023-native-ui/README.md) has valid scoped PASS evidence in Blender **5.2.2 LTS**, with the GUI event loop active inside offline Windows Sandbox. The exact revised ZIP produced V001/V002/V003 and 36 real mixed PNG/OpenEXR outputs. Corrected wording, Camera/marked Empty metadata, artist-node preservation, overwrite protection, official extension installation/enablement, fault-injected mapping rollback, and disabled startup scheduling passed. Actual English/Japanese N-panel screenshots were inspected. Input manifests match, all observed render paths remain inside approved output, and Blender exited normally with code 0. Installer-dialog/button-click checks and live delivery checks remain pending; see the separate current AE campaign for executed native scope.

## Remaining release gates

Earlier [extension/rollback evidence at 0e02c76](evidence/v0.2.5/0e02c76-native-extension/README.md) is INVALID because of the same unbounded main-render output. Use only the fresh fef1023 campaign above for current native scope; package hashes remain unchanged from 604714d.

The [AE availability retry with signed runtime dependencies](evidence/v0.2.5/ae-runtime-probe/README.md) timed out after 90 seconds without executing its version script. Input integrity and isolation passed, but no candidate AE runtime was executed. The cause remains undetermined. This historical availability limitation is superseded by the installed AE 26.5x89 campaign above; its remaining S12 coverage gaps are explicitly recorded.

A further [software-graphics visual AE probe](evidence/v0.2.5/ae-software-graphics-probe/README.md) observed Mocha/plugin, missing-class, and invalid-type startup warnings. The version script still did not execute before the 180-second limit. These are host-initialization observations, not evidence of a CutBridge defect or a conclusive root cause.

1. Review and integrate this preparation through protected `develop` after exact-head CI. Record the immutable candidate SHA and package hashes from the isolated verification bundle before native testing; rebuild only if source or toolchain changes.
2. Complete the remaining applicable Blender visual/manual checks, including panel/install-dialog inspection and manual update behavior. Scripted native render, fault-injected mapping rollback/artist-node preservation, package safety, and normal clean exit are recorded for the exact package hash above. Existing 4.2/4.5 focused probes remain limited to their recorded scope.
3. Complete exact-candidate AE installation sign-off, exhaustive artist/unrelated-object/root-note preservation and the remaining native negative/rollback checks identified in the latest campaign. The recorded Build/QC, V001→V002→V003, status change, optional-content warnings and same-process reopen have executed; retain their exact SHA/hash evidence and do not manufacture representative-user results.
4. Promote the tested candidate through the existing protected-branch process. Explicitly authorize only the exact current-main `v0.2.5` / `stable` / non-prerelease tuple after all required evidence is complete. Require release-tag eligibility before creating the tag.
5. Independently download and verify the published v0.2.5 ZIPs, checksums, metadata, versions, licenses, AE sidecars, and corrected guide before distribution. Any failure keeps distribution held.
6. Add verified v0.2.5 files and its release page to the separate distribution repository; preserve v0.2.3. Add a stable notification entry and generate the Blender repository index with official Blender tooling. Do not add v0.2.4 as an intermediate advertised release.
7. After deployment, verify public hashes, both indexes, repository sync/install, manual v0.2.3→v0.2.5 update selection, no downgrade, and unchanged startup scheduling. Record the distribution commit and delivery results before resolving Issue #99.

Use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and [S12_E2E_VALIDATION.md](S12_E2E_VALIDATION.md) for the existing host/evidence procedures. Preparation completion is distinct from release and production-delivery completion.

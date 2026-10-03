# CutBridge v0.2.5 release preparation

Status: **PREPARING / NOT AUTHORIZED**. Production remains on v0.2.3. Do not mirror the immutable v0.2.4 packages: their AE installation guide has the confirmed Issue #99 documentation defect.

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

Latest runtime candidate `604714d93627a870326a75564eba0af46e5ee957`: [isolated run 37137778152](https://github.com/Unn0wn002/CutBridge/actions/runs/37137778152) and [normal CI 37137778139](https://github.com/Unn0wn002/CutBridge/actions/runs/37137778139) passed **313 tests + 2 subtests**, RNA lifecycle, AE suites/syntax, identical repeated packaging, unchanged input manifests, and offline distribution-preview checks. [Durable logs and manifests](evidence/v0.2.5/604714d/checks.log) bind those results to the corrected handoff wording. The current Blender ZIP hash is `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48`; the AE ZIP remains `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e`.

Earlier candidate `0c1938aeca7815393cdcd131bb9c3cb1a3215bca`: [isolated run 37135550749](https://github.com/Unn0wn002/CutBridge/actions/runs/37135550749) and [normal CI 37135550709](https://github.com/Unn0wn002/CutBridge/actions/runs/37135550709) passed. Its staged Blender entry independently matched the installed Blender 5.2.2 official generator. Its package hashes matched the historical table below. The installed Blender CLI accepted that ZIP, and the downloaded AE guide was release-neutral with its readiness link pinned to `v0.2.5`.

The [structured preparation record](RELEASE_PREPARATION_v0.2.5.json) records candidate/image identities, hashes, scope, and missing release gates. [Durable automated logs and source manifests](evidence/v0.2.5/0c1938a/checks.log) retain the isolated result in the repository; the archived diff and production-index input match their snapshot manifest hashes. This is automated evidence, not a native S12 PASS record.

Candidate `4f2688625980c4cb0905ee498d42c50ed0069ac6`, [isolated run 37135012123](https://github.com/Unn0wn002/CutBridge/actions/runs/37135012123): **PASS** for the isolated automated scope. Full suite: **312 tests + 2 subtests**, Blender 5.2.1 RNA lifecycle, AE Node/syntax checks, and deterministic repeated packaging passed. Source manifests are identical. [Normal CI 37135012125](https://github.com/Unn0wn002/CutBridge/actions/runs/37135012125) passed both required jobs on the same head. Subsequent preparation changes affect only orchestration/evidence/docs; retain their fresh CI separately from this SHA-bound result.

| Historical 4f268862 / 0c1938a / 3f323e1 candidate artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `b221a759208cfd81e22218db20709f0341a4dc931ab7f0c623f74e6bc87986f6` |
| After Effects ZIP | `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e` |

These are unpublished historical candidate hashes. Partial [native Blender evidence at 3f323e1](evidence/v0.2.5/3f323e1-native-blender/README.md) passed a scripted GUI campaign in Blender 5.2.2, including 36 real rendered outputs and three revisions. It exposed the stale warning corrected in 604714d. Visual installation inspection, full native Blender/AE gates, protected promotion, release authorization, publication, and deployed delivery remain pending. The [isolated AE availability probe](evidence/v0.2.5/ae-availability-probe/README.md) did not execute its script; its failure cause is undetermined and no candidate AE runtime was executed. Overall release-readiness verdict: **INSUFFICIENT EVIDENCE** until the remaining gates are satisfied.

Candidate packages are verification artifacts, not published releases. Green isolated checks and normal CI do not authorize tagging or replace native-host evidence.

### Revised native Blender evidence — 4 October 2026

The [fresh 604714d native campaign](evidence/v0.2.5/604714d-native-blender/README.md) passed in Blender **5.2.2 LTS**, with the GUI event loop active inside offline Windows Sandbox. The exact revised ZIP produced V001/V002/V003 and 36 real mixed PNG/OpenEXR outputs. Corrected warning wording, Camera/marked Empty metadata, artist-node preservation, same-version overwrite protection, language identity, and disabled startup scheduling passed. Input manifests match and Blender exited normally with code 0. This is scripted native evidence; visual UI inspection, extension-manager installation, full rollback, manual live update checks, and AE native gates remain pending.

## Remaining release gates

Additional [native extension/rollback evidence at 0e02c76](evidence/v0.2.5/0e02c76-native-extension/README.md) passes official CLI installation, enablement, saved preferences, fresh native GUI loading, panel RNA registration, and fault-injected mapping rollback in Blender 5.2.2. The package hashes are unchanged from 604714d. This reduces the remaining Blender scope to applicable visual/manual checks and live delivery; it does not satisfy AE or publication gates.

The [AE availability retry with signed runtime dependencies](evidence/v0.2.5/ae-runtime-probe/README.md) timed out after 90 seconds without executing its version script. Input integrity and isolation passed, but no candidate AE runtime was executed. The cause remains undetermined. A functioning licensed isolated AE host is required to complete the existing S12 gates.

1. Review and integrate this preparation through protected `develop` after exact-head CI. Record the immutable candidate SHA and package hashes from the isolated verification bundle before native testing; rebuild only if source or toolchain changes.
2. Complete the remaining applicable Blender visual/manual checks, including panel/install-dialog inspection and manual update behavior. Scripted native render, fault-injected mapping rollback/artist-node preservation, package safety, and normal clean exit are recorded for the exact package hash above. Existing 4.2/4.5 focused probes remain limited to their recorded scope.
3. Install the exact AE candidate's four adjacent runtime files, inspect its corrected guide, then run the existing Build/QC, V001→V002→V003, artist-state preservation, negative-package, and save/close/reopen gates. Record host versions and artifact hashes using the existing S12 evidence protocol; do not manufacture representative-user evidence.
4. Promote the tested candidate through the existing protected-branch process. Explicitly authorize only the exact current-main `v0.2.5` / `stable` / non-prerelease tuple after all required evidence is complete. Require release-tag eligibility before creating the tag.
5. Independently download and verify the published v0.2.5 ZIPs, checksums, metadata, versions, licenses, AE sidecars, and corrected guide before distribution. Any failure keeps distribution held.
6. Add verified v0.2.5 files and its release page to the separate distribution repository; preserve v0.2.3. Add a stable notification entry and generate the Blender repository index with official Blender tooling. Do not add v0.2.4 as an intermediate advertised release.
7. After deployment, verify public hashes, both indexes, repository sync/install, manual v0.2.3→v0.2.5 update selection, no downgrade, and unchanged startup scheduling. Record the distribution commit and delivery results before resolving Issue #99.

Use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and [S12_E2E_VALIDATION.md](S12_E2E_VALIDATION.md) for the existing host/evidence procedures. Preparation completion is distinct from release and production-delivery completion.

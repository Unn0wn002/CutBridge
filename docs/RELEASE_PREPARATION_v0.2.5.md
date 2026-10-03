# CutBridge v0.2.5 release preparation

Status: **PREPARING / NOT AUTHORIZED**. Production remains on v0.2.3. Do not mirror the immutable v0.2.4 packages: their AE installation guide has the confirmed Issue #99 documentation defect.

## Candidate identity

- Preparation base: protected `develop` at `8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`.
- Published v0.2.4: immutable tag/main SHA `a393e409d19445c4090460b7e7b4716779161fa4`; release workflow [35843821702](https://github.com/Unn0wn002/CutBridge/actions/runs/35843821702).
- v0.2.5 already includes the Issue #99 source fix, packaged-guide regression checks, version synchronization, modern compositor state-capture repair, and refreshed action pins. This preparation does not change runtime code or schemas.
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

Candidate packages are verification artifacts, not published releases. Green isolated checks and normal CI do not authorize tagging or replace native-host evidence.

## Remaining release gates

1. Review and integrate this preparation through protected `develop` after exact-head CI. Record the immutable candidate SHA and package hashes from the isolated verification bundle before native testing; rebuild only if source or toolchain changes.
2. Complete the applicable native Blender 5.2 campaign with the exact candidate ZIP, including interactive render, output mapping rollback/artist-node preservation, package safety, manual update behavior, and normal clean exit. Validate the changed modern compositor path. Existing 4.2/4.5 focused probes remain limited to their recorded scope.
3. Install the exact AE candidate's four adjacent runtime files, inspect its corrected guide, then run the existing Build/QC, V001→V002→V003, artist-state preservation, negative-package, and save/close/reopen gates. Record host versions and artifact hashes using the existing S12 evidence protocol; do not manufacture representative-user evidence.
4. Promote the tested candidate through the existing protected-branch process. Explicitly authorize only the exact current-main `v0.2.5` / `stable` / non-prerelease tuple after all required evidence is complete. Require release-tag eligibility before creating the tag.
5. Independently download and verify the published v0.2.5 ZIPs, checksums, metadata, versions, licenses, AE sidecars, and corrected guide before distribution. Any failure keeps distribution held.
6. Add verified v0.2.5 files and its release page to the separate distribution repository; preserve v0.2.3. Add a stable notification entry and generate the Blender repository index with official Blender tooling. Do not add v0.2.4 as an intermediate advertised release.
7. After deployment, verify public hashes, both indexes, repository sync/install, manual v0.2.3→v0.2.5 update selection, no downgrade, and unchanged startup scheduling. Record the distribution commit and delivery results before resolving Issue #99.

Use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and [S12_E2E_VALIDATION.md](S12_E2E_VALIDATION.md) for the existing host/evidence procedures. Preparation completion is distinct from release and production-delivery completion.

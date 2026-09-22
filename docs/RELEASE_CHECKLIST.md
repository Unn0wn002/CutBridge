# Release Checklist

Before tagging a CutBridge release:

- [ ] Review the live `main`/`develop` relationship and promote the verified candidate through a PR.
- [ ] Run every command in [CONTRIBUTING.md](CONTRIBUTING.md); all authoritative tests and CI jobs pass on the exact candidate commit.
- [ ] `version.py` (`__version__` and `VERSION`), `blender_manifest.toml`, `bl_info`, generated `cutbridge.json`, README, changelog and `CutBridge.jsx` `PRODUCT_VERSION` agree on the numeric product version.
- [ ] Manifest schema compatibility is preserved or a schema change is intentional and supported by both apps.
- [ ] Both versioned ZIPs contain the full LICENSE; no private client assets, credentials, or production data are included.
- [ ] The After Effects ZIP contains `CutBridge.jsx`, `revision_manager.js`, `INSTALL.md`, and `LICENSE`; do not publish an AE artifact with the revision sidecar or two-file installation guidance missing.
- [ ] Recompute SHA-256 values and compare them with both `SHA256SUMS.txt` and `release-metadata.json`.
- [ ] Repeat the build with the same toolchain; artifacts are identical despite source timestamp/permission changes.
- [ ] Record Blender version, OS, GUI installation, panel, Validate Cut and Build Package results.
- [ ] Record After Effects version and OS, installation/launch method, manifest import, comp setup, sequence import, QC, and revision-manager loading results.
- [ ] In a real After Effects desktop host, perform V001 → V002 → V003 on a representative package and verify only CutBridge-managed sources/metadata change.
- [ ] During the real revision test, verify effects, masks, transforms, parenting, timing, layer order, artist-added layers, unrelated footage/comps/folders, and artist/studio package-root notes are preserved.
- [ ] Save the revised AE project, close/reopen it, reload CutBridge, then run Build Comp and QC again; record the result.
- [ ] In a disposable real-AE copy, delete and separately de-tag a required managed layer while its managed footage and comp remain valid; QC must fail closed on managed-layer ownership/source instead of reporting PASS. Also verify an unambiguous complete optional managed layer can be absent with a warning, and an unavailable optional source sequence remains warning/skip only.
- [ ] Exercise at least one supported required/optional **status** change and confirm the explicit warning/confirmation path.
- [ ] Exercise at least one incompatible geometry/timing revision (for example FPS/frame-range/pixel-aspect/resolution drift) and confirm fail-closed behavior.
- [ ] Exercise candidate removal of an optional pass and confirm source-only revision blocks **before** confirmation, import, `replaceSource()`, or package/tag migration; verify the original package remains coherent for reload, Build and QC. Added-pass and required-pass-removal cases must also remain fail-closed.
- [ ] Exercise a missing/duplicate deterministic managed-folder condition in a safe test project and confirm Build/revision/QC do not silently choose, recreate, or mutate ambiguous structure.
- [ ] Complete a real Blender → package → After Effects smoke test. Do not replace it with headless or host-shaped evidence.
- [ ] Update compatibility records and changelog release status with actual evidence.
- [ ] Obtain the required independent review(s) for the exact release candidate and resolve all review findings before promotion/tagging.
- [ ] Keep root `release-authorization.json` unapproved while any release gate is incomplete.
- [ ] Decide the intended publication class and exact tag: stable `vX.Y.Z`, beta validation `vX.Y.Z-rc.N`/`vX.Y.Z-beta.N`, or development validation `vX.Y.Z-dev.N`.
- [ ] On the validated current `main` candidate, change `release-authorization.json` to explicitly approve that exact tag, matching `channel` and `prerelease`; review/test that authorization commit as part of the release candidate.
- [ ] Confirm the approved tag will point to the **current `main` HEAD** and that the workflow stored at that tagged commit contains the exact-main/authorization gate.
- [ ] Do **not** assume current workflow hardening retroactively protects historical commits. Before release operations, use repository-admin controls to restrict tag creation/release publication to the intended maintainer path (for example an applicable ruleset/environment/Actions permission policy), or keep the Release workflow disabled globally when no release is being performed.
- [ ] For RC/beta/development publication, verify the workflow marks the GitHub Release as a prerelease and `release-metadata.json` carries the matching prerelease version/channel.
- [ ] For the intended Japanese-first market, complete the planned native-user/terminology validation appropriate to the release claim before describing the product as production-ready for Japanese animation/content teams.
- [ ] Create the authorized tag only after all preceding gates are recorded.
- [ ] Confirm the Release workflow publishes both ZIPs, checksums and metadata from the authorized `main` HEAD.
- [ ] Download the published assets, verify the AE ZIP still contains both scripts plus `INSTALL.md` and `LICENSE`, and recompute checksums before distribution.
- [ ] If the publication is an RC/beta/development GitHub prerelease, install/test the downloaded artifacts deliberately. Do not claim in-plugin beta distribution until a matching external index entry and publication path are deployed and verified.
- [ ] Before any stable distribution, mirror only the deliberately approved stable artifacts/update metadata to the separate production distribution endpoint; never use source-repository hosting itself as the client update endpoint.

Current status note — 22 September 2026: stable v0.2.3 completed the checklist through authorized tag creation, GitHub Release publication, independent asset verification, and separate production D1 deployment. Active v0.2.4 development has restored `release-authorization.json` to `approved: false`; no v0.2.4 tag, GitHub Release, or distribution entry exists. Every future release must repeat the checklist on its own exact candidate; completion for v0.2.3 does not weaken or pre-satisfy any v0.2.4 gate.

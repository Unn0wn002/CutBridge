# Release Checklist

Before tagging a CutBridge release:

- [ ] Review the live `main`/`develop` relationship and promote the verified candidate through a PR.
- [ ] Run every command in [CONTRIBUTING.md](CONTRIBUTING.md); all authoritative tests and CI jobs pass on the exact candidate commit.
- [ ] `version.py` (`__version__` and `VERSION`), `blender_manifest.toml`, `bl_info`, generated `cutbridge.json`, README, changelog, tag and release metadata agree.
- [ ] Manifest schema compatibility is preserved or a schema change is intentional and supported by both apps.
- [ ] Both versioned ZIPs contain the full LICENSE; no private client assets, credentials, or production data are included.
- [ ] The After Effects ZIP contains both executable S6 files, `CutBridge.jsx` and `revision_manager.js`, beside the LICENSE; do not publish an AE artifact with the revision sidecar missing.
- [ ] Recompute SHA-256 values and compare them with both `SHA256SUMS.txt` and `release-metadata.json`.
- [ ] Repeat the build with the same toolchain; artifacts are identical despite source timestamp/permission changes.
- [ ] Record Blender version, OS, GUI installation, panel, Validate Cut and Build Package results.
- [ ] Record After Effects version and OS, installation/launch method, manifest import, comp setup, sequence import, QC, and revision-manager loading results.
- [ ] In a real After Effects desktop host, perform V001 → V002 → V003 on a representative package and verify only CutBridge-managed sources/metadata change.
- [ ] During the real revision test, verify effects, masks, transforms, parenting, timing, layer order, artist-added layers, unrelated footage/comps/folders, and artist/studio package-root notes are preserved.
- [ ] Save the revised AE project, close/reopen it, reload CutBridge, then run Build Comp and QC again; record the result.
- [ ] Exercise at least one warning/confirmation revision and at least one incompatible revision (for example FPS/frame-range/pixel-aspect/resolution drift) and confirm the expected fail-closed behavior.
- [ ] Exercise a missing/duplicate deterministic managed-folder condition in a safe test project and confirm Build/revision/QC do not silently choose, recreate, or mutate ambiguous structure.
- [ ] Complete a real Blender → package → After Effects smoke test. Do not replace it with headless or host-shaped evidence.
- [ ] Update compatibility records and changelog release status with actual evidence.
- [ ] Obtain the required independent review(s) for the exact release candidate and resolve all review findings before promotion/tagging.
- [ ] Tag the validated `main` commit and confirm the Release workflow publishes both ZIPs, checksums and metadata.
- [ ] Download the published assets, verify the AE ZIP still contains both scripts, and recompute checksums before distribution.
- [ ] For the intended Japanese-first market, complete the planned native-user/terminology validation appropriate to the release claim before describing the product as production-ready for Japanese animation/content teams.

At the 2026-09-08 S6 reconciliation there are still no GitHub Releases. Package simulation and green branch CI do not prove that tag-triggered publication, release-asset download, or real After Effects desktop behavior works. Do not treat those gates as complete until actual evidence is recorded.

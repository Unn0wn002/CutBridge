# Release Checklist

Before tagging a CutBridge release:

- [ ] Review the live `main`/`develop` relationship and promote the verified candidate through a PR.
- [ ] Run every command in [CONTRIBUTING.md](CONTRIBUTING.md); all authoritative tests and CI jobs pass.
- [ ] `version.py` (`__version__` and `VERSION`), `blender_manifest.toml`, `bl_info`, generated `cutbridge.json`, README, changelog, tag and release metadata agree.
- [ ] Manifest schema compatibility is preserved or a schema change is intentional and supported by both apps.
- [ ] Both versioned ZIPs contain the full LICENSE; no private client assets, credentials, or production data are included.
- [ ] Recompute SHA-256 values and compare them with both SHA256SUMS.txt and release-metadata.json.
- [ ] Repeat the build with the same toolchain; artifacts are identical despite source timestamp/permission changes.
- [ ] Record Blender version, OS, GUI installation, panel, Validate Cut and Build Package results.
- [ ] Record After Effects version, OS, manifest import, comp setup, sequence import and QC results.
- [ ] Complete a real Blender → package → After Effects smoke test. Do not replace it with headless evidence.
- [ ] Update compatibility records and changelog release status with actual evidence.
- [ ] Tag the validated `main` commit and confirm the Release workflow publishes both ZIPs, checksums and metadata.
- [ ] Download the published assets and recompute checksums before distribution.

At the 2026-09-06 baseline audit there were no tags or GitHub releases. Package simulation passes do not prove that tag-triggered publication works. Session 1 does not create a release.

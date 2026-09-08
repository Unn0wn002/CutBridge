# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, compositing setup, QC, and controlled revision handling so artists can move work from Blender into After Effects with less repetitive setup and fewer handoff errors.

The primary audience is Japanese animation and content-creation artists and studios, while English usability remains supported. CutBridge is not a renderer, toon shader, animation generator, or asset manager; it is a structured handoff layer between Blender production and After Effects compositing.

## Current product status

**v0.2.3 — unreleased development baseline**

`main` remains the deliberately conservative release baseline. It includes the fail-closed release-publication lock, but it has **not** been promoted to the current active development feature set and no GitHub Release has been published.

Active integration is on `develop`, where Sessions S1-S5 are completed. Session S6 — non-destructive After Effects revision handling — is implemented on PR #15 with green automated regression evidence, but it is not yet authorized for integration or release. The exact S6 candidate still requires:

- a genuinely independent full-PR review;
- real Adobe After Effects desktop V001 → V002 → V003 validation, including property preservation and save/reopen behavior;
- merge to `develop` followed by green post-merge CI.

S7 must not begin until those S6 integration gates are satisfied.

## Implemented development scope

### Blender

- Project / Episode / Scene / Cut / Take / Version metadata.
- FPS, resolution, frame-range, and active-camera capture.
- Cut validation and deterministic package generation.
- Transactional render-output mapping for CutBridge-owned BEAUTY / LINE / SHADOW / DEPTH outputs while preserving unrelated artist compositor nodes.
- Same-version overwrite protection when an existing package already contains render/user payload.
- V001 / V002 / V003 package coexistence and deterministic package naming.
- UTF-8 `cutbridge.json` manifest generation.
- Modern `blender_manifest.toml` extension metadata.
- Environment/version diagnostics.
- LTS-first compatibility policy.
- Stable / Beta / Development update-channel preference and optional update checking without forced active-session self-replacement.
- Transactional registration cleanup and official Blender 5.2 RNA/integration coverage.

### After Effects

- ExtendScript/ScriptUI importer.
- Manifest schema/version validation and package-relative path safety.
- Deterministic project folders and managed composition creation.
- Complete required image-sequence import, exact frame-coverage validation, and FPS conform.
- Required-pass errors and optional-pass warning/skip behavior.
- Conservative persistent ownership for managed comps, footage, and layers.
- Repeated Build/reload safety that does not adopt unrelated artist objects by name alone.
- QC for managed structure, comp metadata, sequence coverage, footage source/FPS, and ownership drift.
- S6 candidate: newer-package selection, compatibility checks, explicit confirmation, staged replacement import, native `AVLayer.replaceSource(..., false)` source swaps, rollback, historical-footage provenance, managed metadata migration, and fail-closed package-structure resolution.

Automated Node/host-shaped tests are regression evidence only. They do **not** certify native After Effects behavior.

## Repository layout

```text
CutBridge/
├── apps/
│   ├── blender/cutbridge/
│   └── after-effects/
├── packages/
│   ├── shared/
│   └── update/
├── tools/
│   └── build_release.py
├── docs/
├── tests/
└── .github/workflows/
```

## Compatibility

Minimum Blender runtime is **4.2.0**. The current LTS-first targets are Blender **4.2 LTS**, **4.5 LTS**, and **5.2 LTS**. A compatible version is not automatically described as certified until runtime evidence exists.

After Effects compatibility must be established with real desktop-host validation before a stable release claim.

See [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).

## Update and release policy

The private source repository is **not** the client update endpoint. Production distribution is intended to use a separate release/update endpoint.

Release publication is fail-closed by default. `release-authorization.json` must remain unapproved while any release gate is incomplete. Repository-level branch/tag governance, real Blender → package → After Effects end-to-end testing, release-asset/checksum verification, and appropriate Japanese native-user/terminology validation remain required before production release claims.

See [`docs/UPDATE_ARCHITECTURE.md`](docs/UPDATE_ARCHITECTURE.md) and [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md).

## Development flow

- `main` — deliberate release/stable-promotion baseline; currently behind active development by design.
- `develop` — active integration; current completed S1-S5 baseline.
- `feature/*` / `fix/*` / bounded docs branches — focused work branched from the appropriate live baseline.

## Next product work

1. Complete S6 integration gates: independent exact-head review, native After Effects V001 → V002 → V003/property-preservation/save-reopen validation, merge to `develop`, and green post-merge CI.
2. S7 — QC+ diagnostics and revision-aware checks.
3. S8 — English/Japanese UX architecture, Japanese quick-start localization, and terminology QA.
4. S9 — configurable studio presets.
5. S10 — camera/null handoff investigation.
6. S11-S14 — release engineering, real end-to-end validation, manual-finding repair, and target-user validation preparation.
7. Only after repository-level release governance is available and validated: promote a verified candidate to `main`, publish an authorized RC/pre-release, verify downloaded artifacts/checksums, and then consider stable publication.

## License

CutBridge uses **GPL-3.0-or-later**. The full GPL v3 text is in [`LICENSE`](LICENSE).

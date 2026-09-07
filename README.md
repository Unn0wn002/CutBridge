# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, compositing setup, QC, and controlled revision handling so artists can move work from Blender into After Effects with less repetitive setup and fewer handoff errors.

The primary audience is Japanese animation and content-creation artists and studios, with English usability retained and no single studio workflow hard-coded.

CutBridge is designed around cut-based animation production workflows. It is not a renderer, toon shader, animation generator, or asset manager. Its job is to provide a structured handoff layer between 3D production and compositing: validate the cut in Blender, configure deterministic render outputs, build a deterministic package, transfer the manifest and render sequences, reconstruct the expected composition context in After Effects, run QC, and apply compatible revisions without silently replacing unrelated artist work.

## Current development version

**v0.2.3 — unreleased development baseline**

The integrated `develop` baseline contains completed Sessions S1-S5. Session S6 (non-destructive After Effects revision handling) is under active review on PR #15 and is **not yet authorized for merge or stable release**. Real After Effects GUI/end-to-end validation remains a manual release gate.

### Blender

- Project / Episode / Scene / Cut / Take / Version metadata.
- FPS, resolution, frame-range, and active-camera capture.
- Cut validation and deterministic package generation.
- Transactional render-output mapping for CutBridge-owned BEAUTY / LINE / SHADOW / DEPTH outputs while preserving unrelated artist compositor nodes.
- Same-version overwrite protection when a package already contains render/user payload.
- Version coexistence for V001 / V002 / V003 package workflows.
- UTF-8 `cutbridge.json` manifest.
- Modern `blender_manifest.toml` extension metadata.
- Environment diagnostics: CutBridge version, Blender version, Python, platform, online-access status.
- LTS-first compatibility status.
- Stable / Beta / Development update-channel preference.
- Optional startup update **check**.
- No forced or active-session self-update.
- Transactional registration cleanup so failed enables do not leave stale RNA classes behind.

### After Effects

- ExtendScript/ScriptUI importer.
- Manifest schema/version validation.
- Manifest-driven project folders and composition creation.
- Complete required image-sequence import and FPS conform.
- Required-pass errors and optional-pass warning/skip behavior.
- Exact expected-frame coverage with missing, extra, and wrong-padding diagnostics.
- Package-relative path validation and UTF-8 Japanese filenames.
- Legacy JSON parsing without executing manifest data.
- Deterministic CutBridge-managed comp, footage, and layer ownership tags.
- Repeated-build/reload safety with conservative collision handling instead of adopting unrelated artist objects.
- QC for managed comp metadata, sequence coverage, managed footage source/FPS, and ownership drift.
- S6 branch work adds a revision-manager sidecar, newer-package selection, compatibility checks, explicit confirmation, staged replacement import, source-swap rollback, and managed metadata migration. This workflow remains review-blocked until its full lifecycle is proven safe.
- Export frames must start at 0 or later; negative/preroll cuts must be rebased before export. No automatic animation renumbering.

### Engineering

- Private source repository.
- `main` / `develop` / short-lived feature/fix branch workflow.
- CI on main, develop, feature, and fix branches.
- Official `bpy 5.2.1` RNA lifecycle, render-mapping, package-generation, and producer/consumer contract integration tests.
- Executable Node tests for AE contract helpers and mocked host-adapter behavior.
- Deterministic release builder.
- Version/tag consistency validation, including AE product-version drift checks.
- Blender + After Effects ZIP artifacts.
- SHA-256 checksums and release metadata.
- Separate release-index schema for future public distribution.

## Quick Start

See [`docs/QUICK_START.md`](docs/QUICK_START.md) for the current implemented Blender → package → After Effects workflow and explicit manual-validation boundaries.

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

See [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).

Minimum Blender runtime is **4.2.0**. The current LTS-first targets are Blender **4.2 LTS**, **4.5 LTS**, and **5.2 LTS**. A version meeting the minimum is not automatically described as certified until runtime testing is recorded.

After Effects compatibility must be established with real desktop-host validation before a stable release claim. Node/mock tests are regression evidence, not a substitute for native AE execution.

## Update policy

See [`docs/UPDATE_ARCHITECTURE.md`](docs/UPDATE_ARCHITECTURE.md).

The private source repository is **not** the plugin update endpoint. CutBridge can check a separately configured release index and notify the user, but installation remains user-approved. Production distribution is intended to use Blender's Remote Extension Repository system.

## Development flow

- `main` — stable/release-ready only after deliberate promotion and release validation.
- `develop` — active integration and the current completed S1-S5 baseline.
- `feature/*` / `fix/*` / bounded docs branches — focused work branched from current `develop`.

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for complete test commands, [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) for the validation matrix, [`docs/COMPLETION_STATUS.md`](docs/COMPLETION_STATUS.md) for live completion gates, and [`docs/BASELINE_2026-09-06.md`](docs/BASELINE_2026-09-06.md) for the Session 1 repository audit.

## License

CutBridge uses **GPL-3.0-or-later**, as declared by the Blender extension manifest. The full GPL v3 text is in [`LICENSE`](LICENSE); both release ZIPs include it.

## Release status

Version 0.2.3 is an unreleased development baseline. There is no stable GitHub Release yet. Automated package/release simulation does not certify the full Blender → After Effects workflow.

Stable publication remains blocked until the release checklist is satisfied, including real Blender GUI validation, real After Effects import/build/QC, Blender → package → After Effects end-to-end testing, revision-preservation validation, release artifact/checksum verification, and appropriate Japanese-user validation for the intended primary market.

## Next product work

1. Finish and independently review S6 — Non-Destructive Revision Manager, including repeated revision/build/QC/reload lifecycle safety.
2. S7 — QC+ diagnostics and revision-aware checks.
3. S8 — English/Japanese UX architecture, Japanese quick-start localization, and terminology QA.
4. S9 — configurable studio presets.
5. S10 — camera/null handoff investigation.
6. S11-S14 — release engineering, end-to-end validation, manual-finding repair, and target-user validation preparation.
7. Promote a verified candidate from `develop` to `main`, publish an RC/pre-release, verify downloaded artifacts/checksums, and only then consider a stable release.

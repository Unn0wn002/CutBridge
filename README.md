# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, and compositing setup so artists can move work from Blender into After Effects with less repetitive setup and fewer pipeline errors.

The primary audience is Japanese animation and content-creation artists and studios, with English usability retained and no single studio workflow hard-coded.

CutBridge is designed around cut-based animation production workflows. Instead of acting as a renderer, shader, or animation tool, it provides a structured handoff layer between 3D production and compositing: validate the cut in Blender, build a deterministic package, transfer the manifest and render sequences, then let the After Effects side reconstruct the expected composition context and perform QC.

## Current development version

**v0.2.3 — Blender 5.2 runtime and package-generation validation**

### Blender

- Project / Episode / Scene / Cut / Take / Version metadata.
- FPS, resolution, frame-range, and active-camera capture.
- Cut validation and deterministic package generation.
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
- Manifest-driven project folders and composition creation.
- Image-sequence import and FPS conform.
- Layer ordering and exact expected-frame QC.
- Manifest schema/version validation, required-pass errors and optional-pass warnings.
- Package-relative path validation and UTF-8 Japanese filenames.
- Export frames must start at 0 or later; negative/preroll cuts must be rebased before export. No automatic animation renumbering.

S4 repair is tracked in [PR #12](https://github.com/Unn0wn002/CutBridge/pull/12); independent review and real AE GUI validation remain required.

### Engineering

- Private source repository.
- `main` / `develop` / `feature/*` / `fix/*` branch workflow.
- CI on main, develop, and feature branches.
- Official `bpy 5.2.1` RNA lifecycle and package-generation integration tests.
- Deterministic release builder.
- Version/tag consistency validation.
- Blender + After Effects ZIP artifacts.
- SHA-256 checksums and release metadata.
- Separate release-index schema for future public distribution.

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

## Update policy

See [`docs/UPDATE_ARCHITECTURE.md`](docs/UPDATE_ARCHITECTURE.md).

The private source repository is **not** the plugin update endpoint. CutBridge can check a separately configured release index and notify the user, but installation remains user-approved. Production distribution is intended to use Blender's Remote Extension Repository system.

## Development flow

- `main` — stable/release-ready.
- `develop` — active integration.
- `feature/*` / `fix/*` — focused work branched from current `develop`.

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for complete test commands and [`docs/BASELINE_2026-09-06.md`](docs/BASELINE_2026-09-06.md) for the Session 1 repository audit.

## License

CutBridge uses **GPL-3.0-or-later**, as already declared by the Blender extension manifest. The full GPL v3 text is in [`LICENSE`](LICENSE); both release ZIPs include it.

## Release status

Version 0.2.3 is an unreleased development baseline. No GitHub release or tag exists at the Session 1 audit. Release-package simulation does not certify the full Blender → After Effects workflow.

## Next product work

1. Blender render-pass/output mapping.
2. Non-destructive After Effects revision manager.
3. Missing-frame and naming QC expansion.
4. Studio presets.
5. Full English/Japanese UI.
6. Camera/null handoff.
7. Client workflow validation.

# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, and compositing setup so artists can move work from Blender into After Effects with less repetitive setup and fewer pipeline errors.

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
- Layer ordering and basic QC.

### Engineering

- Private source repository.
- `main` / `develop` / `feature/*` branch workflow.
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
- `feature/*` — isolated features.

## Next product work

1. Blender render-pass/output mapping.
2. Non-destructive After Effects revision manager.
3. Missing-frame and naming QC expansion.
4. Studio presets.
5. Full English/Japanese UI.
6. Camera/null handoff.
7. Client workflow validation.

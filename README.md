# CutBridge

CutBridge is an anime-oriented production bridge for **Blender → After Effects** workflows.

The project standardizes cut metadata, deterministic package structures, JSON handoff manifests, After Effects composition setup, production QC, and a controlled release/update foundation.

## Current development version

**v0.2.0 — update/distribution foundation**

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

### After Effects

- ExtendScript/ScriptUI importer.
- Manifest-driven project folders and composition creation.
- Image-sequence import and FPS conform.
- Layer ordering and basic QC.

### Engineering

- Private source repository.
- `main` / `develop` / `feature/*` branch workflow.
- CI on main, develop, and feature branches.
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

Minimum Blender runtime is **4.2.0**. The current LTS-first targets are Blender **4.2 LTS** and **4.5 LTS**. A version meeting the minimum is not automatically described as certified until runtime testing is recorded.

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

# CutBridge

CutBridge is an anime-oriented production bridge for **Blender → After Effects** workflows.

The project standardizes cut metadata, deterministic package structures, JSON handoff manifests, After Effects composition setup, and production QC. The initial MVP focuses on a reliable end-to-end handoff before adding revision management and production update tooling.

## Current MVP

- Blender add-on / extension foundation
- Cut metadata: project, episode, scene, cut, take, version
- Scene metadata capture: FPS, resolution, frame range, active camera
- Validation before package generation
- Deterministic folder/package generation
- UTF-8 `cutbridge.json` handoff manifest
- After Effects ExtendScript importer
- Automatic AE project folders and composition creation
- Image-sequence import and layer ordering
- Basic QC
- Shared JSON Schema
- CI and release workflow foundations

## Repository layout

```text
CutBridge/
├── apps/
│   ├── blender/
│   └── after-effects/
├── packages/
│   └── shared/
├── docs/
├── tests/
└── .github/workflows/
```

## Compatibility target

- Blender: 4.2 LTS+ baseline, with LTS-first compatibility testing
- After Effects: 2024–2026 target
- OS: Windows first, macOS validation planned
- UI/localization target: English + Japanese

## Branch model

- `main` — stable/release-ready
- `develop` — active integration
- `feature/*` — isolated features

## Roadmap

1. Stabilize Blender → package → After Effects handoff.
2. Convert packaging fully to the modern Blender Extension workflow.
3. Add non-destructive revision updates.
4. Add deeper QC and missing-frame detection.
5. Add English/Japanese UI switching.
6. Add release/update infrastructure and compatibility gates.
7. Validate against real client/studio workflows.

## Status

**MVP v0.1.0 — development baseline.**

This repository is private during university-project development.

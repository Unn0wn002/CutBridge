# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, compositing setup, QC, controlled revision handling, Japanese-first workflow UX, safe Studio Presets, and a bounded 3D handoff workflow so artists can move work from Blender into After Effects with less repetitive setup and fewer handoff errors.

The primary audience is Japanese animation and content-production artists and studios. English remains a deterministic supported fallback. Studio Presets let teams adapt naming, folders, pass policy, and presentation conventions without hard-coding one studio workflow into CutBridge.

CutBridge is not a renderer, toon shader, animation generator, general scene exporter, or asset manager. Its role is the handoff layer between 3D cut production and compositing: validate the cut in Blender, resolve an optional declarative Studio Preset, configure deterministic render outputs, build a deterministic package, transfer the manifest and render sequences, reconstruct the supported AE context, run QC, and apply compatible revisions without silently replacing unrelated artist work.

## Current development version

**v0.2.3 — unreleased development baseline**

Sessions **S1–S9 plus S10A–S10C are integrated** on `develop`.

- S10A established the Blender ↔ After Effects coordinate, timing, camera, and Empty/Null contract.
- S10B added an optional/versioned `handoff_3d` producer with evaluated-world Blender sampling for the supported perspective camera and explicitly marked Empties.
- S10C now consumes that contract in After Effects to reconstruct CutBridge-managed camera and 3D Null layers, with native projection parity validated in Adobe After Effects 2026 Build 87.

Stable or RC publication remains blocked by repository-level release governance issue #18 and the deliberately unapproved release authorization state.

### Blender

- Project / Episode / Scene / Cut / Take / Version metadata.
- FPS, resolution, frame-range, and active-camera capture.
- Cut validation and deterministic package generation.
- Transactional BEAUTY / LINE / SHADOW / DEPTH render-output mapping while preserving unrelated artist compositor nodes.
- Same-version overwrite protection when render/user payload exists.
- V001 / V002 / V003 package coexistence.
- UTF-8 `cutbridge.json` manifest.
- Environment diagnostics and LTS-first compatibility status.
- Stable / Beta / Development update-channel preference and notification-only update checks.
- Transactional registration cleanup for Blender 5.2.x RNA lifecycle safety.
- Japanese-first / English-fallback localized panel, validation messaging, and narrow-panel layout.
- S9 Studio Preset modes: **Manual**, **CutBridge Default**, and **Custom JSON**.
- Strict data-only preset validation with stable `PRESET_*` diagnostics.
- Preset-managed package/sequence naming, folder roles, pass order/required flags, PNG/OpenEXR/TIFF format, version token, and AE comp naming.
- One validated custom-preset snapshot per Build Package transaction.
- S10A deterministic axis/timing/FOV primitives.
- S10B optional evaluated-world camera/Empty sampling into `handoff_3d` when explicitly enabled.

### Studio Preset safety

Studio Presets are declarative JSON only.

- custom files are UTF-8 JSON and capped at 64 KiB;
- schema/version/known fields are strict;
- absolute paths, traversal, overlapping folder roles, unsupported placeholders, duplicate passes, and unsupported formats are rejected;
- arbitrary code, command execution, environment expansion, and hidden network behavior are not supported;
- source preset paths are not written to `cutbridge.json`;
- Manual remains the default and preserves historical package identity behavior;
- After Effects never opens the Studio Preset file.

See [`docs/STUDIO_PRESETS.md`](docs/STUDIO_PRESETS.md).

### 3D handoff boundary

S10B produces a versioned optional `handoff_3d` block containing baked evaluated-world samples for:

- the active supported perspective camera;
- explicitly marked Blender Empties only.

The S10 contract does not copy Blender Euler channels directly into AE. It preserves the explicit axis contract:

```text
Blender (x, y, z) -> AE-oriented (x, -z, y)
```

Timing is baked using:

```text
AE time = (frame - frame_start) / fps
```

Unsupported camera projection, non-square pixels, sensor shift, zero-scale/sheared/reflected transforms, invalid object markers, and excessive sample counts fail closed on the producer side.

S10C reconstructs the supported `handoff_3d` subset as managed AE camera and 3D Null layers. Native Adobe After Effects 2026 Build 87 validation measured a maximum 2D projection error of **0.00018066 px** against a **0.05 px** acceptance gate, with idempotent rebuild, collision rejection, QC+, and project persistence also passing.

See [`docs/CAMERA_NULL_HANDOFF_CONTRACT.md`](docs/CAMERA_NULL_HANDOFF_CONTRACT.md) and [`docs/HANDOFF_3D.md`](docs/HANDOFF_3D.md).

### After Effects

- ExtendScript/ScriptUI package importer.
- Manifest schema/version and path validation.
- Deterministic managed project folders, comp, footage, and layer ownership.
- Exact sequence-frame coverage validation with required/optional pass semantics.
- Repeated-build/reload safety and conservative collision handling.
- S6 non-destructive revision workflow using verified source replacement with rollback and historical-footage provenance.
- S7 QC+ deterministic PASS / WARNING / ERROR diagnostics with stable `CBQ-*` identifiers and safe remediation guidance.
- S8 Japanese-first / English-fallback UI through adjacent `localization.js`, with deterministic English fallback if the localization sidecar is unavailable.
- S9 consumes preset-resolved manifest values; AE does not parse Studio Preset JSON.
- S10C validates and consumes the supported `handoff_3d` block, creating/updating CutBridge-managed camera and 3D Null layers with baked transform/projection timing.
- Managed camera/null reconstruction is idempotent and fails closed on unmanaged ownership collisions.
- Build, Revision, QC, and 3D reconstruction fail closed when ownership or package structure is missing or ambiguous.
- Negative/preroll export ranges are unsupported; export must be rebased to frame 0 or later.

## Validation model

Authoritative automated integration requires both GitHub Actions jobs:

- `static-validation` — Python/AE contract tests, Studio Preset tests, S10A/S10B schema/compatibility tests, S10C reconstruction checks, deterministic release simulation, S6/S7/S8 regressions, and ExtendScript syntax;
- `blender-52-rna-runtime` — official `bpy==5.2.1` registration lifecycle and complete Blender/runtime pytest suite, including evaluated-world sampling and package-generation coverage.

S10C integration evidence:

- candidate `3108058f03d11ccba62fb1771079e1b7fd15aa0c`;
- candidate push CI `34439794396`: PASS;
- PR #54 event CI `34439880617`: PASS;
- merge `493625ac5e83a0fcec8a858346ec96e0b4b0f2de`;
- post-merge `develop` CI `34439972955`: PASS.

Native S10C evidence:

- Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11;
- Blender 5.2.1 LTS-produced handoff data;
- maximum measured projection error `0.00018066 px` across the validated spatial fixtures;
- QC+ 10/10 PASS;
- idempotent rebuild with zero duplicate managed layers;
- unmanaged camera/null collision rejection;
- project persistence verified.

Historical real-host evidence remains valid for the scopes it actually tested:

- Blender 5.2.1 LTS S8 narrow-panel/localization/Validate/Build gate: PASS;
- Adobe After Effects 2026 Build 87 S8 localization/fallback gate: PASS;
- S6/S7 real AE revision/QC campaigns: PASS after repaired native findings.

The Blender suite still reports `Scene.use_nodes` deprecation warnings relevant to future Blender 6.0 work; see [`docs/TECHNICAL_DEBT.md`](docs/TECHNICAL_DEBT.md).

## Quick Start

- English: [`docs/QUICK_START.md`](docs/QUICK_START.md)
- 日本語: [`docs/QUICK_START_JA.md`](docs/QUICK_START_JA.md)
- Studio Presets: [`docs/STUDIO_PRESETS.md`](docs/STUDIO_PRESETS.md)
- S10 handoff contract: [`docs/HANDOFF_3D.md`](docs/HANDOFF_3D.md)

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

Minimum declared Blender runtime is **4.2.0**. Current LTS-first targets are Blender **4.2 LTS**, **4.5 LTS**, and **5.2 LTS**. Meeting the minimum version alone is not a certification claim.

Native After Effects behavior has been exercised for S6–S8 and S10C on Adobe After Effects 2026 Build 87. Stable-release compatibility claims still require the broader release checklist, release-target end-to-end validation, and target-user evidence appropriate to the claim.

## Update policy

See [`docs/UPDATE_ARCHITECTURE.md`](docs/UPDATE_ARCHITECTURE.md).

The private source repository is **not** the customer update endpoint. CutBridge can check a separately configured release index and notify the user, but installation remains user-approved.

## Development flow

- `main` — conservative unreleased/release-locked baseline; only deliberate promotion after validation.
- `develop` — active integration branch; S1–S9 plus S10A–S10C are integrated.
- `feature/*`, `fix/*`, `docs/*` — bounded work branched from current `develop`.

See [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md), [`docs/COMPLETION_STATUS.md`](docs/COMPLETION_STATUS.md), [`docs/ROADMAP.md`](docs/ROADMAP.md), and [`docs/TECHNICAL_DEBT.md`](docs/TECHNICAL_DEBT.md).

## License

CutBridge uses **GPL-3.0-or-later**. The full GPL v3 text is in [`LICENSE`](LICENSE), and release packaging includes the license.

## Release status

Version 0.2.3 remains **unreleased**. There are no release tags or GitHub Releases, and `release-authorization.json` remains unapproved by design.

Stable/RC publication is blocked until repository-level release governance in issue #18 is actually enforced and validated, a deliberate candidate is promoted to `main`, the exact tag/current-main tuple is explicitly authorized, published assets are independently checksum-verified, and the remaining release/end-to-end/target-user validation checklist is satisfied.

## Next product work

1. **S11 — QA / docs / release engineering**.
2. **S12 — End-to-end validation harness**.
3. **S13 — Manual-finding repair**, only when real manual failures exist.
4. **S14 — Japanese target-user validation preparation**.

Release-governance work remains independent of feature development. Do not interpret green CI or S10C integration as publication authorization.

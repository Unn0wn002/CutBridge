# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, compositing setup, QC, controlled revision handling, Japanese-first workflow UX, and safe Studio Presets so artists can move work from Blender into After Effects with less repetitive setup and fewer handoff errors.

The primary audience is Japanese animation and content-production artists and studios. English remains a deterministic supported fallback. Studio Presets let teams adapt naming, folders, pass policy, and presentation conventions without hard-coding one studio workflow into CutBridge.

CutBridge is not a renderer, toon shader, animation generator, or asset manager. Its role is the handoff layer between 3D cut production and compositing: validate the cut in Blender, resolve an optional declarative Studio Preset, configure deterministic render outputs, build a deterministic package, transfer the manifest and render sequences, reconstruct the expected AE context, run QC, and apply compatible revisions without silently replacing unrelated artist work.

## Current development version

**v0.2.3 — unreleased development baseline**

Sessions **S1–S9 are integrated**. S10 — Camera / Null Handoff Investigation — is currently an **evidence-first research session**. It has not changed the production manifest or enabled managed AE camera/null creation.

S9 adds the data-only Studio Preset contract while preserving the pre-S9 Manual workflow, canonical Blender↔AE package identity, S5/S6/S7 ownership/revision/QC safety, S8 localization behavior, and the fail-closed release boundary.

Stable or RC publication remains blocked by repository-level release governance issue #18 and the deliberate unapproved release authorization state.

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

### After Effects

- ExtendScript/ScriptUI package importer.
- Manifest schema/version and path validation.
- Deterministic managed project folders, comp, footage, and layer ownership.
- Exact sequence-frame coverage validation with required/optional pass semantics.
- Repeated-build/reload safety and conservative collision handling.
- S6 non-destructive revision workflow using verified source replacement with rollback and historical-footage provenance.
- S7 QC+ deterministic PASS / WARNING / ERROR diagnostics with stable `CBQ-*` identifiers and safe remediation guidance.
- S8 Japanese-first / English-fallback UI through adjacent `localization.js`, with deterministic English fallback if the localization sidecar is unavailable.
- S9 continues using the existing manifest boundary: preset-managed path/order/comp values are resolved in Blender and consumed by AE from `cutbridge.json`; AE does not parse preset JSON.
- Build, Revision, and QC fail closed when ownership or package structure is missing or ambiguous.
- Negative/preroll export ranges are unsupported; export must be rebased to frame 0 or later.

### S10 camera/null research — not production runtime

S10 currently provides a research harness only.

- production `cutbridge.json` still carries only the legacy active-camera name string;
- the production AE importer does not create a managed 3D camera or null from S10 data;
- candidate basis under test: Blender `(X,Y,Z)` → AE `(X,-Z,Y)`;
- the first synthetic fixture uses a centered 1920×1080 perspective camera, 50 mm lens, 36 mm horizontal sensor, and five axis/mixed points;
- Blender 5.2 source projection is checked with `world_to_camera_view()` using a separate **0.00005 px** numeric precision bound;
- native AE issue #47 uses a disposable comp, CameraLayer, 3D nulls, `toComp()`, and an unchanged **0.05 px** acceptance threshold;
- `100 px / Blender unit` is fixture scale only, not a production spatial-scale policy;
- arbitrary orientation, parenting/constraints, orthographic/panoramic cameras, lens shift, and DOF equivalence remain unapproved.

See [`docs/CAMERA_NULL_HANDOFF.md`](docs/CAMERA_NULL_HANDOFF.md).

## Validation model

Authoritative automated integration requires both GitHub Actions jobs:

- `static-validation` — Python/AE contract tests, Studio Preset tests, S10 research math/probe-contract tests, deterministic release simulation, S6/S7/S8 regressions, and ExtendScript/probe syntax;
- `blender-52-rna-runtime` — official `bpy==5.2.1` registration lifecycle and complete Blender/runtime pytest suite, including the isolated S10 source projection probe.

Historical real-host evidence remains valid for the scopes it actually tested:

- Blender 5.2.1 LTS S8 narrow-panel/localization/Validate/Build gate: PASS;
- Adobe After Effects 2026 v26.3.0 Build 87 S8 localization/fallback gate: PASS;
- S6/S7 real AE revision/QC campaigns: PASS after repaired native findings.

S9 does not invent a new native AE gate because AE receives no preset parser or preset UI. S10 native AE spatial evidence is tracked separately in issue #47. Automated Blender evidence does not substitute for native AE or later release-target GUI/user validation.

The Blender suite still reports `Scene.use_nodes` deprecation warnings relevant to future Blender 6.0 work; see [`docs/TECHNICAL_DEBT.md`](docs/TECHNICAL_DEBT.md).

## Quick Start

- English: [`docs/QUICK_START.md`](docs/QUICK_START.md)
- 日本語: [`docs/QUICK_START_JA.md`](docs/QUICK_START_JA.md)
- Studio Presets: [`docs/STUDIO_PRESETS.md`](docs/STUDIO_PRESETS.md)
- S10 camera/null research: [`docs/CAMERA_NULL_HANDOFF.md`](docs/CAMERA_NULL_HANDOFF.md)

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
│   ├── build_release.py
│   └── research/
├── docs/
├── tests/
└── .github/workflows/
```

## Compatibility

See [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).

Minimum declared Blender runtime is **4.2.0**. Current LTS-first targets are Blender **4.2 LTS**, **4.5 LTS**, and **5.2 LTS**. Meeting the minimum version alone is not a certification claim.

Native After Effects behavior has been exercised for the S6–S8 validation scopes on Adobe After Effects 2026 v26.3.0 Build 87. S10 native spatial-probe evidence is still pending and stable-release compatibility claims still require the broader release checklist and end-to-end release validation.

## Update policy

See [`docs/UPDATE_ARCHITECTURE.md`](docs/UPDATE_ARCHITECTURE.md).

The private source repository is **not** the customer update endpoint. CutBridge can check a separately configured release index and notify the user, but installation remains user-approved.

## Development flow

- `main` — conservative unreleased/release-locked baseline; only deliberate promotion after validation.
- `develop` — active integration branch; S1–S9 are integrated.
- `feature/session-10-camera-null-handoff` — current bounded S10 research branch from the exact green S9 merge.
- other `feature/*`, `fix/*`, `docs/*` branches — bounded work from current `develop`.

See [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md), [`docs/COMPLETION_STATUS.md`](docs/COMPLETION_STATUS.md), [`docs/ROADMAP.md`](docs/ROADMAP.md), and [`docs/TECHNICAL_DEBT.md`](docs/TECHNICAL_DEBT.md).

## License

CutBridge uses **GPL-3.0-or-later**. The full GPL v3 text is in [`LICENSE`](LICENSE), and release packaging includes the license.

## Release status

Version 0.2.3 remains **unreleased**. There are no release tags or GitHub Releases, and `release-authorization.json` remains unapproved by design.

Stable/RC publication is blocked until repository-level release governance in issue #18 is actually enforced and validated, a deliberate candidate is promoted to `main`, the exact tag/current-main tuple is explicitly authorized, published assets are independently checksum-verified, and the remaining release/end-to-end/target-user validation checklist is satisfied.

## Current / next product work

1. **S10 — Camera / Null Handoff Investigation** — active; native AE gate #47 pending.
2. **S11 — QA / docs / release engineering** — not eligible until S10 reaches an explicit completion decision.
3. **S12 — End-to-end validation harness**.
4. **S13 — Manual-finding repair**, only when real manual failures exist.
5. **S14 — Japanese target-user validation preparation**.

Release-governance work remains independent of S10+ feature development. Do not interpret green research CI, S9 integration, or any S10 probe result as publication authorization.

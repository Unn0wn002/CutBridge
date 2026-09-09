# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, compositing setup, QC, controlled revision handling, and Japanese-first workflow UX so artists can move work from Blender into After Effects with less repetitive setup and fewer handoff errors.

The primary audience is Japanese animation and content-production artists and studios. English remains a deterministic supported fallback, and CutBridge intentionally avoids hard-coding a single studio workflow.

CutBridge is not a renderer, toon shader, animation generator, or asset manager. Its role is the handoff layer between 3D cut production and compositing: validate the cut in Blender, configure deterministic render outputs, build a deterministic package, transfer the manifest and render sequences, reconstruct the expected AE context, run QC, and apply compatible revisions without silently replacing unrelated artist work.

## Current development version

**v0.2.3 — unreleased development baseline**

The current `develop` baseline has completed and integrated **Sessions S1–S8**. S8 merged as `368b977582feadc26543825b4d31ffd5f6266a4f`; post-merge CI run `34380737455` passed both `static-validation` and `blender-52-rna-runtime` on that exact merge commit.

S7 QC+ and S8 Japanese-first UX both completed their native After Effects / Blender validation gates before integration. Stable or RC publication remains blocked by repository-level release governance issue #18 and the deliberate fail-closed release authorization state.

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
- S8 Japanese-first / English-fallback localized panel, validation messaging, and narrow-panel layout.

### After Effects

- ExtendScript/ScriptUI package importer.
- Manifest schema/version and path validation.
- Deterministic managed project folders, comp, footage, and layer ownership.
- Exact sequence-frame coverage validation with required/optional pass semantics.
- Repeated-build/reload safety and conservative collision handling.
- S6 non-destructive revision workflow using verified source replacement with rollback and historical-footage provenance.
- S7 QC+ deterministic PASS / WARNING / ERROR diagnostics with stable `CBQ-*` identifiers and safe remediation guidance.
- S8 Japanese-first / English-fallback UI through adjacent `localization.js`, with deterministic English fallback if the localization sidecar is unavailable.
- Build, Revision, and QC fail closed when ownership or package structure is missing or ambiguous.
- Negative/preroll export ranges are unsupported; export must be rebased to frame 0 or later.

### Native validation evidence

S8 targeted native retesting passed on exact candidate `f477b745cc600b85708b63d059d6c4eaed9f0249` before merge:

- Blender 5.2.1 LTS at approximately 245 px N-panel width: JA/EN readability, localized validation, Validate Cut, and Build Package passed.
- Adobe After Effects 2026 v26.3.0 Build 87: persisted Japanese locale, missing-`localization.js` English fallback, visible selector synchronization, zero unintended project mutation, restored JA behavior, and representative fail-closed guards passed.

Automated post-merge evidence on `368b977...`:

- static suite: **88 passed + 2 subtests**;
- complete Blender/runtime suite: **179 passed + 2 subtests**;
- deterministic release simulation and checksums: PASS;
- S5/S6/S7/S8 regression suites: PASS;
- ExtendScript/JS syntax: PASS.

The Blender suite currently emits 61 `Scene.use_nodes` deprecation warnings associated with future Blender 6.0 compatibility work; they are tracked as technical debt rather than current test failures.

## Quick Start

- English: [`docs/QUICK_START.md`](docs/QUICK_START.md)
- 日本語: [`docs/QUICK_START_JA.md`](docs/QUICK_START_JA.md)

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

Native After Effects behavior has been exercised for the S6–S8 validation gates on Adobe After Effects 2026 v26.3.0 Build 87, but stable-release compatibility claims still require the broader release checklist and end-to-end release validation.

## Update policy

See [`docs/UPDATE_ARCHITECTURE.md`](docs/UPDATE_ARCHITECTURE.md).

The private source repository is **not** the customer update endpoint. CutBridge can check a separately configured release index and notify the user, but installation remains user-approved.

## Development flow

- `main` — conservative unreleased/release-locked baseline; only deliberate promotion after validation.
- `develop` — active integration branch; S1–S8 are integrated.
- `feature/*`, `fix/*`, `docs/*` — bounded work branched from current `develop`.

See [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md), [`docs/COMPLETION_STATUS.md`](docs/COMPLETION_STATUS.md), [`docs/ROADMAP.md`](docs/ROADMAP.md), and [`docs/TECHNICAL_DEBT.md`](docs/TECHNICAL_DEBT.md).

## License

CutBridge uses **GPL-3.0-or-later**. The full GPL v3 text is in [`LICENSE`](LICENSE), and release packaging includes the license.

## Release status

Version 0.2.3 remains **unreleased**. There are no release tags or GitHub Releases, and `release-authorization.json` remains unapproved by design.

Stable/RC publication is blocked until repository-level release governance in issue #18 is actually enforced and validated, a deliberate candidate is promoted to `main`, the exact tag/current-main tuple is explicitly authorized, published assets are independently checksum-verified, and the remaining release/end-to-end validation checklist is satisfied.

## Next product work

1. **S8.5 — repository state reconciliation**: documentation/status cleanup only; no runtime redesign and no release authorization.
2. **S9 — Studio Presets**: configurable naming, folders, passes, layer ordering, formats, and version-pattern presets with a safe data-only schema.
3. **S10 — Camera / Null handoff investigation**.
4. **S11 — QA / docs / release engineering**.
5. **S12 — End-to-end validation harness**.
6. **S13 — Manual-finding repair**, only when real manual failures exist.
7. **S14 — Japanese target-user validation preparation**.

Release-governance work remains independent of S9+ feature development. Do not interpret green CI or S8 integration as publication authorization.

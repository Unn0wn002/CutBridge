# CutBridge Quick Start

This guide describes the **currently implemented development workflow** on `develop` after S4 AE contract hardening. It is not a stable-release certification document.

CutBridge connects a Blender animation cut to After Effects through a deterministic package and `cutbridge.json` manifest. The intended flow is:

`Blender metadata/validation → render-output mapping → deterministic package → rendered image sequences → After Effects manifest import → comp/QC`

## 1. Install the Blender extension

For development testing, package/install the contents of `apps/blender/cutbridge/` as the CutBridge Blender extension ZIP, or use a verified release artifact when one exists.

1. Open a supported Blender version (minimum declared runtime: 4.2.0; current automated runtime target includes official `bpy 5.2.1`).
2. Open Blender Preferences and choose the appropriate **Install from Disk** / extension-install action for that Blender version.
3. Select the CutBridge Blender ZIP.
4. Enable CutBridge.
5. In a 3D View, open the `N` sidebar and select the **CutBridge** tab.

Do not describe a Blender/OS combination as certified solely because it meets the minimum version. See [COMPATIBILITY.md](COMPATIBILITY.md).

## 2. Prepare the Blender cut

Before package generation:

1. Save the `.blend` file.
2. Assign an active scene camera.
3. Set the intended FPS and resolution.
4. Set the export frame range.
5. Fill CutBridge Project / Episode / Scene / Cut / Take / Version metadata.
6. Choose the package output directory.
7. Select the logical passes required for the cut: BEAUTY, LINE, SHADOW, and/or DEPTH.

### Frame-range rule

CutBridge currently supports export ranges starting at frame `0` or later. Negative/preroll export frames are rejected consistently by the Blender producer, shared schema, and After Effects consumer. CutBridge does **not** silently renumber animation; rebase the export/preroll before building the package.

## 3. Validate the cut

Use **Validate Cut** before package generation.

Validation checks include the required identifiers, active camera, FPS, resolution, frame range, pass selection, output target, renderer/View Layer pass capability, and package-target safety.

Treat an `ERROR` as a blocker. Warnings should be reviewed before proceeding; for example, DEPTH is more appropriate in a floating-point format such as OpenEXR when numerical depth fidelity matters.

## 4. Render-output mapping

CutBridge configures its own compositor output mapping for the selected logical passes. The mapping is transactional:

- CutBridge-owned nodes use the `CUTBRIDGE_` namespace.
- Unrelated artist compositor nodes are preserved.
- A replacement mapping is not committed until every selected pass has a usable source/output configuration.
- If setup fails, pending CutBridge nodes/settings are rolled back and a prior valid CutBridge mapping is preserved where applicable.

Renderer/View Layer capabilities still matter. If a selected logical pass is unavailable in the active renderer/View Layer, validation/build must fail with actionable guidance rather than silently producing an incomplete mapping.

## 5. Build Package

After validation succeeds, run **Build Package**.

CutBridge creates a deterministic package named from the cut identifiers and version, for example:

```text
PROJECT_EP01_SC010_C012_T01_V001/
├── cutbridge.json
├── camera/
├── preview/
└── render/
    ├── beauty/
    ├── line/
    ├── shadow/
    └── depth/
```

Only selected passes are represented. The exact generated sequence filename pattern is recorded in `cutbridge.json`.

### Version / overwrite safety

Do not use a same-version rebuild to overwrite an existing package that already contains rendered or user payload. CutBridge blocks that case and expects a new version such as V002/V003, or deliberate manual handling of the older package. Empty CutBridge scaffolds may be refreshed through the explicitly supported path.

## 6. Inspect `cutbridge.json`

The manifest is the Blender → AE handoff contract. Important fields include:

- `schema` / `schema_version`
- `cutbridge_version`
- Project / Episode / Scene / Cut / Take / Version
- FPS
- resolution / pixel aspect
- frame start / end / count
- pass records with package-relative path, sequence pattern, and required/optional state
- AE composition/layer-order metadata where present

Do not hand-edit a manifest to bypass validation. Rebuild the package from the source cut when contract data is wrong.

## 7. Render the sequences

Render the Blender cut so each selected CutBridge output directory contains the complete image sequence described by the manifest.

S4's AE contract expects exact frame coverage. A missing required frame blocks a complete required-pass import. Extra or mis-padded matching filenames are diagnosed separately rather than accepted as substitutes for expected frames.

## 8. Run CutBridge in After Effects

For the first development test:

1. Open After Effects.
2. Choose `File > Scripts > Run Script File...`.
3. Select `apps/after-effects/CutBridge.jsx`.

For a dockable panel, copy `CutBridge.jsx` into the After Effects `Scripts/ScriptUI Panels` folder appropriate to the installed AE/OS version, restart AE, and open CutBridge from the `Window` menu.

Adobe script paths vary by version/OS, so **Run Script File** is the least ambiguous first test.

## 9. Import the package

In CutBridge:

1. Choose/import the generated `cutbridge.json`.
2. Let CutBridge validate schema/version, frame contract, pass paths, and sequence coverage.
3. Build the composition only after the package passes the current import checks.
4. Run QC and review warnings/errors.

Current S4 behavior includes:

- unsupported schema/version rejection;
- required-pass errors;
- optional-pass warning/skip behavior;
- exact expected-frame coverage;
- unexpected/mis-padded filename diagnostics;
- package-relative path safety checks;
- Japanese/Unicode filename handling in the tested contract/helpers;
- data-only fallback JSON parsing for legacy ExtendScript environments;
- release-time checking that the AE product version matches the canonical CutBridge version.

## 10. Current limitations

The following are **not yet complete product claims**:

- S5 repeated-import/idempotency and broader AE import/comp reliability hardening;
- S6 non-destructive V001→V002 revision management;
- S7 expanded QC+;
- complete EN/JA localized UI;
- studio presets;
- camera/null transfer;
- stable commercial release certification.

Real After Effects GUI/end-to-end behavior is not certified by Node mocks or headless tests. Blender GUI behavior, Blender→AE end-to-end handoff, native Japanese-user validation, and production/client validation must remain `MANUAL NOT EXECUTED` unless actual evidence is recorded.

## 11. Troubleshooting checklist

If package generation is blocked:

- confirm the `.blend` file is saved;
- confirm an active camera exists;
- confirm all cut identifiers are populated;
- confirm FPS/resolution/frame range are valid;
- confirm export frames start at 0 or later;
- confirm at least one pass is selected;
- confirm the active renderer/View Layer exposes the selected logical passes;
- confirm the output directory is valid;
- confirm the target version package does not already contain payload that must be preserved.

If AE rejects a package:

- use the package's original `cutbridge.json` rather than a hand-edited manifest;
- confirm the package was generated by the supported CutBridge contract/version;
- confirm pass paths remain inside the package;
- confirm required pass folders exist;
- confirm every required expected frame exists with the exact sequence padding/name;
- inspect warnings for optional passes and unexpected filenames;
- do not bypass path/alias checks.

For development commands and automated gates, see [CONTRIBUTING.md](CONTRIBUTING.md) and [TEST_PLAN.md](TEST_PLAN.md).

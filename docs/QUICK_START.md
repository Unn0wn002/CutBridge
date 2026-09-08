# CutBridge Quick Start

This guide describes the **current v0.2.3 development workflow through the S6 revision implementation under review on PR #15**. The integrated `develop` branch still contains S1–S5 until S6 passes its independent-review/native-AE gates and is merged. This is not a stable-release certification document.

CutBridge connects a Blender animation cut to After Effects through a deterministic package and `cutbridge.json` manifest. The intended flow is:

`Blender metadata/validation → render-output mapping → deterministic package → rendered image sequences → After Effects manifest import → comp/QC → compatible revision update`

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

The AE contract expects exact frame coverage. A missing required frame blocks a complete required-pass import. Extra or mis-padded matching filenames are diagnosed separately rather than accepted as substitutes for expected frames.

## 8. Install/run the After Effects scripts

The S6 After Effects workflow consists of **two adjacent runtime files**:

- `CutBridge.jsx` — panel/import/build/QC/native adapter
- `revision_manager.js` — S6 revision core

Keep both runtime files in the same directory. The revision button loads `revision_manager.js` beside `CutBridge.jsx`; copying only the JSX leaves revision support unavailable.

For the first development test:

1. Keep `apps/after-effects/CutBridge.jsx` and `apps/after-effects/revision_manager.js` together.
2. Read `apps/after-effects/INSTALL.md` for the two-file installation requirement and native-test boundary.
3. Open After Effects.
4. Choose `File > Scripts > Run Script File...`.
5. Select `CutBridge.jsx`.

For a dockable panel, copy **both runtime files** into the After Effects `Scripts/ScriptUI Panels` folder appropriate to the installed AE/OS version, restart AE, and open CutBridge from the `Window` menu.

The deterministic AE release ZIP contains exact `CutBridge.jsx`, `revision_manager.js`, `INSTALL.md`, and `LICENSE` contents. Adobe script paths vary by version/OS, so **Run Script File** is the least ambiguous first test.

## 9. Import, build, and run QC

In CutBridge:

1. Choose **1. Import Package / 読み込み** and select the package's `cutbridge.json`.
2. Let CutBridge validate schema/version, frame contract, pass paths, and sequence coverage.
3. Choose **2. Build Comp / コンポ作成** only after the package passes the import checks.
4. Choose **3. Run QC / QC実行** and review warnings/errors.

Current automated coverage includes:

- unsupported schema/version rejection;
- required-pass errors and optional-pass warning/skip behavior;
- exact expected-frame coverage and unexpected/mis-padded filename diagnostics;
- package-relative path/alias safety;
- Japanese/Unicode filename handling in contract/host-shaped tests;
- data-only fallback JSON parsing for legacy ExtendScript environments;
- deterministic managed comp/footage/layer ownership;
- repeated Build and script-reload discovery without silent adoption of unrelated artist work;
- comp/source/FPS/ownership QC;
- missing/duplicate deterministic package-folder rejection;
- release-time AE product-version and package-content checks.

Node/host-shaped tests are regression evidence, not native AE certification.

## 10. Update a compatible revision (S6)

Use the revision workflow only after a current CutBridge package has already been imported and its managed composition has been built successfully.

1. In Blender, generate and render a **newer version of the same Project / Episode / Scene / Cut / Take**, for example V002 after V001.
2. Keep the source-only revision geometry compatible with the current AE comp: FPS, frame start/end/count, pixel aspect, resolution, and composition identity/name must remain unchanged.
3. Ensure the newer package contains complete sequences for the managed passes that will be replaced.
4. In the AE panel, choose **4. Update Revision / 差し替え**.
5. Select the newer package's `cutbridge.json`.
6. Review any compatibility warning. Required/optional status changes use an explicit warning/confirmation path; unsupported changes are blocked.
7. Confirm the revision only when the selected package is intentional.
8. After the update, run **Build Comp** again and then **Run QC**.
9. Save the AE project, close/reopen it, reload the newer package, and repeat Build/QC as part of the manual validation gate.
10. For lifecycle validation, repeat the process with V003.

The S6 implementation stages and validates all replacement footage before changing existing managed layer sources, uses native `AVLayer.replaceSource(..., false)` for source swaps/restoration, migrates managed ownership metadata only after successful swaps, and attempts rollback on failure. Historical CutBridge footage keeps its old version-scoped provenance tag.

Source-only revision deliberately blocks:

- a different Project / Episode / Scene / Cut / Take identity;
- same/older candidate version;
- composition identity/name change;
- FPS change;
- frame-range/count change;
- pixel-aspect change;
- width/height resolution change;
- addition of a new pass;
- removal of a previously required pass.

Removed optional passes are retained unchanged. Required/optional status changes warn and require confirmation.

CutBridge also fails closed when current AE project ownership is ambiguous. A duplicate current package root, missing/duplicate `01_COMP` / `02_RENDER` / `03_PRECOMP` / `04_OUTPUT`, duplicate/misplaced managed comp ownership, or managed-layer/source drift must be resolved deliberately instead of being auto-adopted or repaired.

### What must be checked manually in real After Effects

Automated host-shaped tests preserve mock non-source layer properties, but real AE still requires explicit evidence for:

- effects and effect parameters;
- masks;
- transforms;
- parenting;
- timing/start time;
- switches/blend mode and unrelated artist layers;
- source replacement and undo behavior;
- package-root/item comments across save/reopen;
- V001 → V002 → V003 lifecycle;
- Build/QC after revision and after script/project reload.

Do not claim these as validated until they are actually observed in a supported desktop AE version.

## 11. Current limitations / release boundary

The following are **not yet stable product claims**:

- native After Effects desktop validation of S5/S6 behavior;
- Blender → package → After Effects end-to-end certification;
- S7 expanded QC+;
- complete EN/JA localized UI;
- studio presets;
- camera/null transfer;
- Japanese native-user/studio validation;
- stable commercial release certification.

S5 import/composition hardening is integrated on `develop`. S6 implementation is present on PR #15 with green automated gates but remains blocked for merge by independent review and the real AE/manual validation gate.

## 12. Troubleshooting checklist

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

If AE rejects a package/build/revision:

- keep `revision_manager.js` beside `CutBridge.jsx` for S6 revision support;
- use the package's original `cutbridge.json` rather than a hand-edited manifest;
- confirm the package was generated by the supported CutBridge contract/version;
- confirm pass paths remain inside the package;
- confirm required pass folders exist;
- confirm every required expected frame exists with the exact sequence padding/name;
- inspect warnings for optional passes and unexpected filenames;
- confirm current managed root/folders/comp have not been duplicated, moved, renamed, or stripped of ownership tags;
- confirm the candidate is a newer revision of the same cut/take with compatible FPS/frame range/pixel aspect/resolution/comp identity;
- do not bypass path, alias, ownership, confirmation, or compatibility checks.

For development commands and automated gates, see [CONTRIBUTING.md](CONTRIBUTING.md), [TEST_PLAN.md](TEST_PLAN.md), and [S6_REVISION_CONTRACT.md](S6_REVISION_CONTRACT.md).
